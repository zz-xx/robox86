import discord
from discord.ext import commands

from x86 import helpers

class AnonymousMessage:
    "Commands associated with anonymously messaging guild members"

    @commands.command(aliases = ['anon_msg'])
    async def anonymous_message(self, ctx, user, *message):
        "Send an completely anonymous message to someone in guild"
        "Recipients must allow DM's from guild members"

        #check if it's DM channel , if it is then process further
        if not isinstance(ctx.channel, discord.DMChannel):
            await ctx.send("Don't do this in front of everyone <:stonedjerry:427827597406109697>", delete_after=5)
            return

        user = await helpers.search_user(user, ctx)
        
        await user.send(" ".join(message))



def setup(Bot):
    Bot.add_cog(AnonymousMessage())