import asyncio
from datetime import date
import sys
import time

import discord
from discord.ext import commands

from x86 import helpers




class OnePieceUpdatesTask:
    '''Task for regularly checking One Piece Manga Updates and Spoilers'''



    def __init__(self, bot):
        self.bot = bot
        self.task = self.bot.loop.create_task(self.main_task())


    
    async def main_task(self):

        await self.bot.wait_until_ready()


        while True:
            print('Inside One Piece Updates Task')
            #docCount = await ctx.bot.onePieceCollection.count_documents({})

            #monday is 0 and so on
            #only need to constantly check reddit on wednesdays, thursdays and fridays
            if date.today().weekday() in [2,3,4]:           
    
                async for document in self.bot.onePieceCollection.find({}):
                    print(document)

                    if document['_id'] == 1:
                        continue
                    

                    guild = self.bot.get_guild(document['_id'])
                    
                    #only post updates if post_updates is set to true
                    #at least one user must be subscribed in a guild for updates to be posted 
                    #non empty dictionaries evaluate to true
                    #if assigned_channel for updates is not set and post_updates is on 
                    #send update to fist channel that bot has access too
                    if document['subscribed_users']:

                        if document['post_updates']:
                        
                            if document['assigned_channel'] is None:
                                for channel in guild.text_channels:
                                    print(channel)
                                    
                                    try:
                                        await channel.send('This is message for unassigned channels.')
                                        break
                                    #will update later with more specific exception
                                    except discord.DiscordException:
                                        continue
                            
                            else:
                                channel = self.bot.get_channel(document['assigned_channel'])
                                await channel.send('Test message to assigned channel.')
            
                    else:
                        pass    

            else:
                channel = self.bot.get_channel(483021431232397343)
                await channel.send('Today is not Wednesday, Thursday or Friday so nothing to do.')                


            await asyncio.sleep(600)



    async def make_request(self, ctx: commands.context, url: str):
        '''make request'''
        
        async with ctx.bot.session.get(url) as response:
            json = await response.json()
            return json



def setup(bot):
    bot.add_cog(OnePieceUpdatesTask(bot))  