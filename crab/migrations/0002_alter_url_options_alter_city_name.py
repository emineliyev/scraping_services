# Generated by Django 4.0.5 on 2022-07-01 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crab', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='url',
            options={'verbose_name': 'Url', 'verbose_name_plural': 'Url'},
        ),
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(max_length=60, unique=True, verbose_name='Şəhər adı'),
        ),
    ]
