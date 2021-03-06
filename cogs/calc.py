import discord
from discord.ext import commands
from simpcalc import simpcalc

class InteractiveView(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.expr = ""
            self.calc = simpcalc.Calculate()  # if you are using the above function, no need to declare this!

        @discord.ui.button(style=discord.ButtonStyle.blurple, label="1", row=0)
        async def one(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.expr += "1"
            await interaction.message.edit(content=f"```\n{self.expr}\n```")

        @discord.ui.button(style=discord.ButtonStyle.blurple, label="2", row=0)
        async def two(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.expr += "2"
            await interaction.message.edit(content=f"```\n{self.expr}\n```")

        @discord.ui.button(style=discord.ButtonStyle.blurple, label="3", row=0)
        async def three(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.expr += "3"
            await interaction.message.edit(content=f"```\n{self.expr}\n```")

        @discord.ui.button(style=discord.ButtonStyle.green, label="+", row=0)
        async def plus(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.expr += "+"
            await interaction.message.edit(content=f"```\n{self.expr}\n```")

        @discord.ui.button(style=discord.ButtonStyle.blurple, label="4", row=1)
        async def last(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.expr += "4"
            await interaction.message.edit(content=f"```\n{self.expr}\n```")

        @discord.ui.button(style=discord.ButtonStyle.blurple, label="5", row=1)
        async def five(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.expr += "5"
            await interaction.message.edit(content=f"```\n{self.expr}\n```")

        @discord.ui.button(style=discord.ButtonStyle.blurple, label="6", row=1)
        async def six(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.expr += "6"
            await interaction.message.edit(content=f"```\n{self.expr}\n```")

        @discord.ui.button(style=discord.ButtonStyle.green, label=":", row=1)
        async def divide(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.expr += "/"
            await interaction.message.edit(content=f"```\n{self.expr}\n```")

        @discord.ui.button(style=discord.ButtonStyle.blurple, label="7", row=2)
        async def seven(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.expr += "7"
            await interaction.message.edit(content=f"```\n{self.expr}\n```")

        @discord.ui.button(style=discord.ButtonStyle.blurple, label="8", row=2)
        async def eight(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.expr += "8"
            await interaction.message.edit(content=f"```\n{self.expr}\n```")

        @discord.ui.button(style=discord.ButtonStyle.blurple, label="9", row=2)
        async def nine(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.expr += "9"
            await interaction.message.edit(content=f"```\n{self.expr}\n```")

        @discord.ui.button(style=discord.ButtonStyle.green, label="x", row=2)
        async def multiply(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.expr += "*"
            await interaction.message.edit(content=f"```\n{self.expr}\n```")

        @discord.ui.button(style=discord.ButtonStyle.blurple, label=".", row=3)
        async def dot(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.expr += "."
            await interaction.message.edit(content=f"```\n{self.expr}\n```")

        @discord.ui.button(style=discord.ButtonStyle.blurple, label="0", row=3)
        async def zero(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.expr += "0"
            await interaction.message.edit(content=f"```\n{self.expr}\n```")

        @discord.ui.button(style=discord.ButtonStyle.green, label="=", row=3)
        async def equal(self, button: discord.ui.Button, interaction: discord.Interaction):
            try:
                self.expr = await self.calc.calculate(self.expr)
            except errors.BadArgument:  # if you are function only, change this to BadArgument
                return await interaction.response.send_message("Um, looks like you provided a wrong expression....")
            await interaction.message.edit(content=f"```\n{self.expr}\n```")

        @discord.ui.button(style=discord.ButtonStyle.green, label="-", row=3)
        async def minus(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.expr += "-"
            await interaction.message.edit(content=f"```\n{self.expr}\n```")

        @discord.ui.button(style=discord.ButtonStyle.green, label="(", row=4)
        async def left_bracket(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.expr += "("
            await interaction.message.edit(content=f"```\n{self.expr}\n```")

        @discord.ui.button(style=discord.ButtonStyle.green, label=")", row=4)
        async def right_bracket(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.expr += ")"
            await interaction.message.edit(content=f"```\n{self.expr}\n```")

        @discord.ui.button(style=discord.ButtonStyle.red, label="<==", row=4)
        async def back(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.expr = self.expr[:-1]
            await interaction.message.edit(content=f"```\n{self.expr}\n```")

        @discord.ui.button(style=discord.ButtonStyle.grey, label="OFF", row=4)
        async def clear(self, button: discord.ui.Button, interaction: discord.Interaction):
            await interaction.message.edit(content=f"```OFF```")
            self.stop()

class calc(commands.Cog):
    def __init__(self, bot):
      self.bot = bot

    @commands.command()
    async def calc(self, ctx, *, arg:str=None):
        if not arg == None:
            i = arg.lower().replace("x", "*").replace(":", "/").replace(",", ".")
            await ctx.reply(f"```{arg} = {await simpcalc.Calculate().calculate(i)}```")
        if arg == None:
            view = InteractiveView()
            test = await ctx.send("```\n```", view=view)
    
def setup(bot):
    bot.add_cog(calc(bot))
