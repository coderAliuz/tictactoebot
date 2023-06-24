from aiogram.types import Message,CallbackQuery
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from tgbot.keyboards import check_type,boards_kb
from .check import is_winner,get_best_move
import asyncio
import random
async def computer_game(call:CallbackQuery,state:FSMContext):
    boards=['-']*9
    await call.message.edit_text("X - 🤵 Player\nO - 🤖 Computer")
    await call.message.answer("🤵 Turn X",reply_markup=boards_kb(boards))
    await state.update_data(boards=boards,turn="X")
    await state.set_state("check_state_1")


async def check_boards_1(call:CallbackQuery,state:FSMContext):
    data=int(call.data)
    data_state=await state.get_data()
    boards=data_state['boards']
    if boards[data]=="-":
        await state.set_state("other")
        boards[data]=data_state["turn"]

        turn="X"
        if is_winner(board=boards,player=turn):
            await call.message.edit_text(f'🤵 Win {turn} 🏆',reply_markup=boards_kb(boards))
            await call.answer(f'🤵 Win {turn} 🏆')
            await state.set_state("restart_1")

        elif "-" not in boards:
            await call.message.edit_text(f"TIE 🤝",reply_markup=boards_kb(boards))
            await call.answer(f'TIE 🤝')
            await state.set_state("restart_1")
            
        else:
            turn="O"
            await call.message.edit_text(f"🤖 Turn {turn}",reply_markup=boards_kb(boards))
            await asyncio.sleep(2)
            boards[get_best_move(boards)]=turn
            await state.update_data(boards=boards,turn=turn)
            if is_winner(board=boards,player=turn):
                await call.message.edit_text(f'🤖 Win {turn} 🏆',reply_markup=boards_kb(boards))
                await call.answer(f'🤖 Win {turn} 🏆')
                await state.set_state("restart_1")

            elif "-" not in boards:
                await call.message.eddit_text(f"TIE",reply_markup=boards_kb(boards))
                await call.answer(f'TIE 🤝')
                await state.set_state("restart_1")
            else:
                turn="X"
                await state.update_data(boards=boards,turn=turn)
                await call.message.edit_text(f"🤵 Turn {turn}",reply_markup=boards_kb(boards))
                await state.set_state("check_state_1")
    else:
        await call.answer("Can't click ❗️")

async def restart_game(call:CallbackQuery,state:FSMContext):
    data_state=await state.get_data()
    boards=['-']*9
    turn=data_state["turn"]
    if call.data=="restart":
        if turn=="O":
            boards[random.randint(0,8)]="O"
        await call.message.edit_text(f"Turn {turn}",reply_markup=boards_kb(boards))
        await state.update_data(boards=boards,turn="X")
        await state.set_state("check_state_1")
    else:
        await call.answer("Click restart 🔄")
def game_register_1(dp:Dispatcher):
    dp.register_callback_query_handler(computer_game,text="1x",state="game_state")
    dp.register_callback_query_handler(check_boards_1,text=list(range(9)),state="check_state_1")
    dp.register_callback_query_handler(restart_game,text=["restart"]+list(range(9)),state=["check_state_1","restart_1"])