import discord
from discord.ext import commands
from x86 import helpers

class Ping:
    """Ping command"""

    @commands.command()
    @commands.cooldown(6,12)
    async def ping(self, ctx):
        """Ping the bot"""

        #heartbeat latency (i'll be honest, dont really understand how it works)
        hb_latency = round(ctx.bot.latency*1000, 2)

        '''
        await ctx.send(hb_latency)
        #this is a tuple
        await ctx.send(ctx.bot.latencies)
        await ctx.send(len(ctx.bot.latencies)>1)
        await ctx.send(ctx.guild)
        await ctx.send(ctx.guild.shard_id)
        '''

        #only valid if bot gets big enough 
        if ctx.guild and len(ctx.bot.latencies) > 1:
            current_shard_latency = ctx.bot.latencies[ctx.guild.shard_id]
            #shard heartbeat latency
            shb_latency = round(current_shard_latency*1000, 2)
            latency_message = f'\n**```ini\nHeartbeat Latency: [{hb_latency} ms] \nCurrent Shard Heartbeat: [{shb_latency} ms]```**'
        
        else:
            latency_message = f'\n**```ini\nHeartbeat Latency:  [{hb_latency} ms] ```**'

        #create embed
        embed = discord.Embed(description=latency_message, color=await helpers.get_color())
        ping_message = await ctx.send(embed=embed)
        #ping_message = await ctx.send(latency_message)

        #round trip ping
        rt_ping = round((ping_message.created_at - ctx.message.created_at).total_seconds() * 1000, 2)

        embed = discord.Embed(description=f'{latency_message[:-6]} \nRound-trip time:    [{rt_ping} ms] ```**', color=await helpers.get_color())

        await ping_message.edit(embed=embed)



def setup(bot):
    bot.add_cog(Ping())

