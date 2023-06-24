from aiogram.types import Message,CallbackQuery
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from tgbot.keyboards import check_type,boards_kb
from .check import is_winner

async def freand_game(call:CallbackQuery,state:FSMContext):
    boards=['-']*9
    await call.message.edit_text("X - Player1\nO - Player2")
    await call.message.answer("🤵 Turn X",reply_markup=boards_kb(boards))
    await state.update_data(boards=boards,turn="X")
    await state.set_state("check_state")


async def check_boards(call:CallbackQuery,state:FSMContext):
    data=int(call.data)
    data_state=await state.get_data()
    boards=data_state['boards']

    if boards[data]=="-":
        boards[data]=data_state["turn"]
        if is_winner(board=boards,player=data_state["turn"]):
            await call.message.edit_text(f'🤵 Win {data_state["turn"]} 🏆',reply_markup=boards_kb(boards))
            await call.answer(f'🤵 Win {data_state["turn"]} 🏆')
            await state.set_state("restart")

        elif "-" not in boards:
            await call.message.edit_text(f"TIE 🤝",reply_markup=boards_kb(boards))
            await call.answer(f'TIE 🤝')
            await state.set_state("restart")
            
        else:
            turn="O" if data_state["turn"]=="X" else "X"
            await state.update_data(boards=boards,turn=turn)
            await call.message.edit_text(f"🤵 Turn {turn}",reply_markup=boards_kb(boards))
    else:
        await call.answer("Can't click ❗️")

async def restart_game(call:CallbackQuery,state:FSMContext):
    data_state=await state.get_data()
    boards=['-']*9
    turn=data_state["turn"]
    if call.data=="restart":
        await call.message.edit_text(f"🤵 Turn {turn}",reply_markup=boards_kb(boards))
        await state.update_data(boards=boards,turn=turn)
        await state.set_state("check_state")
    else:
        await call.answer("Click restart 🔄")
def game_register_2(dp:Dispatcher):
    
    dp.register_callback_query_handler(freand_game,text="2x",state="game_state")
    dp.register_callback_query_handler(check_boards,text=list(range(9)),state="check_state")
    dp.register_callback_query_handler(restart_game,text=["restart"]+list(range(9)),state=["check_state","restart"])