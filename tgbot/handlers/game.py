from aiogram.types import Message
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from tgbot.keyboards import check_type

async def started(message:Message,state:FSMContext):
    await message.answer(f"🖐 Hello {message.chat.full_name}\n"
                         f"/game - start game\n/help - help!")
    await state.finish()

async def start_game(message:Message,state:FSMContext):
    await state.finish()
    await message.answer(f"Choose a game type.\n"
                         f"1x-play with the computer\n2x-play with your friend",reply_markup=check_type)
    await state.set_state("game_state")

async def helped(message:Message):
    await message.answer("💡 With this bot you can play 🎲 tictactoe with 🤖 AI or your 🤵 friend.\n❕ The ability to play remotely with a friend will be added soon.\n\n👨‍💻 Coder: @coder_ali")

def game_register(dp:Dispatcher):
    dp.register_message_handler(started,commands="start",state="*")
    dp.register_message_handler(start_game,commands="game",state="*")
    dp.register_message_handler(helped,commands="help",state="*")