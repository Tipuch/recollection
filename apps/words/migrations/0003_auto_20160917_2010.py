# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-17 20:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('words', '0002_auto_20160917_0358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='japaneseword',
            name='kanjis',
            field=models.ManyToManyField(blank=True, related_name='words', to='words.Kanji', verbose_name='Kanjis'),
        ),
    ]
