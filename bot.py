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
    raise ValueError("❌ BOT_TOKEN не найден! Добавь его в Railway Variables")

bot = Bot(token=TOKEN)
dp = Dispatcher()

models = ["R32", "R33", "R34", "R35"]

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
        "После прекращения GT-R в 1970-х Nissan решил вернуть легенду как оружие для автоспорта.\n\n"
        "🏁 Достижения:\n"
        "• 29 побед подряд в JTCC\n"
        "• доминирование в гонках\n\n"
        "🔧 Инженерия:\n"
        "• ATTESA E-TS\n"
        "• RB26DETT\n"
        "• HICAS\n\n"
        "⚙️ Факт:\n"
        "Мощность была занижена (реально больше 280 л.с.)\n\n"
        "👑 Итог:\n"
        "Godzilla — легенда автоспорта"
    ),

    "R33": (
        "🏎 Nissan Skyline GT-R R33 (1995–1998)\n\n"
        "📌 Контекст:\n"
        "Эволюция R32 с упором на стабильность и контроль.\n\n"
        "🏁 Достижения:\n"
        "• Nürburgring < 8 минут\n\n"
        "🔧 Инженерия:\n"
        "• ATTESA E-TS Pro\n"
        "• улучшенная подвеска\n"
        "• усиленный кузов\n\n"
        "⚙️ Факт:\n"
        "Несмотря на вес, быстрее R32 на треке\n\n"
        "👑 Итог:\n"
        "Самый стабильный Skyline"
    ),

    "R34": (
        "🏎 Nissan Skyline GT-R R34 (1999–2002)\n\n"
        "📌 Контекст:\n"
        "Финальная эволюция Skyline GT-R.\n\n"
        "🏁 Достижения:\n"
        "• культовый статус\n"
        "• популярность благодаря Fast & Furious\n\n"
        "🔧 Инженерия:\n"
        "• дисплей телеметрии\n"
        "• улучшенный полный привод\n\n"
        "⚙️ Факт:\n"
        "Один из первых авто с телеметрией\n\n"
        "👑 Итог:\n"
        "Икона JDM"
    ),

    "R35": (
        "🏎 Nissan GT-R R35 (2007–)\n\n"
        "📌 Контекст:\n"
        "Полностью новая модель GT-R.\n\n"
        "🏁 Достижения:\n"
        "• конкурирует с суперкарами\n"
        "• рекорды Nürburgring\n\n"
        "🔧 Инженерия:\n"
        "• VR38DETT\n"
        "• полный привод\n"
        "• роботизированная коробка\n\n"
        "⚙️ Факт:\n"
        "Быстрее многих суперкаров\n\n"
        "👑 Итог:\n"
        "Современный технологичный суперкар"
    )
}

