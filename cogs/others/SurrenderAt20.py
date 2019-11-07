from discord.ext import commands 
from x86 import helpers

class SurrenderAt20:
    """commands associated with managing surrenderAt20 task"""



    def __init__(self, bot):
        self.bot = bot
    


    @commands.command(aliases=['get_surrender_at_20_updates'])
    async def get_s20_up(self, ctx, channel_name:str):
        """
        Usage       : get_s20_up [channel_name]
        Description : Type a correct channel name to subscribe to surrender at 20 updates.
        """

        try:
            textChannel = await helpers.textchannel_by_substring(ctx, channel_name)

            channelDetails = {
                'ChannelId': textChannel.id,
                'GuildId: ': ctx.guild.id,
            }

            result = await self.bot.db.sat20Subs.insert_one(channelDetails)
            print(f'Result id: {result.inserted_id}')

        except Exception as error:
            print(error)



def setup(bot):
    bot.add_cog(SurrenderAt20(bot))

        
