from aiogram import Bot, Dispatcher, F
from aiogram.fsm.context import FSMContext

from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from aiogram.types import Message,CallbackQuery
import asyncio
import logging
from config import *
from keyboards import *
from helpers import *
from aiogram.types import ReplyKeyboardRemove

bot=Bot(token=TOKEN)
dp=Dispatcher()

class Form(StatesGroup):
    
    phone = State()
    check = State()
    
@dp.message(Command("start"))
async def start(message: Message,state:FSMContext):
    name= message.from_user.first_name
    await message.answer(f"Assalomu alekum {name}, Xush kelibsiz!", reply_markup=contact_keyboard())
    await state.set_state(Form.phone)
    
@dp.message(Form.phone, F.contact)
async def process_contact(message: Message, state: FSMContext,bot:Bot):
    message_id = message.message_id
    contact = message.contact
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username if message.from_user.username else "Aniqlanmadi"
    
    if not is_true_contact(contact,message):
        await message.answer("Iltimos, to'g'ri kontaktni ulang")
        return
    phone_number = contact.phone_number
    
    if not str(phone_number).startswith("+"):
        phone_number = f"+{phone_number}"
    await state.update_data(phonenumber=phone_number,message_id=message_id,user_id=user_id,full_name=full_name,username=username)
    await state.set_state(Form.check)
    
    await message.answer(f"Translyatsiyaga qo'shilishuchun  uchun bizning Telegram va Instagram sahifalarimizga  a`zo bo`ling",reply_markup=subs_key())
async def check_subscription(user_id:int,bot:Bot) -> bool:
    try:
        user = await bot.get_chat_member(CHANNEL_ID, user_id)
        if user.status in ["member", "administrator", "creator"]:
            return True
    except Exception as e:
        logging.error(f"Error checking subscription: {e}")
    return False 
@dp.callback_query(Form.check,F.data=="check")
async def get_callback(callback:CallbackQuery,state:FSMContext,bot:Bot):
    user_id=callback.from_user.id
    
    
    user_data = await state.get_data()
    print("📍📍📍📍📍📍📍📍📍📍")
    print(user_data)
    print("📍📍📍📍📍📍📍📍📍📍")
    # Check if the user is subscribed to the channel
    if not await check_subscription(user_id,bot):
        await callback.answer("Iltimos, avval kanalga a'zo bo'ling", show_alert=True)
        return
    if await check_subscription(user_id,bot):
        print(user_data)
        #send file to user by id file
        order_text = (
        f"Yangi buyurtma!\n"
        f"Ism: {user_data.get('full_name', 'Aniqlanmadi')}\n"
        f"Foydalanuvchi ID: {user_data.get('user_id', 'Aniqlanmadi')}\n"
        f"Telefon: {user_data.get('phonenumber')}\n"
        f"Username: @{callback.from_user.username if callback.from_user.username else ' Aniqlanmadi'}"
    )
        for admin_id in ADMIN_IDS:
            try:
                if not callback.from_user.username:
                    await bot.forward_message(
                    chat_id=admin_id,
                    from_chat_id=callback.from_user.id,
                #any_message_id_from_user
                    message_id=user_data.get('message_id')
             )
                await bot.send_message(admin_id, order_text)
            
                

            except Exception as e:
                logging.error(f"Adminga yuborishda xatolik: {e}")
                await callback.answer(
                "Xatolik yuz berdi, yana bir bor urinib ko`ring:\n/start",
                reply_markup=ReplyKeyboardRemove()
                )
        
        
        await bot.send_message(
                user_id,
                f"!Translyatsiyaga shu yerda bo`ladi : \n{LINK}\n\n",
                reply_markup=ReplyKeyboardRemove()
                )
        await callback.answer("Tabriklaymiz , siz ro`yhatdan o`tdingiz 🚨\n Jonli efir havolasi jo`natildi 🎁🎁",show_alert=True)
           
            
       
    await state.clear()    
        



async def main():
   
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    try: 
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")
