# Generated by Django 3.1.1 on 2020-09-20 05:48

import apps.words.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='JapaneseSyllable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('romaji', models.CharField(db_index=True, max_length=3, unique=True, validators=[apps.words.validators.validate_eng_char], verbose_name='Romaji')),
                ('hiragana', models.CharField(db_index=True, max_length=2, validators=[apps.words.validators.validate_hiragana_char], verbose_name='Hiragana')),
                ('katakana', models.CharField(db_index=True, max_length=2, validators=[apps.words.validators.validate_katakana_char], verbose_name='Katakana')),
            ],
        ),
        migrations.CreateModel(
            name='Reading',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('romaji', models.CharField(blank=True, db_index=True, max_length=100, validators=[apps.words.validators.validate_eng_char], verbose_name='Romaji Reading')),
                ('hiragana', models.CharField(blank=True, db_index=True, max_length=50, validators=[apps.words.validators.validate_hiragana_char], verbose_name='Hiragana Reading')),
                ('katakana', models.CharField(blank=True, db_index=True, max_length=50, validators=[apps.words.validators.validate_katakana_char], verbose_name='Katakana Reading')),
                ('default_display', models.IntegerField(choices=[(1, 'Romaji'), (2, 'Hiragana'), (3, 'Katakana')], default=2, verbose_name='Default Display')),
            ],
        ),
        migrations.CreateModel(
            name='SearchTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eng_tag', models.CharField(blank=True, db_index=True, max_length=50, validators=[apps.words.validators.validate_eng_char], verbose_name='English Tag')),
                ('jap_tag', models.CharField(blank=True, db_index=True, max_length=25, validators=[apps.words.validators.validate_jap_char], verbose_name='Japanese Tag')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
            options={
                'verbose_name': 'Search Tag',
                'unique_together': {('eng_tag', 'jap_tag', 'owner')},
            },
        ),
        migrations.CreateModel(
            name='Kanji',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('character', models.CharField(max_length=1, verbose_name='Kanji')),
                ('meaning', models.TextField(blank=True, max_length=500, verbose_name='Meaning')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
                ('readings', models.ManyToManyField(blank=True, related_name='kanjis_reading', to='words.Reading', verbose_name='Readings')),
            ],
            options={
                'unique_together': {('owner', 'character')},
            },
        ),
        migrations.CreateModel(
            name='JapaneseWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=100, validators=[apps.words.validators.validate_jap_char], verbose_name='Word')),
                ('meaning', models.TextField(blank=True, max_length=1000, verbose_name='Meaning')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created Date')),
                ('kanjis', models.ManyToManyField(blank=True, to='words.Kanji', verbose_name='Kanjis')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
                ('readings', models.ManyToManyField(blank=True, to='words.Reading', verbose_name='Readings')),
                ('tags', models.ManyToManyField(blank=True, to='words.SearchTag', verbose_name='Search Tags')),
            ],
            options={
                'verbose_name': 'Japanese Word',
                'unique_together': {('owner', 'word')},
            },
        ),
        migrations.CreateModel(
            name='EnglishWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=100, validators=[apps.words.validators.validate_eng_char], verbose_name='Word')),
                ('meaning', models.TextField(blank=True, max_length=1000, verbose_name='Meaning')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created Date')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
                ('readings', models.ManyToManyField(blank=True, to='words.Reading', verbose_name='Reading')),
                ('tags', models.ManyToManyField(blank=True, to='words.SearchTag', verbose_name='Search Tags')),
            ],
            options={
                'verbose_name': 'English Word',
                'unique_together': {('owner', 'word')},
            },
        ),
    ]
