from aiogram.types.inline_keyboard import InlineKeyboardButton,InlineKeyboardMarkup

check_type=InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("1x",callback_data="1x"),
        InlineKeyboardButton("2x",callback_data="2x")]
    ]
)

def boards_kb(k):
    key=InlineKeyboardMarkup(row_width=3)
    boards=[]
    for i in range(9):
        boards.append(InlineKeyboardButton(k[i],callback_data=i))
    boards.append(InlineKeyboardButton("Restart",callback_data="restart"))
    key.add(*boards)
    return key