# Generated by Django 4.2.11 on 2024-04-19 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0005_alter_campaign_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='target_achieved_notified_at',
            field=models.DateTimeField(default=None, null=True, verbose_name='Notifiacacion de objetivo alcanzado'),
        ),
    ]
