import discord

from mochuh import bot


async def check_achievement(connection, discord_id: int, message_count: int, message):
    if message_count >= 2000:
        existing_achievement_spacemaker = await connection.fetchval("SELECT COUNT(*) "
                                                         "FROM achievements "
                                                         "WHERE discord_id = $1 "
                                                         "AND achievement_name = 'Спейсователь'", discord_id)

        if existing_achievement_spacemaker == 0:
            await connection.execute("INSERT INTO achievements (discord_id, achievement_name) "
                                     "VALUES ($1, 'Спейсователь')", discord_id)
            user = bot.get_user(discord_id)
            channel = bot.get_channel(1034698950369874010)
            await channel.send(f"{user.mention} получил ачивку «Спейсователь» за 2000 сообщений на сервере!")

    if 'получка' in message.content.lower():
        existing_achievement_poluchka = await connection.fetchval("SELECT COUNT(*) "
                                                                    "FROM achievements "
                                                                    "WHERE discord_id = $1 "
                                                                    "AND achievement_name = 'Прадед'", discord_id)

        if existing_achievement_poluchka == 0:
            await connection.execute("INSERT INTO achievements (discord_id, achievement_name) "
                                     "VALUES ($1, 'Прадед')", discord_id)
            user = bot.get_user(discord_id)
            channel = bot.get_channel(1034698950369874010)
            await channel.send(f"{user.mention} получил ачивку «Прадед»")
