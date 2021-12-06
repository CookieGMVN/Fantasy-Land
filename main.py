import sys
import os
import cpuinfo
import platform
import logging
import random
import discord, time, datetime
import asyncio
import aiohttp
import json 
import requests
import urllib
import pytz
import psutil
import json
import wikipedia
import googletrans
import urllib.parse
import pickle
import argparse
import contextlib
import io
import traceback
import subprocess
from io import BytesIO, StringIO
from os import system
from typing import List
from discord import member, guild, FFmpegPCMAudio
from requests import PreparedRequest
from hentai import Utils, Hentai, Format
from discord.ext.commands import Bot
from discord.ext import commands, tasks
from discord.utils import get
from random import randint
from datetime import timezone, timedelta
from datetime import datetime
from pytz import timezone
from discord.ext import tasks
from discord_together import DiscordTogether
from googletrans import Translator, LANGUAGES
from PIL import ImageColor
from sqlitekeyvaluestore import KeyValueStore
from discord.ext.commands import cooldown, BucketType
from simpcalc import simpcalc
from custom_google_search import search
from keep_alive import keep_alive
from pathlib import Path
from hurry.filesize import size, alternative
from colorama import *
from aioconsole import aexec

async def get_prefix(bot, message):
    try:
      guild =  str(message.guild.id)
      db = KeyValueStore('./data/prefix.db')
      default_prefix = db[guild]
      db.close()
      prefix=default_prefix.lower(), default_prefix.upper()
    except:
      db = KeyValueStore('./data/prefix.db')
      db.close()
      prefix = "s!", "S!"
    return commands.when_mentioned_or(*prefix)(bot, message)

intents = discord.Intents.all()
bot = commands.AutoShardedBot(shard_count=2, command_prefix=get_prefix, help_command=None, intents=intents)
khong = "không có tin nhắn"
sup = ""
ggl = ""
rb = ""
toplit = ""
users_on_cooldown = []

def get_prefix(ctx):
    try:
      try:
        guild =  str(ctx.guild.id)
        db = KeyValueStore('./data/prefix.db')
        default_prefix = db[guild]
        db.close()
      except:
        db = KeyValueStore('./data/prefix.db')
        db.close()
        default_prefix = "s!"
      return default_prefix
    except:
      pass

def restart_bot(): 
  os.execv(sys.executable, ['python'] + sys.argv)

def tas(names=""):
  global sup
  sup = names

def gg(names=""):
  global ggl
  ggl = names

def rbl(names=""):
  global rb
  rb = names

def topchat(names=""):
  global toplit
  toplit = names

async def net_usage(inf = "eth0"):
    net_stat = psutil.net_io_counters(pernic=True, nowrap=True)[inf]
    net_in_1 = net_stat.bytes_recv
    net_out_1 = net_stat.bytes_sent
    net_stat = psutil.net_io_counters(pernic=True, nowrap=True)["lo"]
    net_in_2 = net_stat.bytes_recv
    net_out_2 = net_stat.bytes_sent

    net_in = round((net_in_1 + net_in_2) / 1024 / 1024, 3)
    net_out = round((net_out_1 + net_out_2) / 1024 / 1024, 3)
    net_all = round((net_out_1 + net_in_1 + net_out_2 + net_in_2) / 1024 / 1024, 3)
    return f"**Network Total :** {net_all} MB\n> **Network In :** {net_in} MB\n> **Network Out : **{net_out} MB"

def folder(names):
  path, dirs, files = next(os.walk(names))
  file_count = files
  t = [str(os.path.getsize(f"{names}/{x}")) for x in file_count]
  t = "+".join(t)
  t = eval(t)
  return t

@bot.command()
@commands.guild_only()
async def google(ctx, args=None):
  if args == None:
    embed=discord.Embed(title=f"Google Search", description=f"VD : \n`{get_prefix(ctx)}google <câu hỏi>`")
    await ctx.send(embed=embed)

  if not args == None:
    API_KEY = os.getenv('google')
    CX = os.getenv('CX')
    hi = search(args, key=API_KEY, cx=CX)
    hi = hi["items"]
    if len(hi) == 10:
      del hi[9]
      del hi[8]
      del hi[7]
      del hi[6]
      del hi[5]
    for s in hi:
      name = s["title"]
      url = s["link"]
      description = s["snippet"]
      urld = s["displayLink"]
      gg(f"{ggl}**[{name}]({url})**\n`{urld}`\n{description}\n\n")
    embed=discord.Embed(title=f"Google Search", description=f"{ggl}")
    await ctx.send(embed=embed)
    gg()

@bot.command()
@commands.guild_only()
async def hex(ctx, args=None):
  if not args == None:
    try:
      los = args.replace("#", "")
      lol = f"#{los}"
      rgb = ImageColor.getcolor(lol, "RGB")
      rgb = str(rgb)
      rgb = rgb.replace("(", "")
      rgb = rgb.replace(")", "")
      embed=discord.Embed(color=int(los, 16))
      embed.add_field(name="Hex", value=lol, inline=False)
      embed.add_field(name="RGB", value=rgb, inline=False)
      embed.set_image(url=f"https://singlecolorimage.com/get/{los}/200x2")
      embed.set_thumbnail(url=f"https://singlecolorimage.com/get/{los}/200x200")
      await ctx.send(embed=embed)
    except:
      embed=discord.Embed(title=f"Mã hex không đúng")
      await ctx.send(embed=embed)
      
  if args == None:
    embed=discord.Embed(title=f"HEX COLOR", description=f"VD : \n`{get_prefix(ctx)}hex <hex color code>`")
    await ctx.send(embed=embed)

@bot.command()
@commands.guild_only()
async def tran(ctx, id=None,*, args=None):
  if not id == None:
    if ctx.message.reference == None:  
      embed=discord.Embed(title=f"Đang Translate")
      load = await ctx.reply(embed=embed)
    if not ctx.message.reference == None:
      channel = bot.get_channel(ctx.message.reference.channel_id)
      msg = await channel.fetch_message(ctx.message.reference.message_id)
      embed=discord.Embed(title=f"Đang Translate")
      load = await msg.reply(embed=embed)
    translator = Translator(service_urls=['translate.googleapis.com'])
    try:
      try:
        letters = id.split("_")
        url =  letters[0]
        dis =  letters[1]
        translated = translator.translate(args, src=url, dest=dis)
        embed=discord.Embed(title=f"Google Translate")
        embed.add_field(name=LANGUAGES.get(url), value=args, inline=False)
        embed.add_field(name=LANGUAGES.get(translated.dest), value=translated.text, inline=False)
        msg = await load.edit(embed=embed)
      except:
        letters = id.split("_")
        url =  letters[0]
        translated1 = translator.translate(args, dest=url)
        embed=discord.Embed(title=f"Google Translate")
        embed.add_field(name=f"Phát hiên ngôn ngữ ({LANGUAGES.get(translated1.src)})", value=args, inline=False)
        embed.add_field(name=LANGUAGES.get(translated1.dest), value=translated1.text, inline=False)
        try:
          dis =  letters[1]
          embed1=discord.Embed(title=f"Lỗi không dịch được `{get_prefix(ctx)}tran` để lấy mã Nước")
          await load.edit(embed=embed1)
        except:
          await load.edit(embed=embed)
    except:
      embed=discord.Embed(title=f"Lỗi không dịch được `{get_prefix(ctx)}tran` để lấy mã Nước")
      await load.edit(embed=embed)

  if id == None:
    hi = googletrans.LANGUAGES
    hi = str(hi)
    lol = hi.replace("{", "")
    lol = lol.replace("}", "")
    lol = lol.replace(":", " =")
    lol = lol.replace("'", "")
    lol = lol.replace(", ", " | ")
    embed=discord.Embed(title=f"Translate ", description=f"**HD : **\n`{get_prefix(ctx)}tran <s>_<s> <text>`\n**OR**\n`{get_prefix(ctx)}tran <s> <text>`\n<s> = Mã Ngôn Ngữ (check DMs để biết)\n <text> = text cần dịch\n**VD**\n`{get_prefix(ctx)}tran en-vi hi`\n`{get_prefix(ctx)}tran vi hi`")
    embed2=discord.Embed(title=f"Mã ngôn ngữ Translate", description=f"**Mã Ngôn Ngữ**\n{lol}")
    await ctx.reply(embed=embed)
    await ctx.author.send(embed=embed2)

@bot.command(name= 'r')
@commands.guild_only()
async def r(ctx):
  if ctx.author.id == 542602170080428063:
    await asyncio.sleep(0.2)
    await ctx.message.delete()
    await ctx.send("Restarting bot...")
    restart_bot()


@bot.command(name="ncode")
@commands.is_nsfw()
@commands.guild_only()
async def ncode(ctx):
    embed1=discord.Embed(title=f"Đang Load Sauce")
    load = await ctx.send(embed=embed1)
    code = Utils.get_random_id()
    doujin = Hentai(code)
    link = doujin.image_urls
    url =  link[0]
    tag = [tag.name for tag in doujin.tag]
    tag = '` , `'.join(tag)
    tag = f"`{tag}`"
    view = discord.ui.View()
    style = discord.ButtonStyle.gray
    item = discord.ui.Button(style=style, label="Click để đọc", url=f"https://nhentai.net/g/{code}")
    view.add_item(item=item)
    embed=discord.Embed(title=f"{doujin.title(Format.Pretty)}", description=f"Code nhentai: {code}")
    embed.add_field(name="Tag:", value=f"{tag}", inline=False)
    embed.set_footer(text="By Fantasy Land#5272")
    embed.set_image(url=url)
    await load.edit(embed=embed, view=view)

