import os
import random
import discord
from dotenv import load_dotenv

from discord.ext import commands
from discord.enums import Enum

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='?')

class Button(Enum):
    YES = True
    NO = False

BUTTON_COL: dict[Button, discord.ButtonStyle] = {
    Button.YES: discord.ButtonStyle.primary,
    Button.NO: discord.ButtonStyle.danger,
}

yes = 0
no = 0
pollCreated = False
pollHolder = None

class UIButton(discord.ui.Button["Poll"]):
    def __init__ (self, button: Button):
        self.button = button
        super().__init__(style=BUTTON_COL[self.button], label = self.button.name)

    async def callback(self, interaction: discord.Interaction):
        await self.view.press(self.button)

class Poll(discord.ui.View):
    children: list[UIButton]

    
    def __init__(self):
        super().__init__()
        self.add_item(UIButton(Button.YES))
        self.add_item(UIButton(Button.NO))

        timeout=None
        
    async def press(self, button: Button):
        global yes
        global no
        if button.value:
            yes += 1
            print(f'Yes Has been pressed')
        else:
            no += 1

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name = "poll", help = 'Creates a poll')
async def poll_start(ctx, *,poll: str):
    global pollCreated
    global pollHolder
    if pollCreated:
        await ctx.send('Poll already in progress, cannot create another poll ?endPoll')
    else:
        channel = ctx.channel
        responce = poll
        pollCreated = True
        pollHolder = Poll()
        await ctx.send(responce, view = pollHolder)

@bot.command(name = "endPoll", help = "Ends the current Poll")
async def poll_end(ctx):
    global yes
    global no
    global pollCreated
    global pollHolder

    await ctx.send(f"Poll Results: YES {yes}, NO {no}")
    yes = 0
    no = 0
    pollCreated = False
    pollHolder.timeout = 0
    pollHolder = None
    
bot.run(TOKEN)