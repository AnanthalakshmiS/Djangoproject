# Generated by Django 2.0 on 2020-04-24 08:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_remove_users_phonenumber'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Customer',
        ),
        migrations.DeleteModel(
            name='Users',
        ),
    ]