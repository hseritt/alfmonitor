# Generated by Django 2.0.3 on 2018-03-30 00:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0005_auto_20180328_1646'),
    ]

    operations = [
        migrations.CreateModel(
            name='JmxDumpData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_time', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='agents.Profile')),
            ],
            options={
                'ordering': ['-event_time'],
            },
        ),
    ]