@ncode.error
async def on_command_error(ctx, error):
  if isinstance(error, commands.errors.NSFWChannelRequired):
     await ctx.send(f"{ctx.author.mention} Chỉ dùng ở khu NSFW <:Minecraft_Deny:903118973946707969>", delete_after=10)
     await ctx.message.delete()


@bot.command(name="hneko")
@commands.guild_only()
@commands.is_nsfw()
async def hneko(ctx):
    q = [f"https://nekos.life/api/v2/img/nsfw_neko_gif", f"https://nekos.life/api/v2/img/lewd", "https://api.waifu.pics/nsfw/neko"]
    s = random.choice(q)
    r = requests.get(s)
    r = r.json()
    ulr = r['url']
    embed=discord.Embed(title=f"Ảnh neko hentai của bạn đây")
    embed.set_footer(text="By Fantasy Land#5272")
    embed.set_image(url=ulr)
    await ctx.send(embed=embed)

@hneko.error
async def on_command_error(ctx, error):
  if isinstance(error, commands.errors.NSFWChannelRequired):
     await ctx.send(f"{ctx.author.mention} Chỉ dùng ở khu NSFW <:Minecraft_Deny:903118973946707969>", delete_after=10)
     await ctx.message.delete()

@bot.command(name="hentai")
@commands.guild_only()
@commands.is_nsfw()
async def hentai(ctx):
    q = ["https://api.waifu.pics/nsfw/waifu",f"https://nekos.life/api/v2/img/hentai", f"https://nekos.life/api/v2/img/Random_hentai_gif"]
    s = random.choice(q)
    r = requests.get(s)
    r = r.json()
    ulr = r['url']
    embed=discord.Embed(title=f"Ảnh hentai của bạn đây")
    embed.set_image(url=ulr)
    embed.set_footer(text="By Fantasy Land#5272")
    await ctx.send(embed=embed)

@hentai.error
async def on_command_error(ctx, error):
  if isinstance(error, commands.errors.NSFWChannelRequired):
     await ctx.send(f"{ctx.author.mention} Chỉ dùng ở khu NSFW <:Minecraft_Deny:903118973946707969>", delete_after=10)
     embed.set_footer(text="By Fantasy Land#5272")
     await ctx.message.delete()

@bot.command()
@commands.guild_only()
async def hug(ctx, user_1: discord.Member, user_2: discord.Member=None):
  try:
    r = requests.get(f"https://nekos.life/api/v2/img/hug")
    r = r.json()
    ulr = r['url']
    embed=discord.Embed(description=f"{user_1.mention} hug {user_2.mention}")
    embed.set_image(url=ulr)
    await ctx.send(embed=embed)

  except:
    r = requests.get(f'https://nekos.life/api/v2/img/hug')
    r = r.json()
    ulr = r["url"]
    embed=discord.Embed(description=f" {ctx.author.mention} hug {user_1.mention}")
    embed.set_image(url=ulr)
    await ctx.send(embed=embed)

@bot.command(name="neko")
@commands.guild_only()
async def neko(ctx):
    q = [f"https://nekos.life/api/v2/img/neko","https://api.waifu.pics/sfw/neko"]
    s = random.choice(q)
    r = requests.get(s)
    r = r.json()
    ulr = r['url']
    embed=discord.Embed(title=f"Ảnh neko của bạn đây")
    embed.set_image(url=ulr)
    embed.set_footer(text="By Fantasy Land#5272")
    await ctx.send(embed=embed)

@bot.command()
@commands.guild_only()
async def sv(ctx, args=khong, args4=khong, args3=khong):
  embed=discord.Embed(title=f"Đang load")
  load = await ctx.send(embed=embed)
  if args == khong:
    embed=discord.Embed(title=f"Server check help command", description=f"**Check server MC java/pe  \n Vd server java : **\n `{get_prefix(ctx)}sv java <ip> <port>` \n **Vd server pe : **\n `{get_prefix(ctx)}sv java <ip> <port>` \n **Note : Nếu là port mặc định bạn có thể không điền port \nPort mặc định pe : 19132\nPort mặc định java : 25565**")
    await load.edit(embed=embed)
  
  if args == "pe":
    try:
      try:
        argss = args4.lower()
        args2 = f"{argss}"
        if args3 == khong:
          port = ""
        if not args3 == khong:
          port = f":{args3}"
        r = requests.get(f"https://api.mcsrvstat.us/bedrock/2/{args2}{port}")
        r = r.json()
        ulr = r['ip']
        ulr1 = r['port']
        ulr2 = r['motd']['clean']
        ulr3 = r['players']['online']
        ulr4 = r['players']['max']
        ulr5 = r['version']
        ulr2 = '\n'.join(ulr2)
        embed=discord.Embed(title=f"{args2}", description=f"**IP : **{ulr}\n**Port : **{ulr1} \n**Trạng thái : **<:Online:903117591353122877> Online \n**Server info : **{ulr2} \n**Phiên bản : **{ulr5} Trở lên \n**Số người chơi : **{ulr3} / {ulr4}")
        await load.edit(embed=embed)
      except:
        argss = args4.lower()
        args2 = f"{argss}"
        if args3 == khong:
          port = ""
        if not args3 == khong:
          port = f":{args3}"
        r = requests.get(f"https://api.mcsrvstat.us/bedrock/2/{args2}{port}")
        r = r.json()
        ulr = r['ip']
        ulr1 = r['port']
        if not ulr == "127.0.0.1":
          embed=discord.Embed(title=f"{args2}", description=f"**IP : **{ulr}\n**Port : **{ulr1} \n**Trạng thái : **<:Offline:903118375264333824> Offline")
          await load.edit(embed=embed)
        if ulr == "127.0.0.1":
          embed=discord.Embed(title=f"Không tìm thấy server")
          await load.edit(embed=embed)
    except:
      embed=discord.Embed(title=f"Lỗi thử lại sau")
      await load.edit(embed=embed)  

  if args == "java":
    try:
      try:
        argss = args4.lower()
        args2 = f"{argss}"
        if args3 == khong:
          port = ""        
        if not args3 == khong:
          port = f":{args3}"
        r = requests.get(f"https://api.mcsrvstat.us/2/{args2}{port}")
        r = r.json()
        ulr = r['ip']
        ulr1 = r['port']
        ulr2 = r['motd']['clean']
        ulr3 = r['players']['online']
        ulr4 = r['players']['max']
        ulr5 = r['version']
        ulr2 = '\n'.join(ulr2)
        lol = f"https://eu.mc-api.net/v3/server/favicon/{args2}{port}"
        embed=discord.Embed(title=f"{args2}", description=f"**IP : **{ulr}\n**Port : **{ulr1} \n**Trạng tái : **<:Online:903117591353122877> Online \n**Server info :**\n{ulr2} \n**Phiên bản : **{ulr5}\n**Số người chơi : **{ulr3} / {ulr4}")
        embed.set_thumbnail(url=lol)
        await load.edit(embed=embed)
      except:        
        argss = args4.lower()
        args2= f"{argss}"
        if args3 == khong:
          por = ""
        if not args3 == khong:
          por = f":{args3}"
        r = requests.get(f"https://api.mcsrvstat.us/2/{args2}{port}")
        r = r.json()
        ulr = r['ip']
        ulr1 = r['port']
        if not ulr == "127.0.0.1":
          lol = f"https://eu.mc-api.net/v3/server/favicon/{args2}{port}"
          embed=discord.Embed(title=f"{args2}", description=f"**IP : **{ulr}\n**Port :** {ulr1} \n**Trạng thái :** <:Offline:903118375264333824> Offline")
          embed.set_thumbnail(url=lol)
          await load.edit(embed=embed)
        if ulr == "127.0.0.1":
          embed=discord.Embed(title=f"Không tìm thấy server")
          await load.edit(embed=embed)
    except:
      embed=discord.Embed(title=f"Lỗi thử lại sau")
      await load.edit(embed=embed) 

@bot.command()
@commands.guild_only()
async def mc(ctx,*, args=khong):
  if ctx.message.reference == None:  
    embed=discord.Embed(title=f"Đang load tài khoản MC")
    load = await ctx.send(embed=embed)
  if not ctx.message.reference == None:
    channel = bot.get_channel(ctx.message.reference.channel_id)
    msg = await channel.fetch_message(ctx.message.reference.message_id)
    embed=discord.Embed(title=f"Đang load tài khoản MC")
    load = await msg.reply(embed=embed)
  if args == khong:
    embed=discord.Embed(title=f"MC help command", description=f"**Lấy thông tin acc MC JAVA \n VD : **\n `{get_prefix(ctx)}mc <mc java name>`\n**OR**\n `{get_prefix(ctx)}mc <mc java uuid>` \n **Note : chỉ hỗ trợ acc pre**")
    await load.edit(embed=embed)

  if not args == khong:
    try:
      try:
        r = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{args}")
        r = r.json()
        ulr = r['name']
        uuid1 = r['id']
        s = requests.get(f"https://api.ashcon.app/mojang/v2/user/{uuid1}")
        s = s.json()
        uuid = s['uuid']
        embed=discord.Embed(title=f"{ulr}", url=f"https://vi.namemc.com/profile/{uuid}", description=f"**User uuid :**\n{uuid} \n**Note : chỉ hỗ trợ acc pre**")
        embed.set_thumbnail(url=f"https://mc-heads.net/avatar/{uuid}.png")
        await load.edit(embed=embed)
      except:
        r = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{args}")
        r = r.json()
        ulr = r['name']
        uuid1 = r['id']
        s = requests.get(f"https://api.ashcon.app/mojang/v2/user/{uuid1}")
        s = s.json()
        uuid = s['uuid']
        embed=discord.Embed(title=f"{ulr}", url=f"https://vi.namemc.com/profile/{uuid}", description=f"**User uuid :**\n{uuid} \n**Note : chỉ hỗ trợ acc pre**")
        embed.set_thumbnail(url=f"https://mc-heads.net/avatar/{uuid}.png")
        await load.edit(embed=embed)

    except:
      embed=discord.Embed(title=f"Không tìm thấy acc MC Java `{args}`")
      await load.edit(embed=embed)



