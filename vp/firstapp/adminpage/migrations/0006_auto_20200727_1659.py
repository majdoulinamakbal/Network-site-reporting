# Generated by Django 3.0.8 on 2020-07-27 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpage', '0005_auto_20200727_1657'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logfile',
            name='SerialNo',
        ),
        migrations.AddField(
            model_name='logfile',
            name='SerialNo',
            field=models.ManyToManyField(to='adminpage.Serial', verbose_name='Serial Numbers'),
        ),
    ]
