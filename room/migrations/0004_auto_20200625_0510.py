# Generated by Django 3.0.7 on 2020-06-25 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0003_auto_20200625_0448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catan',
            name='game_name',
            field=models.CharField(db_index=True, default='Catan', max_length=32, verbose_name='game_name'),
        ),
        migrations.AlterField(
            model_name='chess',
            name='game_name',
            field=models.CharField(db_index=True, default='Chess', max_length=32, verbose_name='game_name'),
        ),
    ]
