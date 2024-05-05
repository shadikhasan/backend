# In your_app/management/commands/create_superuser.py

from django.core.management.base import BaseCommand
from core.models import CustomUser

class Command(BaseCommand):
    help = 'Creates a superuser if not already exists'

    def handle(self, *args, **kwargs):
        if CustomUser.objects.exists():
            self.stdout.write(self.style.SUCCESS("Superuser not created because users already exist."))
            return

        username = 'admin2'
        email = 'admin2@gmail.com'
        password = 'admin2'

        user = CustomUser.objects.create_superuser(username=username, email=email, password=password)

        self.stdout.write(self.style.SUCCESS('\n' + '*' * 40))
        self.stdout.write(self.style.SUCCESS(' Superuser created successfully '))
        self.stdout.write(self.style.SUCCESS('*' * 40 + '\n'))
        self.stdout.write(self.style.SUCCESS(f' {self.style.HTTP_INFO("Username:")}   {username}'))
        self.stdout.write(self.style.SUCCESS(f' {self.style.HTTP_INFO("Email:")}      {email}'))
        self.stdout.write(self.style.SUCCESS(f' {self.style.HTTP_INFO("Password:")}   {password}\n'))
        self.stdout.write(self.style.SUCCESS('*' * 40 + '\n'))
