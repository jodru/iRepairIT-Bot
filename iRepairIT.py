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
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token  = os.getenv("TWILIO_AUTH_TOKEN")
phone = os.getenv("TWILIO_PHONE")

client = Client(account_sid, auth_token)
 
     
class RegComs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
  
    @commands.command()
    async def address(self, ctx, location : str, *, num=''):
    
        """Sends a text to the number given. Example: !text B 1234567890 sends Buckhead info to that number."""
        
        #Gets the letter location
        where = location[-1]
        
        buc = "Thank you for calling iRepairIT, per your request, here is our address:\n\n324 Pharr Road NE, Atlanta, GA 30305\n\nWe are located across the street from the Chevron gas station, in the all white shopping center.\n\nQuestions? Call us at 678-650-2822\n\nThis message is AUTOMATED. Replies are not received."
        mid = "Thank you for calling iRepairIT, per your request, here is our address:\n\n1715 Howell Mill Rd NW, Suite C8-A, Atlanta, GA 30318\n\nWe are located in the Kroger shopping center, 4 doors to the right of Kroger.\n\nQuestions? Call us at 404-889-7993\n\nThis message is AUTOMATED. Replies are not received."
        smy = "Thank you for calling iRepairIT, per your request, here is our address:\n\n2517 Spring Road SE, Suite 102, Smyrna, GA 30080\n\nWe are located across the street from RaceTrac in the same plaza as Taco Cantina. \n\nQuestions? Call us at 678-575-1808\n\nThis message is AUTOMATED. Replies are not received."
        aloc = "Thank you for calling iRepairIT, per your request, here are all our addresses:\n\nSmyrna\n2517 Spring Road SE, Suite 102, Smyrna, GA 30080\n\nBuckhead\n324 Pharr Road NE, Atlanta, GA 30305\n\nMidtown\n1715 Howell Mill Road NW, Suite C8-A, Atlanta, GA 30318\n\nThis message is AUTOMATED. Replies are not received."
        
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
                raise ValueError('Wrong letter.')
    
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
