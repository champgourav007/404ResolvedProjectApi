# Generated by Django 4.0.3 on 2022-04-02 21:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postmodel',
            name='post_image2',
        ),
        migrations.RemoveField(
            model_name='postmodel',
            name='post_image3',
        ),
        migrations.RemoveField(
            model_name='postmodel',
            name='post_image4',
        ),
    ]
