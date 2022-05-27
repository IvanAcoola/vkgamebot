import random
from vk_api.longpoll import VkEventType

import pictures
from config import longpool
import methods
from db import db
import msgs

def main():
    founders = dict()
    founders_attempts = dict()

    pictured = dict()

    while True:
        for event in longpool.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    if db.getinfo(event.user_id) == []:
                        db.createuser(event.user_id)

                    if event.user_id in pictured.keys():
                        try:
                            if pictures.picsinfo[pictured[event.user_id]['next_ans']][event.text]:
                                methods.sendMsgGroup(event.user_id, 'Ответ... ПРАВИЛЬНЫЙ!')
                                pictured.update({
                                    event.user_id: {
                                        'next_ans': pictured[event.user_id]['next_ans'],
                                        'more': pictured[event.user_id]['more'],
                                        'right': pictured[event.user_id]['right'] + 1
                                    }
                                })
                            else:
                                methods.sendMsgGroup(event.user_id, 'Ответ... неправильный(')
                        except:
                            methods.sendMsgGroup(event.user_id, 'Выбери ответ в списке, не нужно писать свой.')

                        if pictured[event.user_id]['more'] != 0:
                            methods.sendMsgGroup(event.user_id, 'Едем дальше!')

                            quest = methods.give_pict_test(event.user_id, denied=pictured[event.user_id]['next_ans'])
                            pictured.update({
                                event.user_id: {
                                    'next_ans': quest,
                                    'more': pictured[event.user_id]['more'] - 1,
                                    'right': pictured[event.user_id]['right']
                                }
                            })
                        else:
                            methods.sendMsgGroupKeyb(event.user_id, f'Вы закончили и получили {pictured[event.user_id]["right"] * 10}💰!', msgs.hellokeyb())
                            money = db.getinfo(event.user_id)[0][1]
                            db.setbal(event.user_id, money + pictured[event.user_id]["right"] * 10)
                            del pictured[event.user_id]


                    elif event.user_id in founders.keys():
                        try:
                            user_number = int(event.text)
                            right_number = founders[event.user_id]
                            if user_number == right_number:
                                attempts = founders_attempts[event.user_id]
                                methods.sendMsgGroupKeyb(event.user_id, f'Правильно, вы получаете {attempts} 💰!', msgs.hellokeyb())
                                del founders[event.user_id]
                                del founders_attempts[event.user_id]
                                money = db.getinfo(event.user_id)[0][1]
                                db.setbal(event.user_id, money + attempts)
                            else:
                                attempts = founders_attempts[event.user_id]
                                if attempts > 50:
                                    attempts -= 10

                                elif attempts <= 50:
                                    attempts -= 5

                                if attempts < 0:
                                    attempts = 0

                                founders_attempts.update({
                                    event.user_id:attempts
                                })
                                if user_number < right_number:
                                    suggest_word = 'больше'
                                else:
                                    suggest_word = 'меньше'
                                methods.sendMsgGroup(event.user_id, f'Неправильно, {suggest_word}')

                        except:
                            methods.sendMsgGroup(event.user_id, 'Я сказал говорить число, а не белиберду.')

                    elif event.text == 'Начать':
                        methods.sendMsgGroupKeyb(event.user_id, 'Выбирай:', msgs.hellokeyb())

                    elif event.text == 'Профиль':
                        userdata = db.getinfo(event.user_id)
                        if bool(userdata[0][2]):
                            admin_status = 'Администратор.'
                        else:
                            admin_status = 'Пользователь'
                        methods.sendMsgGroupKeyb(event.user_id, f'Ваш ID: {userdata[0][0]}\nБаланс: {userdata[0][1]}💰\nСтатус: {admin_status}', msgs.hellokeyb())

                    elif event.text == 'Угадай число (50💰)':
                        if not db.getinfo(event.user_id)[0][1] >= 50:
                            methods.sendMsgGroupKeyb(event.user_id, 'У вас не хватает баланса.', msgs.hellokeyb())
                            break
                        else:
                            db.setbal(event.user_id, db.getinfo(event.user_id)[0][1] - 50)
                        right_number = random.randint(1, 100)
                        founders.update({
                            event.user_id: right_number
                        })
                        founders_attempts.update({
                            event.user_id: 100
                        })
                        methods.sendMsgGroup(event.user_id, 'Тебе загадали число от 1 до 100. Угадаешь?')

                    elif event.text == 'Угадай фильм (30💰)':
                        if not db.getinfo(event.user_id)[0][1] >= 30:
                            methods.sendMsgGroupKeyb(event.user_id, 'У вас не хватает баланса.', msgs.hellokeyb())
                            break
                        else:
                            db.setbal(event.user_id, db.getinfo(event.user_id)[0][1] - 30)
                        methods.sendMsgGroup(event.user_id, 'Отгадаешь фильмы по картинкам? Поехали!')
                        quest = methods.give_pict_test(event.user_id)
                        pictured.update({
                            event.user_id: {
                                'next_ans': quest,
                                'more': 4,
                                'right': 0
                            }
                        })

                    elif '!выдать' in event.text and len(event.text.split()) == 3:
                        if bool(db.getinfo(event.user_id)[0][2]):
                            words = event.text.split()
                            db.setbal(words[1], db.getinfo(words[1])[0][1] + int(words[2]))
                            methods.sendMsgGroup(event.user_id, 'Выдал баланс.')
                        else:
                            methods.sendMsgGroup(event.user_id, 'Недостаточно прав.')

                    elif '!снять' in event.text and len(event.text.split()) == 3:
                        if bool(db.getinfo(event.user_id)[0][2]):
                            words = event.text.split()
                            db.setbal(words[1], db.getinfo(words[1])[0][1] - int(words[2]))
                            methods.sendMsgGroup(event.user_id, 'Вычел из баланса.')
                        else:
                            methods.sendMsgGroup(event.user_id, 'Недостаточно прав.')

                    elif '!просмотр' in event.text and len(event.text.split()) == 2:
                        if bool(db.getinfo(event.user_id)[0][2]):
                            target_id = int(event.text.split()[1])
                            userdata = db.getinfo(target_id)
                            if bool(userdata[0][2]):
                                admin_status = 'Администратор.'
                            else:
                                admin_status = 'Пользователь'
                            methods.sendMsgGroup(event.user_id,f'ID: {userdata[0][0]}\nБаланс: {userdata[0][1]}💰\nСтатус: {admin_status}')
                        else:
                            methods.sendMsgGroup(event.user_id, 'Недостаточно прав.')

                    elif '!админ' in event.text and len(event.text.split()) == 2:
                        if bool(db.getinfo(event.user_id)[0][2]):
                            target_id = int(event.text.split()[1])
                            methods.sendMsgGroup(event.user_id, f'Установил права @id{target_id} -> {db.switchRights(target_id)}')

                    else:
                        methods.sendMsgGroupKeyb(event.user_id, 'Ваше сообщение не распознано.', msgs.hellokeyb())


if __name__ == '__main__':
    main()