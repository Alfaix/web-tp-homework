# Generated by Django 2.1.2 on 2018-12-25 17:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import question.models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0006_auto_20181103_0945'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'verbose_name': 'answer', 'verbose_name_plural': 'answers'},
        ),
        migrations.AlterModelOptions(
            name='questionvote',
            options={'verbose_name': 'answer', 'verbose_name_plural': 'answers'},
        ),
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', question.models.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='answer',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name="answer's author"),
        ),
        migrations.AlterField(
            model_name='answer',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created date'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='is active'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.Question', verbose_name='relevant question'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='rating',
            field=models.IntegerField(default=0, verbose_name="answer's rating"),
        ),
        migrations.AlterField(
            model_name='answer',
            name='text',
            field=models.TextField(verbose_name="answer's text"),
        ),
        migrations.AlterField(
            model_name='answer',
            name='update_date',
            field=models.DateTimeField(auto_now=True, verbose_name='edit date'),
        ),
        migrations.AlterField(
            model_name='answervote',
            name='answer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.Answer', verbose_name='Voted for'),
        ),
        migrations.AlterField(
            model_name='answervote',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='voter'),
        ),
        migrations.AlterField(
            model_name='answervote',
            name='value',
            field=models.IntegerField(verbose_name='Vote value'),
        ),
        migrations.AlterField(
            model_name='question',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name="question's author"),
        ),
        migrations.AlterField(
            model_name='question',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created date'),
        ),
        migrations.AlterField(
            model_name='question',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='is active'),
        ),
        migrations.AlterField(
            model_name='question',
            name='n_answers',
            field=models.IntegerField(default=0, verbose_name='number of answers'),
        ),
        migrations.AlterField(
            model_name='question',
            name='rating',
            field=models.IntegerField(default=0, verbose_name="question's rating"),
        ),
        migrations.AlterField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(to='question.Tag', verbose_name='relevant tags'),
        ),
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.TextField(verbose_name="question's text"),
        ),
        migrations.AlterField(
            model_name='question',
            name='title',
            field=models.CharField(max_length=200, verbose_name="question's title"),
        ),
        migrations.AlterField(
            model_name='question',
            name='update_date',
            field=models.DateTimeField(auto_now=True, verbose_name='edit date'),
        ),
        migrations.AlterField(
            model_name='questionvote',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='voter'),
        ),
        migrations.AlterField(
            model_name='questionvote',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.Question', verbose_name='voted for'),
        ),
        migrations.AlterField(
            model_name='questionvote',
            name='value',
            field=models.IntegerField(verbose_name='vote value'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='n_posts',
            field=models.IntegerField(default=0, verbose_name='number of posts'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='title',
            field=models.CharField(max_length=200, unique=True, verbose_name='tag name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='rating',
            field=models.IntegerField(default=0, verbose_name='rating'),
        ),
        migrations.AlterField(
            model_name='user',
            name='upload',
            field=models.ImageField(default='default.png', upload_to='', verbose_name='avatar'),
        ),
    ]
