# Generated by Django 4.2.1 on 2023-06-18 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookfeedback',
            old_name='autor',
            new_name='author',
        ),
    ]