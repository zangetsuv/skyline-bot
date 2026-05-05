import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    FSInputFile, InputMediaPhoto
)

# --- 🔐 ТОКЕН ---
TOKEN = os.environ.get("BOT_TOKEN")

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

# --- 📜 ПОДРОБНАЯ ИСТОРИЯ ---
history = {
    "R32": (
        "🏎 Nissan Skyline GT-R R32 (1989–1994)\n\n"
        "📌 Контекст:\n"
        "R32 стал возрождением легендарной серии GT-R после долгого перерыва. "
        "Модель создавалась с конкретной целью — доминировать в автоспорте.\n\n"
        "🏁 Достижения:\n"
        "• 29 побед подряд в JTCC\n"
        "• фактически не имел конкурентов\n\n"
        "🔧 Технологии:\n"
        "• ATTESA E-TS\n"
        "• RB26DETT\n"
        "• HICAS\n\n"
        "👑 Итог:\n"
        "Прозвище 'Godzilla'"
    ),

    "R33": (
        "🏎 Nissan Skyline GT-R R33 (1995–1998)\n\n"
        "📌 Контекст:\n"
        "Развитие R32 с упором на стабильность.\n\n"
        "🏁 Достижения:\n"
        "• Nürburgring < 8 минут\n\n"
        "🔧 Технологии:\n"
        "• ATTESA E-TS Pro\n"
        "• улучшенная подвеска\n\n"
        "👑 Итог:\n"
        "Самый стабильный Skyline"
    ),

    "R34": (
        "🏎 Nissan Skyline GT-R R34 (1999–2002)\n\n"
        "📌 Контекст:\n"
        "Финальная версия Skyline.\n\n"
        "🏁 Достижения:\n"
        "• культовый статус\n\n"
        "🔧 Технологии:\n"
        "• дисплей телеметрии\n\n"
        "👑 Итог:\n"
        "Икона JDM"
    ),

    "R35": (
        "🏎 Nissan GT-R R35 (2007–)\n\n"
        "📌 Контекст:\n"
        "Отдельная модель GT-R.\n\n"
        "🏁 Достижения:\n"
        "• конкурирует с Ferrari\n\n"
        "🔧 Технологии:\n"
        "• VR38DETT\n"
        "• полный привод\n\n"
        "👑 Итог:\n"
        "Современный суперкар"
    )
}

# --- ⚙️ ХАРАКТЕРИСТИКИ ---
specs = {
    "R32": {"text": "🏎 R32\n💪 280 л.с.\n⚡ 5.5 сек"},
    "R33": {"text": "🏎 R33\n💪 280 л.с.\n⚡ 5.4 сек"},
    "R34": {"text": "🏎 R34\n💪 280 л.с.\n⚡ 4.9 сек"},
    "R35": {"text": "🏎 R35\n💪 480+ л.с.\n⚡ 3 сек"}
}

# --- ФАКТЫ ---
car_facts = {
    "R32": ["29 побед подряд", "Godzilla", "1000+ л.с."],
    "R33": ["<8 мин Nürburgring", "ATTESA Pro", "стабильность"],
    "R34": ["Fast & Furious", "телеметрия", "JDM"],
    "R35": ["ручная сборка", "суперкар", "<3 сек"]
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
            InlineKeyboardButton(text=f"{model}", callback_data="noop"),
            InlineKeyboardButton(text="➡️", callback_data=f"car_{index+1}")
        ],
        [
            InlineKeyboardButton(text="📜 История", callback_data=f"{model}_history"),
            InlineKeyboardButton(text="⚙️ Характеристики", callback_data=f"{model}_specs")
        ],
        [
            InlineKeyboardButton(text="🔥 Факты", callback_data=f"{model}_facts")
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
            InlineKeyboardButton(text="⬅️ Назад", callback_data=f"cars")
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

    if data == "cars":
        model = models[0]
        media = InputMediaPhoto(
            media=FSInputFile(car_photos[model]),
            caption=f"🏎 {model}"
        )
        await callback.message.edit_media(media, reply_markup=car_menu(0))

    elif data.startswith("car_"):
        index = int(data.split("_")[1]) % len(models)
        model = models[index]
        media = InputMediaPhoto(
            media=FSInputFile(car_photos[model]),
            caption=f"🏎 {model}"
        )
        await callback.message.edit_media(media, reply_markup=car_menu(index))

    elif "_history" in data:
        model = data.split("_")[0]
        await callback.message.edit_caption(
            caption=history[model]
        )

    elif "_specs" in data:
        model = data.split("_")[0]
        await callback.message.edit_caption(
            caption=specs[model]["text"]
        )

    elif "_facts" in data:
        model = data.split("_")[0]
        await callback.message.edit_caption(
            caption=car_facts[model][0],
            reply_markup=car_facts_menu(model, 0)
        )

# --- ЗАПУСК ---
async def main():
    print("✅ Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
