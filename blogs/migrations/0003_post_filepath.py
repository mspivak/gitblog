# Generated by Django 4.0.6 on 2022-09-02 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_category_post_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='filepath',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
