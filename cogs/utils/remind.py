import asyncio

import discord
from discord.ext import commands

class Reminder:
    "Reminds you to do things"
    
    
    async def callback(self, ctx, time):
        await asyncio.sleep(time)
        print(f'{ctx.author.display_name} asked me to remind them {time} secs ago.')
        return f'{ctx.author.display_name} asked me to remind them {time} secs ago.'

    
    @commands.command(aliases=['rem'])
    async def reminder(self, ctx, time):
        "Will remind you after specified time"

        timeup = await self.callback(ctx, int(time))

        await ctx.send(timeup)

    

def setup(bot):
    bot.add_cog(Reminder())