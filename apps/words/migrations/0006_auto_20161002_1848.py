# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-02 18:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('words', '0005_auto_20161001_1945'),
    ]

    operations = [
        migrations.AddField(
            model_name='englishword',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='eng_words_user', to=settings.AUTH_USER_MODEL, verbose_name='Owner'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='japaneseword',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='jap_words_user', to=settings.AUTH_USER_MODEL, verbose_name='Owner'),
            preserve_default=False,
        ),
    ]
