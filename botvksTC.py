import requests
import json
from datetime import datetime, timedelta, date, time

# TcTg bot v.02
# Все вопросы, предложения, пожелания и донаты => https://t.me/gorod190
# Делалось для удобства информирования разных учреждений
# Для запуска в определенное время используется crontab в Linux и Планировщик заданий в Windows

sitename = '10.10.10.10'                                                #Адрес сервера TrueConf
tokenTK = 'poipuNqPocnjUy0hVNABYb5Q7eN-rAcDb'                           #Токен API сервера TrueConf
crtCA = '/home/user/ca.crt'                                             #Адрес сертефиката CA TrueConf Server либо написать false
botTg = 'bot2084329747:AAHyYfyNIsdF7swa9GXzRwYXX-afbvIeHnQ'             #Токен API бота Telegram
idTg = '1754587554'                                                     #ID группы или пользователя Telegram
tagTc = '@vcs.trueconf.ru'                                              #Адрес обрезки для вывода организатора в TrueConf

headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'
}
r = requests.get(url = 'https://'+sitename+'/api/v3.4/conferences/?access_token='+tokenTK+'&page_size=1', headers = headers, verify = crtCA, timeout = 5)
pags = r.json()
size = 100
for pages in range(1, int(pags.get('cnt') / int(size) + 2)):
        response = requests.get(url = 'https://'+sitename+'/api/v3.4/conferences/?access_token='+tokenTK+'&page_id='+str(pages)+'&page_size='+str(size), headers = headers, verify = crtCA, timeout = 20)
        data = response.json()
        all_count = data.get('conferences')
        full_data = []
        dt = time(00, 00, 00)
        dd = ['Воскресенье','Понедельник','Вторник','Среду','Четверг','Пятницу','Субботу']
        daytc = dd[datetime.today().isoweekday()]
        ds = date.today()
        dk = datetime.combine(ds, dt).timestamp()
        dn = dk + timedelta(days=1).total_seconds()

        for conf in all_count:
                uz = conf.get('invitations')
                times = conf.get('schedule').get('type')
                td = conf.get('schedule').get('start_time')

                if times != -1 and dn > td > dk not in full_data:
                        full_data.append(
                            {
                            "names": conf.get("topic"),
                            "ids": conf.get("id"),
                            "owners": dict([[*conf.values()] for conf in uz])[conf.get("owner").replace(tagTc, "")],
                            "times": datetime.fromtimestamp(conf.get("schedule").get("start_time")).strftime('%d.%m.%Y в %H:%M'),
                            "users": str([conf['display_name'] for conf in uz]).replace("[", "").replace("]", "").replace("'", "")
                            }
                        )
                        for o in full_data:
                            address = o['ids']
                            name = o['names']
                            owner = o['owners']
                            timeconf = o['times']
                            user = o['users'].replace(owner, "")

                        data_call2 = [(f'📆 <b>Расписание на {daytc}</b>\n\n✏ <b>Название ВКС:</b> <i>{name}</i>\n🧘‍ <b>Организатор:</b> {owner}\n\n🪤 <b>Сылка для подключения:</b> https://{sitename}/c/{address}\n⏰ <b>Время начала подключения:</b> {timeconf}\n\n👯 <b>Список участников:</b> {user}')]
                        for calendar in data_call2:
                                url = 'https://api.telegram.org/'+botTg+'/sendMessage?chat_id='+idTg+'&parse_mode=html&text={}'.format(calendar)
                                requests.get(url)
