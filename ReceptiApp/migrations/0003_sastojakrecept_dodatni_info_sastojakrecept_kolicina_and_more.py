# Generated by Django 4.2.1 on 2023-05-21 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ReceptiApp', '0002_recept_sastojak_sastojakrecept'),
    ]

    operations = [
        migrations.AddField(
            model_name='sastojakrecept',
            name='dodatni_info',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='sastojakrecept',
            name='kolicina',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='sastojakrecept',
            name='mjerna_jedinica',
            field=models.CharField(choices=[('G', 'Gram'), ('B', 'Broj'), ('K', 'Komad'), ('M', 'Kasikica'), ('V', 'Kasika'), ('S', 'Soljica'), ('O', 'Ostali')], default='B', max_length=1),
        ),
    ]
