# Generated by Django 5.1.2 on 2024-10-24 12:01

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
                ('full_url', models.URLField(unique=True)),
                ('short_url', models.CharField(blank=True, db_index=True, max_length=20, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'короткая ссылка',
                'verbose_name_plural': 'Короткие ссылки',
                'ordering': ('-created_at',),
                'unique_together': {('full_url', 'short_url')},
            },
        ),
    ]