import discord, time
import asyncio
from discord.ext import commands

class nuck(commands.Cog):
    def __init__(self, bot):
      self.bot = bot

    @commands.command()
    async def nuke(self, ctx):
      if ctx.author.guild_permissions.administrator:
        try:
          embed = discord.Embed(
            title=f"Kênh **#{ctx.channel.name}** sẽ nuke său 5s",
            description=f"Nuked bởi: {ctx.author}"
          )
          load = await ctx.send(embed=embed)
          await asyncio.sleep(1)
          embed = discord.Embed(
            title=f"Kênh **#{ctx.channel.name}** sẽ nuke său 4s",
            description=f"Nuked bởi: {ctx.author}"
          )
          await load.edit(embed=embed)
          await asyncio.sleep(1)
          embed = discord.Embed(
            title=f"Kênh **#{ctx.channel.name}** sẽ nuke său 3s",
            description=f"Nuked bởi: {ctx.author}"
          )
          await load.edit(embed=embed)
          await asyncio.sleep(1)
          embed = discord.Embed(
            title=f"Kênh **#{ctx.channel.name}** sẽ nuke său 2s",
            description=f"Nuked bởi: {ctx.author}"
          )
          await load.edit(embed=embed)
          await asyncio.sleep(1)
          embed = discord.Embed(
            title=f"Kênh **#{ctx.channel.name}** sẽ nuke său 1s",
            description=f"Nuked bởi: {ctx.author}"
          )
          await load.edit(embed=embed)
          await asyncio.sleep(1)
          embed = discord.Embed(
            title=f"Kênh **#{ctx.channel.name}** sẽ nuke său 0s",
            description=f"Nuked bởi: {ctx.author}"
          )
          await load.edit(embed=embed)
          await ctx.channel.delete(reason=f"Nuke by {ctx.author}")
          p = ctx.channel.position
          B = ctx.channel.category
          done = await ctx.channel.clone(reason=f"Nuke by {ctx.author}")
          await done.edit(category=B, position=p)
          embed = discord.Embed(
            title=f"Kênh này đã nuked/tạo lại kênh!",
            description=f"Nuked bởi: {ctx.author}"
          )
          await done.send(embed=embed) 
        except:
          embed = discord.Embed(
            title=f"Kênh **#{ctx.channel.name}** không Nuke được lỗi",
            description=f"Nuked bởi: {ctx.author}"
          )
          await load.edit(embed=embed)
      else:
        await ctx.reply(f'**Bạn không có quyền dùng command này**')
    
def setup(bot):
    bot.add_cog(nuck(bot))
