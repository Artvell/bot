from aiogram import executor
from bot.bot_class import dp,bot
from bot import handlers
import logging
async def on_shutdown(dp):
    logging.warning('Shutting down..')
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning('Bye!')

if __name__ == "__main__":
    executor.start_polling(
        dp,
        on_shutdown=on_shutdown,
        skip_updates=True
        )