@bot.command()
@commands.guild_only()
async def user(ctx, args=khong):  
  if ctx.message.reference == None:  
    embed=discord.Embed(title=f"Đang load user")
    load = await ctx.send(embed=embed)
  if not ctx.message.reference == None:
    channel = bot.get_channel(ctx.message.reference.channel_id)
    msg = await channel.fetch_message(ctx.message.reference.message_id)
    embed=discord.Embed(title=f"Đang load user")
    load = await msg.reply(embed=embed)
  try:
    guild = ctx.message.guild
    if args == khong:
      member = ctx.author
    if not args == khong:
      x = args.replace("<@", "")
      s = x.replace(">", "")
      e = s.replace("!", "")
      member = await bot.fetch_user(e)
    view = discord.ui.View()
    style = discord.ButtonStyle.gray
    item = discord.ui.Button(style=style, label="User Link", emoji="<:discord:907120262514872352>", url=f"https://discord.com/users/{member.id}")
    view.add_item(item=item)
    if guild.get_member(member.id) is not None:
      user = get(bot.get_all_members(), id=member.id)
      channel = user.voice
      if channel == None:
        voice = ""
      if not channel == None:
        voice = f"**User in Voice Channel:**\n<#{channel.channel.id}>\n"
      s = user.status
      lol1 = f"{s}"
      lol2 = lol1.replace("dnd", "<:Do_Not_Disturb:903117744239685663>")
      lol3 = lol2.replace("online", "<:Online:903117591353122877>")
      lol4 = lol3.replace("idle", "<:Idle:903118458252840971>")
      stastu1 = lol4.replace("offline", "<:Offline:903118375264333824>")
      join = user.joined_at.timestamp()
      join = f"<t:{int(join)}:d> <t:{int(join)}:T>\n(<t:{int(join)}:R>)"
      stastu1 = f"**User status : **{stastu1} {s}\n"
      nick = user.nick
      if nick == None:
        nick1 = ""
      if not nick == None:
        nick1 = f"**Server nickname : **\n{nick}\n"
    if not guild.get_member(member.id) is not None:
      stastu1 = ""
      join = "Chưa join server"
      nick1 = ""
      voice = ""
    if guild.get_member(member.id) is not None:
        try:  
          em1 = f"{member.activities[0].emoji} **|** "
          em = em1.replace("None **|** ", "")
        except:
          em1 = "None **|** "
          em = ""
    if guild.get_member(member.id) is not None:
      if not em1 == "None **|** ":
        at1 = user.activities[0].name
        at1 = f"{at1}"
        if not at1 == "None":
          at = user.activities[0].name
        if at1 == "None":
          at = ""
      if em1 == "None **|** ":
        try:
          try:
            at1 = user.activities[0].name
            at1 = f"{at1}"
            at = user.activities[0].name
          except:
            at = user.activities[0].name
        except:
          at = "Không có activities"
    if not guild.get_member(member.id) is not None:
      at = ":question: Không thấy user activities"
      em = ""
    ats = f"**User activities :**\n{em}{at}\n"
    if not guild.get_member(member.id) is not None:
      ats = f""
    if not member.bot:
      bot1 = "<:Minecraft_Deny:903118973946707969>"
    if member.bot:
      bot1 = "<:Minecraft_Accept:903118896368869447>"
    est = ""
    try:
      bar = "\n**User banner :**"
      lol1 = member.banner.url
    except:
      bar =""
      lol1 = "https://i.ibb.co/4gyPPjD/404.png"
    hypesquad_class = str(member.public_flags.all()).replace('<UserFlags.', '').replace('>', '').replace('_', ' ').replace(':', '').title()
    hypesquad_class = ''.join([i for i in hypesquad_class if not i.isdigit()])
    hypesquad_class = hypesquad_class.replace("[", "").replace("]", "").replace(" , ", "\n-")
    hypesquad_class = f"**User Badges :**\n-{hypesquad_class}\n"
    if hypesquad_class == "**User Badges :**\n-\n":
      hypesquad_class = ""
    if not hypesquad_class == "**User Badges :**\n-\n":
      hypesquad_class = hypesquad_class
    lol = f"{member.avatar.url}"
    dow = lol.replace(".webp?size=1024", ".png?size=1024")
    ulr = member.created_at.timestamp()
    ulr = f"<t:{int(ulr)}:d> <t:{int(ulr)}:T>\n(<t:{int(ulr)}:R>)"
    embed=discord.Embed(title=f"{member.name}#{member.discriminator}", description=f"{nick1}**Thời gian lập acc :**\n{ulr} \n**Thời gian join server :**\n{join} \n**User ID : **\n{member.id}\n{ats} {stastu1}{voice}{hypesquad_class}**Bot : ** {bot1}{est}{bar}")
    embed.set_thumbnail(url=f"{dow}")
    embed.set_image(url=lol1)
    await load.edit(embed=embed, view=view)
  except:
    embed=discord.Embed(title=f"Không tìm thấy user")
    await load.edit(embed=embed)

@bot.command()
@commands.guild_only()
async def help(ctx):
    embed=discord.Embed(title=f"Commands List", description=f"**Utility Command**\n`{get_prefix(ctx)}tran` : Google Translaten\n`{get_prefix(ctx)}google` : Google Search\n`{get_prefix(ctx)}wiki` : Wikipedia\n`{get_prefix(ctx)}youtubetogether` : dùng Youtube Together \n`{get_prefix(ctx)}afk <lí do>` : AFK. \n`{get_prefix(ctx)}calc` or `{get_prefix(ctx)}calc <phép tính>`: mở máy tính bot túi \n**Random Command**\n`{get_prefix(ctx)}ship` : check tình cảm dành cho nhău.\n**Anime Command**\n`{get_prefix(ctx)}sanime` : Check phim anime.\n`{get_prefix(ctx)}anime` : Nhận ảnh anime random.\n`{get_prefix(ctx)}neko` : Nhận ảnh neko random. \n**Info Command**\n`{get_prefix(ctx)}avatar <@user>` : Lấy avatar của bạn hoặc ai đấy \n`{get_prefix(ctx)}user  <@user>` : Hiển thị thông tin về bạn hoặc ai đó. \n`{get_prefix(ctx)}roblox` : Lấy thông tin acc Roblox \n`{get_prefix(ctx)}hex <hex code>` : Check HEX COLOR \n`{get_prefix(ctx)}sv <java/pe> <ip> <port>` : Check server MC java/pe \n`{get_prefix(ctx)}mc <mc java name>` : Lấy thông tin acc MC JAVA \n**Global Chat**\n`{get_prefix(ctx)}achat` : Add kênh vào list global chat (Administration)\n`{get_prefix(ctx)}rchat` : bỏ kênh khỏi list global chat (Administration)\n**Level Command**\n`{get_prefix(ctx)}rank` : Check rank chat\n`{get_prefix(ctx)}top` : Check top chat của server\n**Economy Command**\n`{get_prefix(ctx)}start` : tạo acc Flcoin\n`{get_prefix(ctx)}cash` : xem số Flcoin trong tài khoản\n`{get_prefix(ctx)}bank` : gửi hoặc rút tiên vào bank để có lãi\n`{get_prefix(ctx)}bcash` : xem tiên trong bank \n`{get_prefix(ctx)}give <@user> <FLcoin>` : đưa tiên cho ai đấy\n`{get_prefix(ctx)}coinflip <FLcoin>` : đỏ đen kiếm Flcoin \n`{get_prefix(ctx)}slot <FLcoin>` : Slot đỏ đen kiếm Flcoin\n`{get_prefix(ctx)}minly` : nhận tiên theo phút \n**NSFW command**\n||`{get_prefix(ctx)}ncode`: Nhận random code sauce from nhentai||\n||`{get_prefix(ctx)}hentai`: Nhận random ảnh hentai|| \n||`{get_prefix(ctx)}hneko` : Nhận random ảnh neko hentai||\n**Moderation Command**\n`{get_prefix(ctx)}ban` : Ban a user\n`{get_prefix(ctx)}unban` : Unban a user\n`{get_prefix(ctx)}kick` : Kick a user\n`{get_prefix(ctx)}mute` : Mute a user\n`{get_prefix(ctx)}unmute` : Unmute a user\n`{get_prefix(ctx)}lock` : Lock kênh chat\n`{get_prefix(ctx)}unlock` : Unlock kênh chat\n`{get_prefix(ctx)}clear <number of messages>` : Dọn dẹp tin nhắn ở một kênh chat\n**Administration Command**\n`{get_prefix(ctx)}prefix` : set bot prefix\n`{get_prefix(ctx)}nuke` : Nuke kênh nào đó (tạo lại kênh đấy)\n**Bot Command**\n`{get_prefix(ctx)}info` : Xem bot info \n`{get_prefix(ctx)}support` : for bot support")
    view = discord.ui.View()
    style = discord.ButtonStyle.gray
    item = discord.ui.Button(style=style, label="Invite Bot", emoji="<:Invite:912854840156246078>", url=f"https://discord.com/api/oauth2/authorize?client_id=903120513243693116&permissions=8&scope=bot%20applications.commands")
    view.add_item(item=item)
    await ctx.send(embed=embed, view=view)
  
