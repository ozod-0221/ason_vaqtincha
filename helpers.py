from aiogram.types import Message, Contact
def is_true_contact(contact: Contact,message: Message) -> bool:
    if contact.first_name== message.from_user.first_name :
        return True
    elif contact.last_name== message.from_user.last_name:
        return True
    elif contact.first_name== message.from_user.last_name:
        return True
    elif contact.last_name== message.from_user.first_name:
        return True
    else:
        return False