# Generated by Django 2.1.2 on 2018-11-02 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0003_auto_20181102_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='upload',
            field=models.ImageField(upload_to='static/media'),
        ),
    ]
