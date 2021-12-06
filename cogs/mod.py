import discord, time
import asyncio
import requests
import traceback
from discord.ext import commands
from keep_alive import get_prefix
from discord.utils import get

class mod(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  @commands.guild_only()
  async def ban(self, ctx, args=None, *, reason = "Không có lí do"):
    if args == None:
      embed=discord.Embed(title="Ban command", description=f"**HD**\n`{get_prefix(ctx)}ban <@user/userid> <lí do>`\n**VD**\n`{get_prefix(ctx)}ban @user test`\n**OR**\n`{get_prefix(ctx)}ban 123456789 test`")
      embed.add_field(name="Yêu cầu", value=f"User dùng command có quyền : \nBan users", inline=False)
      await ctx.send(embed=embed)

    if not args == None:
      if ctx.author.guild_permissions.ban_members:
        x = args.replace("<@", "")
        s = x.replace(">", "")
        e = s.replace("!", "")
        try:
          member = await self.bot.fetch_user(e)
          if not member == ctx.author:
            try:
              await ctx.guild.ban(member, reason = reason)
              embed=discord.Embed(title=f"Đã ban {member} ", description=f"**Lí do : **{reason}")
              await ctx.send(embed=embed)
            except:
              embed=discord.Embed(title=f"Không thể ban {member}")
              await ctx.send(embed=embed)
          else:
            await ctx.reply(f'**Bạn không Thể ban chính mình**')
        except:
          embed=discord.Embed(title=f"Không thấy user bạn cung cấp")
          await ctx.send(embed=embed)
      else:
        await ctx.reply(f'**Bạn không có quyền dùng command này\nBạn cần quyền : Ban members**')

  @commands.command()
  @commands.guild_only()
  async def unban(self, ctx, args=None, *, reason = "Không có lí do"):
    if args == None:
      embed=discord.Embed(title="Unban command", description=f"**HD**\n`{get_prefix(ctx)}unban <userid> <lí do>`\n**VD**\n`{get_prefix(ctx)}unban 123456789 test`")
      embed.add_field(name="Yêu cầu", value=f"User dùng command có quyền : \nBan users", inline=False)
      await ctx.send(embed=embed)

    if not args == None:
      if ctx.author.guild_permissions.ban_members:
        x = args.replace("<@", "")
        s = x.replace(">", "")
        e = s.replace("!", "")
        try:
          member = await self.bot.fetch_user(e)
          try:
            await ctx.guild.unban(member, reason = reason)
            embed=discord.Embed(title=f"Đã unban {member} ", description=f"**Lí do : **{reason}")
            await ctx.send(embed=embed)
          except:
            embed=discord.Embed(title=f"Không có {member} Trong list ban")
            await ctx.send(embed=embed)
        except:
          embed=discord.Embed(title=f"Không thấy user bạn cung cấp")
          await ctx.send(embed=embed)
      else:
        await ctx.reply(f'**Bạn không có quyền dùng command này\nBạn cần quyền : Ban members**')    

  @commands.command()
  @commands.guild_only()
  async def kick(self, ctx, args=None, *, reason = "Không có lí do"):
    if args == None:
      embed=discord.Embed(title="Kick command", description=f"**HD**\n`{get_prefix(ctx)}kick <@user/userid> <lí do>`\n**VD**\n`{get_prefix(ctx)}kick 123456789 test`\n**OR**\n`{get_prefix(ctx)}kick @user test`")
      embed.add_field(name="Yêu cầu", value=f"User dùng command có quyền : \nKick users", inline=False)
      await ctx.send(embed=embed)

    if not args == None:
      if ctx.author.guild_permissions.kick_members:
        x = args.replace("<@", "")
        s = x.replace(">", "")
        e = s.replace("!", "")
        try:
          member = await self.bot.fetch_user(e)
          try:
            if ctx.guild.get_member(member.id) is None:
              embed=discord.Embed(title=f"User {member} Không có trong server")
              await ctx.send(embed=embed)
            if ctx.guild.get_member(member.id) is not None:
              await ctx.guild.kick(member, reason = reason)
              embed=discord.Embed(title=f"Đã kick {member} ", description=f"**Lí do : **{reason}")
              await ctx.send(embed=embed)
          except:
            if ctx.guild.get_member(member.id) is not None:
              embed=discord.Embed(title=f"Không thể kick {member}")
              await ctx.send(embed=embed)
        except:
          embed=discord.Embed(title=f"Không thấy user bạn cung cấp")
          await ctx.send(embed=embed)
      else:
        await ctx.reply(f'**Bạn không có quyền dùng command này\nBạn cần quyền : Kick members**')
  
  @commands.command()
  @commands.guild_only()
  async def clear(self, ctx, amount:int=100):
    if ctx.author.guild_permissions.manage_messages:
      if amount <= 1000:
        try:
          await ctx.channel.purge(limit=amount+1)
          await ctx.send(f'**Đã clear {amount} tin nhắn**', delete_after=2)
        except:
          await ctx.send(f"**Không thể clear kênh <#{ctx.channel.id}>**", delete_after=4)
      else:
        await asyncio.sleep(0.2)
        await ctx.message.delete()
        await ctx.send(f'**Vui lòng chỉ clear dưới 1,000**', delete_after=5)
    else:
      await ctx.reply(f'**Bạn không có quyền dùng command này\nBạn cần quyền : Manage messages**')

  @commands.command()
  @commands.guild_only()
  async def warn(self, ctx, args=None, *, reason = "Không có lí do"):
    if args == None:
      embed=discord.Embed(title="Warn command", description=f"**HD**\n`{get_prefix(ctx)}warn <@user/userid> <lí do>`\n**VD**\n`{get_prefix(ctx)}warn 123456789 test`\n**OR**\n`{get_prefix(ctx)}warn @user test`")
      embed.add_field(name="Yêu cầu", value=f"User dùng command có quyền : \nManage Messages", inline=False)
      await ctx.send(embed=embed)

    if not args == None:
      if ctx.author.guild_permissions.manage_messages:
        x = args.replace("<@", "")
        s = x.replace(">", "")
        e = s.replace("!", "")
        try:
          member = await self.bot.fetch_user(e)
          if ctx.guild.get_member(member.id) is None:
            embed=discord.Embed(title=f"User {member} Không có trong server")
            await ctx.send(embed=embed)
          if ctx.guild.get_member(member.id) is not None:
            embed=discord.Embed(title=f"{member} đã bị warn", description=f"**Lí do : **{reason}")
            await ctx.send(embed=embed)
            embed=discord.Embed(title=f"Bạn đã bị Warn!", description=f"**Lí do : **{reason}")
            svname = ctx.guild.name
            try:
              urlg = ctx.guild.icon.url
            except:
              pass
            try:
              embed.set_footer(text=svname, icon_url=urlg)
            except:
              embed.set_footer(text=svname)
            try:
              await member.send(embed=embed)
            except:
              pass
        except:
          embed=discord.Embed(title=f"Không thấy user bạn cung cấp")
          await ctx.send(embed=embed)
      else:
        await ctx.reply(f'**Bạn không có quyền dùng command này\nBạn cần quyền : Manage messages**')

  @commands.command()
  @commands.guild_only()
  async def mute(self, ctx, args=None, *, reason = "Không có lí do"):
    if args == None:
      embed=discord.Embed(title="Mute command", description=f"**HD**\n`{get_prefix(ctx)}mute <@user/userid> <lí do>`\n**VD**\n`{get_prefix(ctx)}mute 123456789 test`\n**OR**\n`{get_prefix(ctx)}mute @user test`")
      embed.add_field(name="Yêu cầu", value=f"User dùng command có quyền : \nManage Roles", inline=False)
      await ctx.send(embed=embed)


    if not args == None:
      if ctx.author.guild_permissions.manage_roles:
        role = get(ctx.guild.roles, name="Muted")
        x = args.replace("<@", "")
        s = x.replace(">", "")
        e = s.replace("!", "")
        try:
          member = await self.bot.fetch_user(e)
          if not role is None:
            try:
              if ctx.guild.get_member(member.id) is None:
                  embed=discord.Embed(title=f"User {member} Không có trong server")
                  await ctx.send(embed=embed)
              if ctx.guild.get_member(member.id) is not None:
                await ctx.guild.get_member(member.id).add_roles(role)
                if not discord.utils.get(ctx.guild.get_member(member.id).roles, name="Muted") is None:
                  embed=discord.Embed(title=f"Đã mute {member} ", description=f"**Lí do : **{reason}")
                  await ctx.send(embed=embed)
                if discord.utils.get(ctx.guild.get_member(member.id).roles, name="Muted") is None:
                  await ctx.send(f"Không thể mute {member}")
            except:
                await ctx.send(f"Không thể mute {member}")
            for i in ctx.guild.text_channels:
              try:
                ov = i.overwrites_for(role)
                if not ov.send_messages == ov.create_private_threads == ov.create_public_threads == ov.send_messages_in_threads == ov.add_reactions == False:
                  await i.set_permissions(role, 
                  send_messages=False, 
                  create_private_threads=False, 
                  create_public_threads=False, 
                  send_messages_in_threads=False,
                  add_reactions=False)
              except:
                pass
          if role is None:
            try:
              perms = discord.Permissions(view_channel=True)
              role = await ctx.guild.create_role(name="Muted", permissions=perms)
              try:
                if ctx.guild.get_member(member.id) is None:
                  embed=discord.Embed(title=f"User {member} Không có trong server")
                  await ctx.send(embed=embed)
                if ctx.guild.get_member(member.id) is not None:
                  await ctx.guild.get_member(member.id).add_roles(role)
                  if not discord.utils.get(ctx.guild.get_member(member.id).roles, name="Muted") is None:
                    embed=discord.Embed(title=f"Đã mute {member} ", description=f"**Lí do : **{reason}")
                    await ctx.send(embed=embed)
                  if discord.utils.get(ctx.guild.get_member(member.id).roles, name="Muted") is None:
                    await ctx.send(f"Không thể mute {member}")
              except:
                await ctx.send(f"Không thể mute {member}")
              for i in ctx.guild.text_channels:
                try:
                  await i.set_permissions(role, 
                  send_messages=False, 
                  create_private_threads=False, 
                  create_public_threads=False, 
                  send_messages_in_threads=False,
                  add_reactions=False)
                except:
                  pass
            except:
              await ctx.send("**Lỗi không tạo và set up được role mute**")
        except:
          embed=discord.Embed(title=f"Không thấy user bạn cung cấp")
          await ctx.send(embed=embed)
      else:
        await ctx.reply(f'**Bạn không có quyền dùng command này \nBạn cần quyền : Manage roles**')

  @commands.command()
  @commands.guild_only()
  async def unmute(self, ctx, args=None, *, reason = "Không có lí do"):
    if args == None:
      embed=discord.Embed(title="Unute command", description=f"**HD**\n`{get_prefix(ctx)}unmute <@user/userid> <lí do>`\n**VD**\n`{get_prefix(ctx)}unmute 123456789 test`\n**OR**\n`{get_prefix(ctx)}unmute @user test`")
      embed.add_field(name="Yêu cầu", value=f"User dùng command có quyền : \nManage Roles", inline=False)
      await ctx.send(embed=embed)


    if not args == None:
      if ctx.author.guild_permissions.manage_roles:
        role = get(ctx.guild.roles, name="Muted")
        x = args.replace("<@", "")
        s = x.replace(">", "")
        e = s.replace("!", "")
        try:
          member = await self.bot.fetch_user(e)
          try:
            if discord.utils.get(ctx.guild.get_member(member.id).roles, name="Muted") is None:
              await ctx.send(f"**User {member} đang không bị mute**")
            if not discord.utils.get(ctx.guild.get_member(member.id).roles, name="Muted") is None:
              await ctx.guild.get_member(member.id).remove_roles(role)
              embed=discord.Embed(title=f"Đã unmute {member} ", description=f"**Lí do : **{reason}")
              await ctx.send(embed=embed)
          except:
            embed=discord.Embed(title=f"bot không có quyên để unmute")
            await ctx.send(embed=embed)
        except:
          embed=discord.Embed(title=f"Không thấy user bạn cung cấp")
          await ctx.send(embed=embed)
      else:
        await ctx.reply(f'**Bạn không có quyền dùng command này \nBạn cần quyền : Manage roles**')

  @commands.command()
  async def lock(self, ctx):
    if ctx.author.guild_permissions.manage_channels:
      overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
      overwrite.send_messages = False
      await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
      await ctx.send('**Đã khóa kênh.**')
    else:
      await ctx.reply(f'**Bạn không có quyền dùng command này\nBạn cần quyền : Manage Channels**')
  
  @commands.command()
  async def unlock(self, ctx):
    if ctx.author.guild_permissions.manage_channels:
      overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
      overwrite.send_messages = None
      await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
      await ctx.send('**Đã bỏ khóa kênh.**')
    else:
      await ctx.reply(f'**Bạn không có quyền dùng command này\nBạn cần quyền : Manage Channels**')

def setup(bot):
    bot.add_cog(mod(bot))
