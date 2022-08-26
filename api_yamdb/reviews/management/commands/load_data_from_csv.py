from csv import DictReader
from django.core.management import BaseCommand

from ...models import Genre


class Command(BaseCommand):
    help = "Loads data from genres.csv"

    def handle(self, *args, **options):
        print("Loading genres data")
        print("Delete genres from db")
        Genre.objects.all().delete()
        for row in DictReader(
            open('./static/data/genre.csv', encoding='utf-8')
        ):
            genre = Genre(name=row['name'], slug=row['slug'])
            genre.save()
        print("Жанры занесены в БД")
