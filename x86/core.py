""" This is custom bot class """

import json

import aiohttp
from discord.ext import commands
import motor.motor_asyncio



#check discord.py rewrite documentation for why AutoShardedBot was used.
class Bot(commands.AutoShardedBot):

    """ 
    This is a custom object which extends default commands.Bot class and provides
    a configuration handler and a common aiohttp ClientSession.
    """ 


    def __init__(self, *args, **kwargs):
        """`config_file`: A string representing name of .json file which contains 
        configurations for bot. Can be anything but will default to `config.json`

        Instance variables:

        `session` - An `aiohttp.ClientSession` used for performing API hooks.
        `config` - A `dictionary` containing key value pairs represnting bot configs.
        """

        #pass arguments to constructor of parent class
        super().__init__(*args, **kwargs)
        self.config = {}

        #in case I ever forget why kwargs.get method is used(god help me), just google it
        self.config_file = kwargs.get("config_file","config.json")

        #also apparently you can do Bot.loop, did not knew this.
        self.session = aiohttp.ClientSession(loop = self.loop)

        #create mongoDB client. MongoDB database server must be running in background
        self.DBClient = motor.motor_asyncio.AsyncIOMotorClient()

        #create Bot databsase
        self.db = self.DBClient.RoboX86

        #get settings of all of which bot is part. it's basically a collection
        #self.guildSettings = self.db.guilds

        #get collection containing details of all users subscribed to one piece updates
        self.onePieceCollection = self.db.onePieceCollection

        #get collection containing details of all users subscribed to unOrdinary updates
        self.unOrdinaryCollection = self.db.unOrdinaryCollection
    
    

    def load_config(self, filename: str=None):
        """
        Load congig from a .JSON file. If not specified will default to 
        `Bot.config_file`.
        """

        if not filename:
            filename = self.config_file

        #pro tip: google difference between json `load,dump` and `loads,dumps`.
        with open(filename) as file_object:
            config = json.load(file_object)
        
        #also google `isinstance` vs `type`. Hint: `isinstance` is better.
        if isinstance(config,dict):
            for key,value in config.items():
                self.config[key] = value

    

    def save_config(self, filename:str=None):
        """save config to a .JSON file. Defaults to `Bot.config_file`."""

        if not filename:
            filename = self.config_file

        with open(filename,'w') as file_object:
            json.dump(self.config_file, file_object, indent=4, sort_keys=True)
    


    #add database connection..

