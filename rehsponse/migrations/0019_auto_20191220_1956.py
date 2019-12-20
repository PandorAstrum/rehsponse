# Generated by Django 3.0 on 2019-12-20 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rehsponse', '0018_auto_20191220_1707'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='responded_by',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='username',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
    ]
