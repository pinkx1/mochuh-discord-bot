import random
import os
import discord
import requests
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


@bot.event
async def on_ready():
    Channel = bot.get_channel(1024728422724943893)
    Text= "тыкать сюда."
    Moji = await Channel.send(Text)
    await Moji.add_reaction('🏖')


@bot.event
async def on_reaction_add(reaction, user):
    Channel = bot.get_channel(1024728422724943893)
    if reaction.message.channel.id != Channel.id:
        return
    if reaction.emoji == "🏖":
      Role = discord.utils.get(user.guild.roles, name="🏖")
      await user.add_roles(Role)


@commands.has_permissions(administrator=True)
@bot.command()
async def bump(ctx):
    await ctx.channel.purge(limit = 1)
    import http.client
    import mimetypes
    from codecs import encode

    conn = http.client.HTTPSConnection("2ch.hk")
    cookie = os.getenv('cookie')
    boundary = os.getenv('boundary')
    usercode = os.getenv('usercode')
    
    dataList = []
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=task;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("post"))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=board;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("ch"))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=thread;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("216992"))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=usercode;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode(usercode))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=captcha_type;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("2chcaptcha"))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=formimages[];'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("(binary)"))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=comment;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("bump"))
    dataList.append(encode('--'+boundary+'--'))
    dataList.append(encode(''))
    body = b'\r\n'.join(dataList)
    payload = body
    headers = {
    'scheme': 'https',
    'path': '/user/posting?nc=1',
    'method': 'POST',
    'authority': '2ch.hk',
    'x-requested-with': 'XMLHttpRequest',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'referer': 'https://2ch.hk/ch/res/216992.html',
    'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
    'cookie': cookie,
    'origin': 'https://2ch.hk',
    'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
    }
    conn.request("POST", "/user/posting?nc=1", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))

    # pepeEZ = bot.get_emoji(1032917084906192977)
    # await ctx.send('Бампнул тредю ' + pepeEZ)
    # get(bot.get_all_emojis(), id='1032917084906192977')
    emoji = discord.utils.get(bot.emojis, name='EZ')
    await ctx.send(str(emoji))

bot.run(token)
