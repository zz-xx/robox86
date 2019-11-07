import json

import discord
from discord.ext import commands

from x86 import helpers



BASE_REDDIT_URL = 'https://www.reddit.com/r/'
SORT = {'n': 'new', 'r':'rising', 'c':'controversial', 't':'top', 'g':'gilded'}
TIME = {'h': 'hour', 'd': 'day', 'w': 'week', 'm': 'month', 'y': 'year', 'all' : 'all' }



class Reddit:
    """Commands for fetching posts and images from Reddit"""

    @commands.command(aliases=['r'])
    @commands.cooldown(6,12)
    async def reddit(self, ctx, *args):
        """Description: Get posts and images from given subreddit
           Usage: reddit [subreddit] [sort] [time]
        """
        
        #checking if proper args are provided, will add exception handling later
        if len(args) != 3:
            return
        
        url = f"{BASE_REDDIT_URL}{args[0]}/{SORT[args[1]]}.json?sort=top&t={TIME[args[2]]}&limit=5"
        print(url)

        raw_data = await helpers.make_request(ctx, url)

        data = json.loads(raw_data.decode('utf-8'))
        
        for i in data['data']['children']:
            await ctx.channel.trigger_typing()
            
            score = i['data']['score']
            title = i['data']['title']
            author = i['data']['author']
            user = 'u/' + author
            user_link = "https://www.reddit.com/user/" + author
            permalink = i['data']['permalink']
            post_link = "https://www.reddit.com" + permalink
            image_link = i['data']['url']
            children = i['data']['num_comments']
            footer_text = f"{score} upvotes   {children} comments"
            await ctx.send(image_link)
            
            '''
            reddit_icon_url = "https://images-na.ssl-images-amazon.com/images/I/418PuxYS63L.png"

            formats = ['.jpg','.png','gifv']
        
            if image_link[-4:] not in formats:
                #image_link = reddit_icon_url 

            post_embed = discord.Embed(description=user)
            post_embed.set_author(name=title, url=post_link)
            post_embed.set_image(url=image_link)
            #post_embed.set_thumbnail(url=image_link)
            post_embed.set_footer(text=footer_text)

            post = str(score) + ': ' + title + ' (' + post_link + ')'
            print(post)
            await ctx.send(embed=post_embed)
            '''




def setup(bot):
    bot.add_cog(Reddit()) 

        


