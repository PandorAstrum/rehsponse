# Generated by Django 3.0 on 2019-12-14 10:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rehsponse', '0008_rehsponse_loved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rehsponse',
            name='loved',
            field=models.ManyToManyField(blank=True, related_name='loved_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
