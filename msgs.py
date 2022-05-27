import methods
import json

def hellokeyb():
    keyboard = {
        "one_time": True,
        "buttons": [
            [methods.get_but('Профиль', 'secondary')],
            [methods.get_but('Угадай число (50💰)', 'primary'), methods.get_but('Угадай фильм (30💰)', 'primary')]
        ]
    }
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    return keyboard