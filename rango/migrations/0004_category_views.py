# Generated by Django 2.1.5 on 2022-03-07 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0003_category_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
