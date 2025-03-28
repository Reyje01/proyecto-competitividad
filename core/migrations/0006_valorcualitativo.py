# Generated by Django 5.1.7 on 2025-03-28 02:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_registro'),
    ]

    operations = [
        migrations.CreateModel(
            name='ValorCualitativo',
            fields=[
                ('idregistro', models.OneToOneField(db_column='idregistro', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='core.registro')),
                ('valor_cualitativo', models.CharField(blank=True, max_length=45, null=True)),
            ],
            options={
                'db_table': 'valor_cualitativo',
            },
        ),
    ]
