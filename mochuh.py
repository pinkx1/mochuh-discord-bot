import aiohttp
import logging
import random
import os
import discord
from discord.ext import commands
from discord_slash import SlashCommand
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('token')

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)



# To avoid logging such messages like:
# discord.ext.commands.errors.CommandNotFound: Command + is not found
# We use command_prefix as '!'.
# In addition to this one we would not log such events even for the commands like: ping
# In case if the ping command does not exist.
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error



@bot.event
async def on_ready():
    print('bot connected')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('жижу 2'))



@commands.has_permissions(administrator=True)
@bot.command()
async def say(ctx, *, arg):
    await ctx.channel.purge(limit = 1)
    await ctx.send(arg)



@slash.slash(description="Лобби SiGame")
async def sigame(ctx):
    await ctx.send('Программа на пк: <https://vladimirkhil.com/si/game>\n'
                                    'Онлайн: <https://vladimirkhil.com/si/online/>\n'
                                    'Название лобби: gay123\n'
                                    'Пароль: 1099\n',
                                    file=discord.File('./sigame.png'))



@slash.slash(description="Бросить монетку")
async def coinflip(ctx):
    await ctx.send(random.choice(['Орел', 'Решка']))



@bot.event
async def on_member_join(member):
    channel = bot.get_channel(973593062045548636)  # channel_id of the channel you want the message to be displayed
    await channel.send(f"{member.mention} проскальзывает на сервер! Ласкаво просимо!")


@bot.event
async def on_message(message):
    # Skip reaction to bot's messages
    if message.author == bot.user:
        return
    
    if message.content.lower() in ( "да", "дa"):
        await message.channel.send(content='пизда')
    
    if message.content.lower() == "нет":
        await message.channel.send(content='пидора ответ')


    await bot.process_commands(message)


bot.run(token)
