# Generated by Django 3.1.7 on 2021-03-16 19:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recruit', '0007_auto_20210316_2107'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sith',
            name='shadowHandsList',
        ),
        migrations.AddField(
            model_name='recruit',
            name='mainSith',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='recruit.sith'),
        ),
    ]
