# Generated by Django 3.1.1 on 2020-10-17 17:04

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
                ('id',
                 models.AutoField(auto_created=True,
                                  primary_key=True,
                                  serialize=False,
                                  verbose_name='ID')),
                ('romaji',
                 models.CharField(
                     db_index=True,
                     max_length=3,
                     unique=True,
                     validators=[apps.words.validators.validate_eng_char],
                     verbose_name='Romaji')),
                ('hiragana',
                 models.CharField(
                     db_index=True,
                     max_length=2,
                     validators=[apps.words.validators.validate_hiragana_char],
                     verbose_name='Hiragana')),
                ('katakana',
                 models.CharField(
                     db_index=True,
                     max_length=2,
                     validators=[apps.words.validators.validate_katakana_char],
                     verbose_name='Katakana')),
            ],
        ),
        migrations.CreateModel(
            name='JapaneseWord',
            fields=[
                ('id',
                 models.AutoField(auto_created=True,
                                  primary_key=True,
                                  serialize=False,
                                  verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('word',
                 models.CharField(
                     max_length=100,
                     validators=[apps.words.validators.validate_jap_char],
                     verbose_name='Word')),
                ('meaning',
                 models.TextField(blank=True,
                                  max_length=1000,
                                  verbose_name='Meaning')),
                ('created_at',
                 models.DateTimeField(auto_now_add=True,
                                      db_index=True,
                                      verbose_name='Created Date')),
            ],
            options={
                'verbose_name': 'Japanese Word',
            },
        ),
        migrations.CreateModel(
            name='JPQuiz',
            fields=[
                ('id',
                 models.AutoField(auto_created=True,
                                  primary_key=True,
                                  serialize=False,
                                  verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('completed_at',
                 models.DateTimeField(blank=True,
                                      null=True,
                                      verbose_name='Completed At')),
                ('question_index',
                 models.PositiveIntegerField(default=0,
                                             verbose_name='Question Index')),
                ('owner',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to=settings.AUTH_USER_MODEL,
                                   verbose_name='Owner')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Reading',
            fields=[
                ('id',
                 models.AutoField(auto_created=True,
                                  primary_key=True,
                                  serialize=False,
                                  verbose_name='ID')),
                ('romaji',
                 models.CharField(
                     blank=True,
                     db_index=True,
                     max_length=100,
                     validators=[apps.words.validators.validate_eng_char],
                     verbose_name='Romaji Reading')),
                ('hiragana',
                 models.CharField(
                     blank=True,
                     db_index=True,
                     max_length=50,
                     validators=[apps.words.validators.validate_hiragana_char],
                     verbose_name='Hiragana Reading')),
                ('katakana',
                 models.CharField(
                     blank=True,
                     db_index=True,
                     max_length=50,
                     validators=[apps.words.validators.validate_katakana_char],
                     verbose_name='Katakana Reading')),
                ('default_display',
                 models.IntegerField(choices=[(1, 'Romaji'), (2, 'Hiragana'),
                                              (3, 'Katakana')],
                                     default=2,
                                     verbose_name='Default Display')),
            ],
        ),
        migrations.CreateModel(
            name='SearchTag',
            fields=[
                ('id',
                 models.AutoField(auto_created=True,
                                  primary_key=True,
                                  serialize=False,
                                  verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('eng_tag',
                 models.CharField(
                     blank=True,
                     db_index=True,
                     max_length=50,
                     validators=[apps.words.validators.validate_eng_char],
                     verbose_name='English Tag')),
                ('jap_tag',
                 models.CharField(
                     blank=True,
                     db_index=True,
                     max_length=25,
                     validators=[apps.words.validators.validate_jap_char],
                     verbose_name='Japanese Tag')),
                ('owner',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to=settings.AUTH_USER_MODEL,
                                   verbose_name='Owner')),
            ],
            options={
                'verbose_name': 'Search Tag',
                'unique_together': {('eng_tag', 'jap_tag', 'owner')},
            },
        ),
        migrations.CreateModel(
            name='Kanji',
            fields=[
                ('id',
                 models.AutoField(auto_created=True,
                                  primary_key=True,
                                  serialize=False,
                                  verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('character',
                 models.CharField(max_length=1, verbose_name='Kanji')),
                ('meaning',
                 models.TextField(blank=True,
                                  max_length=500,
                                  verbose_name='Meaning')),
                ('owner',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to=settings.AUTH_USER_MODEL,
                                   verbose_name='Owner')),
                ('readings',
                 models.ManyToManyField(blank=True,
                                        related_name='kanjis_reading',
                                        to='words.Reading',
                                        verbose_name='Readings')),
            ],
            options={
                'unique_together': {('owner', 'character')},
            },
        ),
        migrations.CreateModel(
            name='JPQuizTemplate',
            fields=[
                ('id',
                 models.AutoField(auto_created=True,
                                  primary_key=True,
                                  serialize=False,
                                  verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title',
                 models.CharField(max_length=100,
                                  unique=True,
                                  verbose_name='Title')),
                ('frequency',
                 models.PositiveIntegerField(
                     default=7, verbose_name='Frequency in days')),
                ('number_of_questions',
                 models.PositiveIntegerField(
                     default=20, verbose_name='Number of questions')),
                ('owner',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to=settings.AUTH_USER_MODEL,
                                   verbose_name='Owner')),
                ('words',
                 models.ManyToManyField(to='words.JapaneseWord',
                                        verbose_name='Words')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='JPQuizQuestion',
            fields=[
                ('id',
                 models.AutoField(auto_created=True,
                                  primary_key=True,
                                  serialize=False,
                                  verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('index', models.PositiveIntegerField(verbose_name='Index')),
                ('choices',
                 models.ManyToManyField(related_name='questions_as_choices',
                                        to='words.JapaneseWord',
                                        verbose_name='Choices')),
                ('owner',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to=settings.AUTH_USER_MODEL,
                                   verbose_name='Owner')),
                ('quiz',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to='words.jpquiz',
                                   verbose_name='Quiz')),
                ('right_answer',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   related_name='questions_as_answer',
                                   to='words.japaneseword',
                                   verbose_name='Right answer')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='JPQuizAnswer',
            fields=[
                ('id',
                 models.AutoField(auto_created=True,
                                  primary_key=True,
                                  serialize=False,
                                  verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('right', models.BooleanField(verbose_name='Right Answer')),
                ('answer',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to='words.japaneseword',
                                   verbose_name='Answer')),
                ('owner',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to=settings.AUTH_USER_MODEL,
                                   verbose_name='Owner')),
                ('question',
                 models.OneToOneField(
                     on_delete=django.db.models.deletion.CASCADE,
                     related_name='answer',
                     to='words.jpquizquestion',
                     verbose_name='Question')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='jpquiz',
            name='quiz_template',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='words.jpquiztemplate',
                verbose_name='Quiz Template'),
        ),
        migrations.AddField(
            model_name='japaneseword',
            name='kanjis',
            field=models.ManyToManyField(blank=True,
                                         to='words.Kanji',
                                         verbose_name='Kanjis'),
        ),
        migrations.AddField(
            model_name='japaneseword',
            name='owner',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name='Owner'),
        ),
        migrations.AddField(
            model_name='japaneseword',
            name='readings',
            field=models.ManyToManyField(blank=True,
                                         to='words.Reading',
                                         verbose_name='Readings'),
        ),
        migrations.AddField(
            model_name='japaneseword',
            name='tags',
            field=models.ManyToManyField(blank=True,
                                         to='words.SearchTag',
                                         verbose_name='Search Tags'),
        ),
        migrations.AlterUniqueTogether(
            name='japaneseword',
            unique_together={('owner', 'word')},
        ),
        migrations.CreateModel(
            name='EnglishWord',
            fields=[
                ('id',
                 models.AutoField(auto_created=True,
                                  primary_key=True,
                                  serialize=False,
                                  verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('word',
                 models.CharField(
                     max_length=100,
                     validators=[apps.words.validators.validate_eng_char],
                     verbose_name='Word')),
                ('meaning',
                 models.TextField(blank=True,
                                  max_length=1000,
                                  verbose_name='Meaning')),
                ('created_at',
                 models.DateTimeField(auto_now_add=True,
                                      db_index=True,
                                      verbose_name='Created Date')),
                ('owner',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to=settings.AUTH_USER_MODEL,
                                   verbose_name='Owner')),
                ('readings',
                 models.ManyToManyField(blank=True,
                                        to='words.Reading',
                                        verbose_name='Reading')),
                ('tags',
                 models.ManyToManyField(blank=True,
                                        to='words.SearchTag',
                                        verbose_name='Search Tags')),
            ],
            options={
                'verbose_name': 'English Word',
                'unique_together': {('owner', 'word')},
            },
        ),
    ]
