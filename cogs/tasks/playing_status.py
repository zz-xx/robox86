"""This extension sets the bot's playing status."""

import asyncio
import discord


class PlayingStatus:
    """Bot playing status manager."""


    def __init__(self, bot):
        self.bot = bot
        self.statuses = []
        self.index = 0

        #this must be created as task bc it must be checked after specific intervals
        self.playing_status_task = self.bot.loop.create_task(self.update_playing_status())

   

    def get_next_status(self):
        """Get next playing status type."""

        status = self.statuses[self.index]

        if isinstance(status, tuple):
            #mind fucking and super fancy way of calling functions
            status = status[0].format(status[1]())

        self.index += 1

        if self.index >= len(self.statuses):
            self.index = 0

        return status



    def guild_count(self):
        """Get guild count from bot."""

        guilds = len(self.bot.guilds)
        return guilds



    def member_count(self):
        """Get human users count from bot."""

        member_count = sum(not m.bot for m in self.bot.get_all_members())
        return member_count



    async def update_playing_status(self):
        """Every 10 seconds, update the bot's playing status."""

        await self.bot.wait_until_ready()

        display_prefix = self.bot.config['prefix']
        if len(display_prefix) > 1: 
            display_prefix += " " #extra space appended for bigger prefixes

        self.statuses = [
            f"'{display_prefix}help' for help.",
            f"'{display_prefix}info' for info.",
            ("in {0} servers", self.guild_count),
            ("with {0} Pewdiepie fans", self.member_count),
        ]

        while True:
            status = self.get_next_status()
            activity=discord.Streaming(name=status, url="https://www.twitch.tv/pewdiepie")
            await self.bot.change_presence(activity=activity)
            await asyncio.sleep(10)



def setup(bot):
    """Set up the extension."""
    bot.add_cog(PlayingStatus(bot))


