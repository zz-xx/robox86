"""Helper functions for xxx bot"""

import asyncio
from random import choice

import discord
from discord.ext import commands


MEMBER_CONVERTER = commands.MemberConverter()
ROLE_CONVERTER = commands.RoleConverter()
USER_CONVERTER = commands.UserConverter()
TEXTCHANNEL_CONVERTER = commands.TextChannelConverter()


async def get_color():
    """Get a random hex color for use with embed. In case I forget this was taken from SO"""
    color = ''.join([choice('0123456789ABCDEF') for x in range(6)])
    color = int(color, 16)
    return color



async def get_parameters(raw_string: str):
    """Get parameters seperated by `|` by using string.split(). Returns list of parameters """ 
    parameters = raw_string.split('|')
    return parameters



async def make_request(ctx: commands.context, url: str, data=None, headers=None):
    """search and get results in json file or read page in html form"""

    try:
        async with ctx.bot.session.get(url, params=data, headers=headers) as response:
            if data and headers != None:
                json = await response.json()
                return json

            #note to me(if I forget): I wrote this to get page to scrape and get images
            page = await response.read()
            print(response.status)
            return page
    
    except Exception as error:
        print(f'Something went wrong, {error}')
#add exception handling to above methods



#note to me(if I forget): check documentation for `commands.CommandError`
#also check `converters` and how they are used with annotations
async def search_member(ctx: commands.context, member: str):
    """Check and return member(if they exist) by given name string"""

    try:
        return await MEMBER_CONVERTER.convert(ctx, member)
    except commands.CommandError:
        pass
    
    member = member.lower()
    for m in ctx.guild.members:
        if member in m.name.lower() or member in m.display_name.lower():
            return m
    
    raise commands.BadArgument(f"No user with `{member}` was found.")



async def role_by_substring(ctx: commands.Context, role: str):
    """Check and return role(if it exists) by given role string"""

    try:
        return await ROLE_CONVERTER.convert(ctx, role)
    except commands.CommandError:
        pass

    role = role.lower()
    for r in ctx.guild.roles:
        if role in r.name.lower():
            return r

    raise commands.BadArgument(f"No role with substring `{role}` was found.")



async def textchannel_by_substring(ctx: commands.Context, textchannel: str):
    """Check and return text channel(if it exists) by given text string"""

    try:
        return await TEXTCHANNEL_CONVERTER.convert(ctx, textchannel)
    except commands.CommandError:
        pass

    textchannel = textchannel.lower()
    for t in ctx.guild.text_channels:
        if textchannel in t.name.lower():
            return t

    raise commands.BadArgument(f"No text channel with substring **`{textchannel}`** was found.")



async def yes_or_no(ctx: commands.Context,  
                    message: str="Are you sure? Type **yes** within 10 seconds to confirm. o.o"):

    """Helper for asking `yes`/`no` to user to confirm choice."""

    await ctx.send(message)

    try:
        message = ctx.bot.wait_for("message", timeout=10,
                                   check = lambda message: message.author == ctx.message.author)
        
    except asyncio.TimeoutError:
        await ctx.send("I got tired, waiting for you!")
        return False
    
    if message.clean_content.lower() not in ['yes','no']:
        await ctx.send("You did not answer me in **yes/no**")
        return False
    
    return True
        


async def search_user(ctx: commands.context, user:str):
    "Check and return user(if they exist) by given string"

    return await USER_CONVERTER.convert(user, ctx)
    



