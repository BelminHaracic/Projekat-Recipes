# Generated by Django 4.2.1 on 2023-06-01 21:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ReceptiApp', '0011_kontakt_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='komentar',
            name='recept',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='ReceptiApp.recept'),
            preserve_default=False,
        ),
    ]
