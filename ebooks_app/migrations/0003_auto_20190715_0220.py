# Generated by Django 2.2.3 on 2019-07-14 23:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ebooks_app', '0002_auto_20190715_0219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='publish_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
