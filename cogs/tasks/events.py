import discord
from discord.ext import commands
#from discord.utils import get

class Events:


    def __init__(self, bot):
        self.bot = bot



    async def on_ready(self):
        "This event displays message when logged in as bot and change the status of bot"

        print("Logged in as {}".format(self.bot.user.name))
        print("with id {}".format(self.bot.user.id))
        print("------------")
        #await self.bot.change_presence(activity=discord.Game(name=' with your mom', url="https://www.twitch.tv/mailadmin", type=1))
        #await self.bot.change_presence(activity=discord.Streaming(name=' `.x help` with your mom ', url="https://www.twitch.tv/mailadmin"))
    


    async def on_message(self,message):
        "Greet users with following reply's on corresponding message events"

        if message.content.startswith('hello'): #or message.content.startswith('Hello'): 
            channel = message.channel
            user_id = str(message.author.id)
            await channel.send('Hello Ningen!  {mention}'.format(mention='<@'+user_id+'>'))
 
        
        if isinstance(message.channel, discord.DMChannel):
            if 'send nudes' in message.clean_content.lower():
                await message.author.send(f'<a:jerrydank:435178964005158912><a:jerrydank:435178964005158912>') #{message.author.mention!')
            """
            else:
                #know there is error here but couldn't solve it. 
                #it's here only because it still does what it's supposed to do
                try:
                    if message.author is not self.bot.user:
                        await message.author.send("Sorry, but I don't accept commands through direct messages! Please use the `#bots` channel of your corresponding server!")
                except discord.HTTPException as e:
                    print(f'Something went wrong {e.text}')
            """
                
        if self.bot.user.mentioned_in(message) and message.mention_everyone is False:
            await message.add_reaction('👀')
        
            
        #if this list goes any further, might have to implement some diff mechanism to keep this readable.
        if 'loli' in message.clean_content.lower():
            await message.add_reaction('🍭') 

        if 'instagram.com' in message.clean_content.lower():
            await message.add_reaction('💩') 

        if 'tan' in message.clean_content.lower():
            #this event is only supposed to happen in these servers..sort of joke
            try:
                if message.guild.id in [int(318353359197306880), int(404681481110290462)]:
                    emojis = self.bot.emojis
                    #print(message.guild.id)

                    for emoji in emojis:
                        if emoji.id == int(433627765288337409):
                            await message.add_reaction(emoji)
                            return

            except Exception as error:
                print(f'Something went wrong because {error}.')

            
        if 'fortnite' in message.clean_content.lower():
            emojis = self.bot.emojis
            #add helper for this
            for emoji in emojis:
                if emoji.id == int(399856865242120193):
                    await message.add_reaction(emoji)
                    return

        #await bot.process_commands(message)

    

    async def on_typing(self, channel, user, when):
        "If a user tries to start a DM with bot send the message below and delete it after 3 secs (Creepy I know)"

        if isinstance(channel, discord.DMChannel):
            if user.dm_channel == None:
                await user.create_dm()
            
            await user.dm_channel.send(f'I see you typing since `{when.time()} UTC` 👀', delete_after=3)
        
    

    async def on_command_error(self, ctx, error):

        #if isinstance(error, commands.BadArgument):

        print(error)


        # if command has local error handler, return
        if hasattr(ctx.command, 'on_command_error'):
            return

        
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('<a:jerrydank:435178964005158912><a:jerrydank:435178964005158912>', delete_after=3)
            await ctx.send(f"""**{str(error).replace('"','`')}!!**""", delete_after=3)
            return


        #this part is skimmed from example usage of on_command_error except fstring and author mention part
        if isinstance(error, commands.MissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            
            _message = f'You need the **{fmt}** permission(s) to use this command. <@{ctx.author.id}>'
            await ctx.send(_message)
            return
        

        #if user tries to invoke command without argument
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'You need to provide **`{error.param.name}`** while invoking this command.')

        

def setup(bot):
    bot.add_cog(Events(bot))
