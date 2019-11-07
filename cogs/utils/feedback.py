from datetime import datetime

import discord
from discord.ext import commands

from x86 import helpers

class Feedback:
    "Commands related to getting feedback from humans"

    #@commands.cooldown(1,3600)
    @commands.command(aliases=['fdbk'])
    async def feedback(self, ctx, *args):
        "Gets the feedback from user through direct message and guilds"
 
        is_dm = True
 
        #check if feedback is being given through dm's or in guild channel
        if not isinstance(ctx.channel, discord.DMChannel):
            await ctx.send('I prefer to accept criticism through **`Direct Messages`** only, but nvm.', delete_after = 5)
            await ctx.send('feedback recieved',delete_after=5)
            is_dm = False
        else:
             await ctx.send('feedback recieved', delete_after=5)

        channel = ctx.bot.get_channel(435034403610034176)
        embed = await self.create_feedback_embed(ctx, args, is_dm)
        await channel.send(embed=embed)

    #@staticmethod()
    async def create_feedback_embed(self, ctx, args, is_dm):
        "I am ashamed of this but had to make something temporary that works"
    
        if is_dm == True:
            embed = discord.Embed(description=f'\n```ini\nUser Id:    [{ctx.author.id}] \nGuild Name: [None] \nGuild Id:   [None]```', color = await helpers.get_color())
        else:
            embed = discord.Embed(description=f'\n```ini\nUser Id:    [{ctx.author.id}] \nGuild Name: [{ctx.guild.name}] \nGuild Id:   [{ctx.guild.id}]```', color = await helpers.get_color())
            
        embed.set_author(name=f'Feedback from {ctx.author}', icon_url=ctx.author.avatar_url_as(format='png', size=1024))

        embed.add_field(name='Feedback:', value=' '.join(args)[:1024])

        #embed.add_field(name='_ _', value='------------------------------------------------------------------------------------------------',)

        days=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        embed.set_footer(text=f'on {days[datetime.utcnow().weekday()]} at {str(datetime.utcnow())[:19]} UTC')

        return embed


def setup(Bot):
    Bot.add_cog(Feedback())