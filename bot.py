import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    FSInputFile, InputMediaPhoto
)

TOKEN = os.environ.get("BOT_TOKEN")

if not TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден!")

bot = Bot(token=TOKEN)
dp = Dispatcher()

models = ["R32", "R33", "R34", "R35"]
compare_state = {}

car_photos = {
    "R32": "r32.jpg",
    "R33": "r33.jpg",
    "R34": "r34.jpg",
    "R35": "r35.jpg",
    "menu": "gtr.jpg"
}

# --- УМНОЕ РЕДАКТИРОВАНИЕ ---
async def smart_edit(message, text, reply_markup):
    try:
        if message.photo:
            await message.edit_caption(caption=text, reply_markup=reply_markup)
        else:
            await message.edit_text(text=text, reply_markup=reply_markup)
    except:
        await message.answer(text, reply_markup=reply_markup)

# --- ИСТОРИЯ ---
history = {
    "R32": "🏎 R32 GT-R\n29 побед подряд, Godzilla, RB26DETT",
    "R33": "🏎 R33 GT-R\n<8 мин Nürburgring, стабильность",
    "R34": "🏎 R34 GT-R\nJDM икона, телеметрия",
    "R35": "🏎 R35 GT-R\nсуперкар, Takumi, VR38DETT"
}

# --- ХАРАКТЕРИСТИКИ ---
specs = {
    "R32": {"text": "R32\n280+ л.с.\n0-100: 5.5 сек"},
    "R33": {"text": "R33\n280 л.с.\n0-100: 5.4 сек"},
    "R34": {"text": "R34\n280 л.с.\n0-100: 4.9 сек"},
    "R35": {"text": "R35\n480+ л.с.\n0-100: ~3 сек"}
}

# --- ФАКТЫ ---
car_facts = {
    "R32": ["29 побед подряд", "Godzilla", "1000+ л.с."],
    "R33": ["<8 мин Nürburgring", "стабильность", "ATTESA"],
    "R34": ["Fast & Furious", "телеметрия", "JDM легенда"],
    "R35": ["Takumi сборка", "суперкар", "очень быстрый"]
}

# --- МЕНЮ ---
def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚗 Машины", callback_data="cars")],
        [InlineKeyboardButton(text="⚖️ Сравнение", callback_data="compare")]
    ])

def car_menu(index):
    model = models[index]
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️", callback_data=f"car_{index-1}"),
            InlineKeyboardButton(text=model, callback_data="noop"),
            InlineKeyboardButton(text="➡️", callback_data=f"car_{index+1}")
        ],
        [
            InlineKeyboardButton(text="📜 История", callback_data=f"{model}_history"),
            InlineKeyboardButton(text="⚙️ Характеристики", callback_data=f"{model}_specs")
        ],
        [
            InlineKeyboardButton(text="🔥 Факты", callback_data=f"{model}_facts")
        ],
        [
            InlineKeyboardButton(text="🏠 В меню", callback_data="back")
        ]
    ])

def facts_menu(model, index):
    facts = car_facts[model]
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️", callback_data=f"fact_{model}_{index-1}"),
            InlineKeyboardButton(text=f"{index+1}/{len(facts)}", callback_data="noop"),
            InlineKeyboardButton(text="➡️", callback_data=f"fact_{model}_{index+1}")
        ],
        [
            InlineKeyboardButton(text="⬅️ К машине", callback_data=f"car_{models.index(model)}")
        ],
        [
            InlineKeyboardButton(text="🏠 В меню", callback_data="back")
        ]
    ])

# --- СТАРТ ---
@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer_photo(
        FSInputFile(car_photos["menu"]),
        caption="🚀 Главное меню",
        reply_markup=main_menu()
    )

# --- CALLBACK ---
@dp.callback_query()
async def cb(callback: types.CallbackQuery):
    await callback.answer()
    data = callback.data

    if data == "back":
        await callback.message.edit_media(
            InputMediaPhoto(
                media=FSInputFile(car_photos["menu"]),
                caption="🚀 Главное меню"
            ),
            reply_markup=main_menu()
        )

    elif data == "cars":
        model = models[0]
        await callback.message.edit_media(
            InputMediaPhoto(media=FSInputFile(car_photos[model]), caption=f"🏎 {model}"),
            reply_markup=car_menu(0)
        )

    elif data.startswith("car_"):
        index = int(data.split("_")[1]) % len(models)
        model = models[index]
        await callback.message.edit_media(
            InputMediaPhoto(media=FSInputFile(car_photos[model]), caption=f"🏎 {model}"),
            reply_markup=car_menu(index)
        )

    elif "_history" in data:
        model = data.split("_")[0]
        await smart_edit(
            callback.message,
            history[model],
            InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ Назад", callback_data=f"car_{models.index(model)}")],
                [InlineKeyboardButton(text="🏠 В меню", callback_data="back")]
            ])
        )

    elif "_specs" in data:
        model = data.split("_")[0]
        await smart_edit(
            callback.message,
            specs[model]["text"],
            InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ Назад", callback_data=f"car_{models.index(model)}")],
                [InlineKeyboardButton(text="🏠 В меню", callback_data="back")]
            ])
        )

    elif "_facts" in data:
        model = data.split("_")[0]
        await smart_edit(callback.message, car_facts[model][0], facts_menu(model, 0))

    elif data.startswith("fact_"):
        _, model, index = data.split("_")
        index = int(index)
        facts = car_facts[model]

        if index < 0:
            index = len(facts) - 1
        elif index >= len(facts):
            index = 0

        await smart_edit(callback.message, facts[index], facts_menu(model, index))

    elif data == "compare":
        await smart_edit(
            callback.message,
            "⚖️ Выбери первую машину",
            InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=m, callback_data=f"c1_{m}") for m in models]
            ])
        )

    elif data.startswith("c1_"):
        m1 = data.split("_")[1]
        compare_state[callback.from_user.id] = m1

        await smart_edit(
            callback.message,
            f"Первая: {m1}\nВыбери вторую",
            InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=m, callback_data=f"c2_{m}") for m in models]
            ])
        )

    elif data.startswith("c2_"):
        m2 = data.split("_")[1]
        m1 = compare_state.get(callback.from_user.id)

        await smart_edit(
            callback.message,
            f"{m1} vs {m2}\n\n{specs[m1]['text']}\n\n🆚\n\n{specs[m2]['text']}",
            InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🏠 В меню", callback_data="back")]
            ])
        )

# --- ЗАПУСК ---
async def main():
    print("✅ Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
