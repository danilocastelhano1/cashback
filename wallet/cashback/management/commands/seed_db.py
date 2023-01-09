from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Seed the database informations'

    def create_super_user(self):
        if User.objects.count() == 0:
            self.stdout.write(self.style.WARNING('Iniciando o processo de Inserção de Super User'))
            User.objects.create_superuser('admin', 'admin@example.com', 'mystrongpassword')
            self.stdout.write(self.style.SUCCESS('processo de criação de Super User Finalizado'))

    def handle(self, *args, **options):
        self.create_super_user()