# Generated by Django 3.1.7 on 2021-03-12 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recruit', '0003_sith'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recruit',
            name='planet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recruit.planets'),
        ),
    ]