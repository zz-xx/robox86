import discord
from discord.ext import commands

from x86 import helpers

class Spotify:
    "commands associated with spotify"

    #@commands.cooldown(1,60)
    @commands.command(aliases=['spot'])
    async def spotify(self, ctx, member_string):
        '''Get details of song being played by user on Spotify'''
        print(member_string)
       
        member = await helpers.search_member(ctx,member_string)
        artists = ','.join(member.activity.artists)
        data = discord.Embed(description=artists, colour=member.activity.color)
        data.set_author(name=member.activity.title)
        data.set_thumbnail(url=member.activity.album_cover_url)
        data.add_field(value='<a:spotify:433908041910321172><a:spotify:433908041910321172><a:spotify:433908041910321172><a:spotify:433908041910321172><a:spotify:433908041910321172><a:spotify:433908041910321172><a:spotify:433908041910321172><a:spotify:433908041910321172><a:spotify:433908041910321172><a:spotify:433908041910321172><a:spotify:433908041910321172><a:spotify:433908041910321172><a:spotify:433908041910321172><a:spotify:433908041910321172>', name='_ _')
        #data.add_field(name='-._-._-._-._-._-._-._-._-._-._-._-._-._-._-._-._-._-._-._-._-._-._-._-._-._-._-._-._-._-._-._-._-._-._-.-._-._-._-._-.', value='_ _')
        data.add_field(name='Album:', value=member.activity.album)
        #data.add_field(name='Track Id:', value=member.activity.track_id)
        data.add_field(name='Duration:', value=f'{str(member.activity.duration).split(".")[0]}')
        data.add_field(name='Started playing at', value=f'{member.activity.start.hour}:{member.activity.start.minute}:{member.activity.start.second} UTC')
        data.add_field(name='_ _ _ _ Will stop playing at', value=f'{member.activity.end.hour}:{member.activity.end.minute}:{member.activity.end.second} UTC')
        await ctx.send(embed=data)


    @commands.command()
    async def test(self, ctx):
        emojis = ctx.bot.emojis
        for emoji in emojis:
            #<a:spotify:433908041910321172>
            print(emoji)
    

def setup(bot):
    bot.add_cog(Spotify())