# --- ⚙️ ХАРАКТЕРИСТИКИ ---
specs = {
    "R32": {
        "text": (
            "🏎 Nissan Skyline GT-R R32\n\n"
            "⚙️ Двигатель: RB26DETT (2.6L, рядный 6, twin-turbo)\n"
            "💪 Мощность: 280 л.с. (реально 300+)\n"
            "🧠 Привод: полный (ATTESA E-TS)\n"
            "🔧 Коробка: 5-ступенчатая механика\n"
            "⚡ 0–100 км/ч: ~5.5 сек\n"
            "🏁 Макс. скорость: ~250 км/ч (ограничена)\n"
            "⚖️ Вес: ~1430 кг\n"
            "🔥 Тюнинг: потенциал 1000+ л.с.\n"
            "🛠 Особенности: HICAS (подруливание задних колёс)"
        )
    },

    "R33": {
        "text": (
            "🏎 Nissan Skyline GT-R R33\n\n"
            "⚙️ Двигатель: RB26DETT (2.6L twin-turbo)\n"
            "💪 Мощность: 280 л.с.\n"
            "🧠 Привод: полный (ATTESA E-TS Pro)\n"
            "🔧 Коробка: 5-ступенчатая механика\n"
            "⚡ 0–100 км/ч: ~5.4 сек\n"
            "🏁 Макс. скорость: ~250 км/ч\n"
            "⚖️ Вес: ~1540 кг\n"
            "📊 Управляемость: лучше баланс и стабильность\n"
            "🛠 Особенности: улучшенная подвеска и охлаждение"
        )
    },

    "R34": {
        "text": (
            "🏎 Nissan Skyline GT-R R34\n\n"
            "⚙️ Двигатель: RB26DETT (2.6L twin-turbo)\n"
            "💪 Мощность: 280 л.с.\n"
            "🧠 Привод: полный (ATTESA E-TS Pro)\n"
            "🔧 Коробка: 6-ступенчатая механика\n"
            "⚡ 0–100 км/ч: ~4.9 сек\n"
            "🏁 Макс. скорость: ~250 км/ч\n"
            "⚖️ Вес: ~1560 кг\n"
            "🖥 Особенность: экран телеметрии\n"
            "🔥 Статус: одна из самых желанных машин в мире"
        )
    },

    "R35": {
        "text": (
            "🏎 Nissan GT-R R35\n\n"
            "⚙️ Двигатель: VR38DETT (3.8L V6 twin-turbo)\n"
            "💪 Мощность: 480–600+ л.с.\n"
            "🧠 Привод: полный\n"
            "🔧 Коробка: роботизированная (6-ступенчатая)\n"
            "⚡ 0–100 км/ч: 2.7–3.5 сек\n"
            "🏁 Макс. скорость: ~315 км/ч\n"
            "⚖️ Вес: ~1750 кг\n"
            "🧑‍🔧 Сборка: каждый двигатель собирается вручную (Takumi)\n"
            "🚀 Класс: полноценный суперкар"
        )
    }
}
# --- ФАКТЫ ---
car_facts = {
    "R32": [
        "🏁 R32 выиграл 29 гонок подряд в JTCC — абсолютное доминирование без шансов для соперников.",
        "👾 Прозвище 'Godzilla' появилось в Австралии после разгрома местных команд.",
        "⚙️ RB26DETT официально 280 л.с., но фактически выдавал больше — это было частью джентльменского соглашения.",
        "🔧 Многие R32 спокойно разгоняются до 1000+ л.с. при тюнинге.",
        "🧠 ATTESA E-TS могла перераспределять момент между осями за доли секунды."
    ],

    "R33": [
        "🏁 R33 стал первым серийным авто быстрее 8 минут на Nürburgring.",
        "⚖️ Несмотря на больший вес, на треке он быстрее R32 благодаря стабильности.",
        "🔧 Версия LM создавалась для Ле-Мана и имеет уникальный дизайн.",
        "🧠 ATTESA E-TS Pro умела распределять тягу даже между задними колёсами.",
        "📊 Считается самым недооценённым GT-R среди всех поколений."
    ],

    "R34": [
        "🎬 Стал мировой иконой после фильма Fast & Furious.",
        "🖥 Один из первых авто с экраном телеметрии (давление турбин, перегрузки и т.д.).",
        "🔥 Версия V-Spec II считается одной из самых редких и ценных.",
        "💰 Сейчас цена на R34 может превышать сотни тысяч долларов.",
        "🧠 Очень любим в дрифте и тайм-аттаке за баланс и контроль."
    ],

    "R35": [
        "🧑‍🔧 Каждый двигатель собирается вручную мастером Takumi.",
        "🚀 Разгон быстрее многих суперкаров, стоящих в 2–3 раза дороже.",
        "🏁 GT-R регулярно устанавливал рекорды на Nürburgring.",
        "💻 Управление полностью электронное — от подвески до распределения тяги.",
        "🔥 За годы выпуска мощность выросла с ~480 до 600+ л.с."
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
            InlineKeyboardButton(text=f"{model}", callback_data="noop"),
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

def car_facts_menu(model, index):
    facts = car_facts[model]
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️", callback_data=f"carfact_{model}_{index-1}"),
            InlineKeyboardButton(text=f"{index+1}/{len(facts)}", callback_data="noop"),
            InlineKeyboardButton(text="➡️", callback_data=f"carfact_{model}_{index+1}")
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
    await message.answer("🚀 Главное меню", reply_markup=main_menu())

# --- CALLBACK ---
@dp.callback_query()
async def cb(callback: types.CallbackQuery):
    await callback.answer()
    data = callback.data

    if data == "back":
        await callback.message.edit_text("🚀 Главное меню", reply_markup=main_menu())

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
            caption=facts[index],
            reply_markup=car_facts_menu(model, index)
        )

# --- ЗАПУСК ---
async def main():
    print("✅ Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
