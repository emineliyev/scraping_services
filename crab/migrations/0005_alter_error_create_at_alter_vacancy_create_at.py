# Generated by Django 4.0.5 on 2022-07-03 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crab', '0004_alter_error_create_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='error',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Xətanın tarixi'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Yükləmə tarixi'),
        ),
    ]
