# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-17 20:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('words', '0004_japaneseword_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='japaneseword',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created Date'),
        ),
    ]
