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
    "R35": "r35.jpg"
}

# --- ИСТОРИЯ (сокращена чтобы влезала) ---
history = {
    "R32": (
        "🏎 R32 GT-R (1989–1994)\n\n"
        "Возрождение GT-R как машины для автоспорта.\n"
        "Создавался под гонки Group A.\n\n"
        "🏁 29 побед подряд в JTCC\n"
        "🔧 RB26DETT + ATTESA E-TS + HICAS\n\n"
        "⚙️ Реальная мощность выше 280 л.с.\n\n"
        "👑 Godzilla — легенда автоспорта"
    ),

    "R33": (
        "🏎 R33 GT-R (1995–1998)\n\n"
        "Эволюция R32 с упором на стабильность.\n"
        "Больше, тяжелее, но управляемее.\n\n"
        "🏁 Nürburgring < 8 минут\n"
        "🔧 ATTESA E-TS Pro\n\n"
        "⚙️ Быстрее R32 на треке\n\n"
        "👑 Самый стабильный Skyline"
    ),

    "R34": (
        "🏎 R34 GT-R (1999–2002)\n\n"
        "Финальная версия Skyline GT-R.\n"
        "Компактнее и технологичнее.\n\n"
        "🏁 Культовый статус + Fast & Furious\n"
        "🔧 Телеметрия + полный привод\n\n"
        "⚙️ Один из первых авто с дисплеем данных\n\n"
        "👑 Икона JDM"
    ),

    "R35": (
        "🏎 GT-R R35 (2007–)\n\n"
        "Полностью новая модель GT-R.\n"
        "Отделён от Skyline.\n\n"
        "🏁 Конкурирует с суперкарами\n"
        "🔧 VR38DETT + AWD + робот\n\n"
        "⚙️ Рекорды Nürburgring\n\n"
        "👑 Современный суперкар"
    )
}

# --- ХАРАКТЕРИСТИКИ ---
specs = {
    "R32": {
        "text": (
            "🏎 R32 GT-R\n\n"
            "⚙️ RB26DETT (2.6L twin-turbo)\n"
            "💪 280+ л.с.\n"
            "🧠 AWD (ATTESA E-TS)\n"
            "🔧 5MT\n"
            "⚡ 0–100: ~5.5 сек\n"
            "🏁 ~250 км/ч\n"
            "⚖️ ~1430 кг"
        )
    },

    "R33": {
        "text": (
            "🏎 R33 GT-R\n\n"
            "⚙️ RB26DETT\n"
            "💪 280 л.с.\n"
            "🧠 AWD (ATTESA Pro)\n"
            "🔧 5MT\n"
            "⚡ ~5.4 сек\n"
            "🏁 ~250 км/ч\n"
            "⚖️ ~1540 кг"
        )
    },

    "R34": {
        "text": (
            "🏎 R34 GT-R\n\n"
            "⚙️ RB26DETT\n"
            "💪 280 л.с.\n"
            "🧠 AWD\n"
            "🔧 6MT\n"
            "⚡ ~4.9 сек\n"
            "🏁 ~250 км/ч\n"
            "🖥 Телеметрия"
        )
    },

    "R35": {
        "text": (
            "🏎 GT-R R35\n\n"
            "⚙️ VR38DETT (3.8L V6)\n"
            "💪 480–600+ л.с.\n"
            "🧠 AWD\n"
            "🔧 робот\n"
            "⚡ 2.7–3.5 сек\n"
            "🏁 ~315 км/ч\n"
            "🧑‍🔧 Takumi"
        )
    }
}

# --- ФАКТЫ ---
car_facts = {
    "R32": [
        "🏁 29 побед подряд — абсолютное доминирование",
        "👾 Прозвище Godzilla из Австралии",
        "⚙️ Мощность была занижена",
        "🔧 Тюнинг до 1000+ л.с.",
        "🧠 Умный полный привод"
    ],

    "R33": [
        "🏁 <8 мин Nürburgring",
        "⚖️ Быстрее R32 на треке",
        "🔧 Версия LM для Ле-Мана",
        "🧠 Улучшенный полный привод",
        "📊 Самый недооценённый GT-R"
    ],

    "R34": [
        "🎬 Икона после Fast & Furious",
        "🖥 Дисплей телеметрии",
        "🔥 V-Spec II — редкий",
        "💰 Очень дорогой сейчас",
        "🧠 Отличный баланс"
    ],

    "R35": [
        "🧑‍🔧 Двигатель собирает Takumi",
        "🚀 Быстрее многих суперкаров",
        "🏁 Рекорды Nürburgring",
        "💻 Полностью электронный",
        "🔥 Мощность выросла до 600+"
    ]
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
        FSInputFile(car_photos["R32"]),
        caption="🚀 Главное меню",
        reply_markup=main_menu()
    )

# --- CALLBACK ---
@dp.callback_query()
async def cb(callback: types.CallbackQuery):
    await callback.answer()
    data = callback.data

    if data == "back":
        await callback.message.edit_caption(
            caption="🚀 Главное меню",
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
        await callback.message.edit_caption(
            caption=history[model],
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ Назад", callback_data=f"car_{models.index(model)}")],
                [InlineKeyboardButton(text="🏠 В меню", callback_data="back")]
            ])
        )

    elif "_specs" in data:
        model = data.split("_")[0]
        await callback.message.edit_caption(
            caption=specs[model]["text"],
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ Назад", callback_data=f"car_{models.index(model)}")],
                [InlineKeyboardButton(text="🏠 В меню", callback_data="back")]
            ])
        )

    elif "_facts" in data:
        model = data.split("_")[0]
        await callback.message.edit_caption(
            caption=car_facts[model][0],
            reply_markup=facts_menu(model, 0)
        )

    elif data.startswith("fact_"):
        _, model, index = data.split("_")
        index = int(index)
        facts = car_facts[model]

        if index < 0:
            index = len(facts) - 1
        elif index >= len(facts):
            index = 0

        await callback.message.edit_caption(
            caption=facts[index],
            reply_markup=facts_menu(model, index)
        )

    elif data == "compare":
        await callback.message.edit_caption(
            caption="⚖️ Выбери первую машину",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=m, callback_data=f"c1_{m}") for m in models]
            ])
        )

    elif data.startswith("c1_"):
        m1 = data.split("_")[1]
        compare_state[callback.from_user.id] = m1

        await callback.message.edit_caption(
            caption=f"Первая: {m1}\nВыбери вторую",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=m, callback_data=f"c2_{m}") for m in models]
            ])
        )

    elif data.startswith("c2_"):
        m2 = data.split("_")[1]
        m1 = compare_state.get(callback.from_user.id)

        await callback.message.edit_caption(
            caption=f"{m1} vs {m2}\n\n{specs[m1]['text']}\n\n🆚\n\n{specs[m2]['text']}",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🏠 В меню", callback_data="back")]
# --- ЗАПУСК ---
async def main():
    print("✅ Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
