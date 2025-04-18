# Generated by Django 5.1.7 on 2025-03-28 02:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnidadAnalisis',
            fields=[
                ('idunidad_analisis', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_unidad', models.CharField(max_length=45)),
                ('provincia', models.CharField(max_length=45)),
                ('descripcion_unidad', models.CharField(blank=True, max_length=100, null=True)),
                ('idtipo_unidad', models.ForeignKey(db_column='idtipo_unidad', on_delete=django.db.models.deletion.CASCADE, to='core.tipounidad')),
            ],
            options={
                'db_table': 'unidad_analisis',
            },
        ),
    ]
