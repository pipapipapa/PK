import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from Bot import VkBot
import random
from config import TOKEN

# 'https://sun9-43.userapi.com/impg/8Vg_obeU4Rjkafg8xWTbhvmkFqn1ZIYxpdCqzA/E0IfNHxcKPU.jpg?size=604x604&quality=96&sign=38e9a2018d1fdb4beedd84755a3fc241&type=album'

def write_msg(user_id, message):
    vk.method('messages.send', {
        'user_id': user_id,
        'message': message,
        'random_id': random.randint(1, 2**31)
    })

vk = vk_api.VkApi(token=TOKEN)
longpoll = VkLongPoll(vk)
bots = {}

print("Server started")
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            print('Сообщение:')
            print(f' ID: {event.user_id}', end='')
            print(' Содержание: ', event.text)

            user_id = event.user_id
            if user_id not in bots:
                bots[user_id] = VkBot(user_id)

            bot = bots[user_id]
            response_message = bot.new_message(event.text, event.attachments)
            write_msg(user_id, response_message)