# Generated by Django 3.0 on 2019-12-20 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rehsponse', '0017_remove_rehsponse_reply'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rehsponse',
            name='height_field',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='rehsponse',
            name='width_field',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
