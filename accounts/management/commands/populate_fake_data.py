# app_name/management/commands/populate_fake_data.py
from django.core.management.base import BaseCommand
from accounts.models import Person
import random

class Command(BaseCommand):
    help = 'Populates the database with fake data for the DataTables example'

    def handle(self, *args, **kwargs):
        fake_names = ['Alice', 'Bob', 'Charlie', 'David', 'Eva', 'Frank', 'Grace']
        for _ in range(20):
            name = random.choice(fake_names)
            age = random.randint(20, 50)
            Person.objects.create(name=name, age=age)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with fake data!'))
