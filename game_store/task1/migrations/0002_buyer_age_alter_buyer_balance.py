# Generated by Django 5.1.1 on 2024-09-13 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyer',
            name='age',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='buyer',
            name='balance',
            field=models.DecimalField(decimal_places=2, max_digits=12),
        ),
    ]
