# Generated by Django 4.1.1 on 2022-11-24 14:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('usuarios', '0016_usuarios_delete_area'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.CharField(choices=[('None', 'None'), ('Administracion', 'Administracion'), ('Sistemas', 'Sistemas'), ('Imagen', 'Imagen'), ('RRHH', 'RRHH'), ('Abastecimiento', 'Abastecimiento'), ('Mantenimiento', 'Mantenimiento'), ('Gerentes', 'Gerentes'), ('Compras', 'Compras'), ('Legales', 'Legales'), ('Otra', 'Otra')], max_length=25, verbose_name='Area')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Usuarios',
        ),
    ]
