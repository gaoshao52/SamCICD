# Generated by Django 2.0.5 on 2018-05-03 07:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cicd', '0002_auto_20180502_1627'),
    ]

    operations = [
        migrations.CreateModel(
            name='CodeServer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=64)),
                ('person_token', models.CharField(max_length=64)),
                ('myuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
