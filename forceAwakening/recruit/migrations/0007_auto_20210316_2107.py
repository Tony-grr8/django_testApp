# Generated by Django 3.1.7 on 2021-03-16 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruit', '0006_recruit_main_sith'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Planets',
            new_name='Planet',
        ),
        migrations.RenameModel(
            old_name='Questions',
            new_name='Question',
        ),
        migrations.RenameModel(
            old_name='RecruitAnswers',
            new_name='RecruitAnswer',
        ),
        migrations.RemoveField(
            model_name='recruit',
            name='main_sith',
        ),
        migrations.RemoveField(
            model_name='recruit',
            name='shadowHand',
        ),
        migrations.AddField(
            model_name='sith',
            name='shadowHandsList',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='sith',
            name='shadowHandsNumber',
            field=models.SmallIntegerField(default=0),
        ),
    ]