@bot.command()
@commands.guild_only()
async def avatar(ctx, args=khong):
  guild = ctx.message.guild
  try:
    if args == khong:
      member = ctx.author
    if not args == khong:
      x = args.replace("<@", "")
      s = x.replace(">", "")
      e = s.replace("!", "")
      member = await bot.fetch_user(e)
    if guild.get_member(member.id) is not None:
      test = "Đã join Server"
    if not guild.get_member(member.id) is not None:
      test = "Chưa join server"
    embed=discord.Embed(title=f"Avatar {member.name}#{member.discriminator}")
    lol = f"{member.avatar.url}"
    dow = lol.replace(".webp?size=1024", ".png?size=1024")
    embed.set_image(url=f'{dow}')
    embed.set_footer(text=f"{test}\nUser ID : {member.id}")
    await ctx.send(embed=embed)
  except:
    embed=discord.Embed(title=f"Không tìm thấy Avatar của  `{args}`")
    await ctx.send(embed=embed)

@bot.command(pass_context=True)
@commands.guild_only()
async def info(ctx):
  embed=discord.Embed(title=f"Đang load info Bot")
  load = await ctx.reply(embed=embed)
  shard_id = ctx.guild.shard_id
  shard = bot.get_shard(shard_id)
  shard_ping = shard.latency
  delta_uptime = datetime.now() - startdate
  hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
  minutes, seconds = divmod(remainder, 60)
  days, hours = divmod(hours, 24)
  uptime = f"{hours} Hours, {minutes} Minutes, {seconds} Seconds"
  test = size(folder(".") + folder("./data") + folder("./data/level") + folder("./cogs"), system=alternative)
  embed=discord.Embed(title=f"Info", description=f"**Bot Code by : [{await bot.fetch_user(542602170080428063)}](https://discord.com/users/542602170080428063)**\n**Info :**\n```Discord.py : {discord.__version__}\nPython : {platform.python_version()}\nOS : {platform.system()}\nCPU : {cpuinfo.get_cpu_info()['brand_raw']}```\n**Shard Status**\n> **Shard Online :** {int(len(bot.shards))}/{int(len(bot.shards))} \n> **Guilds Shard Ping : **{round(shard_ping * 1000)} ms\n> **Guilds Shard ID : **{shard_id + 1}\n**Bot Status**\n> **Uptime : **{uptime}\n> **Ping :** {round(bot.latency * 1000)} ms\n> **Guilds : **{int(len(bot.guilds))-1} Guilds\n> **Member : **{int(len(bot.users))} Member\n**Bot process data**\n> **CPU :  **{str(round(psutil.cpu_percent(),1))}% \n> **RAM : **{str(round(psutil.virtual_memory().percent,1))}%\n> **Disk Use** : {test}\n> {await net_usage()}\n**[Invite Bot](https://discord.com/api/oauth2/authorize?client_id=903120513243693116&permissions=8&scope=bot%20applications.commands)**")
  await load.edit(embed=embed)

@bot.command()
@commands.guild_only()
async def anime(ctx):
    r = requests.get("https://api.waifu.pics/sfw/waifu")
    r = r.json()
    ulr = r['url']
    embed=discord.Embed(title=f"Ảnh anime của bạn đây")
    embed.set_image(url=ulr)
    embed.set_footer(text="By Fantasy Land#5272")
    await ctx.send(embed=embed)

@bot.event
async def on_member_join(member):  
  if member.guild.id == 886959744714149988:
        await bot.get_channel(912710131379236946).send(f"{member.mention} vừa server {member.guild.name} vùa mới join server và đang verify")
        """embed = discord.Embed(title=f"Chào mừng bạn đến với {member.guild.name} của chúng tui {member}", colour=discord.Colour.random())
        req = PreparedRequest()
        req.prepare_url(
            url='https://api.xzusfin.repl.co/card?',
            params={
                'avatar': str(member.avatar.url),
                'middle': 'welcome',
                'name': str(member),
                'bottom': str(f"to {member.guild.name}"),
                'text': '#ffffff',
                'avatarborder': '#437ef7',
                'avatarbackground': '#00437ef700',
                'background': 'https://i.ibb.co/jZWVw00/Untitled-1.png' #or image url
            }
        )
        try:
          urllib.request.urlretrieve(req.url, 'wellcome.png')
          file = discord.File("wellcome.png")
          embed.set_image(url="attachment://wellcome.png")
          await bot.get_channel(887138286341091328).send(embed=embed, file=file)
        except:
          embed.set_image(url=req.url)
          await bot.get_channel(887138286341091328).send(embed=embed)"""

        
    

@bot.event
async def on_member_remove(member):
  if not member.id == 903120513243693116:
    sid = str(member.guild.id)
    s = str(member.id)
    try:
      db = KeyValueStore('./data/svafk.db')
      b = db[sid]
      s = b.replace(f" '{s}',", "")
      db[sid] = s
      db.close()
    except:
      pass
    try:
      af = KeyValueStore('./data/afk.db')
      del af[f"{s}, {sid}"]
      af.close()
    except:
      pass
    try:
      db = KeyValueStore(f'./data/level/{sid}.db')
      del  db[f"{s}, {sid}"]
      db.close()
    except:
      pass

@bot.event 
async def on_guild_remove(guild):
      sid = str(guild.id)
      try:
        db = KeyValueStore('./data/prefix.db')
        del db[guild]
        db.close()
      except:
        pass
      try:
        db = KeyValueStore('./data/svafk.db')
        del db[sid]
        db.close()
      except:
        pass
      try:
        af = KeyValueStore('./data/afk.db')
        keys = af.keys()
        af.close()
        for i in keys: 
          if str(i).endswith(str(sid)):
            af = KeyValueStore('./data/afk.db')
            del af[i]
            af.close()
      except:
        pass
      try:
        os.remove(f'./data/level/{sid}.db')
      except:
        pass


@bot.command(aliases=['youtubetogether'])
@commands.guild_only()
async def ytt(ctx):
  try:
    link = await bot.togetherControl.create_link(ctx.author.voice.channel.id, 'youtube', max_age=12, max_uses=1)
    view = discord.ui.View()
    style = discord.ButtonStyle.gray
    item = discord.ui.Button(style=style, label=" Youtube Together", emoji="<:YouTube:907111757204561951>", url=link)
    view.add_item(item=item)
    test = await ctx.send("**Nhấn vào nút ở dưới để dùng Youtube Together**\n(chỉ dành cho pc)", view=view)
    await asyncio.sleep(10)
    view = discord.ui.View()
    await test.edit(f"**Link Youtube Together hết hạn\n`{get_prefix(ctx)}ytt` để dùng tạo link Youtube Together mới**", view=view)
  except:
    await ctx.send("Vào voice để dùng Youtube Together bro <:Minecraft_Deny:903118973946707969> ")

########################################################

@bot.command()
@commands.guild_only()
async def start(ctx):
  try:
    try:
      db = KeyValueStore('./data/usercoin.db')
      ba = KeyValueStore('./data/bank.db')
      user = str(ctx.author.id)
      s = ba[user]
      c = db[user]
      await ctx.send('**Bạn đã có tài khoản**')
      db.close() 
    except:
      db = KeyValueStore('./data/usercoin.db')
      ba = KeyValueStore('./data/bank.db')
      c = db[user]
      ba[user] = "0"
      db.close()
      ba.close()
      await ctx.send('**Bạn đã tạo tài khoản Bank**')
  except:
    db = KeyValueStore('./data/usercoin.db')
    ba = KeyValueStore('./data/bank.db')
    user = str(ctx.author.id)
    db[user] = "100"
    ba[user] = "0"
    await ctx.send('**Bạn đã tạo tài khoản và có 100 FLcoin trong tài khoản**')
    db.close()
    ba.close()

@bot.command(aliases=['c'])
@commands.guild_only()
async def cash(ctx):
  try:
    db = KeyValueStore('./data/usercoin.db')
    user = str(ctx.author.id)
    c = db[user]
    await ctx.send(f'**{ctx.author} Bạn có {c} FLcoin**')
    keys = db.keys()
    db.close()
  except:
    await ctx.send(f'**Bạn chưa lập tài khoản dùng \n`{get_prefix(ctx)}start` để lập tài khoản**')

@bot.command()
@commands.guild_only()
async def give(ctx, users, tien:int=0):
  try:
    db = KeyValueStore('./data/usercoin.db')
    user = str(ctx.author.id)
    x = users.replace("<@", "")
    s = x.replace(">", "")
    e = s.replace("!", "")
    c = db[user]
    try:
      member = await bot.fetch_user(e)
      if not int(c) == 0:
        if tien > 0:
          if tien <= int(c):
            if not member.bot:
              if ctx.author == ctx.author:
                try:
                  db = KeyValueStore('./data/usercoin.db')
                  x = users.replace("<@", "")
                  s = x.replace(">", "")
                  e = s.replace("!", "")
                  g = db[e]
                  #trừ tiền trong tài khoản
                  user = str(ctx.author.id)
                  c = db[user]
                  z = int(c) - tien
                  db[user] = z
                  #gửi tiền
                  g = db[e]
                  a = int(g) + tien
                  db[e] = a
                  db.close()
                  member = await bot.fetch_user(e)
                  await ctx.send(f'**💳 | {ctx.author} gửi {tien} FLcoin tới {member}**')
                except:
                  await ctx.reply(f'**User bạn gửi chưa lập tài khoản**')
              else:
                db.close()
                await ctx.send(f'**💳 | {ctx.author} gửi {tien} FLcoin tới {ctx.author} nhưng tại sao ?**')
            else:
              db.close()
              await ctx.reply(f'**Không thể chuyển tiên cho bot**')
          else:
            db.close()
            await ctx.reply(f'**💳 | {ctx.author} bạn không con đủ tiền để giao dịch**')
        else:
          db.close()
          await ctx.reply(f'**Số tiền cần chuyên không hợp lệ**')
      else:
        db.close()
        await ctx.reply(f'**Bạn còn 0 FLcoin không thể giao dịch**')
    except:
      await ctx.send(f'**người chuyển không hợp lệ**')
  except:
    db.close()
    await ctx.send(f'**Bạn chưa lập tài khoản dùng \n`{get_prefix(ctx)}start` để lập tài khoản**')

