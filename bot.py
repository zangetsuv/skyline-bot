import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    FSInputFile, InputMediaPhoto
)

# --- 🔐 ТОКЕН ---
TOKEN = os.getenv("8285484329:AAGmSRXSeUvgqhDljq-TxOK6dSBx7p6FKPw")

if not TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден! Добавь его в Railway Variables")

bot = Bot(token=TOKEN)
dp = Dispatcher()

models = ["R32", "R33", "R34", "R35"]

# --- ФОТО ---
car_photos = {
    "R32": "r32.jpg",
    "R33": "r33.jpg",
    "R34": "r34.jpg",
    "R35": "r35.jpg"
}

# --- ИСТОРИЯ ---
history = {
    "R32": "🏎 R32 GT-R\n\nЛегендарная 'Godzilla'. Доминировала в JTCC.",
    "R33": "🏎 R33 GT-R\n\nСтабильность, Nürburgring < 8 минут.",
    "R34": "🏎 R34 GT-R\n\nИкона JDM и Fast & Furious.",
    "R35": "🏎 R35 GT-R\n\nСовременный суперкар."
}

# --- ХАРАКТЕРИСТИКИ ---
specs = {
    "R32": {"engine": "RB26DETT", "power": "280 л.с.", "0-100": "5.5 сек"},
    "R33": {"engine": "RB26DETT", "power": "280 л.с.", "0-100": "5.4 сек"},
    "R34": {"engine": "RB26DETT", "power": "280 л.с.", "0-100": "4.9 сек"},
    "R35": {"engine": "VR38DETT", "power": "480–600+ л.с.", "0-100": "2.7–3.5 сек"}
}

# --- ФАКТЫ ---
car_facts = {
    "R32": ["29 побед подряд", "Godzilla", "1000+ л.с. потенциал"],
    "R33": ["<8 мин Nürburgring", "ATTESA Pro", "самый стабильный"],
    "R34": ["Fast & Furious", "экран телеметрии", "JDM легенда"],
    "R35": ["ручная сборка", "конкурент Ferrari", "<3 сек разгон"]
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
            InlineKeyboardButton(text=f"{model} • {index+1}/{len(models)}", callback_data="noop"),
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
            InlineKeyboardButton(text="⬅️ Меню", callback_data="back")
        ]
    ])

def car_facts_menu(model, index):
    facts = car_facts[model]
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️", callback_data=f"carfact_{model}_{index-1}"),
            InlineKeyboardButton(text=f"{index+1}/{len(facts)}", callback_data="noop"),
            InlineKeyboardButton(text="➡️", callback_data=f"carfact_{model}_{index+1}")
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data=f"car_{models.index(model)}")
        ]
    ])

# --- СТАРТ ---
@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("🚀 Главное меню", reply_markup=main_menu())

# --- CALLBACK ---
@dp.callback_query()
async def cb(callback: types.CallbackQuery):
    await callback.answer()
    data = callback.data

    if data == "back":
        await callback.message.edit_text("🚀 Главное меню", reply_markup=main_menu())

    elif data == "cars":
        index = 0
        model = models[index]
        media = InputMediaPhoto(
            media=FSInputFile(car_photos[model]),
            caption=f"🏎 {model}"
        )
        await callback.message.edit_media(media, reply_markup=car_menu(index))

    elif data.startswith("car_"):
        index = int(data.split("_")[1])

        if index < 0:
            index = len(models) - 1
        elif index >= len(models):
            index = 0

        model = models[index]
        media = InputMediaPhoto(
            media=FSInputFile(car_photos[model]),
            caption=f"🏎 {model}"
        )
        await callback.message.edit_media(media, reply_markup=car_menu(index))

    elif "_history" in data:
        model = data.split("_")[0]
        await callback.message.edit_caption(
            caption=history[model],
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ Назад", callback_data=f"car_{models.index(model)}")]
            ])
        )

    elif "_specs" in data:
        model = data.split("_")[0]
        s = specs[model]

        text = (
            f"🏎 {model}\n\n"
            f"⚙️ {s['engine']}\n"
            f"💪 {s['power']}\n"
            f"⚡ {s['0-100']}"
        )

        await callback.message.edit_caption(
            caption=text,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ Назад", callback_data=f"car_{models.index(model)}")]
            ])
        )

    elif "_facts" in data:
        model = data.split("_")[0]
        await callback.message.edit_caption(
            caption=f"🔥 {car_facts[model][0]}",
            reply_markup=car_facts_menu(model, 0)
        )

    elif data.startswith("carfact_"):
        _, model, index = data.split("_")
        index = int(index)

        facts = car_facts[model]

        if index < 0:
            index = len(facts) - 1
        elif index >= len(facts):
            index = 0

        await callback.message.edit_caption(
            caption=f"🔥 {facts[index]}",
            reply_markup=car_facts_menu(model, index)
        )

    elif data == "compare":
        await callback.message.edit_text("⚖️ Выбери машины для сравнения (скоро улучшим 👇)", reply_markup=main_menu())

    elif data == "noop":
        pass

# --- ЗАПУСК ---
async def main():
    print("✅ Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())