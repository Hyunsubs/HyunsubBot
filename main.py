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
        
        
        driver = webdriver.Chrome(executable_path = os.environ.get("GOOGLE_CHROME_BIN"), chrome_options = chrome_options)
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
        csv_file = youtubeDf.to_csv("play_list.csv")

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

@bot.command()
async def play1(ctx):
    channel = ctx.author.voice.channel
    file = pd.read_csv("play_list.csv")
    url = file["주소"][0]
    if bot.voice_clients == []:
        await channel.connect()
        await ctx.send("채널 연결됨" + str(bot.voice_clients[0].channel))

    ydl_opts = {'format': 'bestaudio'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
    voice = bot.voice_clients[0]
    voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))

@bot.command()
async def play2(ctx):
    channel = ctx.author.voice.channel
    file = pd.read_csv("play_list.csv")
    url = file["주소"][1]
    if bot.voice_clients == []:
        await channel.connect()
        await ctx.send("채널 연결됨" + str(bot.voice_clients[0].channel))

    ydl_opts = {'format': 'bestaudio'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
    voice = bot.voice_clients[0]
    voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))

@bot.command()
async def play3(ctx):
    channel = ctx.author.voice.channel
    file = pd.read_csv("play_list.csv")
    url = file["주소"][2]
    if bot.voice_clients == []:
        await channel.connect()
        await ctx.send("채널 연결됨" + str(bot.voice_clients[0].channel))

    ydl_opts = {'format': 'bestaudio'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
    voice = bot.voice_clients[0]
    voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))

@bot.command()
async def play4(ctx):
    channel = ctx.author.voice.channel
    file = pd.read_csv("play_list.csv")
    url = file["주소"][3]
    if bot.voice_clients == []:
        await channel.connect()
        await ctx.send("채널 연결됨" + str(bot.voice_clients[0].channel))

    ydl_opts = {'format': 'bestaudio'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
    voice = bot.voice_clients[0]
    voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))

@bot.command()
async def play5(ctx):
    channel = ctx.author.voice.channel
    file = pd.read_csv("play_list.csv")
    url = file["주소"][4]
    if bot.voice_clients == []:
        await channel.connect()
        await ctx.send("채널 연결됨" + str(bot.voice_clients[0].channel))

    ydl_opts = {'format': 'bestaudio'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
    voice = bot.voice_clients[0]
    voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))


@bot.command()
async def l(ctx):
    if (ctx.voice_client): #만약에 봇이 채널에 있다면
        await ctx.guild.voice_client.disconnect() # 채널 나가기
    else: #채널에 없다면
        await ctx.send("현재 채널에 없습니다")




bot.run('OTIzOTEwMTEyMTE5MjI2Mzc4.YcW4WA.uWeYH3wd9N3v5z8FVl8CjzvFoM8') # 봇의 토큰으로 실행시키는 것입니다.


