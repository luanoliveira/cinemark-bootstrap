# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-29 13:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filmes', '0002_auto_20161029_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filme',
            name='ano_lancamento',
            field=models.DateField(),
        ),
    ]