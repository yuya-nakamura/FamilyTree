from csv import reader
from django.core.management.base import BaseCommand
from people.models import People, Marriage


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('file_path', nargs='+', type=str)

    def handle(self, *args, **options):
        for file_path in options['file_path']:
            with open(file_path, newline='') as csv_file:
                csv_reader = reader(
                    csv_file,
                    delimiter=','
                )
                for row in csv_reader:
                    parent1 = row[0]
                    parent2 = row[1]
                    name = row[2]
                    print(parent1)
                    people1 = People.objects.get(name=parent1)
                    people2 = People.objects.get(name=parent2)
                    marry = Marriage(label=name)
                    if people1.sex:
                        marry.husband = people1
                        marry.wife = people2
                    else:
                        marry.husband = people2
                        marry.wife = people1
                    marry.save()
