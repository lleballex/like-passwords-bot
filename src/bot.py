from aiogram import executor

import sys
from pathlib import Path
from dotenv import load_dotenv


if __name__ == '__main__':
    load_dotenv(Path(__file__).resolve().parent.parent / '.env')

    if len(sys.argv) == 1:
        import handlers
        from misc import dp, bot
        from misc import USE_LONGPOLL, WEBHOOK_HOST, WEBHOOK_PATH
        from misc import WEBAPP_HOST, WEBAPP_PORT, SSL_CERTIFICATE

        if USE_LONGPOLL:
            executor.start_polling(dp, skip_updates=True)
        else:
            async def on_startup(_):
                if SSL_CERTIFICATE:
                    certificate=open(SSL_CERTIFICATE, 'rb')
                else:
                    certificate=None

                await bot.set_webhook(f'{WEBHOOK_HOST}{WEBHOOK_PATH}',
                                      certificate)

            async def on_shutdown(_):
                await bot.delete_webhook()

            executor.start_webhook(dp,
                                   WEBHOOK_PATH,
                                   on_startup=on_startup,
                                   on_shutdown=on_shutdown,
                                   skip_updates=True,
                                   host=WEBAPP_HOST,
                                   port=WEBAPP_PORT)

    elif sys.argv[1] == 'migrate':
        from misc import db
        from models import User, Password

        db.create_tables([User, Password])

        print('Successfully migrated')