@bot.command(name="minly", aliases=['mly'])
@commands.guild_only()
@commands.cooldown(1, 60, commands.BucketType.user)
async def minly(ctx):
  db = KeyValueStore('./data/usercoin.db')
  coin = random.randint(30, 50)
  user = str(ctx.author.id)
  c = db[user]
  t = int(c) + int(coin)
  db[user] = t
  db.close()
  await ctx.send(f'**Bạn nhận được {coin} FLcoin**')

@minly.error
async def command_name_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
          em = discord.Embed(title=f"Chậm xuống bro!",description=f"thử lại sau {error.retry_after:.2f}s.")
          await ctx.reply(embed=em)

@bot.command(name="cf", aliases=['coinfilp'])
@commands.guild_only()
@commands.cooldown(1, 5, commands.BucketType.user)
async def cf(ctx, arg:int=0):
  try:
    user = str(ctx.author.id)
    db = KeyValueStore('./data/usercoin.db')
    c = db[user]
    if not int(c) == 0:
      if arg > 0:
        if arg <= 50000:
          if arg <= int(c):
            load = await ctx.reply(f'**{ctx.author} Tung coin <a:Sonic_Coin_Spin:906198269758177310> và chọn Head**')
            ran = ["1", "0"]
            p = random.choices(ran, weights=[65, 35])
            p = ''.join(p)
            await asyncio.sleep(1)
            if p == "1":
              db = KeyValueStore('./data/usercoin.db')
              user = str(ctx.author.id)
              c = db[user]
              t = int(c) + arg
              db[user] = t
              db.close()
              await load.edit(f'**{ctx.author} Tung coin và chọn Head\nVà coin là <:head:906197948151504916> Head và bạn thắng {arg + arg} FLcoin**')
            if p == "0":
              db = KeyValueStore('./data/usercoin.db')
              user = str(ctx.author.id)
              c = db[user]
              t = int(c) - arg
              db[user] = t
              db.close()
              await load.edit(f'**{ctx.author} Tung coin và chọn Head\nVà coin là  <:tail:906197948134740008> Tail và bạn mất hết**')
          else:
            db.close()
            await ctx.reply(f'**Số tiên của bạn không đủ**')
        else:
          db.close()
          await ctx.reply(f'**Số tiền để chơi vui lòng dươi 50,000 FLcoin**')
      else:
        db.close()
        await ctx.reply(f'**Số tiền để chơi không hợp lệ**')
    else:
      db.close()
      await ctx.reply(f'**Bạn còn 0 FLcoin không thể giao dịch**')
  except:
    db.close()
    await ctx.send(f'**Bạn chưa lập tài khoản dùng \n`{get_prefix(ctx)}start` để lập tài khoản**')

@cf.error
async def command_name_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f"{ctx.author} Chậm xuông!",description=f"thử lại sau {error.retry_after:.2f}s.")
            d =  await ctx.reply(embed=em, delete_after=error.retry_after)

@bot.command(name="slot", aliases=['s'])
@commands.guild_only()
@commands.cooldown(1, 5, commands.BucketType.user)
async def slot(ctx, arg:int=0):
  try:
    user = str(ctx.author.id)
    db = KeyValueStore('./data/usercoin.db')
    c = db[user]
    if not int(c) == 0:
      if arg > 0:
        if arg <= 50000:
          if arg <= int(c):
            load = await ctx.reply(f'**{ctx.author} Spin <a:spen:907857437745365013> và đặt cược {arg}**')
            ran = ["1", "0", "2"]
            p = random.choices(ran, weights=[35, 36, 28])
            p = ''.join(p)
            await asyncio.sleep(2)
            if p == "1":
              db = KeyValueStore('./data/usercoin.db')
              user = str(ctx.author.id)
              c = db[user]
              t = int(c) + arg
              db[user] = t
              db.close()
              await load.edit(f'**{ctx.author} Spin  <:2_:907857437355290654> \nVà bạn thắng {arg + arg} FLcoin**')
            if p == "0":
              db = KeyValueStore('./data/usercoin.db')
              user = str(ctx.author.id)
              c = db[user]
              t = int(c) - arg
              db[user] = t
              db.close()
              await load.edit(f'**{ctx.author} Spin  <:1_:907857437367894057> \nVà bạn mất hết**')
            if p == "2":
              db = KeyValueStore('./data/usercoin.db')
              user = str(ctx.author.id)
              c = db[user]
              t = int(c) + arg + arg
              db[user] = t
              db.close()
              await load.edit(f'**{ctx.author} Spin  <:3_:907857436994568194> \nVà bạn trúng {arg + arg + arg} FLcoin**')
          else:
            db.close()
            await ctx.reply(f'**Số tiên của bạn không đủ**')
        else:
          db.close()
          await ctx.reply(f'**Số tiền để chơi vui lòng dươi 50,000 FLcoin**')
      else:
        db.close()
        await ctx.reply(f'**Số tiền để chơi không hợp lệ**')
    else:
      db.close()
      await ctx.reply(f'**Bạn còn 0 FLcoin không thể giao dịch**')
  except:
    db.close()
    await ctx.send(f'**Bạn chưa lập tài khoản dùng \n`{get_prefix(ctx)}start` để lập tài khoản**')

@slot.error
async def command_name_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f"{ctx.author} Chậm xuông!",description=f"thử lại sau {error.retry_after:.2f}s.")
            d =  await ctx.reply(embed=em, delete_after=error.retry_after)

@bot.command()
@commands.guild_only()
async def reset(ctx, arg):
  if ctx.author.id == 542602170080428063:
    db = KeyValueStore('./data/usercoin.db')
    db[arg] = "100"
    db.close()

@bot.command(aliases=['b'])
@commands.guild_only()
async def bank(ctx, args=None, ci:int=0):
  user = str(ctx.author.id)
  try:
    if args == "+":
      ba = KeyValueStore('./data/bank.db')
      db = KeyValueStore('./data/usercoin.db')
      a = ba[user]
      c = db[user]
      if not int(c) == 0:
        if not int(ci) == 0:
          if ci > 0:
            if ci <= int(c):
              try:
                ba = KeyValueStore('./data/bank.db')
                db = KeyValueStore('./data/usercoin.db')
                c = db[user]
                d = int(c) - int(ci)
                db[user] = d
                a = ba[user]
                d = int(a) + int(ci)
                ba[user] = d
                db.close()
                ba.close()
                await ctx.send(f'**{ctx.author} bạn đã chuyển {ci} FLcoin vào bank**')
              except:
                db.close()
                ba.close()
                await ctx.send(f'lỗi')
            else:
              db.close()
              ba.close()
              await ctx.reply(f'**Số tiên của bạn không có đủ từng đấy FLcoin để chuyển vào bank**')
          else:
            db.close()
            ba.close()
            await ctx.reply(f'**số tiển nạp vào không hợp lệ**')
        else:
          db.close()
          ba.close()
          await ctx.reply(f'**số tiển nạp vào không hợp lệ**')
      else:
        db.close()
        ba.close()
        await ctx.reply(f'**bạn còn 0 FLcoin không thể nạp vào**')

        
    if args == "-":
      ba = KeyValueStore('./data/bank.db')
      db = KeyValueStore('./data/usercoin.db')
      c = db[user]
      fl = ba[user]
      if not int(fl) == 0:
        if ci > 0:
          if ci <= int(fl):
            try:
              ba = KeyValueStore('./data/bank.db')
              db = KeyValueStore('./data/usercoin.db')
              a = ba[user]
              d = int(a) - int(ci)
              ba[user] = d              
              c = db[user]
              d = int(c) + int(ci)
              db[user] = d
              db.close()
              ba.close()
              await ctx.send(f'**{ctx.author} bạn đã chuyển {ci} FLcoin từ bank vào ví của bạn**')
            except:
              db.close()
              ba.close()
              await ctx.send(f'**lỗi**')
          else:
            db.close()
            ba.close()
            await ctx.reply(f'**Số tiên của bạn trong bank không có đủ từng đấy FLcoin để rút**')
        else:
          db.close()
          ba.close()
          await ctx.reply(f'**số tiển rút vào không hợp lệ**')
      else:
        db.close()
        ba.close()
        await ctx.reply(f'**Bank của bạn còn 0 FLcoin không thể rut tiền nũa**')
      

    if args == None:
      embed=discord.Embed(title=f"Hưỡng dẫn dùng bank")
      embed.add_field(name="Nạp tiền", value=f"`{get_prefix(ctx)}bank + <FLcoin>`", inline=False)
      embed.add_field(name="VD:", value=f"`{get_prefix(ctx)}bank + 1`", inline=False)
      embed.add_field(name="Rút tiền", value=f"`{get_prefix(ctx)}bank - <FLcoin>`", inline=False)
      embed.add_field(name="VD:", value=f"`{get_prefix(ctx)}bank - 1`", inline=False)
      embed.add_field(name="xem tiền trong bank", value=f"`{get_prefix(ctx)}bcash`", inline=False)
      await ctx.send(embed=embed)

  except:
    db.close()
    ba.close()
    await ctx.send(f'**Bạn chưa lập tài khoản `{get_prefix(ctx)}start` để tạo**')

@bot.command(aliases=['bc'])
@commands.guild_only()
async def bcash(ctx):
  try:
    db = KeyValueStore('./data/bank.db')
    user = str(ctx.author.id)
    c = db[user]
    await ctx.send(f'**{ctx.author} Bạn có {c} FLcoin ở trong bank**')
    keys = db.keys()
    db.close()
  except:
    db.close()
    await ctx.send(f'**Bạn chưa lập tài khoản `{get_prefix(ctx)}start` để tạo**')

