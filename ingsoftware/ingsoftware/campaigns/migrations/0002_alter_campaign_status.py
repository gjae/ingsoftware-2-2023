# Generated by Django 4.2.11 on 2024-04-11 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='status',
            field=models.IntegerField(choices=[(0, 'En Progreso'), (1, 'Finalizada'), (2, 'Cancelada'), (3, 'Borrador')], default=3),
        ),
    ]