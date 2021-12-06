import discord, time
import asyncio
import os
import youtube_dl
import pickle
from keep_alive import get_prefix
from discord.ext import commands
from discord import member, guild, FFmpegPCMAudio
from discord.utils import get
from datetime import datetime
import traceback

async def after_play(ctx, bot):
  try:
    with open(f"./data/queue/{ctx.guild.id}.db", "rb") as fp:
      listu = pickle.load(fp)
    if int(len(listu)) == 0:
      os.remove(f"./data/queue/{ctx.guild.id}.db")
      await ctx.voice_client.disconnect()
    if not int(len(listu)) == 0:
          texts = listu[0]
          listu.remove(texts)
          with open(f"./data/queue/{ctx.guild.id}.db", "wb") as fp:
            pickle.dump(listu, fp)
          ydl_opts = {'format': 'bestaudio/best', 'noplaylist': True, "cookies": "youtube.com_cookies.txt", "default_search": "auto"}
          load = await ctx.send(f"Đang load nhạc")
          if texts.startswith("http"):
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
              info = ydl.extract_info(texts, download=False)
              URL = info['formats'][0]['url']
              title = info['title']
            now = datetime.utcnow()
            now = now.strftime("%Y-%m-%d %H:%M")
            if not title.endswith(now):
              source = FFmpegPCMAudio(URL)
              ctx.voice_client.pause()
              ctx.voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(after_play(ctx, bot), bot.loop))
              await load.edit(f"Đang play **{title}**")
            else:
              await load.edit(f'**Chung tôi không support live Music**')
          if not texts.startswith("http"):
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
              info = ydl.extract_info(f"ytsearch5:{texts}", download=False)
              info = info['entries']
            now = datetime.utcnow()
            now3 = now.strftime("%Y-%m-%d %H:%M")
            now1 = now.strftime("%Y-%m-%d %H:")
            now2 = now.strftime("%M")
            now2 = int(now2) + 1
            nolive = []
            for i in info:
              title = i['title']
              if not title.endswith(now3):
                if not title.endswith(f"{now1}{now2}"):
                  nolive.append(i)
            try:
              URL = nolive[0]['formats'][0]['url']
              title = nolive[0]['title']
              source = FFmpegPCMAudio(URL)
              ctx.voice_client.pause()
              ctx.voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(after_play(ctx, bot), bot.loop))
              await load.edit(f"Đang play **{title}**")
            except Exception:
              print(traceback.format_exc())
              await load.edit(f"**404 chúng tôi không thấy nhạc bạn yêu cầu**")
  except:
    try:
      os.remove(f"./data/queue/{ctx.guild.id}.db")
    except:
      pass
    await ctx.voice_client.disconnect()

class music(commands.Cog):
  def __init__(self, bot):
      self.bot = bot

  @commands.command()
  async def stop(self, ctx):
    channel = ctx.author.voice
    if not channel == None:
      voice = get(self.bot.voice_clients, guild=ctx.guild)
      if voice.channel == channel.channel:
        try:
          os.remove(f"./data/queue/{ctx.guild.id}.db")
        except:
          pass
        await ctx.voice_client.disconnect()

  @commands.command()
  async def skip(self, ctx):
    channel = ctx.author.voice
    voice = get(self.bot.voice_clients, guild=ctx.guild)
    if not channel == None:
      if voice.channel == channel.channel:
        await after_play(ctx, self.bot)

  @commands.command()
  async def pause(self, ctx):
    channel = ctx.author.voice
    voice = get(self.bot.voice_clients, guild=ctx.guild)
    if not channel == None:
      if voice.channel == channel.channel:
        ctx.voice_client.pause()

  @commands.command()
  async def resume(self, ctx):
    channel = ctx.author.voice
    voice = get(self.bot.voice_clients, guild=ctx.guild)
    if not channel == None:
      if voice.channel == channel.channel:
        ctx.voice_client.resume()

  @commands.command(aliases=['p'])
  async def play(self, ctx,*, texts=None):
    if not texts == None:
      channel = ctx.author.voice
      if not channel == None:
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice == None:
          ydl_opts = {'format': 'bestaudio/best', 'noplaylist': True, "cookies": "youtube.com_cookies.txt", "default_search": "auto"}
          load = await ctx.send(f"Đang load nhạc")
          if texts.startswith("http"):
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
              info = ydl.extract_info(texts, download=False)
              URL = info['formats'][0]['url']
              title = info['title']
            now = datetime.utcnow()
            now = now.strftime("%Y-%m-%d %H:%M")
            if not title.endswith(now):
              source = FFmpegPCMAudio(URL)
              await channel.channel.connect()
              try:
                bot = ctx.guild.get_member(self.bot.user.id)
                await bot.edit(suppress = False)
              except:
                pass
              await ctx.guild.change_voice_state(channel=channel.channel, self_mute=False, self_deaf=True)
              ctx.voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(after_play(ctx, self.bot), self.bot.loop))
              await load.edit(f"Đang play **{title}**")
            else:
              await load.edit(f'**Chung tôi không support live Music**')
          if not texts.startswith("http"):
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
              info = ydl.extract_info(f"ytsearch5:{texts}", download=False)
              info = info['entries']
            now = datetime.utcnow()
            now3 = now.strftime("%Y-%m-%d %H:%M")
            now1 = now.strftime("%Y-%m-%d %H:")
            now2 = now.strftime("%M")
            now2 = int(now2) + 1
            nolive = []
            for i in info:
              title = i['title']
              if not title.endswith(now3):
                if not title.endswith(f"{now1}{now2}"):
                  nolive.append(i)
            try:
              URL = nolive[0]['formats'][0]['url']
              title = nolive[0]['title']
              source = FFmpegPCMAudio(URL)
              await channel.channel.connect()
              try:
                bot = ctx.guild.get_member(self.bot.user.id)
                await bot.edit(suppress = False)
              except:
                pass
              await ctx.guild.change_voice_state(channel=channel.channel, self_mute=False, self_deaf=True)
              ctx.voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(after_play(ctx, self.bot), self.bot.loop))
              await load.edit(f"Đang play **{title}**")
            except:
              await load.edit(f"**404 chúng tôi không thấy nhạc bạn yêu cầu**")
        else:
          channel = ctx.author.voice
          if not channel == None:
            voice = get(self.bot.voice_clients, guild=ctx.guild)
            if voice.channel == channel.channel:
              try:
                with open(f"./data/queue/{ctx.guild.id}.db", "rb") as fp:
                  listu = pickle.load(fp)
                listu.append(texts)
                print(texts)
                with open(f"./data/queue/{ctx.guild.id}.db", "wb") as fp:
                  pickle.dump(listu, fp)
                await ctx.reply(f"**Đã add vào queue**")
              except:
                await ctx.reply(f"**Đã add vào queue**")
                hi = []
                hi.append(texts)
                print(hi)
                open(f"./data/queue/{ctx.guild.id}.db","w")
                with open(f"./data/queue/{ctx.guild.id}.db", "wb") as fp:
                  pickle.dump(hi, fp)
            else:
              await ctx.send("<:Minecraft_Deny:903118973946707969> bạn không cùng voice với bot")
      else:
        await ctx.send("Vào voice để dùng music bro <:Minecraft_Deny:903118973946707969>")

def setup(bot):
    bot.add_cog(music(bot))
