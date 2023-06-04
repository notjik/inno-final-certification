from aiogram import Bot, types


async def set_starting_commands(bot: Bot, chat_id: int):
    commands = {
        'ru': [
            types.BotCommand('start', 'Начать диалог'),
            types.BotCommand('help', 'Помощь по боту'),
        ],
        'en': [
            types.BotCommand('start', 'Start a dialogue'),
            types.BotCommand('help', 'Help on the bot'),
        ]
    }
    for lang, comm in commands.items():
        await bot.set_my_commands(
            commands=comm,
            scope=types.BotCommandScopeChat(chat_id),
            language_code=lang
        )
