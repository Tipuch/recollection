# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-17 23:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('words', '0007_auto_20160917_2351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reading',
            name='default_display',
            field=models.IntegerField(choices=[(1, 'Romaji'), (2, 'Hiragana'), (3, 'Katakana')], default=1, verbose_name='Default Display'),
        ),
    ]
