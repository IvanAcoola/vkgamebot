import vk_api
from vk_api.longpoll import VkLongPoll

token = ''

session = vk_api.VkApi(token = token)
vk = session.get_api()
longpool = VkLongPoll(session)