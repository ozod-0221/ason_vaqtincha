import json
from aiogram.types import Message

USER_DATA_FILE = 'users.json'

# Foydalanuvchi IDlarini saqlash uchun json faylga yozish
def save_user_id(user_id):
    try:
        # Avvalgi foydalanuvchilarni o'qish
        with open(USER_DATA_FILE, 'r') as file:
            users = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        users = []

    # Agar foydalanuvchi ID mavjud bo'lmasa, uni qo'shish
    if user_id not in users:
        users.append(user_id)
        with open(USER_DATA_FILE, 'w') as file:
            json.dump(users, file, indent=4)

# Barcha foydalanuvchi IDlarini olish
def get_all_user_ids():
    try:
        with open(USER_DATA_FILE, 'r') as file:
            users = json.load(file)
        return users
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Agar fayl mavjud bo'lmasa yoki xato bo'lsa, bo'sh ro'yxat qaytaradi