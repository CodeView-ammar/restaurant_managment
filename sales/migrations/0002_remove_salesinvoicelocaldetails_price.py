# Generated by Django 3.2.6 on 2023-09-02 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salesinvoicelocaldetails',
            name='price',
        ),
    ]
