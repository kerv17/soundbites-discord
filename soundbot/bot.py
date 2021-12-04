import os
import json
import discord
import time
import youtube_dl
from discord.ext import commands


with open('config/options.json') as f:
    data = json.load(f)

client = commands.Bot(command_prefix=data["prefix"], help_command=None)
@client.command()
async def play(ctx: commands.context, sound: str):
    voicechannel = ctx.author.voice.channel
    voice = await voicechannel.connect()

    voice.play(discord.FFmpegPCMAudio(executable="./ffmpeg.exe", source="clips/"+ sound + ".mp3"))
    while voice.is_playing():
        time.sleep(5)
    await voice.disconnect()

@client.command()
async def add(ctx: commands.context, input: str, url: str):
    song_there = os.path.isfile(input+".mp3")
    if song_there:
        await ctx.send("This name is already in use")
        return
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
       ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "clips/"+input+".mp3")
    emoji = "\N{THUMBS UP SIGN}"
    await ctx.message.add_reaction(emoji)
    pass


@client.command()
async def list(ctx: commands.context):
    list = os.listdir('./clips')
    string = "Here is the list:"

    for i in list:
        string += "\n- "+ i.removesuffix('.mp3')
    await ctx.send(string)

@client.command()
async def help(ctx:commands.context):
    string = "`*play <sound>`: play a soundbite in the server you are in \n" \
            "`*add <sound-name> <url>`: add soundbite to database \n" \
            "`*list`: list all the sounds in the database"
    await ctx.send(string)




client.run(data["bot-token"])
