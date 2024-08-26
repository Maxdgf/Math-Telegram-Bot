from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

TOKEN = "bot token" #your bot api token

class Robot(StatesGroup):
    input_data = State()

bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(commands=['start'])
async def start_message(message:types.message):
    chat_id = message.chat.id
    await Robot.input_data.set()
    await bot.send_message(chat_id, text="Hello! I am math bot. Send me math example and i solve it!", parse_mode="Markdown")

def math_solve(expression):
    expression = expression.replace('×', '*').replace(':', '/').replace('÷', '/').replace('x', '*')
    try:
        return eval(expression)
    except:
        return "I cant solve it :("
        #print("Error")

@dp.message_handler(state=Robot.input_data)
async def math_solves(message: types.Message, state: FSMContext):
    example = message.text
    try:
        result = math_solve(example)
        await message.reply(f"Answer: {result}" + "\n" + "Solved: @MathSolvesCalculationBot")
    except:
        await message.reply("I cant solve it :(")
        #print("Error")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
