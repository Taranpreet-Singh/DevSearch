# Generated by Django 4.0.5 on 2022-06-30 16:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0011_alter_review_body'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-vote_ratio', 'vote_total', 'title']},
        ),
    ]