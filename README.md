# Проект YaMDb. Протокол "Фантом".
## _Отличный специализированный портал для получения актуальной информации о любых современных произведениях во всех видах искусств!_
Проект YaMDb представляет из себя API-ориентированную базу данных произведений в различных сферах искусств и абсолютно всех жанров. YaMDb предоставляет расширенный функционал для взаимодействия пользователей с произведениями а именно:

* Создание произведений различных жанров и категорий
* Добавление рецензий к произведениям с возможностью поставить оценку от 1 до 10
* Создание комментариев к конкретному отзыву.

Таким образом пользователи могут активно взаимодействовать с ресурсом, общаясь и обсуждая произведения и свои впечатления о них, читать отзывы других пользователей или создавать свои собственные, а так же комментировать и ставить оценки произведениям! Вкупе всё это создает потрясающий програмный продукт для пользователя, который хочет получать подробную информацию о конкретном произведении, основанную на персональных ощущениях других пользователей! 

[![N|Solid](https://img.freepik.com/free-photo/businesspeople-at-office-meeting_23-2148908967.jpg?w=2000&t=st=1661689328~exp=1661689928~hmac=9b24a57975b0c56f0d8762a872114722c62c117f7d0c80f979880b2060f72487)]()

На сайте реализована расширенная версия ролей, включающая в себя модератора, который имеет право удалять и редактировать любые отзывы и комментарии. Тем самым внося гармонию, покой и упорядочность в бурлящих реках онлайн обсуждений!

Кроме всего прочего в проекте реализована полноценная админ зона с полным функционалом для работы со всем контентом проекта!


### Технологии:

| Plugin | Release version |
| ------ | ------ |
| Python **3.7** | [Release Date: June 27, 2018] |
| Django **2.2.16** | [Release notes] |
| djangorestframework **3.12.4** | [3.12.4 Date: 26th March 2021] |
| djangorestframework-simplejwt **4.7.2** | [Project description] |
| charset-normalizer **2.0.12** | [Charset Detection, for Everyone] |
| PyJWT **2.1.0** | [Docs] |
| importlib-metadata **4.2.0** | [Project description] |
| requests **2.26.0** | [Released: Jun 29, 2022] |

### Для запуска проекта необходимо:

Клонировать репозиторий и перейти в него в командной строке:

```sh
git clone git@github.com:kotbarbarossa/api_yamdb.git
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```sh
python3 -m venv env
source venv/bin/activate
```

Обновить pip:

```sh
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```sh
pip install -r requirements.txt
```

Выполнить миграции:

```sh
python3 manage.py migrate
```

Запустить проект:
```sh
python3 manage.py runserver
```

### Наполнение базы прямиком из ```.csv``` файла!
«Закинь данные из csv в БД» — достаточно распространённая задача.
В проекте YaMDb реализован програмный модуль автоматического наполнения баз данных!
Для это необходимо всего лишь поместить файлы по адресу ```/api_yamdb/static/data``` и ввести команду:
```sh
python manage.py load_data_from_csv
```

### Актуальная информация по взаимодействию с эндпоинтами

Для быстро ориентирования в системе эндоитов API в проекте подключена документация API! Возпользоваться ей можно пройдя по адресу:
```sh
http://127.0.0.1:8000/redoc/ 
```
В ней описаны возможные запросы к API и структура ожидаемых ответов. Для каждого запроса указаны уровни прав доступа: пользовательские роли, которым разрешён запрос, права доступа и дополнительные параметры, если это необходимо.


### Авторы 

Проект был создан и протестирован в кратчайшие сроки всего лишь тремя таллантливыми молодыми разработчиками из сердца кремниевой долины России - Татарстана:

[![N|Solid](https://sun9-north.userapi.com/sun9-77/s/v1/ig2/yQB4AzD-dchlG-XdyxgRSWwW3juGJwIzweL_M4hmTXvaJ4Etm-9ukE9OUFYSv49Q1YNlq5-CaBG3iDF0xH3t7jMj.jpg?size=2000x1418&quality=95&type=album)](https://www.youtube.com/channel/UC0NWbtRrU1YvsCP_0Slq-9A/featured)


**Эльдар Барбаросса** 
[INSTAGRAM]

**Николай Слесарев** 
[github.com/Kolanser]

**Марсель Галиаскаров** 
[github.com/Marsel168]

В кодревью принял участие известный и всеми любимый ревьюер Яндекс практикума [Максим Митягин]:
> Тут должен быть коментарий ревьюера


_Если этот Readme был полезен не забудь поддержить подпиской [youtube] канал тимлида (не свзанный с програмированием)! Ведь это дает:_
*  +150 кармы от фракции Бородатых Котов Вегетарианцев!
*  +135 репутации Казанских золотордынцев
*  а также один бесплатный просмотр фильма на сайте Лордфильм-одинихксбет-мелбет-казинотрилопаты точка ру

[//]: # (links)

   [Максим Митягин]: <https://github.com/mityagin>
   [github.com/Kolanser]: https://github.com/Kolanser
   [github.com/Marsel168]: https://github.com/Marsel168
   [Release Date: June 27, 2018]: https://www.python.org/downloads/release/python-370/
   [Release notes]: https://docs.djangoproject.com/en/4.0/releases/2.2.16/
   [3.12.4 Date: 26th March 2021]: https://www.django-rest-framework.org/community/release-notes/#312x-series
   [Project description]: https://pypi.org/project/djangorestframework-simplejwt/4.7.2/
   [Charset Detection, for Everyone]: https://pypi.org/project/charset-normalizer/
   [Docs]: https://pyjwt.readthedocs.io/en/2.1.0/
   [Project description]: https://pypi.org/project/importlib-metadata/
   [Released: Jun 29, 2022]: https://pypi.org/project/requests/
   [youtube]: https://www.youtube.com/channel/UC0NWbtRrU1YvsCP_0Slq-9A/
   [INSTAGRAM]: https://instagram.com/kot.barbarossa?igshid=YmMyMTA2M2Y=
