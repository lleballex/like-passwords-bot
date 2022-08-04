from aiogram import executor

import sys
from pathlib import Path
from dotenv import load_dotenv


if __name__ == '__main__':
    load_dotenv(Path(__file__).resolve().parent.parent / '.env')

    if len(sys.argv) == 1:
        import handlers
        from misc import dp

        executor.start_polling(dp, skip_updates=True)
    elif sys.argv[1] == 'migrate':
        from misc import db
        from models import User, Password

        db.create_tables([User, Password])

        print('Successfully migrated')
