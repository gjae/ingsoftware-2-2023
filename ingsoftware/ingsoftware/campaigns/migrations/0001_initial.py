# Generated by Django 4.2.11 on 2024-04-11 02:33

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import ingsoftware.campaigns.models
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Beneficiary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('Beneficiary', models.CharField(verbose_name='A quien va dirigido')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('title', models.CharField(db_index=True, max_length=95, verbose_name='Título de la campaña')),
                ('summary', models.TextField(blank=True, default='', verbose_name='Resumen de la campaña')),
                ('body', models.TextField(verbose_name='Descripción de la campaña')),
                ('total_collected', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Total recaudado')),
                ('total_donations', models.PositiveBigIntegerField(default=0, verbose_name='Donaciones recaudadas')),
                ('tags', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=32), db_index=True, help_text='Etiquetas de la publicación', size=32)),
                ('img_frontpage', models.ImageField(upload_to=ingsoftware.campaigns.models.user_directory_path, verbose_name='Imagen de portada')),
                ('target', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Meta de recaudació')),
                ('date_target', models.DateTimeField(default=None, null=True, verbose_name='Fecha limite de recaudación')),
                ('status', model_utils.fields.StatusField(choices=[(0, 'En Progreso'), (1, 'Finalizada'), (2, 'Cancelada'), (3, 'Borrador')], default=3, max_length=100, no_check_for_status=True)),
                ('beneficiary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='campaigns', to='campaigns.beneficiary')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('title', models.CharField(db_index=True, max_length=77, verbose_name='Título de la categoría')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CampaignUserFollowing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_followers', to='campaigns.campaign')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='campaigns_follows', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='campaign',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='campaigns', to='campaigns.category'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='campaigns', to=settings.AUTH_USER_MODEL),
        ),
    ]