########################################################

@bot.command()
@commands.guild_only()
async def invt(ctx):
  if ctx.author.id == 542602170080428063:
    for hi in bot.guilds:
      ivt = await hi.text_channels[0].create_invite(max_age=120, max_uses=1)
      await ctx.send(f'{hi.name}\n{ivt}')

@bot.command()
@commands.guild_only()
async def ship(ctx, user_1 : discord.Member=None, user_2 : discord.Member=None):
  if not user_1 == None:
    if user_2 == None:
      user = ctx.author
      users = user_1
    if not user_2 == None:
      user = user_1
      users = user_2
    arg = random.randint(1, 100)   
    await ctx.channel.send(f"Tình cảm mà {user.mention} giành cho {users.mention} là {arg}%")
  if user_1 == None:
    embed=discord.Embed(title=f"Ship command", description=f"VD\n`{get_prefix(ctx)}ship <@user>`\nOR\n`{get_prefix(ctx)}ship <@user1> <@user2>`")
    await ctx.send(embed=embed)

@bot.command()
@commands.guild_only()
async def roblox(ctx,*, arg=None):
  if not arg == None:
    def check(msg):
          return msg.author == ctx.author and msg.channel == ctx.channel  
    r = requests.get(f"https://users.roblox.com/v1/users/search?keyword={arg}&limit=10")
    r = r.json()
    embed=discord.Embed(title=f"Đang load")
    load = await ctx.reply(embed=embed)
    try:
      t = r["data"]
      if len(t) == 10:
        del t[9]
        del t[8]
        del t[7]
        del t[6]
        del t[5]
      for count, hi in enumerate(t, 1):
        n = hi["name"]
        id = hi["id"]
        dn = hi["displayName"]
        rbl(f"{rb}**{count} :** {n}\n**ID :** {id}\n**Display Name :** {dn}\n")
      embed=discord.Embed(title=f"Roblox account", description=f"{rb}---------------------------------\nNhập một số ở trên để xem")
      await load.edit(embed=embed)
      rbl()
      msg = await bot.wait_for("message", timeout=60, check=check)
      await msg.delete()
      s = int(msg.content) - 1
      try:
        url =  t[s]
      except:
        embed=discord.Embed(title=f"Bạn nhập không đúng", description=f"nhập `{get_prefix(ctx)}roblox {arg}` để làm lại")
        await load.edit(embed=embed)
      id = url["id"]
      r = requests.get(f"https://users.roblox.com/v1/users/{id}")
      r = r.json()
      ban = r["isBanned"]
      if ban == False:
        ban = "<:Minecraft_Deny:903118973946707969>"
      if ban == True:
        ban = "<:Minecraft_Accept:903118896368869447>"
      timec = r["created"]
      dn = r["displayName"]
      name = r["name"]
      timec = requests.get(f"https://showcase.api.linx.twenty57.net/UnixTime/tounixtimestamp?datetime={timec}").json()
      timec = timec["UnixTimeStamp"]
      embed=discord.Embed(title=f"{name}", description=f"**ID : **{id}\n**Thời gian lâp acc :**\n<t:{timec}:d> <t:{timec}:T> (<t:{timec}:R>)\n**Display Name : **{dn}\nBan : {ban}")
      embed.set_thumbnail(url=f"http://www.roblox.com/Thumbs/Avatar.ashx?x=352&y=352&Format=Png&userid={id}")
      view = discord.ui.View()
      style = discord.ButtonStyle.gray
      item = discord.ui.Button(style=style, label="User Link", url=f"https://www.roblox.com/users/{id}/profile")
      view.add_item(item=item)
      await load.edit(embed=embed, view=view)
    except:
      embed=discord.Embed(title=f"Không có kết quả")
      await load.edit(embed=embed)
  if arg == None:
    embed=discord.Embed(title=f"Roblox Command", description=f"**HD**\n`{get_prefix(ctx)}roblox <username>`\n**VD**\n`{get_prefix(ctx)}roblox duongtuan30306`")
    await ctx.send(embed=embed)

@bot.command()
@commands.guild_only()
async def wiki(ctx,*, arg=None):
  if not arg == None:
    def check(msg):
          return msg.author == ctx.author and msg.channel == ctx.channel
    embed=discord.Embed(title=f"Đang load")
    load = await ctx.send(embed=embed)
    x = wikipedia.search(arg, results=8)
    if not int(len(x)) == 0:
      for count, item in enumerate(x, 1):
        t = f"{count} : {item}\n"
        n = f"{sup}{t}"
        tas(n)
      embed=discord.Embed(title=f"List tìm kiếm được", description=f"{sup}**Nhập một số trên để xem**")
      await load.edit(embed=embed)
      tas()
      msg = await bot.wait_for("message", timeout=60, check=check)
      embed=discord.Embed(title=f"Đang load")
      await load.edit(embed=embed)
      await msg.delete()
      s = int(msg.content) - 1
      try:
        url =  x[s]
      except:
        embed=discord.Embed(title=f"Bạn nhập không đúng", description=f"nhập `{get_prefix(ctx)}wiki {arg}` để làm lại")
        await load.edit(embed=embed)
      try:
        ny = wikipedia.page(str(url))
        text = ny.content
        text = text.split("\n\n\n")
        embed=discord.Embed(title=ny.title, url=ny.url, description=f"{text[0]}..")
        try:
          await load.edit(embed=embed)
        except:
          embed=discord.Embed(title=ny.title, url=ny.url, description=f"Dài quá không thể up lên Click ở trên để đọc")
          await load.edit(embed=embed)
      except:
        embed=discord.Embed(title=f"404", description=f" Chúng tôi không thây trang bạn yêu cầu xin hoặc là NSFW thông cảm")
        await load.edit(embed=embed)
    else:
      embed=discord.Embed(title=f"Không có kết quả")
      await load.edit(embed=embed)
  else:
    embed=discord.Embed(title=f"wiki help", description=f"HD\n`{get_prefix(ctx)}wiki <vặt cần tìm>`\nVD\n`{get_prefix(ctx)}wiki Minecraft`")
    await ctx.send(embed=embed)

@bot.command()
@commands.guild_only()
async def afk(ctx,*, afk="AFK"):
  try:
    i = str(ctx.author.id)
    sid = str(ctx.guild.id)
    db = KeyValueStore('./data/svafk.db')
    af = KeyValueStore('./data/afk.db')
    s = db[sid]
    k = f"{s} '{i}',"
    db[sid] = k
    af[f"{i}, {sid}"] = afk
    db.close()
    af.close()
    db = KeyValueStore('./data/afkt.db')
    db[f"{i}, {sid}"] = str(int(time.time()))
    db.close()
    nick = ctx.author.nick
    try:
      if nick is None:
        await ctx.author.edit(nick=f"[AFK] {ctx.author.name}")
      if not nick is None:
        if not nick.startswith("[AFK] "):
          await ctx.author.edit(nick=f"[AFK] {nick}")
    except:
      pass
    await ctx.send(f'**{ctx.author.mention} Đặt afk là :** {afk} ')
  except:
    i = str(ctx.author.id)
    sid = str(ctx.guild.id)
    db = KeyValueStore('./data/svafk.db')
    af = KeyValueStore('./data/afk.db')
    k = f" '{i}',"
    db[sid] = k
    af[f"{i}, {sid}"] = afk
    db.close()
    af.close()
    nick = ctx.author.nick
    try:
      if nick == None:
        await ctx.author.edit(nick=f"[AFK] {ctx.author.name}")
      if not nick == None:
        await ctx.author.edit(nick=f"[AFK] {nick}")
    except:
      pass
    db = KeyValueStore('./data/afkt.db')
    db[f"{i}, {sid}"] = str(int(time.time()))
    db.close()
    await ctx.send(f'**{ctx.author.mention} Đặt afk là :** {afk} ')

@bot.command()
@commands.guild_only()
async def prefix(ctx, arg=None):
  if not arg == None:
    guild =  str(ctx.guild.id)
    if ctx.author.guild_permissions.administrator:
      if not arg.lower() == "reset":
        if not arg.lower() == "s!":
          db = KeyValueStore('./data/prefix.db')
          db[guild] = arg
          db.close()
          embed=discord.Embed(title=f"Đã set Prefix là : `{arg}`")
          await ctx.send(embed=embed)
        if arg.lower() == "s!":
          db = KeyValueStore('./data/prefix.db')
          try:
            del db[guild]
          except:
            pass
          db.close()
          embed=discord.Embed(title=f"Đã set Prefix là : `{arg}`")
          await ctx.send(embed=embed)
      if arg.lower() == "reset":
        db = KeyValueStore('./data/prefix.db')
        try:
          del db[guild]
        except:
          pass
        db.close()
        embed=discord.Embed(title=f"Đã reset Prefix")
        await ctx.send(embed=embed)
    else:
      await ctx.reply(f'Bạn không có quyền dùng command này')
  if arg == None:
    embed=discord.Embed(title=f"Prefix help", description=f"VD\n`{get_prefix(ctx)}prefix <prefix>`\nReset prefix\n`{get_prefix(ctx)}prefix reset`")
    embed.add_field(name="Yêu cầu", value=f"User dùng command có quyền : \nAdministrator", inline=False)
    await ctx.send(embed=embed)

