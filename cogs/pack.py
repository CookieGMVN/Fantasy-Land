import discord, time
import asyncio
import requests
from discord.ext import commands
from keep_alive import get_prefix

class pack(commands.Cog):
    def __init__(self, bot):
      self.bot = bot

    @commands.command()
    async def pip(self, ctx,*, args=None):
      if args == None:
        embed=discord.Embed(title="pip command", description=f"**HD**\n`{get_prefix(ctx)}pip <pack name>`\n**VD**\n`{get_prefix(ctx)}pip discord.py`")
        await ctx.send(embed=embed)
      
      if not args == None:
        args = args.replace(" ", "-")
        r = requests.get(f"https://pypi.org/pypi/{args}/json")
        if r.status_code == 200:
          r = r.json()["info"]
          author = r["author"]
          name = r["name"]
          rati = r["project_url"]
          img = r["version"]
          embed=discord.Embed(title=name, description=f"**Author : **{author}\n**Version :** {img}\n**Project url :** {rati}")
          embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/766274397257334814.png")
          await ctx.send(embed=embed)
        else:
          embed=discord.Embed(title=f"Không tìm thấy pack")
          await ctx.send(embed=embed)          

def setup(bot):
    bot.add_cog(pack(bot))
