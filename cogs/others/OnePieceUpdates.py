import json
from datetime import date

import discord
from discord.ext import commands

from x86 import helpers




'''
def check_if_its_owner_or_mod():

        #although correct no need for this
        #just copied my id manually  
        #app_info = await ctx.bot.application_info()
        #owner = f'<@{app_info.owner.id}>'

        def predicate(ctx):
            if ctx.author.id == 526814235779399710 or commands.has_permissions(kick_members=True):
                return True
        
        return commands.check(predicate)
'''




class OnePieceUpdates:
    '''Reminds you when spoilers and new chapter of OnePiece is out'''



    @commands.group(aliases=['onepiece', 'onePiece', 'Onepiece', 'op', 'Op', 'oP', 'OP'])
    async def OnePiece(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send(f"You must specify a subcommand. <@{ctx.author.id}>")



    #@commands.command(aliases=['op_subscribe', 'sub_op', 'ops'])
    @OnePiece.command(aliases=['Subscribe', 'sub', 'Sub'])
    async def subscribe(self, ctx: commands.Context):
        '''Subscribe to One Piece Manga updates'''

        docCount = await ctx.bot.onePieceCollection.count_documents({})

        #this will only be run once when collection is initialized first time
        #no chance users will ever run into this condition
        if docCount == 0:
            await ctx.send('Empty Collection')
            
            #id 1 is being reserved for metadata like current chap no, no of users, etc
            tempDoc = {'_id': 1}
            result = await ctx.bot.onePieceCollection.insert_one(tempDoc)
            await ctx.send(f'result = {result}')

            #after adding id 1 document add user and guild
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

            result = await ctx.bot.onePieceCollection.insert_one(document)
            await ctx.send(f'result: {result.inserted_id}')
            await ctx.send(f'Successfully subscribed to One Piece updates. <@{ctx.author.id}>')

        
        else:
            await ctx.send('Collection not empty anymore.')

            #find if document for guild already exists
            result = await ctx.bot.onePieceCollection.find_one({'_id': ctx.guild.id})
            #print(result)

            #record for guild doesn't exists add it to db
            #Assigned channel is none by default. It can be assigned by user with
            #'manage_channels' permission
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

                result = await ctx.bot.onePieceCollection.insert_one(document)
                await ctx.send(f'result: {result.inserted_id}')
                await ctx.send(f'Successfully subscribed to One Piece updates. <@{ctx.author.id}>')

            else:
                #Record for guild exists. Only user needs to be added to collection.

                #check if user is already subscribed or not
                #could have entirely skipped this because dictionary don't allows repeat keys anyway
                #doing it for sake of interface
                #print(result)
                subscribedUsers = result['subscribed_users']
                #print(subscribedUsers)
                #print(list(subscribedUsers))
                for userId in list(subscribedUsers):

                    if int(userId) == ctx.author.id:
                        await ctx.send(f"You're already subscribed. <@{ctx.author.id}>")
                        return
                
                #User is not subscribed. Add them to list.
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

                status = await ctx.bot.onePieceCollection.replace_one({'_id': ctx.guild.id}, result)

                await ctx.send(f'Replaced {status.modified_count} document.')
                await ctx.send(f'Successfully subscribed to One Piece updates. <@{ctx.author.id}>')



    #@commands.command(aliases=['op_unsubscribe', 'unsub_op', 'opuns'])
    @OnePiece.command(aliases=['unsub', 'Unsub', 'Unsubscribe'])
    async def unsubscribe(self, ctx: commands.Context):
        '''Unsubscribe from One Piece Manga updates'''

        result = await ctx.bot.onePieceCollection.find_one({'_id': ctx.guild.id})

        if result is not None:

            try:
                del result['subscribed_users'][str(ctx.author.id)]
                #print(result)

                status = await ctx.bot.onePieceCollection.replace_one({'_id': ctx.guild.id}, result)

                await ctx.send(f'Replaced {status.modified_count} document.')
                await ctx.send(f'Successfully unsubscribed from One Piece updates. <@{ctx.author.id}>')

            except KeyError:
                await ctx.send(f'You were never subscribed to begin with. <@{ctx.author.id}>')
                return
        
        else:
            return



    '''
    @commands.has_permissions(kick_members=True)
    @commands.is_owner()
    @commands.check(check_if_its_owner_or_mod)
    @check_if_its_owner_or_mod()
    '''


    #allow only mods and owner to run this command by creating a custom check 
    @commands.check(lambda ctx: True if ctx.author.id == 526814235779399710 or commands.has_permissions(manage_channels=True) else False)
    @OnePiece.command(aliases=['set'])
    async def set_channel(self, ctx: commands.Context, inputTextChannel:str):
        '''
        Set an channel where bot will post the updates. 
        Only users with manage_channels permission or admins can do this.
        If channel is already assigned it would be over written with the new one.
        '''
        #await ctx.send('You are owner or a mod.')


        try:
            textChannel = await helpers.textchannel_by_substring(ctx, inputTextChannel)

            result = await ctx.bot.onePieceCollection.find_one({'_id': ctx.guild.id})

            #Record for guild doesn't exist. Make a record, assign a channel and add to db
            if result is None:  
                document = {
                    '_id'    : ctx.guild.id,
                    'guild'  : ctx.guild.name,
                    'assigned_channel' : textChannel.id,
                    'post_updates' : True,
                    'subscribed_users': {}         
                }
                result = await ctx.bot.onePieceCollection.insert_one(document)
                await ctx.send(f'result: {result.inserted_id}')
            
            #record for guild exists just add assigned_channel
            else:
                result['assigned_channel'] = textChannel.id
                status = await ctx.bot.onePieceCollection.replace_one({'_id': ctx.guild.id}, result)
                await ctx.send(f'Replaced {status.modified_count} document.')

            await ctx.send(f'Channel **`{textChannel}`** found. Updates will be posted on that channel.')


        except commands.BadArgument:
            await ctx.send(f"No text channel **`{inputTextChannel}`** found. Try again!")



    @commands.check(lambda ctx: True if ctx.author.id == 526814235779399710 or commands.has_permissions(manage_channels=True) else False)
    @OnePiece.command()
    async def stop(self, ctx: commands.Context):
        '''
        Stop receiving One Piece updates even if users are subscribed.
        Only users with manage_channels permission or admins can do this
        '''

        result = await ctx.bot.onePieceCollection.find_one({'_id': ctx.guild.id})

        if result is not None:
            if result['post_updates'] == False:
                await ctx.send('One Piece updates have already been stopped in this guild. Nothing to do.')
            else:
                result['post_updates'] = False
                status = await ctx.bot.onePieceCollection.replace_one({'_id': ctx.guild.id}, result)
                await ctx.send(f'Replaced {status.modified_count} document.')
                await ctx.send('Successfully stopped bot from posting One Piece updates in this guild.')

        else:
            await ctx.send("No one in this guild is subscribed to One Piece updates. \nGuild is already not receiving any updates.")



    @commands.check(lambda ctx: True if ctx.author.id == 526814235779399710 or commands.has_permissions(manage_channels=True) else False)
    @OnePiece.command()
    async def start(self, ctx: commands.Context):
        '''
        Start receiving One Piece updates in the guild.
        Only users with manage_channels permission or admins can do this.
        Even if you start the updates and no users are subscribed, no updates will be posted.
        Only use this if you stopped updates previously and wanna resume them.
        '''

        result = await ctx.bot.onePieceCollection.find_one({'_id': ctx.guild.id})

        if result is not None:
            if result['post_updates'] == True:
                await ctx.send('One Piece updates are already enabled in this guild. Nothing to do.')
            else:
                result['post_updates'] = True
                status = await ctx.bot.onePieceCollection.replace_one({'_id': ctx.guild.id}, result)
                await ctx.send(f'Replaced {status.modified_count} document.')
                await ctx.send('This guild will now start receiving One Piece updates on assigned channel.')

        else:
            document = {
                '_id'    : ctx.guild.id,
                'guild'  : ctx.guild.name,
                'assigned_channel' : None,
                'post_updates' : True,
                'subscribed_users': {}         
            }
            result = await ctx.bot.onePieceCollection.insert_one(document)
            await ctx.send(f'result: {result.inserted_id}')



    #This doesn't belong here. Just wrote this to test new library function.
    @commands.command(aliases=['on_mobile'])
    async def is_on_mobile(self, ctx: commands.Context, inputUser: str):
        '''Check if member is on mobile'''

        try:
            user = await helpers.search_member(ctx, inputUser)
            
            if user.is_on_mobile():
                await ctx.send(f'{user.name} is on mobile.')
            else:
                await ctx.send(f'{user.name} is not on mobile.')


        except commands.BadArgument:
            await ctx.send('No such user was found.')



def setup(bot):
    bot.add_cog(OnePieceUpdates())