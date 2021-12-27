import discord # discord 모듈을 불러오기
from selenium import webdriver
import pandas as pd
from ydl import *

from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from urllib import parse

from discord.ext import commands

from random import randint
# discord.ext 에서 commands 모듈 가져오기
prefix = '$' # 접두사 설정 ( 꼭 느낌표로 안해두 됩니다. 본인이 직접 정하는것 입니다.)
bot = commands.Bot(command_prefix = prefix) # 봇 접두사 설정 @bot.event # 봇 이벤트시 실행 되는 구문 입니다.


async def on_ready(): # 실행이 된다면
    await bot.change_presence(status=discord.Status.online)
    print('Bot 준비완료!') # 터미널 부분에 출력하라 (' Bot 준비완료!' ) 를

play_list =[]

@bot.event
async def on_message(message):
    channel = message.channel

    # 로스트아크 레벨 로딩
    if message.content.startswith("$레벨"):
        url = "https://lostark.game.onstove.com/Profile/Character/"+parse.quote(message.content[4:])
        print(url)
        html = urlopen(url)
        bsObject = bs(html, "html.parser")
        #tmpContent = bsObject.find_all(class_="level-info2__expedition")
        tmpContent = bsObject.find_all("div", {"class":"level-info2__expedition"})[0].find_all("span")[1].text
        tmpContent2 = bsObject.find_all("div", {"class": "level-info__expedition"})[0].find_all("span")[1].text
        tmpContent3 = bsObject.find_all("div", {"class": "level-info__item"})[0].find_all("span")[1].text


        print(tmpContent)
        await channel.send(message.content[4:]+" : 아이템 레벨: " +str(tmpContent) + " 원정대 레벨 :" + str(tmpContent2) + " 전투 레벨 :" + str(tmpContent3))
    
    #유튜브 음악 재생
    elif message.content.startswith("$검색"):
        channel = message.channel
        keyword = message.content[4:]

        url = 'https://www.youtube.com/results?search_query={}'.format(keyword)

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        
        driver.get(url)
        soup = bs(driver.page_source, "html.parser")
        driver.close()
        name = soup.select('a#video-title')
        video_url = soup.select("a#video-title")
        view = soup.select("a#video-title")

        name_list = []
        url_list = []
        view_list = []

        for i in range(len(name)):
            name_list.append(name[i].text.strip())
            view_list.append(view[i].get("aria-label").split()[-1])
        for i in video_url:
            url_list.append("{}{}".format("https://www.youtube.com",i.get("href")))
        youtubeDic = {
            "제목": name_list,
            "주소": url_list,
            "조회수": view_list
        }

        youtubeDf = pd.DataFrame(youtubeDic)
        youtubeDf.to_csv(str(channel) + "play_list.csv")

        for i in range(0,5):
            await channel.send("'''" + f"{i+1}" + ". " + youtubeDf["제목"][i] + "'''")
    await bot.process_commands(message)



@bot.command()
async def 허허(ctx):
    await ctx.send(f"호호호")

@bot.command()
async def 동석(ctx):
    await ctx.send(f"ㅎㅇ")


@bot.command()
async def 주사위(ctx):
    await ctx.send(f"결과는 {randint(1,6)} 입니다")



def next_url():
    ydl_opts = {'format': 'bestaudio'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                      'options': '-vn'}
    if len(play_list) > 0:
        url = play_list[0]
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            URL = info['formats'][0]['url']
        print(URL)
        play_list.pop(0)
        return URL
    else:
        pass



