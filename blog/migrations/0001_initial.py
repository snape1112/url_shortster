# Generated by Django 3.2.13 on 2022-06-08 21:20

from django.db import migrations, models
import jsonfield.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.IntegerField(default=0, help_text='The id of post', primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(blank=True, help_text='Who wrote this post', max_length=50, null=True, verbose_name='Author')),
                ('authorId', models.IntegerField(blank=True, default=0, help_text='ID of author', null=True, verbose_name='Author ID')),
                ('likes', models.IntegerField(blank=True, default=0, help_text='Number of likes', null=True, verbose_name='Likes')),
                ('popularity', models.DecimalField(blank=True, decimal_places=2, default=0, help_text='Popularity of post', max_digits=18, null=True, verbose_name='Popularity')),
                ('reads', models.IntegerField(blank=True, default=0, help_text='Number of reads', null=True, verbose_name='Reads')),
                ('tags', jsonfield.fields.JSONField(blank=True, help_text='List of tags. Ex: ["tech", "health]', null=True, verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'BlogPost',
                'verbose_name_plural': 'BlogPosts',
            },
        ),
        migrations.CreateModel(
            name='TagHistory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='The unique identifier of the instance this object belongs to. Mandatory, unless a new instance to create is given.', primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, help_text='Name of tag', max_length=50, null=True, verbose_name='Name')),
            ],
        ),
    ]