# Generated by Django 3.1.7 on 2021-03-11 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Recruit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=42)),
                ('planet', models.CharField(max_length=42)),
                ('age', models.SmallIntegerField()),
                ('email', models.CharField(max_length=42, unique=True)),
            ],
        ),
    ]
