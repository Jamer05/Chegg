import discord
import os
import requests
import json
import asyncio
import youtube_dl
import re
import wikipedia
import math
import reddit
import random
import aiohttp
import nacl
import praw

from utils import get_momma_jokes
from discord import FFmpegPCMAudio
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext import commands
from discord import Embed
from discord.ext.commands import Bot
from discord.ext.commands import Cog
from discord.voice_client import VoiceClient
from dotenv import load_dotenv
from discord.ext import commands
from random import choice
from discord.utils import get
from typing import Optional
from keep_alive import keep_alive

load_dotenv()

DISCORD_TOKEN = os.getenv("TOKEN")
bot = discord.Client()
bot = commands.Bot(command_prefix="apt -")

bot.remove_command("help")
@bot.command()
async def clear(ctx, amount=5):
	await ctx.channel.purge(limit=amount)
@bot.command()
async def help(ctx):

    embed = discord.Embed(
        colour = discord.Colour.orange()
    )

    embed.set_author(name='Jamer-SSL Bot at your service')
    embed.set_author(name="Bot prefix = apt -<command>")
    embed.add_field(name='apt -help/music', value='show available command to listen some music', inline=False)
    embed.add_field(name='apt -motivate', value='Gives you a randome quotes', inline=False)
    embed.set_image
    embed.add_field(name='apt -clear <value>', value='delete some multiple messages', inline=False)
    embed.set_image
    embed.add_field(name='apt -credits', value='The owner of this bot', inline=False)
    embed.set_image
    embed.add_field(name='apt -ping', value='Show your current ping', inline=False)
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/808149875539312690/189d6d113941c6797f2d9df5a2283463.png")
   
    await ctx.send(embed=embed)

@bot.command(name = "help/music")
async def helpMusic(ctx):

    embed = discord.Embed(
        colour = discord.Colour.orange()
    )
    embed.add_field(name='apt -join', value='Join the discord bot', inline=False)
    embed.add_field(name='apt -play -n', value='Play music from the queue', inline=False)
    embed.add_field(name='apt -pause', value='Pause the music for a moment', inline=False)
    embed.add_field(name='apt -queue', value='Add musc in the queue', inline=False)
    embed.add_field(name='apt -stop', value='Stop music for a while', inline=False)
    embed.add_field(name='apt -leave', value='Leave bot from channel', inline=False)
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/808149875539312690/189d6d113941c6797f2d9df5a2283463.png")
    await ctx.send(embed=embed)

def get_quote():
	response = requests.get("https://zenquotes.io/api/random")
	json_data = json.loads(response.text)
	quote = json_data[0]['q'] + " -" + json_data[0]['a']
	return (quote)


@bot.command(name="Jamer")
async def some_crazy_function_name(ctx):
	await ctx.channel.send("Cute si Jamer")

@bot.command(name="motivate")
async def motivate_message(ctx):
	q = get_quote()
	await ctx.channel.send(q)


@bot.event
async def on_message(message):
	if message.content == "Hello" or message.content == 'Hi':
		await message.channel.send(
		    "Software is the another term for house of the bugs. change my mind."
		)

	await bot.process_commands(message)


@bot.command()
async def print(ctx, *args):
	response = ""

	for arg in args:
		response = response + " " + arg

	await ctx.channel.send(response)

@bot.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("You are not connected to a voice channel")
        return
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    source = FFmpegPCMAudio('1.m4a')
    player = voice.play(source)

@bot.command(pass_context=True)
async def leave(ctx):
  server = ctx.message.guild.voice_client
  await server.disconnect()
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}   

def endSong(guild, path):
    os.remove(path)                                   
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)




status = ['Kenji', 'Eating!', 'Sleeping!']
queue = []


@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name='general')
    await channel.send(f'Welcome {member.mention}!  Ready to jam out? See `?help` command for details!')
        
@bot.command(name='ping', help='This command returns the latency')

async def ping(ctx):
    
    await ctx.send(f'**Pong!** Latency: {round(bot.latency * 1000)}ms')

@bot.command(name='hello', help='This command returns a random welcome message')
async def hello(ctx):
    responses = ['***grumble*** Why did you wake me up?', 'Top of the morning to you lad!', 'Hello, how are you?', 'Hi', '**Wasssuup!**']
    await ctx.send(choice(responses))

@bot.command(name='die', help='This command returns a random last words')
async def die(ctx):
    responses = ['why have you brought my short life to an end', 'i could have done so much more', 'i have a family, kill them instead']
    await ctx.send(choice(responses))

@bot.command(name='credits', help='This command returns the credits')
async def credits(ctx):
    await ctx.send(f'***Made by*** `Jamer Cute`')
    await ctx.send('Thanks to him')


@bot.command(name='queue', help='This command adds a song to the queue')
async def queue_(ctx, url):
    global queue

    queue.append(url)
    await ctx.send(f'`{url}` added to queue!')

@bot.command(name='remove', help='This command removes an item from the list')
async def remove(ctx, number):
    global queue

    try:
        del(queue[int(number)])
        await ctx.send(f'Your queue is now `{queue}!`')
    
    except:
        await ctx.send('Your queue is either **empty** or the index is **out of range**')
        
@bot.command(name='play', help='This command plays songs')
async def play(ctx):
    global queue

    server = ctx.message.guild
    voice_channel = server.voice_client

    async with ctx.typing():
        player = await YTDLSource.from_url(queue[0], loop=bot.loop)
        voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

    await ctx.send('**Now playing:** {}'.format(player.title))
    await ctx.message.add_reaction('✅')
    del(queue[0])

@bot.command(name='play_now', help='This command plays songs now')
async def play_now(ctx, url):
    server = ctx.message.guild
    voice_channel = server.voice_client

    async with ctx.typing():
        player = await YTDLSource.from_url(url, loop=bot.loop)
        voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

    await ctx.send('**Now playing:** {}'.format(player.title))
    await ctx.message.add_reaction('✅')
  


@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.pause()

@bot.command(name='resume', help='This command resumes the song!')
async def resume(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.resume()
    await ctx.message.add_reaction('⏯')
    
@bot.command(name='view', help='This command shows the queue')
async def view(ctx):
    await ctx.send(f'Your queue is now `{queue}!`')


@bot.command(name='stop', help='This command stops the song!')
async def stop(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.stop()

@bot.command(name ="dog")
async def dog(ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://random.dog/woof.json") as r:
                    data = await r.json()

                    embed = discord.Embed(title="Woof")
                    embed.set_image(url=data['url'])                 
                    await ctx.send(embed=embed)

@bot.command(name = "floopy")
async def fox(ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://randomfox.ca/floof/") as r:
                    data = await r.json()

                    embed = discord.Embed(title="Floof")
                    embed.set_image(url=data['image'])               
                    await ctx.send(embed=embed)

@bot.command(brief="Creates an invite link to the channel")
@commands.guild_only()
async def invite(ctx):
        link = await ctx.channel.create_invite(max_age=1)
        await ctx.send(link)

@bot.command(name ="cat")
async def cat(ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("http://aws.random.cat/meow") as r:
                    data = await r.json()

                    embed = discord.Embed(title="Meow")
                    embed.set_image(url=data['file'])

                    await ctx.send(embed=embed)

@bot.command(brief="You Momma is!")
async def insult(ctx, member: discord.Member = None):
        insult = await get_momma_jokes()
        if member is not None:
            print("1")
            await ctx.send("@%s eat this: %s " % (member.name, insult))
        else:
            print("we are in here")
            await ctx.send("@%s for yourself: %s " % (ctx.message.send, insult))

keep_alive()  
bot.run(DISCORD_TOKEN)
