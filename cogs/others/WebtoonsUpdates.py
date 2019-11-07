from datetime import date

import discord
from discord.ext import commands

from x86 import helpers




class WebtoonsUpdates:
    '''Reminds you when new chapter of your favorite webtoon is out'''



    @commands.group(aliases=['Webtoons', 'WebToons', 'WEBTOONS', 'webt', 'Webt'])
    async def webtoons(self, ctx: commands.Context):
        '''Commands associated with webtoons'''
        
        if ctx.invoked_subcommand is None:
            await ctx.send(f"You must specify a webtoon. <@{ctx.author.id}>")
            await ctx.send(f'Currently available webtoons are : ')
            '''
            await ctx.send(f'{ctx.bot.cogs}')
            coms = ctx.bot.get_cog(self.__class__.__name__)
            print(coms)
            '''
            #t = (ctx.bot.get_cog(self.__class__.__name__), ctx.bot.get_cog_commands(self.__class__.__name__))
            #print(ctx.send(t))
            cogCommands = ctx.bot.get_cog_commands(self.__class__.__name__)

            for c in cogCommands:
              
                #if isinstance(c, commands.Group):
                    #grouped = '  \n'.join(com.name for com in c.commands)
                    grouped = '  \n'.join(f'{com.name}\n{com.short_doc}\n\n' for com in c.commands)
                    print(grouped)
                    await ctx.send(f'{c.name} {c.short_doc if c.short_doc else "Nothing"}\n\n`{grouped}`')
                #else:
                    #await ctx.send(f'{c.name}, {c.short_doc if c.short_doc else "Nothing"}')

        
    
    @webtoons.group(aliases=['unordinary', 'uno'])
    async def unOrdinary(self, ctx: commands.Context):
        '''
        The world is not perfect. Learning to deal with its flaws is just a normal part of life. 
        '''
        if ctx.invoked_subcommand is None:
            await ctx.send('Holder for embed. unOrdinary description here.')



    #no comments here because all these functions are same and just ported from one piece updates cog
    @unOrdinary.command(aliases=['Subscribe', 'sub', 'Sub'])
    async def subscribe(self, ctx: commands.Context):
        '''Subscribe to unOrdinary updates'''

        docCount = await ctx.bot.unOrdinaryCollection.count_documents({})

        if docCount == 0:
            await ctx.send('Empty Collection')
            
            tempDoc = {
                '_id': 1, 
                'current_chap_id' : None
            }
            result = await ctx.bot.unOrdinaryCollection.insert_one(tempDoc)
            await ctx.send(f'result = {result}')

            document = {
                '_id'    : ctx.guild.id,
                'guild'  : ctx.guild.name,
                'assigned_channel' : None,
                'post_updates' : True,
                'subscribed_users': {
                    str(ctx.author.id) : {
                        'date'   : str(date.today()),
                        'user'   : ctx.author.name,
                        'discriminator': ctx.author.discriminator
                    }
                }         
            }

            result = await ctx.bot.unOrdinaryCollection.insert_one(document)
            await ctx.send(f'result: {result.inserted_id}')
            await ctx.send(f'Successfully subscribed to unOrdinary updates. <@{ctx.author.id}>')

        
        else:
            await ctx.send('Collection not empty anymore.')

            result = await ctx.bot.unOrdinaryCollection.find_one({'_id': ctx.guild.id})
            
            if result is None:

                document = {
                    '_id'    : ctx.guild.id,
                    'guild'  : ctx.guild.name,
                    'assigned_channel' : None,
                    'post_updates' : True,
                    'subscribed_users': {
                        str(ctx.author.id) : {
                            'date'   : str(date.today()),
                            'user'   : ctx.author.name,
                            'discriminator': ctx.author.discriminator
                        }
                    }         
                }

                result = await ctx.bot.unOrdinaryCollection.insert_one(document)
                await ctx.send(f'result: {result.inserted_id}')
                await ctx.send(f'Successfully subscribed to unOrdinary updates. <@{ctx.author.id}>')

            else:
                
                subscribedUsers = result['subscribed_users']

                for userId in list(subscribedUsers):

                    if int(userId) == ctx.author.id:
                        await ctx.send(f"You're already subscribed. <@{ctx.author.id}>")
                        return
                
                document = {
                        'date'   : str(date.today()),
                        'user'   : ctx.author.name,
                        'discriminator': ctx.author.discriminator
                }

                result['subscribed_users'][str(ctx.author.id)] = {
                    'date'   : str(date.today()),
                    'user'   : ctx.author.name,
                    'discriminator': ctx.author.discriminator
                }

                print(result)

                status = await ctx.bot.unOrdinaryCollection.replace_one({'_id': ctx.guild.id}, result)

                await ctx.send(f'Replaced {status.modified_count} document.')
                await ctx.send(f'Successfully subscribed to unOrdinary updates. <@{ctx.author.id}>')
    


    @unOrdinary.command(aliases=['unsub', 'Unsub', 'Unsubscribe'])
    async def unsubscribe(self, ctx: commands.Context):
        '''Unsubscribe from unOrdinary updates'''

        result = await ctx.bot.unOrdinaryCollection.find_one({'_id': ctx.guild.id})

        if result is not None:

            try:
                del result['subscribed_users'][str(ctx.author.id)]
                #print(result)

                status = await ctx.bot.unOrdinaryCollection.replace_one({'_id': ctx.guild.id}, result)

                await ctx.send(f'Replaced {status.modified_count} document.')
                await ctx.send(f'Successfully unsubscribed from One Piece updates. <@{ctx.author.id}>')

            except KeyError:
                await ctx.send(f'You were never subscribed to begin with. <@{ctx.author.id}>')
                return
        
        else:
            return
    


    #allow only mods and owner to run this command by creating a custom check 
    @commands.check(lambda ctx: True if ctx.author.id == 526814235779399710 or commands.has_permissions(manage_channels=True) else False)
    @unOrdinary.command(aliases=['set'])
    async def set_channel(self, ctx: commands.Context, inputTextChannel:str):
        '''
        Set an channel where bot will post the updates. 
        Only users with manage_channels permission or admins can do this.
        If channel is already assigned it would be over written with the new one.
        '''

        try:
            textChannel = await helpers.textchannel_by_substring(ctx, inputTextChannel)

            result = await ctx.bot.unOrdinaryCollection.find_one({'_id': ctx.guild.id})

            #Record for guild doesn't exist. Make a record, assign a channel and add to db
            if result is None:  
                document = {
                    '_id'    : ctx.guild.id,
                    'guild'  : ctx.guild.name,
                    'assigned_channel' : textChannel.id,
                    'post_updates' : True,
                    'subscribed_users': {}         
                }
                result = await ctx.bot.unOrdinaryCollection.insert_one(document)
                await ctx.send(f'result: {result.inserted_id}')
            
            #record for guild exists just add assigned_channel
            else:
                result['assigned_channel'] = textChannel.id
                status = await ctx.bot.unOrdinaryCollection.replace_one({'_id': ctx.guild.id}, result)
                await ctx.send(f'Replaced {status.modified_count} document.')

            await ctx.send(f'Channel **`{textChannel}`** found. Updates will be posted on that channel.')


        except commands.BadArgument:
            await ctx.send(f"No text channel **`{inputTextChannel}`** found. Try again!")
        
    

    @commands.check(lambda ctx: True if ctx.author.id == 526814235779399710 or commands.has_permissions(manage_channels=True) else False)
    @unOrdinary.command()
    async def stop(self, ctx: commands.Context):
        '''
        Stop receiving unOrdinary updates even if users are subscribed.
        Only users with manage_channels permission or admins can do this
        '''

        result = await ctx.bot.unOrdinaryCollection.find_one({'_id': ctx.guild.id})

        if result is not None:
            if result['post_updates'] == False:
                await ctx.send('unOrdinary updates have already been stopped in this guild. Nothing to do.')
            else:
                result['post_updates'] = False
                status = await ctx.bot.unOrdinaryCollection.replace_one({'_id': ctx.guild.id}, result)
                await ctx.send(f'Replaced {status.modified_count} document.')
                await ctx.send('Successfully stopped bot from posting unOrdinary updates in this guild.')

        else:
            await ctx.send("No one in this guild is subscribed to unOrdinary updates. \nGuild is already not receiving any updates.")



    @commands.check(lambda ctx: True if ctx.author.id == 526814235779399710 or commands.has_permissions(manage_channels=True) else False)
    @unOrdinary.command()
    async def start(self, ctx: commands.Context):
        '''
        Start receiving unOrdinary updates in the guild.
        Only users with manage_channels permission or admins can do this.
        Even if you start the updates and no users are subscribed, no updates will be posted.
        Only use this if you stopped updates previously and wanna resume them.
        '''

        result = await ctx.bot.unOrdinaryCollection.find_one({'_id': ctx.guild.id})

        if result is not None:
            if result['post_updates'] == True:
                await ctx.send('unOrdinary updates are already enabled in this guild. Nothing to do.')
            else:
                result['post_updates'] = True
                status = await ctx.bot.unOrdinaryCollection.replace_one({'_id': ctx.guild.id}, result)
                await ctx.send(f'Replaced {status.modified_count} document.')
                await ctx.send('This guild will now start receiving unOrdinary updates on assigned channel.')

        else:
            document = {
                '_id'    : ctx.guild.id,
                'guild'  : ctx.guild.name,
                'assigned_channel' : None,
                'post_updates' : True,
                'subscribed_users': {}         
            }
            result = await ctx.bot.unOrdinaryCollection.insert_one(document)
            await ctx.send(f'result: {result.inserted_id}')






def setup(bot):
    bot.add_cog(WebtoonsUpdates())


