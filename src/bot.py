from aiogram import executor

from pathlib import Path
from dotenv import load_dotenv


if __name__ == '__main__':
	load_dotenv(Path().resolve().parent / '.env')

	import handlers
	from misc import dp

	executor.start_polling(dp, skip_updates=True)