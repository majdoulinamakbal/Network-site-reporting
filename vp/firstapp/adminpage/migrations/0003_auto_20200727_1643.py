# Generated by Django 3.0.8 on 2020-07-27 16:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminpage', '0002_auto_20200727_1636'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logfile',
            name='SerialNo',
        ),
        migrations.AddField(
            model_name='logfile',
            name='SerialNo',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='adminpage.Serial', verbose_name='serial Nos'),
            preserve_default=False,
        ),
    ]
