# Generated by Django 5.1.2 on 2024-11-05 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(default='image.png', upload_to='users/'),
        ),
    ]
