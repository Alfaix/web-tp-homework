# Generated by Django 2.1.2 on 2018-11-01 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'verbose_name': 'question', 'verbose_name_plural': 'questions'},
        ),
        migrations.AlterField(
            model_name='answer',
            name='rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='question',
            name='rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterUniqueTogether(
            name='answervote',
            unique_together={('author', 'answer')},
        ),
        migrations.AlterUniqueTogether(
            name='questionvote',
            unique_together={('author', 'question')},
        ),
    ]