import discord # discord 모듈을 불러오기
from selenium import webdriver
import pandas as pd
import asyncio
import datetime as dt
from ydl import *
import re
import os
from playopts import FFMPEG_OPTIONS,url_convert
import reqeusts

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
    
FFMPEG_OPTIONS = FFMPEG_OPTIONS
play_list =[]
list_name =[]

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


def next_url(voice):
    try:
        play_list.pop(0)
        list_name.pop(0)
    except:
        pass
    voice.play(discord.FFmpegPCMAudio(play_list[0], **FFMPEG_OPTIONS),after=lambda e: next_url(voice))



@bot.command()
async def 재생(ctx):
    if ctx.message.content[4:].startswith("https"):
        url = ctx.message.content[4:]
        if url.find("&list") != -1:
            index_num = url.find("&list")
            url = ctx.message.content[4:index_num+4]
            print(url)
            
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice is None:
            voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=ctx.author.voice.channel.name)
            await voiceChannel.connect()
            voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
            URL = url_convert(url)
            play_list.append(URL)
            list_name.append(url)
            voice.play(discord.FFmpegPCMAudio(play_list[0], **FFMPEG_OPTIONS),after=lambda e: next_url(voice))
        else:
            URL = url_convert(url)
            play_list.append(URL)
            list_name.append(url)
            try:
                voice.play(discord.FFmpegPCMAudio(play_list[0], **FFMPEG_OPTIONS),after=lambda e: next_url(voice))
            except:
                await ctx.send("재생목록에 노래를 추가 합니다")
    else:
        num = int(ctx.message.content[4]) - 1
        print(num)
        file = pd.read_csv(str(ctx.channel)+"play_list.csv")
        url = file["주소"][num]
        if url.find("&list") != -1:
            index_num = url.find("&list")
            url = ctx.message.content[4:index_num+4]
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice is None:
            voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=ctx.author.voice.channel.name)
            await voiceChannel.connect()
            voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
            URL = url_convert(url)
            play_list.append(URL)
            list_name.append(url)
            voice.play(discord.FFmpegPCMAudio(play_list[0], **FFMPEG_OPTIONS), after=lambda e: next_url(voice))
        else:
            URL = url_convert(url)
            play_list.append(URL)
            list_name.append(url)
            try:
                voice.play(discord.FFmpegPCMAudio(play_list[0], **FFMPEG_OPTIONS), after=lambda e: next_url(voice))
            except:
                await ctx.send("재생목록에 노래를 추가 합니다")



@bot.command()
async def 리스트(ctx):
    if len(list_name) > 0:
        await ctx.send("재생목록")
        for n in range(0,len(list_name)):
            url = list_name[n]
            print(url)
            html = urlopen(url)
            bsObject = bs(html, "html.parser")
            tmpContent = bsObject.select("title")[0].text
            await ctx.send(f"{n+1} . :" + tmpContent)


    else:
        await ctx.send("재생목록에 대기중인 곡이 없습니다.")


        
@bot.command()
async def 퇴장(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice is None:
        await ctx.send("현재 채널에 없습니다")
    else:
        await voice.disconnect()
        await ctx.send("채널을 나갑니다")
        if len(play_list) > 0 and len(list_name) > 0:
            play_list.clear()
            list_name.clear()


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
        voice = bot.voice_clients[0]
        bot.voice_clients[0].stop()
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(play_list[0], download=False)
            URL = info['formats'][0]['url']
        play_list.pop(0)
        list_name.pop(0)
        voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS),after=lambda e: next_url(voice))
    else:
        await ctx.send("플레이 할 곡이 없습니다.")
        
@bot.command()
async def 생일(ctx):
    now = dt.datetime.now()
    year = now.year
    month = now.month
    day = now.day

    birth_df = pd.read_csv("생일.csv")
    birth_dict = birth_df.to_dict("records")

    for man in birth_dict:
        if man["생월"] == month and man["생일"] == day:
            await ctx.send(f"{man['이름']}님의 {year - man['생년']}번째 생일을 축하합니다!")
            break
        else:
            await ctx.send(f"{man['이름']}님의 생일 : {man['생월']}월 {man['생일']}일")
        
@bot.command()
async def 주식(ctx):
    name = ctx.message.content[4:]
    file = pd.read_csv("종목코드.csv",encoding="cp949")

    for n in range(0,len(file)):
        if file["한글 종목약명"][n].lower() == name.lower():
            code = file["단축코드"][n]
            a = urlopen("https://finance.naver.com/item/main.nhn?code="+code)
            soup = bs(a.read(), "html.parser")
            info = soup.select(".blind")
            slice_info = str(info[5]).split("\n")
            main_info = slice_info[5]
            main_info = re.sub("<dd>", "", main_info)
            main_info = re.sub("</dd>", "", main_info)
            await ctx.send(file["한글 종목약명"][n] + " 정보: " + main_info)
            break

@bot.command()
async def 일어번역(ctx):
    text = ctx.message.content[6:]
    print(text)
    ja_params = {
        "source" : "ja",
        "target" : "ko",
        "text" : text,

    }
    header = {
        "X-Naver-Client-Id": PAPAGO_ID,
        "X-Naver-Client-Secret": PAPAGO_SECRET,

    }
    response = requests.post(url="https://openapi.naver.com/v1/papago/n2mt", headers=header, json=ja_params)
    await ctx.send(response.json()["message"]["result"]["translatedText"])

@bot.command()
async def 영어번역(ctx):
    text = ctx.message.content[6:]
    print(text)
    en_params = {
        "source" : "en",
        "target" : "ko",
        "text" : text,

    }
    header = {
        "X-Naver-Client-Id": PAPAGO_ID,
        "X-Naver-Client-Secret": PAPAGO_SECRET,

    }
    response = requests.post(url="https://openapi.naver.com/v1/papago/n2mt", headers=header, json=en_params)
    await ctx.send("번역결과 : " + response.json()["message"]["result"]["translatedText"])



bot.run('OTIzOTEwMTEyMTE5MjI2Mzc4.YcW4WA.uWeYH3wd9N3v5z8FVl8CjzvFoM8') # 봇의 토큰으로 실행시키는 것입니다.
