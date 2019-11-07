import json
import ast

import discord
from discord.ext import commands

from x86 import helpers

BASE_API_URL = 'http://api.football-data.org/v1/competitions'

class Soccer:
    """Commands associated with fetching Soccer related data"""

    @commands.command()
    @commands.cooldown(6,12)
    async def table(self, ctx, *args):
        """Fetch standings of given league"""

        raw_data = await helpers.make_request(ctx, BASE_API_URL)
        data = json.loads(raw_data.decode('utf-8'))

        prem_league = data[1]
        prem_teams_url = prem_league['_links']['leagueTable']['href']
        print(prem_teams_url)

        raw_data = await helpers.make_request(ctx, prem_teams_url)
        data = json.loads(raw_data.decode('utf-8'))

        data_embed=discord.Embed(title=f"Matchday {data['matchday']}", description="-------------------------------------------------------------------------------", colour=discord.Color(value=await helpers.get_color()))
        data_embed.set_author(name=data['leagueCaption'])

        count = 0
        for team in data['standing']:
            data_embed.add_field(name='\u200b', value='\u200b', inline=True)
            data_embed.add_field(name=f"{team['position']}.  {team['teamName']}" , value=f"Played: {team['playedGames']}    Points: {team['points']}    Wins: {team['wins']}   Draws: {team['draws']}   Losses: {team['losses']}    GF: {team['goals']}    GA: {team['goalsAgainst']}    GD: {team['goalDifference']}", inline=True)
            count+=1
            if count == 10: break
          
        await ctx.send(embed=data_embed)



    @commands.command()
    @commands.cooldown(6,60)
    async def wc(self, ctx, *args):
        "Command associated with Fifa World Cup 2018"

        api_url = BASE_API_URL + '/467'
        raw_data = await helpers.make_request(ctx, api_url)

        #got the solution from stack overflow 
        #converts the byte to dictionary
        #apparently it's `byte` object so this must be done
        #this is first time i am facing such problem with api
        raw_data = raw_data.decode('utf-8')
        data = ast.literal_eval(raw_data)


        if not args:
            print('Working')
            embed = discord.Embed(description='------------------------------------', color=await helpers.get_color())
            embed.set_author(name=data['caption'], icon_url='https://image.jimcdn.com/app/cms/image/transf/dimension=641x10000:format=png/path/s6d54c624f88c95ec/image/i34d2e10b38f67263/version/1490980233/fifa-world-cup.png')
            embed.set_thumbnail(url='http://www.yordes.com/wp-content/uploads/edd/2017/09/world-cup-2018-logo-700x525.jpg')
            embed.add_field(name='Current match day', value=data['currentMatchday'])
            embed.add_field(name='Number of teams', value=data['numberOfTeams'])
            embed.add_field(name='Number of games', value=data['numberOfGames'])
            embed.add_field(name='Number of matchdays', value=data['numberOfMatchdays'])
            embed.set_footer(text=f"last updated on {data['lastUpdated'].split('T')[0]} at {data['lastUpdated'].split('T')[1][:-1]} UTC")
            await ctx.send(embed=embed)


        if args:
            #making request on league table api endpoint and converting it into dict
            leagueTable_url = data['_links']['leagueTable']['href']
            leagueTable_data = await helpers.make_request(ctx, leagueTable_url)
            leagueTable_data = leagueTable_data.decode('utf-8')
            leagueTable_data = ast.literal_eval(leagueTable_data)

            #not proud of this but this works so
            #standings by group
            if args[0] in ['g','group','G','Group'] and args[1] in ['a','A']:
                embed = discord.Embed(title='\u200b', description='**`Group A`**', color=await helpers.get_color())#, description='------------------------------------')
                embed.set_author(name=data['caption'], icon_url='https://image.jimcdn.com/app/cms/image/transf/dimension=641x10000:format=png/path/s6d54c624f88c95ec/image/i34d2e10b38f67263/version/1490980233/fifa-world-cup.png')
                embed.set_thumbnail(url='http://www.yordes.com/wp-content/uploads/edd/2017/09/world-cup-2018-logo-700x525.jpg')
                embed.set_footer(text=f"last updated on {data['lastUpdated'].split('T')[0]} at {data['lastUpdated'].split('T')[1][:-1]} UTC")
                for team in leagueTable_data['standings']['A']:
                    embed.add_field(value='_ _', name='---------------------------------------------------------', inline=True)
                    embed.add_field(name=f"{team['rank']}.  {team['team']}" , value=f"Played: {team['playedGames']}    Points: {team['points']}     GF: {team['goals']}    GA: {team['goalsAgainst']}    GD: {team['goalDifference']}", inline=True)
                embed.add_field(value='_ _', name='---------------------------------------------------------', inline=True)
                await ctx.send(embed=embed)

            elif args[0] in ['g','group','G','Group'] and args[1] in ['b','B']:
                embed = discord.Embed(title='\u200b', description='**`Group B`**', color=await helpers.get_color())#, description='------------------------------------')
                embed.set_author(name=data['caption'], icon_url='https://image.jimcdn.com/app/cms/image/transf/dimension=641x10000:format=png/path/s6d54c624f88c95ec/image/i34d2e10b38f67263/version/1490980233/fifa-world-cup.png')
                embed.set_thumbnail(url='http://www.yordes.com/wp-content/uploads/edd/2017/09/world-cup-2018-logo-700x525.jpg')
                embed.set_footer(text=f"last updated on {data['lastUpdated'].split('T')[0]} at {data['lastUpdated'].split('T')[1][:-1]} UTC")
                for team in leagueTable_data['standings']['B']:
                    embed.add_field(value='_ _', name='---------------------------------------------------------', inline=True)
                    embed.add_field(name=f"{team['rank']}.  {team['team']}" , value=f"Played: {team['playedGames']}    Points: {team['points']}     GF: {team['goals']}    GA: {team['goalsAgainst']}    GD: {team['goalDifference']}", inline=True)
                embed.add_field(value='_ _', name='---------------------------------------------------------', inline=True)
                await ctx.send(embed=embed)

            elif args[0] in ['g','group','G','Group'] and args[1] in ['c','C']:
                embed = discord.Embed(title='\u200b', description='**`Group C`**', color=await helpers.get_color())#, description='------------------------------------')
                embed.set_author(name=data['caption'], icon_url='https://image.jimcdn.com/app/cms/image/transf/dimension=641x10000:format=png/path/s6d54c624f88c95ec/image/i34d2e10b38f67263/version/1490980233/fifa-world-cup.png')
                embed.set_thumbnail(url='http://www.yordes.com/wp-content/uploads/edd/2017/09/world-cup-2018-logo-700x525.jpg')
                embed.set_footer(text=f"last updated on {data['lastUpdated'].split('T')[0]} at {data['lastUpdated'].split('T')[1][:-1]} UTC")
                for team in leagueTable_data['standings']['C']:
                    embed.add_field(value='_ _', name='---------------------------------------------------------', inline=True)
                    embed.add_field(name=f"{team['rank']}.  {team['team']}" , value=f"Played: {team['playedGames']}    Points: {team['points']}     GF: {team['goals']}    GA: {team['goalsAgainst']}    GD: {team['goalDifference']}", inline=True)
                embed.add_field(value='_ _', name='---------------------------------------------------------', inline=True)
                await ctx.send(embed=embed)
                
            elif args[0] in ['g','group','G','Group'] and args[1] in ['d','D']:
                embed = discord.Embed(title='\u200b', description='**`Group D`**', color=await helpers.get_color())#, description='------------------------------------')
                embed.set_author(name=data['caption'], icon_url='https://image.jimcdn.com/app/cms/image/transf/dimension=641x10000:format=png/path/s6d54c624f88c95ec/image/i34d2e10b38f67263/version/1490980233/fifa-world-cup.png')
                embed.set_thumbnail(url='http://www.yordes.com/wp-content/uploads/edd/2017/09/world-cup-2018-logo-700x525.jpg')
                embed.set_footer(text=f"last updated on {data['lastUpdated'].split('T')[0]} at {data['lastUpdated'].split('T')[1][:-1]} UTC")
                for team in leagueTable_data['standings']['D']:
                    embed.add_field(value='_ _', name='---------------------------------------------------------', inline=True)
                    embed.add_field(name=f"{team['rank']}.  {team['team']}" , value=f"Played: {team['playedGames']}    Points: {team['points']}     GF: {team['goals']}    GA: {team['goalsAgainst']}    GD: {team['goalDifference']}", inline=True)
                embed.add_field(value='_ _', name='---------------------------------------------------------', inline=True)
                await ctx.send(embed=embed)
            
            elif args[0] in ['g','group','G','Group'] and args[1] in ['e','E']:
                embed = discord.Embed(title='\u200b', description='**`Group E`**', color=await helpers.get_color())#, description='------------------------------------')
                embed.set_author(name=data['caption'], icon_url='https://image.jimcdn.com/app/cms/image/transf/dimension=641x10000:format=png/path/s6d54c624f88c95ec/image/i34d2e10b38f67263/version/1490980233/fifa-world-cup.png')
                embed.set_thumbnail(url='http://www.yordes.com/wp-content/uploads/edd/2017/09/world-cup-2018-logo-700x525.jpg')
                embed.set_footer(text=f"last updated on {data['lastUpdated'].split('T')[0]} at {data['lastUpdated'].split('T')[1][:-1]} UTC")
                for team in leagueTable_data['standings']['E']:
                    embed.add_field(value='_ _', name='---------------------------------------------------------', inline=True)
                    embed.add_field(name=f"{team['rank']}.  {team['team']}" , value=f"Played: {team['playedGames']}    Points: {team['points']}     GF: {team['goals']}    GA: {team['goalsAgainst']}    GD: {team['goalDifference']}", inline=True)
                embed.add_field(value='_ _', name='---------------------------------------------------------', inline=True)
                await ctx.send(embed=embed)

            elif args[0] in ['g','group','G','Group'] and args[1] in ['f','F']:
                embed = discord.Embed(title='\u200b', description='**`Group F`**', color=await helpers.get_color())#, description='------------------------------------')
                embed.set_author(name=data['caption'], icon_url='https://image.jimcdn.com/app/cms/image/transf/dimension=641x10000:format=png/path/s6d54c624f88c95ec/image/i34d2e10b38f67263/version/1490980233/fifa-world-cup.png')
                embed.set_thumbnail(url='http://www.yordes.com/wp-content/uploads/edd/2017/09/world-cup-2018-logo-700x525.jpg')
                embed.set_footer(text=f"last updated on {data['lastUpdated'].split('T')[0]} at {data['lastUpdated'].split('T')[1][:-1]} UTC")
                for team in leagueTable_data['standings']['F']:
                    embed.add_field(value='_ _', name='---------------------------------------------------------', inline=True)
                    embed.add_field(name=f"{team['rank']}.  {team['team']}" , value=f"Played: {team['playedGames']}    Points: {team['points']}     GF: {team['goals']}    GA: {team['goalsAgainst']}    GD: {team['goalDifference']}", inline=True)
                embed.add_field(value='_ _', name='---------------------------------------------------------', inline=True)
                await ctx.send(embed=embed)
            
            elif args[0] in ['g','group','G','Group'] and args[1] in ['g','G']:
                embed = discord.Embed(title='\u200b', description='**`Group G`**', color=await helpers.get_color())#, description='------------------------------------')
                embed.set_author(name=data['caption'], icon_url='https://image.jimcdn.com/app/cms/image/transf/dimension=641x10000:format=png/path/s6d54c624f88c95ec/image/i34d2e10b38f67263/version/1490980233/fifa-world-cup.png')
                embed.set_thumbnail(url='http://www.yordes.com/wp-content/uploads/edd/2017/09/world-cup-2018-logo-700x525.jpg')
                embed.set_footer(text=f"last updated on {data['lastUpdated'].split('T')[0]} at {data['lastUpdated'].split('T')[1][:-1]} UTC")
                for team in leagueTable_data['standings']['G']:
                    embed.add_field(value='_ _', name='---------------------------------------------------------', inline=True)
                    embed.add_field(name=f"{team['rank']}.  {team['team']}" , value=f"Played: {team['playedGames']}    Points: {team['points']}     GF: {team['goals']}    GA: {team['goalsAgainst']}    GD: {team['goalDifference']}", inline=True)
                embed.add_field(value='_ _', name='---------------------------------------------------------', inline=True)
                await ctx.send(embed=embed)

            elif args[0] in ['g','group','G','Group'] and args[1] in ['h','H']:
                embed = discord.Embed(title='\u200b', description='**`Group H`**', color=await helpers.get_color())#, description='------------------------------------')
                embed.set_author(name=data['caption'], icon_url='https://image.jimcdn.com/app/cms/image/transf/dimension=641x10000:format=png/path/s6d54c624f88c95ec/image/i34d2e10b38f67263/version/1490980233/fifa-world-cup.png')
                embed.set_thumbnail(url='http://www.yordes.com/wp-content/uploads/edd/2017/09/world-cup-2018-logo-700x525.jpg')
                embed.set_footer(text=f"last updated on {data['lastUpdated'].split('T')[0]} at {data['lastUpdated'].split('T')[1][:-1]} UTC")
                for team in leagueTable_data['standings']['H']:
                    embed.add_field(value='_ _', name='---------------------------------------------------------', inline=True)
                    embed.add_field(name=f"{team['rank']}.  {team['team']}" , value=f"Played: {team['playedGames']}    Points: {team['points']}     GF: {team['goals']}    GA: {team['goalsAgainst']}    GD: {team['goalDifference']}", inline=True)
                embed.add_field(value='_ _', name='---------------------------------------------------------', inline=True)
                await ctx.send(embed=embed)


    @commands.command(aliases=['get_channel_list()'])
    async def channel_list(self, ctx):
        "Get list of channels in guild with their id's"

        channels = ctx.guild.channels

        for channel in channels:
            embed = discord.Embed(description=f'**Channel Name :** *__{channel.name}__*\n **Channel Id:** *__{channel.id}__*', color=await helpers.get_color())
            await ctx.send(embed=embed)


    #purge bots last n messages
    @commands.command(aliases=['purge'], is_owner=True)
    async def delete_messages(self, ctx, n:int):

        def is_bot(m):
            return m.author == ctx.bot.user

        deleted = await ctx.channel.purge(limit=n, check=is_bot, bulk=False)
        await ctx.channel.send(f'Deleted {len(deleted)} messages.')
    

    @commands.command(aliases=['get_all_emotes()'], is_owner=True)
    async def all_emotes(self, ctx):
        emojis = ctx.guild.emojis

        for emoji in emojis:
            if emoji.animated:
                description = f'<a:{emoji.name}:{emoji.id}>\n```ini\nEmoji name : [{emoji.name}]\nEmoji id   : [<a:{emoji.name}:{emoji.id}>]```'
            else:
                description = f'<:{emoji.name}:{emoji.id}>\n```ini\nEmoji name : [{emoji.name}]\nEmoji id   : [<:{emoji.name}:{emoji.id}>]```'
            embed = discord.Embed(description=description, color=await helpers.get_color())
            await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Soccer())