import logging
import requests
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '7360763175:AAExfiQFKHYCRR_nz5fmflXDrorRzDbtfxA'
EXCHANGE_API = 'https://open.er-api.com/v6/latest/USD'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton(text="📈 FX Rates", callback_data="fx_rates"),
        types.InlineKeyboardButton(text="📊 Macro Info", callback_data="macro_info")
    )
    await message.reply("👋 Welcome to FX & Macro Bot!\nChoose an option below:", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data)
async def handle_callback(callback_query: types.CallbackQuery):
    data = callback_query.data

    if data == "fx_rates":
        try:
            response = requests.get(EXCHANGE_API)
            rates = response.json().get("rates", {})
            uah = rates.get("UAH")
            eur = rates.get("EUR")
            pln = rates.get("PLN")

            if uah and eur and pln:
                msg = (
                    f"💱 *USD Exchange Rates:*\n"
                    f"🇺🇦 UAH: {uah:.2f}\n"
                    f"🇪🇺 EUR: {eur:.2f}\n"
                    f"🇵🇱 PLN: {pln:.2f}"
                )
            else:
                msg = "⚠️ Could not retrieve all currency rates."

            await bot.send_message(callback_query.from_user.id, msg, parse_mode="Markdown")
        except Exception as e:
            await bot.send_message(callback_query.from_user.id, "❌ Error retrieving data.")
    elif data == "macro_info":
        await bot.send_message(
            callback_query.from_user.id,
            "📊 Macro Overview:\n"
            "- 🇺🇸 Fed Rate: 5.25%\n"
            "- 🇪🇺 ECB Rate: 4.0%\n"
            "- 🇺🇸 US Inflation: 3.2%\n"
            "*Live macro data will be added soon.*"
        )

    await bot.answer_callback_query(callback_query.id)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
