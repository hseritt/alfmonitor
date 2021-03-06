# Generated by Django 2.0.3 on 2018-03-28 22:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0004_auto_20180328_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='admins',
            field=models.ManyToManyField(blank=True, help_text='Alert emails are sent to selected users. Use control or command (on Mac) to select multiple users.', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profile',
            name='agent',
            field=models.ForeignKey(help_text='*Required', on_delete=django.db.models.deletion.PROTECT, to='agents.Agent'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='name',
            field=models.CharField(help_text='*Required', max_length=50, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='protocol',
            field=models.CharField(choices=[('N/A', 'N/A'), ('TCP', 'TCP'), ('UDP', 'UDP')], default='N/A', help_text='For Ping agent, default is TCP', max_length=20, verbose_name='Protocol'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='uri',
            field=models.CharField(help_text='*Required Ex: localhost:22 or localhost:5432/mydb', max_length=1000, verbose_name='URI'),
        ),
    ]
