# Generated by Django 2.1.2 on 2018-11-03 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0005_auto_20181102_1348'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='upload',
            field=models.ImageField(upload_to=''),
        ),
    ]