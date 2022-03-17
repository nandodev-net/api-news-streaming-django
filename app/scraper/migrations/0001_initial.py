# Generated by Django 4.0.2 on 2022-03-17 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='Category name')),
            ],
        ),
        migrations.CreateModel(
            name='ArticleHeadline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scraped_date', models.DateTimeField(auto_created=True, auto_now_add=True, verbose_name='Scraped date')),
                ('title', models.TextField(max_length=200, verbose_name='Title')),
                ('date', models.DateTimeField(null=True, verbose_name='Publication name')),
                ('excerpt', models.TextField(default='Excerpt', max_length=300, null=True)),
                ('image', models.URLField(max_length=300, verbose_name='Image source')),
                ('source', models.CharField(choices=[('la_patilla', 'La Patilla'), ('efecto_cocuyo', 'Efecto cocuyo'), ('unknown', 'unknown')], default='unknown', max_length=30)),
                ('url', models.URLField(max_length=300, unique=True, verbose_name='Full article url')),
                ('relevance', models.BooleanField(default=None, null=True, verbose_name='Relevance')),
                ('categories', models.ManyToManyField(to='scraper.ArticleCategory')),
            ],
        ),
    ]
