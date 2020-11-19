# Generated by Django 3.1.3 on 2020-11-19 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Logger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info', models.CharField(default='', max_length=200)),
                ('date', models.DateTimeField()),
                ('date_range', models.CharField(default='', max_length=40)),
            ],
        ),
    ]
