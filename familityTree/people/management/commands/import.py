from csv import reader
from datetime import datetime
from django.core.management.base import BaseCommand
from people.models import People


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('file_path', nargs='+', type=str)

    '''
    名前,読み仮名,誕生日,死去日,性別,父親,母親
    '''
    def handle(self, *args, **options):
        for file_path in options['file_path']:
            with open(file_path, newline='') as csv_file:
                csv_reader = reader(
                    csv_file,
                    delimiter=','
                )
                for row in csv_reader:
                    name = row[0]
                    kana = row[1]
                    sex = row[4] == '0'
                    birthday = None
                    try:
                        birthday = datetime.strptime(row[2], '%Y.%m.%d')
                    except ValueError:
                        pass
                    dieday = None
                    try:
                        dieday = datetime.strptime(row[3], '%Y.%m.%d')
                    except ValueError:
                        pass
                    people = People(name=name, name_yomi=kana,
                                    birthday=birthday, dieday=dieday, sex=sex)
                    parent1 = row[5]
                    parent2 = row[6]
                    if len(parent1) > 0 and len(parent2):
                        people1 = People.objects.get(name=parent1)
                        people2 = People.objects.get(name=parent2)
                        if people1.sex:
                            people.father = people1
                            people.mother = people2
                        else:
                            people.father = people2
                            people.mother = people1
                    else:
                        people.marriage_flg = True
                    people.save()
