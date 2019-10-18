# Generated by Django 2.2.6 on 2019-10-15 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.CharField(max_length=200)),
                ('invoice_date', models.DateTimeField(verbose_name='date created of invoice')),
                ('client_name', models.CharField(max_length=200)),
                ('total_ttc', models.IntegerField(default=0)),
                ('total_tva', models.IntegerField(default=0)),
            ],
        ),
    ]
