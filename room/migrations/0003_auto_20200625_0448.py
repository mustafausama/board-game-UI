# Generated by Django 3.0.7 on 2020-06-25 01:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0002_auto_20200625_0445'),
    ]

    operations = [
        migrations.AddField(
            model_name='catangrid',
            name='game',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='catan_grid', to='room.Catan'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chessgrid',
            name='game',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='chess_grid', to='room.Chess'),
            preserve_default=False,
        ),
    ]