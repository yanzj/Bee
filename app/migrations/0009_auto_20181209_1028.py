# Generated by Django 2.1.3 on 2018-12-09 10:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20181203_1629'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogarticle',
            name='author',
        ),
        migrations.DeleteModel(
            name='Industry',
        ),
        migrations.DeleteModel(
            name='BlogArticle',
        ),
    ]
