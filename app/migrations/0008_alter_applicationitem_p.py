# Generated by Django 4.1 on 2023-06-03 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_rename_biomass_applicationitem_biomass_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationitem',
            name='P',
            field=models.IntegerField(),
        ),
    ]
