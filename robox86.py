import os
import logging

import discord
from discord.ext import commands

import x86
from x86 import core


BOT = test_core.Bot(command_prefix="", pm_help=None, config_file="config.json")


if __name__ == "__main__":

    BOT.load_config(f'{os.getcwd()}\\config.json')

    BOT.description = BOT.config.get("description","Description Unavailable!")

    prefix = BOT.config.get("prefix","x")

    #possible failsafe lol
    prefixes = [f"{prefix} ", f"{prefix} ".capitalize(), prefix, prefix.capitalize()]

    BOT.command_prefix = commands.when_mentioned_or(*prefixes)

    
    #load all the cogs listed in config file
    for dirpath, dirnames, filenames in os.walk("cogs"):
        for filename in filenames:
            if filename.endswith('.py'):
                fullpath = os.path.join(dirpath, filename).split(os.path.sep)
                module = ".".join(fullpath)[:-3]
                print(module)

                try:
                    BOT.load_extension(module)
                except Exception as error:
                    print(f"Unable to load {module}: {error}")
    
    #add databse handling code
    #add logging support
            
    BOT.run(BOT.config["discord_token"])
    


