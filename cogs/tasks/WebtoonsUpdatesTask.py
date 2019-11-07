import asyncio
from datetime import date
import sys
import time

from bs4 import BeautifulSoup
import discord
from discord.ext import commands

from x86 import helpers


class WebtoonsUpdatesTask:
    'Tasks associated with webtoons.com'

    def __init__(self, bot):
        self.bot = bot
        self.task = self.bot.loop.create_task(self.main_task())


    #@commands.command()
    async def main_task(self):

        await self.bot.wait_until_ready()

        while True:
            print('Inside webtoons Updates Task')
            channel = self.bot.get_channel(483021431232397343)
            await channel.send('Today is Thursday. Looking out for new updates.')

            if date.today().weekday() in [3]:
                        
                url = 'https://www.webtoons.com/en/fantasy/unordinary/list?title_no=679'

                start = time.monotonic()

                async with self.bot.session.get(url) as response:
                    description = f"```ini\nResponse status : [{response.status}]\nResponse time   : [{round(time.monotonic() - start, 2)}s]\n```\n `on URL`\n__**{url}**__"
                    embed = discord.Embed(description=description, color=await helpers.get_color())
                    embed.set_author(name='GET', icon_url=self.bot.user.avatar_url)
                    embed.set_footer(text=time.ctime())
                    channel = self.bot.get_channel(483021431232397343)
                    await channel.send(embed=embed)
                    page = await response.read()
                
                soup = BeautifulSoup(page.decode('utf-8'), 'lxml')

                #await ctx.send(soup.text[0:1999])

                #only one div tag with class detail_lst so no need to use find_all
                #print('works')
                chapters = soup.find('div', {'class':'detail_lst'})
                #print(chapters)
                
                #await ctx.send(chapters.text[0:1999])

                
                chaptersList = chapters.find_all('li')
                current_chap_id = chaptersList[0]['id']
                #await ctx.send(chaptersList[0].find('a')['href'])

                #print('works')
                
                #print('does this works?')
                result = await self.bot.unOrdinaryCollection.find_one({'_id': 1})

                
                #will only happen first time when db is completely empty
                if result is None:
                    print('result is none')

                    #never do a return in task lolol always remember this
                    #return
                    await asyncio.sleep(600)
                    #await asyncio.sleep(60)
                    continue
                
                #print('does this works?')
                if result['current_chap_id'] != current_chap_id:

                    async for document in self.bot.unOrdinaryCollection.find({}):
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
                                            await channel.send('New chapter is out.')
                                            await channel.send(chaptersList[0].find('a')['href'])
                                            subscribed_users = document['subscribed_users']
                                            userMentionString = ''.join(f'<@{user}>' for user in subscribed_users.keys())
                                            await channel.send(f'{userMentionString} Check it out!')
                                            await channel.send('This is message for unassigned channels. Assign a channel.')
                                            break
                                        #will update later with more specific exception
                                        except discord.DiscordException:
                                            continue
                                
                                else:
                                    channel = self.bot.get_channel(document['assigned_channel'])
                                    await channel.send('New chapter of is out.')
                                    await channel.send(chaptersList[0].find('a')['href'])
                                    subscribed_users = document['subscribed_users']
                                    userMentionString = ''.join(f'<@{user}>' for user in subscribed_users.keys())
                                    await channel.send(f'{userMentionString} Check it out!')
                                    #await channel.send('Test message to assigned channel.')
                
                        else:
                            pass  

                    result['current_chap_id'] = current_chap_id
                    status = await self.bot.unOrdinaryCollection.replace_one({'_id': 1}, result)
                    channel = self.bot.get_channel(483021431232397343)
                    await channel.send(f'Replaced {status.modified_count} document.')
                
                #one request every 10 mins
                await asyncio.sleep(600)
                #await asyncio.sleep(60)

        else:
            channel = self.bot.get_channel(483021431232397343)
            await channel.send('Today is not Thursday so nothing to do.')
            #check every 10 mins what day it is
            await asyncio.sleep(600)                 


        '''
        for i in range(0, len(chaptersList)):
            chapterId = chaptersList[i]['id']
            chapterLink = chaptersList[i].find('a')['href']
            await ctx.send(chapterId + ' ' + chapterLink)
        '''


        

def setup(bot):
    bot.add_cog(WebtoonsUpdatesTask(bot))    




