import random
from django.core.management.base import BaseCommand

from django.contrib.admin.utils  import flatten # 2차원 배열 안의 값을 가져올 때 사용 가능
from django_seed                 import Seed

from lists                       import models as list_models
from rooms                       import models as room_models
from users                       import models as user_models

NAME = 'lists'

class Command(BaseCommand):

    help = f'this command create {NAME}!'

    def add_arguments(self, parser):
        parser.add_argument("--number", default=1, type=int, help=f"How many {NAME} do you want to create?")

    def handle(self, *args, **options):
        number = options.get('number')
        seeder = Seed.seeder()

        all_users = [i for i in user_models.User.objects.all()]
        rooms     = room_models.Room.objects.all()

        seeder.add_entity(
            list_models.List, 
            number,
            {
            "user" : next(all_users),
            })

        created_rooms = seeder.execute()
        cleaned       = flatten(list(created_rooms.values()))
        for pk in cleaned:
            list_model = list_models.List.objects.get(pk=pk)
            
            to_add     = rooms[random.randint(0,5): random.randint(6,30)] # 랜덤하게 방 인스턴스를 돌려줌

            list_model.rooms.add(*to_add) # 결속 되어 있는 쿼리셋을 확~ 풀어버림 그럼 내뷰 value만 쏙 나옴
            # 참고 할 만한 사이트 https://mingrammer.com/understanding-the-asterisk-of-python/

        self.stdout.write(self.style.SUCCESS(f"성공적으로 {number}개의 {NAME}가 생성되었습니다."))