# Generated by Django 4.1.7 on 2023-03-26 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('librarian', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='no_of_issued_books',
            field=models.PositiveIntegerField(),
        ),
    ]
