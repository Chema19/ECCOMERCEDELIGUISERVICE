# Generated by Django 3.2.9 on 2022-06-17 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20220616_1737'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='nombre_completo',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
