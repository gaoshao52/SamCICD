# Generated by Django 2.0.5 on 2018-05-08 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cicd', '0008_auto_20180507_1714'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuildProjectAndBranch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('git_repo', models.URLField(unique=True)),
                ('branch', models.CharField(max_length=32)),
                ('group', models.CharField(max_length=32)),
            ],
        ),
        migrations.AlterModelOptions(
            name='codeserver',
            options={'verbose_name': 'GitLab服务器'},
        ),
        migrations.AlterField(
            model_name='buildtools',
            name='name',
            field=models.CharField(max_length=32, unique=True, verbose_name='工程名称'),
        ),
    ]
