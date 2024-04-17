# Generated by Django 4.2.11 on 2024-04-17 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0004_beneficiary_alternative_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='status',
            field=models.IntegerField(choices=[(0, 'En Progreso'), (1, 'Finalizada'), (2, 'Cancelada'), (3, 'Borrador')], default=0),
        ),
    ]
