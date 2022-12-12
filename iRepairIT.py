'''
@author: jodru

iRepairIT bot for various things.

"Forgot to clock out on break, should be an hour" - John
'''

import discord
from requests import get
from discord.ext import commands, tasks
import asyncio
from twilio.rest import Client
import logging
from dotenv import load_dotenv
import os

load_dotenv()

# Logging section
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

logChannel = {}
 
 
# Uses .env file to access account information
# test_account_sid = os.getenv("TEST_TWILIO_ACCOUNT_SID")
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
# test auth_token  = os.getenv("TEST_TWILIO_AUTH_TOKEN")
auth_token  = os.getenv("TWILIO_AUTH_TOKEN")
phone = os.getenv("TWILIO_PHONE")

client = Client(account_sid, auth_token)
 
     
class RegComs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def hellothere(self, ctx):
        """I hate commands like this but here you go."""
        #No seriously I really hate commands like this. Still my first command though so.
        await ctx.send("General Kenobi!")
        
    @commands.command()
    async def remind(self, ctx, time : str, *, message=''):
    
        """Adds a reminder to be sent after the specified time in secs, mins, hours, or days. Example: !remind 3h Message"""
        
        #Random command left over as an example from my own personal Discord bot.
        #It's shitty, I know, I also don't care enough to make it better.
        last = time[-1]
        thyme = time[:-1]
        thymeParse = int(thyme)
        segundo = 0
        try:
        
            if last == "s":
                segundo = thymeParse
            elif last == "m":
                segundo = thymeParse * 60
            elif last == "h":
                segundo = thymeParse * 60 * 60
            elif last == "d":
                segundo = thymeParse * 60 * 60 * 24
            else:
                raise ValueError('Wrong')
    
        except Exception:
            await ctx.send('Incorrect format. Try again idiot.')
            return
        await ctx.send("Reminder set in " + str(time) + ". The message is " + message)
        await asyncio.sleep(segundo)
        await ctx.send(f'Hi {ctx.message.author.mention}, you asked me to remind you about ' + message)
    
    @commands.command()
    async def address(self, ctx, location : str, *, num=''):
    
        """Sends a text to the number given. Example: !text B 1234567890 sends Buckhead info to that number."""
        
        #Gets the letter location
        where = location[-1]
        
        #TODO: Add strings for all options
        buc = os.getenv("BUC")
        mid = os.getenv("MID")
        smy = os.getenv("SMY")
        aloc = os.getenv("ALOC")
        
        #Append the US country code to the number, and declare an empty text message for the following try block.       
        actualNum = ''.join(('+1', num))
        textMessage = ""
        
        #Depending on the code, change the text message to the right string. If the code is invalid, tell the user.          
        try:
            if where == "B":
                textMessage = buc
            elif where == "M":
                textMessage = mid
            elif where == "S":
                textMessage = smy
            elif where == "A":
                textMessage = aloc
            else:
                raise ValueError('Someone was a dummy.')
    
        except Exception:
            await ctx.send('Make sure to use B, M, S, or A before typing the number.')
            return
        
        #Sends text from number. If there is an actual error, lets the user know the phone number is probably invalid.
        try: 
            text = client.messages.create(to=actualNum, from_= phone, body=textMessage)
            print(text.sid)
        
        except Exception:
            await ctx.send('Text not sent. Make sure the number you typed is valid.')
            return
        
        #React with thumbs up to let user know the text sent.
        await ctx.message.add_reaction('\U0001f44d')


TOKEN = os.getenv("DISCORD_TOKEN") 
description = '''Bot designed for iRepairIT.'''
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', description=description, intents= intents)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

async def main():
    async with bot:
        await bot.add_cog(RegComs(bot)) 
        await bot.start(TOKEN)

asyncio.run(main())