@bot.command()
@commands.guild_only()
async def rank(ctx, user:discord.Member=None):
  async with ctx.channel.typing():
      if not user == None:
        user = user
      if user == None:
        user = ctx.author
      s = str(user.id)
      sid = str(ctx.guild.id)
      db = KeyValueStore(f'./data/level/{sid}.db')
      level = db[f"{s}, {sid}"]
      db.close()
      level = level.split(", ")
      exp = 100 * int(level[1]) + int(level[0])
      nexp = (int(level[1]) + 1) * 100
      if not int(level[1]) == 0:
        pexp = (int(level[1]) - 1) * 100
      else:
        pexp = 0
      top = []
      db = KeyValueStore(f'./data/level/{sid}.db')
      keys = db.keys()
      db.close()
      for i in keys: 
        if str(i).endswith(str(sid)):
          db = KeyValueStore(f'./data/level/{sid}.db')
          level1 = db[i]
          db.close()
          level1 = level1.split(", ")
          exp1 = 100 * int(level1[1]) + int(level1[0])
          s1 = i.replace(f", {sid}", "")
          top.append({"exp" : int(exp1), "id" : int(s1)})
      top.sort(key=lambda x: x['exp'], reverse=True)
      top = top.index({"exp" : int(exp), "id" : int(s)})
      req = PreparedRequest()
      req.prepare_url(f"https://vacefron.nl/api/rankcard?username={user.name}&avatar={user.avatar.url}&currentxp={int(exp)}&nextlevelxp={int(nexp)}&previouslevelxp={pexp}&level={int(level[1])}&rank=Top%20{int(top) + 1}&xpcolor=5f76d9&circleavatar=True", params=None)
      response = requests.get(req.url)
      with open(f"{user.id}_rank.png", 'wb') as f:
        f.write(response.content)
      file = discord.File(f'{user.id}_rank.png')
      os.remove(f"{user.id}_rank.png")
      await ctx.reply(file=file)

@bot.command()
@commands.guild_only()
async def achat(ctx, arg: discord.TextChannel=None):
  if ctx.author.guild_permissions.administrator:
    if arg == None:
      arg = ctx.channel
    with open("./data/chat.db", "rb") as fp:
      hi = pickle.load(fp)
    if not arg.id in hi:
      hi.append(arg.id)
      with open("./data/chat.db", "wb") as fp:
        pickle.dump(hi, fp)
      embed=discord.Embed(title=f"Đã add kênh vào list")
      await ctx.reply(embed=embed)
    else:
      embed=discord.Embed(title=f"Kênh đã có sắn trong list")
      await ctx.reply(embed=embed)
  else:
    await ctx.reply(f'**Bạn không có quyền dùng command này**')

@bot.command()
@commands.guild_only()
async def rchat(ctx, arg: discord.TextChannel=None):
  if ctx.author.guild_permissions.administrator:
    if arg == None:
      arg = ctx.channel
    with open("./data/chat.db", "rb") as fp:
      hi = pickle.load(fp)
    if arg.id in hi:
      hi.remove(arg.id)
      with open("./data/chat.db", "wb") as fp:
        pickle.dump(hi, fp)
      embed=discord.Embed(title=f"Đã bỏ kênh Ra Khỏi list")
      await ctx.reply(embed=embed)
    else:
      embed=discord.Embed(title=f"Kênh không có trong list")
      await ctx.reply(embed=embed)
  else:
    await ctx.reply(f'**Bạn không có quyền dùng command này**')


@bot.command()
@commands.guild_only()
async def top(ctx):
  top = []
  sid = str(ctx.guild.id)
  db = KeyValueStore(f'./data/level/{sid}.db')
  keys = db.keys()
  db.close()
  for i in keys: 
    if str(i).endswith(str(sid)):
      db = KeyValueStore(f'./data/level/{sid}.db')
      level = db[i]
      db.close()
      level = level.split(", ")
      exp = 100 * int(level[1]) + int(level[0])
      s = i.replace(f", {sid}", "")
      top.append({"exp" : int(exp), "id" : int(s)})
  top.sort(key=lambda x: x['exp'], reverse=True)
  x = top[:10]
  for count, idsa in enumerate(x, 1):
    user = f"{toplit}**{count} | <@!{idsa['id']}> : `{idsa['exp']}`**\n"
    topchat(user)
  embed=discord.Embed(title=f"Top Chat {ctx.guild.name}", description=f"{toplit}")
  await ctx.reply(embed=embed)
  topchat()
    
@bot.command()
@commands.guild_only()
async def close(ctx):
  if not discord.utils.get(ctx.author.roles, id=916152577752727572) is None:
    with open("./data/support.db", "rb") as fp:
      listu = pickle.load(fp)
    if str(ctx.channel.id) in str(listu):
      for listu in listu:
        if listu["text"] == str(ctx.channel.id):
          user = listu["user"]
          member = await bot.fetch_user(user)
          embed=discord.Embed(title="Support Close 5")
          load  = await ctx.send(embed=embed)
          await asyncio.sleep(1)
          embed=discord.Embed(title="Support Close 4")
          await load.edit(embed=embed)
          await asyncio.sleep(1)
          embed=discord.Embed(title="Support Close 3")
          await load.edit(embed=embed)
          await asyncio.sleep(1)
          embed=discord.Embed(title="Support Close 2")
          await load.edit(embed=embed)
          await asyncio.sleep(1)
          embed=discord.Embed(title="Support Close 1")
          await load.edit(embed=embed)
          await asyncio.sleep(1)
          embed=discord.Embed(title="Support Close 0")
          await ctx.channel.delete()
          embed=discord.Embed(title="Support Close", description="Gửi bất kì cái gì để mở lại support")
          await member.send(embed=embed)
          with open("./data/support.db", "rb") as fp:
            listus = pickle.load(fp)
          listus.remove(listu)
          with open("./data/support.db", "wb") as fp:
            pickle.dump(listus, fp)

@bot.command()
@commands.guild_only()
async def support(ctx):
  await ctx.message.add_reaction("<:Minecraft_Accept:903118896368869447>")
  embed=discord.Embed(title="Nhắn một tin nhắn vào đây để được support")
  await ctx.author.send(embed=embed)

@bot.command()
async def capcha(ctx,*, text=None):
  response = requests.get("https://google.duongtuan30306vn.repl.co/capcha", params={"code" : text})
  with open(f"{text}_rank.png", 'wb') as f:
    f.write(response.content)
  file = discord.File(f'{text}_rank.png')
  os.remove(f"{text}_rank.png")
  await ctx.reply(file=file)

@bot.command()
async def server(ctx):
  name = str(ctx.guild.name)
  description = str(ctx.guild.description)

  owner = str(ctx.guild.owner.mention)
  id = str(ctx.guild.id)
  memberCount = str(ctx.guild.member_count)

  botCount = len([i for i in ctx.guild.members if i.bot])
  userCount = len([i for i in ctx.guild.members if not i.bot])
  icon = ctx.guild.icon
   
  embed = discord.Embed(
      title=name,
      description=f"Description : {description}"
    )
  embed.add_field(name="Owner", value=owner, inline=True)
  embed.add_field(name="Server ID", value=id, inline=True)
  embed.add_field(name="Member Count", value=memberCount, inline=True)
  embed.add_field(name="User Count", value=userCount, inline=True)
  embed.add_field(name="Bot Count", value=botCount, inline=True)
  if not icon == None:
    embed.set_thumbnail(url=icon.url)
  await ctx.send(embed=embed)

@bot.command()
async def tts(ctx,*, texts=None):
  if texts == None:
    embed=discord.Embed(title="TTS command", description=f"**HD**\n`{get_prefix(ctx)}tts <text>`\n**VD**\n`{get_prefix(ctx)}tts test`")
    await ctx.send(embed=embed)
  
  if not texts == None:
    channel = ctx.author.voice
    if not channel == None:
      voice = get(bot.voice_clients, guild=ctx.guild)
      if voice == None:
        text = urllib.parse.quote_plus(texts)
        source = FFmpegPCMAudio(f"https://translate.google.com/translate_tts?ie=UTF-8&q={text}&tl=vi&total=1&idx=0&textlen=15&tk=350535.255567&client=webapp&prev=input", executable="ffmpeg")
        await channel.channel.connect()
        ctx.voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(after_play(ctx), bot.loop))
        await ctx.send(f"Đang nói {texts}")
    else:
      await ctx.send("Vào voice để dùng tts bro <:Minecraft_Deny:903118973946707969>")

async def after_play(ctx):
  await ctx.voice_client.disconnect()

