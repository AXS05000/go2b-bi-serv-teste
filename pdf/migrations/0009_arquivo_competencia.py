# Generated by Django 4.1.9 on 2023-07-01 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdf', '0008_arquivo'),
    ]

    operations = [
        migrations.AddField(
            model_name='arquivo',
            name='competencia',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
