# Generated by Django 2.1.2 on 2018-11-02 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0002_auto_20181101_1928'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='n_answers',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='tag',
            name='title',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]