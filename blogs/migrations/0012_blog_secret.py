# Generated by Django 4.0.6 on 2022-10-19 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0011_alter_category_options_post_summary'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='secret',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
