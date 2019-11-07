import asyncio
import sys
import time
import traceback

from bs4 import BeautifulSoup
import discord 
from discord.ext import commands

from x86 import helpers

#i know this is sort of confusing and unneeded will change it later
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}


class SurrenderAt20:
    """Tasks associated with surrenderat20.net """


    def __init__(self, bot):
        self.bot = bot
        self.currentTopTitle = {
            'PBE': None,
            'Releases' : None,
            'Red Posts' : None,
            'Rotations' : None,
            'Esports' : None
        }
        self.test_task = self.bot.loop.create_task(self.main_task())
        


    async def main_task(self):

        await self.bot.wait_until_ready()
        

        while True:

            print('inside task')
                        
            #this is not blocking 
            try:
                #async with self.bot.session.get('https://www.surrenderat20.net/search/label/PBE/', headers=headers) as response:
                #always remember this and effort spent to researh why it was done this way(ensure_future)
                #wasted lot of time here, more than I want to admit
                #always read documentation carefully I guess...
                #page = await response.read()

                #make requests to all labels

                #PBE
                page = await self.make_requests('https://www.surrenderat20.net/search/label/PBE/', headers)
                asyncio.ensure_future(self.page_extractor(page, 'PBE'), loop=self.bot.loop)
                #print(page)

                #Releases
                page = await self.make_requests('https://www.surrenderat20.net/search/label/Releases/', headers)
                asyncio.ensure_future(self.page_extractor(page, 'Releases'), loop=self.bot.loop)

                #Red Posts
                page = await self.make_requests('https://www.surrenderat20.net/search/label/Red Posts/', headers)
                asyncio.ensure_future(self.page_extractor(page, 'Red Posts'), loop=self.bot.loop)

                #Rotations
                page = await self.make_requests('https://www.surrenderat20.net/search/label/Rotations/', headers)
                asyncio.ensure_future(self.page_extractor(page, 'Rotations'), loop=self.bot.loop)

                #Esports
                page = await self.make_requests('https://www.surrenderat20.net/search/label/Esports/', headers)
                asyncio.ensure_future(self.page_extractor(page, 'Esports'), loop=self.bot.loop)

                   
            except Exception as error:
                print(f'Something went wrong, {error}')
                break

            await asyncio.sleep(1200)

        #for loop here is blocking code for some reason which I cannot quiet comprehend 



    async def page_extractor(self, r:'response', label:str):
        
        #smashed my head here, was really hard to figure out in beginning
        #eventually was very easy to figure out after I checked aiohttp response type(which was class 'byte')
        soup = BeautifulSoup(r.decode('utf-8'), 'lxml')


        #code for scraping titles and url's 
        rawTitles = soup.find_all('h1', {'class':'news-title'})
        
        #comprehensions are AMAZING.. so BEAUTIFUL!!
        #could be written in one comprehension but linter doesn't agree
        title = [BeautifulSoup(str(title), 'lxml') for title in rawTitles]
        titles = [{'url' : link['href'], 'title': link.string} for t in title for link in t.find_all('a', href = True)]
        
        
        #code for scraping dates 
        #thought this up by very minute analysis of source code lol
        rawDates = soup.find_all('span', {'class':'news-date'})

        #backslash cannot be included in curly braces
        #and by extension expression part of f-strings
        #chr(10) is being used as sort of escape character here for '\n'
        #could be written in one comprehension but linter doesn't agree
        date = [BeautifulSoup(str(date), 'lxml') for date in rawDates]
        dates = [f"{d.text.strip(chr(10)).split(' ')[-1]} on {text.string} at {''.join(d.b.contents)}" for d in date for text in d.find_all('abbr', {'class':'published'})]
        
        
        channel = self.bot.get_channel(435168674261893121)
        """
        await channel.send(str(titles)[:1500], delete_after=20)
        await channel.send(str(dates)[:1500], delete_after=20)
        await channel.send('-----------------------------------------------------', delete_after=20)
        """
        """
        collection = self.bot.db['sat20Subs']
        cursor = collection.find({})
        for document in await cursor.to_list(length=100):
            print(document)
        """
        #current title of top post on site is same as old one 
        #hence no updates, do nothing
        if self.currentTopTitle[label] == titles[0]['title']:
            #channel = self.bot.get_channel(435168674261893121)
            #await channel.send(f"No update in {label}")
            return
        
        #current title of top post on site is different than previous one 
        #hence post was updated
        #post it on designated channel
        elif self.currentTopTitle[label] != titles[0]['title']:

            #scrape first post in list of all updates
            try:
                page = await self.make_requests(titles[0]['url'], headers)

                soup = BeautifulSoup(page.decode('utf-8'), 'lxml')

                #get links of all images in post
                images = soup.find_all('img')
                #only concerned about first image of post
                #print(images[0]['src'])

                check = soup.find(text='Table of Contents')
                toc = None

                #table of contents exist 
                if check is not None:
                    #html source code is like this couldn't think of any other way to implement this
                    uTag = check.parent
                    h2Tag = uTag.parent

                    nextUlTag = h2Tag.findNext('ul')

                    #print(type(nextUlTag))

                    #debatable why I did this
                    #I find this convenient insteadd of fiddling with bs4.tags
                    contents = BeautifulSoup(str(nextUlTag), 'lxml')
                    #print(type(contents))
            
                    #list for table of contents
                    toc = [{'link': c['href'], 'title': c.string} for c in contents.find_all('a')]
                    #print(toc)
                    """
                    channel = self.bot.get_channel(435168674261893121)
                    await channel.send(str(toc)[:1500], delete_after=20)
                    """

                self.currentTopTitle[label] = titles[0]['title']
                embed = await self.create_embed(titles[0], dates[0], images[0]['src'], toc, label)
                channel = self.bot.get_channel(435168674261893121)

                #await channel.send(embed=embed)


            except Exception as error:
                    print(f'Something went wrong, {error} on line {sys.exc_info()[-1].tb_lineno}')
                    traceback.print_exc()
                    return


          
    async def create_embed(self, postTitle:dict, postDate:str, postImgUrl:str, toc, label:str):

        surrenderAt20Logo = 'https://3.bp.blogspot.com/-M_ecJWWc5CE/Uizpk6U3lwI/AAAAAAAACLo/xyh6eQNRzzs/s640/sitethumb.jpg'
        
        siteMods = {
            'Aznbeat':{'profile':'https://disqus.com/by/aznbeat/','pfp':'https://c.disquscdn.com/uploads/users/5022/5820/avatar92.jpg?1479364505'},
            'MooBeat':{'profile':'https://disqus.com/by/moobeat/','pfp':'https://c.disquscdn.com/uploads/users/3715/5060/avatar92.jpg?1532471751'}
            }
        
        #this might block code..
        description = None
        
        if toc is None:
            description = "\u200b\n \u200b\n \u200b"
        else:
            description = "\u200b\n \u200b\n \u200b\n **Table of Contents**\n"
            description +=''.join([f"[{content['title']}]({content['link']})\n" for content in toc])
        
        #print(description)

        embed = discord.Embed(title=postTitle['title'], url=postTitle['url'], color=discord.Colour(0xcc0000), description=description)
        embed.set_thumbnail(url=surrenderAt20Logo)
        #no checking here should prob do it later
        embed.set_author(name=postDate.split(' ')[0], url=siteMods[postDate.split(' ')[0]]['profile'], icon_url=siteMods[postDate.split(' ')[0]]['pfp'])
        embed.set_image(url=postImgUrl)
        #add code to update revision later for now hard coding it
        embed.set_footer(text=f"Revision 0 • {' '.join(postDate.split(' ')[2:])}")
        #write code to check all sub categories later, hardcoding for now
        embed.add_field(name='Labels', value=f"{(lambda label: 'Public Beta Environment' if label=='PBE' else f'{label}')(label)}")
        return embed

        
        
    async def make_requests(self, url:str, headers:dict):

        start = time.monotonic()

        async with self.bot.session.get(url, headers=headers) as response:
            #"""
            description = f"```ini\nResponse status : [{response.status}]\nResponse time   : [{round(time.monotonic() - start, 2)}s]\n```\n `on URL`\n__**{url}**__"
            embed = discord.Embed(color=await helpers.get_color(), description=description)
            embed.set_author(name='GET', icon_url=self.bot.user.avatar_url)
            embed.set_footer(text=time.ctime())
            channel = self.bot.get_channel(483021431232397343)
            await channel.send(embed=embed)
            #"""
            #print(f'Request succeeded with status code {response.status}')
            page = await response.read()
            return page



def setup(bot):
    bot.add_cog(SurrenderAt20(bot))    

