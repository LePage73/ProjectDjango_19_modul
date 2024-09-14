from django.db import models

# Create your models here.

CHOICE_GENRE = [
    ('FPS', 'Стрелялка'),
    ('RPG', 'Ролевая игра'),
    ('RTS', 'Стратегия в реальном времени'),
    ('ARC', 'Аркада'),
    ('SIM', 'Симулятор'),
    ('ADV', 'Приключения'),
]

class Buyer(models.Model):
    username = models.CharField(max_length=30)
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    age = models.IntegerField(default=1)
    def __str__(self):
        return self.username
    pass

class Game(models.Model):
    title = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=7, decimal_places=2)
    size = models.DecimalField(max_digits=12, decimal_places=3)
    description = models.TextField()
    age_limited = models.BooleanField(default=False)
    buyer = models.ManyToManyField(Buyer, related_name='games')
    genre = models.CharField(choices=CHOICE_GENRE, max_length=3)
    def __str__(self):
        return self.title
    pass

