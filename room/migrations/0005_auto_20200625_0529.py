# Generated by Django 3.0.7 on 2020-06-25 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0004_auto_20200625_0510'),
    ]

    operations = [
        migrations.AddField(
            model_name='catanitem',
            name='image',
            field=models.ImageField(default=None, upload_to='uploads/catan/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chessitem',
            name='image',
            field=models.ImageField(default=None, upload_to='uploads/chess/'),
            preserve_default=False,
        ),
    ]