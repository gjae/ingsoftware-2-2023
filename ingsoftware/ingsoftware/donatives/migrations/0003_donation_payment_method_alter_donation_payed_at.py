# Generated by Django 4.2.11 on 2024-04-15 04:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_paymentmethodbasedinformation_paymentmethod'),
        ('donatives', '0002_donation_payed_at_donation_transaction_code_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='payment_method',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='donatives', to='users.paymentmethod', verbose_name='donatives'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='payed_at',
            field=models.DateTimeField(default=None, null=True, verbose_name='Fecha en la que se realizó la transacción'),
        ),
    ]
