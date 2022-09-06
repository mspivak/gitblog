# Generated by Django 4.0.6 on 2022-09-06 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0004_alter_category_slug_category_unique_blog_slug'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='category',
            name='unique_blog_slug',
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(max_length=255),
        ),
        migrations.AddConstraint(
            model_name='blog',
            constraint=models.UniqueConstraint(fields=('owner', 'slug'), name='unique_owner_slug'),
        ),
        migrations.AddConstraint(
            model_name='category',
            constraint=models.UniqueConstraint(fields=('blog', 'slug'), name='unique_blog_category_slug'),
        ),
        migrations.AddConstraint(
            model_name='post',
            constraint=models.UniqueConstraint(fields=('blog', 'slug'), name='unique_blog_post_slug'),
        ),
    ]
