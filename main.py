import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram import F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

API_TOKEN = "7490052383:AAEDQZJs8fkhBicjhJxTQyJkmD1hLeMhcDs"
ADMIN_ID = 7752032178

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher()

users = set()

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Menu")],
        [KeyboardButton(text="🛒 Buyurtma berish")],
        [KeyboardButton(text="📞 Admin bilan bog‘lanish")]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    users.add(message.from_user.id)
    await message.answer(
        "👋 Assalomu alaykum!\n\nBotimizga xush kelibsiz!\nIltimos, pastdagi tugmalardan birini tanlang 👇\n" \
        "Admn lar sz bilan boglansh uchun anq nomer kirtng",
        reply_markup=main_keyboard
    )

@dp.message(F.text == "📋 Menu")
async def menu_handler(message: types.Message):
    menu_text = """
📋 *Xizmatlar MENYUSI*:

🤖 Telegram bot yasash  
🌐 Web sayt yaratish  
🎨 Logo yasash  
🖼 Banner yasash  
🎞 Animatsiya tayyorlash  
📽 Slayd tayyorlash  
🎓 Diploma & Rezyume  
💌 Taklifnoma tayyorlash  
🎂 Tug‘ilgan kunga tabrik  
🎧 Video/audio montaj  
📄 PDF qilish  
🔤 Telegram nickname yaratish  
🖌 Ismga rasm/video tayyorlash  
📝 Word ishlari  
👤 Avatar tayyorlash  
📈 Nakrutka urish  
📲 Telegram akkaunt olish  
📦 3D ko‘rinishdagi loyihalar  
➕ Va boshqa xizmatlar mavjud
"""
    await message.answer(menu_text)

@dp.message(F.text == "📞 Admin bilan bog‘lanish")
async def contact_admin_handler(message: types.Message):
    await message.answer("📞 Admin bilan bog‘lanish:\nTelegram: @sardorbeksobirjonov\nTelefon: 94 089 81 19")

user_states = {}

@dp.message(F.text == "🛒 Buyurtma berish")
async def order_handler(message: types.Message):
    user_states[message.from_user.id] = "awaiting_service"
    await message.answer("📝 Qanday xizmat kerakligini yozing (masalan: logo):")

@dp.message()
async def text_handler(message: types.Message):
    user_id = message.from_user.id
    text = message.text

    if text.startswith("reklama1020") and user_id == ADMIN_ID:
        await message.answer("📢 Reklama matnini yuboring:")
        user_states[user_id] = "awaiting_ad_text"
        return

    if user_states.get(user_id) == "awaiting_ad_text":
        ad_text = text
        count = 0
        for uid in users:
            try:
                await bot.send_message(uid, f"📢 {ad_text}")
                count += 1
            except:
                continue
        await message.answer(f"✅ Reklama {count} ta foydalanuvchiga yuborildi.")
        user_states[user_id] = None
        return

    if user_states.get(user_id) == "awaiting_service":
        user_states[user_id] = {"service": text}
        await message.answer("📱 Telefon raqamingizni kiriting:")
        return

    if isinstance(user_states.get(user_id), dict) and "service" in user_states[user_id]:
        service = user_states[user_id]["service"]
        phone = text

        await bot.send_message(
            chat_id=ADMIN_ID,
            text=f"🆕 Yangi buyurtma:\n\n🛠 Xizmat: {service}\n📱 Telefon: {phone}"
        )
        await message.answer(
            "✅ Sizning buyurtmangiz adminlarga yuborildi.\n\n📞 Adminlar bilan bog‘lanishingiz mumkin:\n"
            "Telegram: @sardorbeksobirjonov\nTel: 94 089 81 19"
        )
        user_states[user_id] = None
        return

# Botni ishga tushurish
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
