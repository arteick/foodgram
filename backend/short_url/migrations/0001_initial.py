# Generated by Django 4.2.16 on 2024-10-26 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ShortUrl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_url', models.URLField(unique=True, verbose_name='Полная ссылка')),
                ('short_url', models.CharField(blank=True, db_index=True, max_length=250, unique=True, verbose_name='Короткая ссылка')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активна')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'короткая ссылка',
                'verbose_name_plural': 'Таблица ссылок',
                'ordering': ('-created_at',),
                'unique_together': {('full_url', 'short_url')},
            },
        ),
    ]
