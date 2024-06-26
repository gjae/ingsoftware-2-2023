# Generated by Django 4.2.11 on 2024-04-16 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_paymentmethodbasedinformation_paymentmethod'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentmethod',
            name='account_note',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='Agrega una nota'),
        ),
        migrations.AddField(
            model_name='paymentmethod',
            name='account_type',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Corriente'), (1, 'Ahorros'), (2, 'Otros')], default=None, null=True, verbose_name='Tipo de cuenta'),
        ),
    ]
