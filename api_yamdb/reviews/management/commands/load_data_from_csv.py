from csv import DictReader
from datetime import datetime
from django.core.management import BaseCommand
import logging
import sys

from ...models import (
    Category, Comment, Genre, Review, Title, TitleGenre, User
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)
formatter = logging.Formatter(
    '%(asctime)s, [%(levelname)s] %(message)s'
)
handler.setFormatter(formatter)


class Command(BaseCommand):
    help = 'Загрузка данных в БД'

    def handle(self, *args, **options):
        logger.info('Удаление данных в БД')
        Genre.objects.all().delete()
        User.objects.all().delete()
        Title.objects.all().delete()
        Category.objects.all().delete()
        TitleGenre.objects.all().delete()
        Review.objects.all().delete()
        Comment.objects.all().delete()

        logger.info('Загрузка пользователей в БД')
        users = []
        for row in DictReader(
            open('./static/data/users.csv', encoding='utf-8')
        ):
            users.append(
                User(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name']
                )
            )
        User.objects.bulk_create(users)

        logger.info('Загрузка жанров в БД')
        genres = []
        for row in DictReader(
            open('./static/data/genre.csv', encoding='utf-8')
        ):
            genres.append(
                Genre(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )
            )
        Genre.objects.bulk_create(genres)

        logger.info('Загрузка категорий в БД')
        categories = []
        for row in DictReader(
            open('./static/data/category.csv', encoding='utf-8')
        ):
            categories.append(
                Category(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )
            )
        Category.objects.bulk_create(categories)

        logger.info('Загрузка произведений в БД')
        titles = []
        for row in DictReader(
            open('./static/data/titles.csv', encoding='utf-8')
        ):
            titles.append(
                Title(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category=Category.objects.get(id=row['category'])
                )
            )
        Title.objects.bulk_create(titles)

        logger.info('Загрузка связей произведения и жанров в БД')
        titles_genres = []
        for row in DictReader(
            open('./static/data/genre_title.csv', encoding='utf-8')
        ):
            titles_genres.append(
                TitleGenre(
                    id=row['id'],
                    title_id=Title.objects.get(id=row['title_id']),
                    genre_id=Genre.objects.get(id=row['genre_id'])
                )
            )
        TitleGenre.objects.bulk_create(titles_genres)

        logger.info('Загрузка ревью в БД')
        reviews = []
        for row in DictReader(
            open('./static/data/review.csv', encoding='utf-8')
        ):
            reviews.append(
                Review(
                    id=row['id'],
                    title=Title.objects.get(id=row['title_id']),
                    text=row['text'],
                    author=User.objects.get(id=row['author']),
                    score=row['score'],
                    pub_date=datetime.strptime(
                        row['pub_date'],
                        "%Y-%m-%dT%H:%M:%S.%fZ"
                    )
                )
            )
        Review.objects.bulk_create(reviews)

        logger.info('Загрузка комментариев к ревью в БД')
        comments = []
        for row in DictReader(
            open('./static/data/comments.csv', encoding='utf-8')
        ):
            comments.append(
                Comment(
                    id=row['id'],
                    review=Review.objects.get(id=row['review_id']),
                    text=row['text'],
                    author=User.objects.get(id=row['author']),
                    pub_date=datetime.strptime(
                        row['pub_date'],
                        "%Y-%m-%dT%H:%M:%S.%fZ"
                    )
                )
            )
        Comment.objects.bulk_create(comments)
        logger.info('Загрузка в БД завершена')