@bot.event
async def on_message(message):
  await bot.process_commands(message)
  try:
    if not message.content.lower().startswith(f'{get_prefix(message)}afk'):
        s = str(message.author.id)
        sid = str(message.guild.id)
        db = KeyValueStore('./data/svafk.db')
        b = db[sid]
        db.close()
        if s in b:
          db = KeyValueStore('./data/svafk.db')
          af = KeyValueStore('./data/afk.db')
          b = db[sid]
          s = b.replace(f" '{s}',", "")
          if s == "":
            del db[sid]
          if not s == "":
            db[sid] = s
          nick = message.author.nick
          try:
            r = str(nick).replace(f"[AFK] ", "")
            if str(r) == str(message.author.name):
              await message.author.edit(nick=None)
            if not str(r) == str(message.author.name):
              await message.author.edit(nick=r)
          except:
            pass
          s = str(message.author.id)
          del af[f"{s}, {sid}"]
          db.close()
          af.close()
          db = KeyValueStore('./data/afkt.db')
          del db[f"{s}, {sid}"]
          db.close()
          await message.channel.send(f'**Chào mừng quay trở lại {message.author.mention} . Tôi đã bỏ AFK cho bạn rồi đó.**', delete_after=10)
  except:
    pass
      
  if str(message.channel.type) == "private":
    if not str(message.author.id) == "903120513243693116":
      with open("./data/support.db", "rb") as fp:
        listu = pickle.load(fp)

      if str(message.author.id) in str(listu):
        for listu in listu:
          if listu["user"] == str(message.author.id):
            try:
              send = listu["text"]
              embed=discord.Embed(title=f"{message.author} ({message.author.id})", description=message.content)
              if message.attachments:
                if 'image' in message.attachments[0].content_type:
                  embed.set_image(url=message.attachments[0].url)
              await bot.get_channel(int(send)).send("<@&916152577752727572>", embed=embed)
            except:
              with open("./data/support.db", "rb") as fp:
                listus = pickle.load(fp)
              listus.remove(listu)
              with open("./data/support.db", "wb") as fp:
                pickle.dump(listus, fp)

      with open("./data/support.db", "rb") as fp:
        listu = pickle.load(fp)
      if not str(message.author.id) in str(listu):
        guild = bot.get_guild(890741284745138226)
        category = get(guild.categories, id=914151962927333376)
        send = await guild.create_text_channel(f"{message.author.name}", category=category, reason="Support")
        await send.set_permissions(guild.default_role, view_channel=False)
        embed=discord.Embed(title=f"{message.author} ({message.author.id})", description=message.content)
        if message.attachments:
              if 'image' in message.attachments[0].content_type:
                embed.set_image(url=message.attachments[0].url)
        await send.send("<@&916152577752727572>", embed=embed)
        embed=discord.Embed(title="Team Support", description="Team support trả lời sớm nhất về support của bạn vui lòng đợi !")
        await message.author.send(embed=embed)
        with open("./data/support.db", "rb") as fp:
          listu = pickle.load(fp)
        listu.append({"user" : str(message.author.id), "text" : str(send.id)})
        with open("./data/support.db", "wb") as fp:
          pickle.dump(listu, fp)
  
  with open("./data/support.db", "rb") as fp:
    listu = pickle.load(fp)      
  if str(message.channel.id) in str(listu):
    if not message.content.lower().startswith(f'{get_prefix(message)}close'):
      if not discord.utils.get(message.author.roles, id=916152577752727572) is None:
        for listu in listu:
          if listu["text"] == str(message.channel.id):
            user = listu["user"]
            member = await bot.fetch_user(user)
            await asyncio.sleep(0.2)
            await message.delete()
            embed=discord.Embed(title=f"{message.author} (Support)", description=message.content)
            if message.attachments:
              if 'image' in message.attachments[0].content_type:
                embed.set_image(url=message.attachments[0].url)
            await member.send(embed=embed)
            embed=discord.Embed(title=f"{message.author} (Support)", description=message.content)
            if message.attachments:
              if 'image' in message.attachments[0].content_type:
                embed.set_image(url=message.attachments[0].url)
            await message.channel.send(embed=embed)
          

  if (message.author.bot):
    return 
    
  if message.mentions:
    try:
      sid = str(message.guild.id)
      for i in message.mentions:
        i = i.id
        db = KeyValueStore('./data/svafk.db')
        z = db[sid]
        db.close()
        member = await bot.fetch_user(i)
        if str(i) in z:
          db = KeyValueStore('./data/afk.db')
          s = db[f"{i}, {sid}"]
          db.close()
          db = KeyValueStore('./data/afkt.db')
          t = db[f"{i}, {sid}"]
          db.close()
          await message.reply(f'**{member}** đang AFK : {s} **- <t:{t}:R>**')
    except:
      pass

  with open("./data/chat.db", "rb") as fp:
    id = pickle.load(fp)
  if message.channel.id in id:
    await asyncio.sleep(0.3)
    await message.delete()
    if not message.content.lower().startswith(f'{get_prefix(message)}'):
      url = message.author.avatar.url
      user = message.author
      content = message.content
      svname = message.guild.name
      try:
        urlg = message.guild.icon.url
      except:
        pass
      for x in id:
        try:
          embed=discord.Embed(title=user, description=content)
          embed.set_thumbnail(url=url)
          try:
            embed.set_footer(text=svname, icon_url=urlg)
          except:
            embed.set_footer(text=svname)
          if message.attachments:
            if 'image' in message.attachments[0].content_type:
              embed.set_image(url=message.attachments[0].url)
          await bot.get_channel(x).send(embed=embed)
        except:
          with open("./data/chat.db", "rb") as fp:
            hi = pickle.load(fp)
          hi.remove(x)
          with open("./data/chat.db", "wb") as fp:
            pickle.dump(hi, fp)

  if message.content == f"<@!{bot.user.id}>":
    sid = str(message.guild.id)
    await message.reply(f'**Prefix của server là : `{get_prefix(message)}`**\nNhập `{get_prefix(message)}help` or `@Fantasy Land#5272 help` để xem Commands')

  if message.content == f"<@{bot.user.id}>":
    sid = str(message.guild.id)
    await message.reply(f'**Prefix của server là : `{get_prefix(message)}`**\nNhập `{get_prefix(message)}help` or `@Fantasy Land#5272 help` để xem Commands')
    
  if 1 == 1:
    try:
      try:
        if not message.author.id in users_on_cooldown:
          s = str(message.author.id)
          sid = str(message.guild.id)
          db = KeyValueStore(f'./data/level/{sid}.db')
          level = db[f"{s}, {sid}"]
          level = level.split(", ")
          if int(level[0]) < int(100):
            exp = int(level[0]) + 2
            lv = level[1]
          if int(level[0]) >= int(100):
            lv = int(level[1]) + 1
            exp = 0
            await message.reply(f"**Bạn đã lên level : {lv}**", mention_author=False)
          level = str(f"{exp}, {lv}")
          db[f"{s}, {sid}"] = level
          db.close()
          users_on_cooldown.append(message.author.id)
          await asyncio.sleep(10)
          users_on_cooldown.remove(message.author.id)
      except:
        try:
          s = str(message.author.id)
          sid = str(message.guild.id)
          db = KeyValueStore(f'./data/level/{sid}.db')
          db[f"{s}, {sid}"] = str("0, 0")
          db.close()
        except:
          s = str(message.author.id)
          sid = str(message.guild.id)
          open(f"./data/level/{sid}.db","w")
          db = KeyValueStore(f'./data/level/{sid}.db')
          db[f"{s}, {sid}"] = str("0, 0")
          db.close()
    except:
      pass


@bot.event
async def on_member_update(before, after):
    if len(before.roles) < len(after.roles):
      if after.guild.id == before.guild.id == 886959744714149988:
        if not [i.id for i in before.roles].count(907238166451343421):
          if [i.id for i in after.roles].count(907238166451343421):
            await bot.get_channel(912710131379236946).send(f"Chào mừng {after.mention} đến với server {after.guild.name} !!!\nCác <@&907236948580642886> đâu, ra tiếp khách !!!\n+ Ping role ở <#899644410386608168> \n+ Đọc luật ở <#904989387161489428> \n+ Chat chung ở <#912710131379236946>")
        
        if not [i.id for i in before.roles].count(907889623009730571):
          if [i.id for i in after.roles].count(907889623009730571):
            role = get(after.guild.roles, id=907889623009730571)
            try:
              await after.remove_roles(role)
            except:
              pass

@bot.event
async def on_voice_state_update(member, prev, cur):
    if not member == bot.user:
      if not prev.channel == None:
        test = bot.get_channel(prev.channel.id).members
        if int(len([i for i in test if not i.bot])) == 0:
          if bot.user in test:
            voice = get(bot.voice_clients, channel=prev.channel)
            if not voice == None:
              try:
                os.remove(f"./data/queue/{member.guild.id}.db")
              except:
                pass
              await voice.disconnect()
    if member == bot.user:
      if not prev.channel == None:
        if not cur.channel == None:
          if not prev.channel == cur.channel:
            test = bot.get_channel(cur.channel.id).members
            if int(len([i for i in test if not i.bot])) == 0:
              if bot.user in test:
                voice = get(bot.voice_clients, channel=cur.channel)
                if not voice == None:
                  try:
                    os.remove(f"./data/queue/{member.guild.id}.db")
                  except:
                    pass
                  await voice.disconnect()
            if not int(len([i for i in test if not i.bot])) == 0:
              try:
                tes = member.guild.get_member(bot.user.id)
                await tes.edit(suppress = False)
              except:
                pass

##########################################################

@tasks.loop(seconds=1)
async def myLoop():
    x = datetime.utcnow()+timedelta(hours=7)
    if x.strftime("%H:%M:%S") == "00:00:00":
      db = KeyValueStore('./data/bank.db')
      keys = db.keys()
      db.close()
      for i in keys:
        db = KeyValueStore('./data/bank.db')
        c = db[i]
        t = int(c) * 0.05
        t = int(t) + int(c)
        db[i] = t
        db.close()

    if x.strftime("%H:%M:%S") == "12:00:00":
      db = KeyValueStore('./data/bank.db')
      keys = db.keys()
      db.close()
      for i in keys:
        db = KeyValueStore('./data/bank.db')
        c = db[i]
        t = int(c) * 0.05
        t = int(t) + int(c)
        db[i] = t
        db.close()

#########################################################

@bot.event
async def on_ready():
  global startdate
  startdate = datetime.now()
  bot.togetherControl = await DiscordTogether(os.getenv('TOKEN'))
  bot.loop.create_task(status_task())
  for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
      try:
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(f"Load done cogs {filename}")
      except Exception:
        traceback.print_exc()
        print(Fore.RED + f"Error cogs {filename}" + Fore.RESET)
  print("Bot start")

@bot.event
async def status_task():
   while True: 
      await bot.change_presence(activity=discord.Game(name="Ping me for help"))
      await asyncio.sleep(10)
      await bot.change_presence(activity=discord.Game(name="DM me for Support"))
      await asyncio.sleep(10)



myLoop.start()
keep_alive()
bot.run(os.getenv('TOKEN'), reconnect=True)