# Generated by Django 5.1.4 on 2024-12-11 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='highlights',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='services',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='specifications',
            field=models.TextField(),
        ),
    ]