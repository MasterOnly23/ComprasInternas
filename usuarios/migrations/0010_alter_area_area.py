# Generated by Django 4.1.1 on 2022-11-18 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0009_alter_area_area'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='area',
            field=models.CharField(choices=[('None', 'None'), ('Administracion', 'Administracion'), ('Sistemas', 'Sistemas'), ('Imagen', 'Imagen'), ('RRHH', 'RRHH'), ('Abastecimiento', 'Abastecimiento'), ('Mantenimiento', 'Mantenimiento'), ('Gerentes', 'Gerentes'), ('Compras', 'Compras'), ('Legales', 'Legales'), ('Otra', 'Otra')], max_length=25, verbose_name='Area'),
        ),
    ]