@bot.command()
async def p(ctx):
    ydl_opts = {'format': 'bestaudio'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                      'options': '-vn'}
    if ctx.message.content[3:].startswith("https"):
        url = ctx.message.content[3:]
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if bot.voice_clients == []:
            voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice is None:
            voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=ctx.author.voice.channel.name)
            await voiceChannel.connect()
            voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
            print("Holy")
            await ctx.send(f"노래를 재생함:" + url)
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                URL = info['formats'][0]['url']
            try:
                play_list.append(url)
                voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS),
                           after=lambda e: voice.play(discord.FFmpegPCMAudio(next_url(), **FFMPEG_OPTIONS)))
            except:
                print(play_list)
            # voice.play(play1(num,ctx), after=lambda e: play1(num,ctx))
        else:
            if not bot.voice_clients[0].is_playing():
                play_list.append(url)
                voice.play(discord.FFmpegPCMAudio(play_list[0], **FFMPEG_OPTIONS),
                           after=lambda e: voice.play(discord.FFmpegPCMAudio(next_url(), **FFMPEG_OPTIONS)))
            else:
                play_list.append(url)
                await ctx.send("노래를 예약합니다" + url)
                print("Moly")
    else:
        num = int(ctx.message.content[3]) - 1
        print(num)
        file = pd.read_csv(str(ctx.channel)+"play_list.csv")
        url = file["주소"][num]
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if bot.voice_clients == []:
            voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice is None:
            voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=ctx.author.voice.channel.name)
            await voiceChannel.connect()
            voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
            print("Holy")
            await ctx.send(f"노래를 재생함:" + str(file["제목"][num]))
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                URL = info['formats'][0]['url']
            try:
                play_list.append(url)
                voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS) , after= lambda e: voice.play(discord.FFmpegPCMAudio(next_url(), **FFMPEG_OPTIONS)))
            except:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    URL = info['formats'][0]['url']                
                print(play_list)
            os.remove(str(ctx.channel)+"play_list.csv")
            #voice.play(play1(num,ctx), after=lambda e: play1(num,ctx))
        else:
            if not bot.voice_clients[0].is_playing():
                play_list.append(url)
                voice.play(discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS),
                           after=lambda e: voice.play(discord.FFmpegPCMAudio(next_url(), **FFMPEG_OPTIONS)))
            else:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    URL = info['formats'][0]['url']
                play_list.append(url)
                await ctx.send("노래를 예약함 : " + str(file["제목"][num]) + " ")
                print("Moly")


@bot.command()
async def 리스트(ctx):
    if len(play_list) > 0:
        await ctx.send("재생목록")
        for n in range(0,len(play_list)):
            url = play_list[n]
            print(url)
            html = urlopen(url)
            bsObject = bs(html, "html.parser")
            tmpContent = bsObject.select("title")[0].text
            await ctx.send(f"{n+1} . :" + tmpContent)


    else:
        await ctx.send("재생목록에 대기중인 곡이 없습니다.")



@bot.command()
async def l(ctx):
    if (ctx.voice_client): #만약에 봇이 채널에 있다면
        await ctx.guild.voice_client.disconnect() # 채널 나가기
    else: #채널에 없다면
        await ctx.send("현재 채널에 없습니다")


@bot.command()
async def 멈춤(ctx):
    if not bot.voice_clients[0].is_paused():
        await ctx.send("곡을 멈춥니다")
        bot.voice_clients[0].pause()
    else:
        await ctx.send("이미 일시 정지중 입니다.")

@bot.command()
async def 재개(ctx):
    if bot.voice_clients[0].is_paused():
        await ctx.send("곡을 재개 합니다")
        bot.voice_clients[0].resume()
    else:
        await ctx.send("이미 플레이중 입니다.")

@bot.command()
async def 스킵(ctx):
    ydl_opts = {'format': 'bestaudio'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                      'options': '-vn'}
    if bot.voice_clients[0].is_playing():
        await ctx.send("현재 재생곡을 스킵합니다")
        bot.voice_clients[0].stop()
        url = play_list[0]
        bot.voice_clients[0].play(discord.FFmpegPCMAudio(next_url(), **FFMPEG_OPTIONS),
                   after=lambda e: bot.voice_clients[0].play(discord.FFmpegPCMAudio(next_url(), **FFMPEG_OPTIONS)))
    else:
        await ctx.send("플레이 할 곡이 없습니다.")









bot.run('OTIzOTEwMTEyMTE5MjI2Mzc4.YcW4WA.uWeYH3wd9N3v5z8FVl8CjzvFoM8') # 봇의 토큰으로 실행시키는 것입니다.



