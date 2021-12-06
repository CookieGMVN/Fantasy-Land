import discord, time
import asyncio
import requests
from discord.ext import commands
from keep_alive import get_prefix

class sanime(commands.Cog):
    def __init__(self, bot):
      self.bot = bot

    @commands.command()
    async def sanime(self, ctx,*, args=None):
      if args == None:
        embed=discord.Embed(title="Sanime command", description=f"**HD**\n`{get_prefix(ctx)}sanime <anime name>`\n**VD**\n`{get_prefix(ctx)}sanime nekopara`")
        await ctx.send(embed=embed)
      
      if not args == None:
        r = requests.get(f"https://kitsu.io/api/edge/anime?filter[text]={args}")
        r = r.json()
        r = r["data"][0]
        name = r["attributes"]["slug"]
        info = r["attributes"]["synopsis"]
        rati = r["attributes"]["averageRating"]
        img = r["attributes"]["posterImage"]["large"]
        TYPE = r["type"]
        embed=discord.Embed(title=name, description=info.replace("\n\n", "\n"))
        embed.set_image(url=img)
        embed.add_field(name="Type", value=TYPE, inline=True)
        embed.add_field(name="Rating", value=f"{rati}%", inline=True)
        await ctx.send(embed=embed)
    
def setup(bot):
    bot.add_cog(sanime(bot))
