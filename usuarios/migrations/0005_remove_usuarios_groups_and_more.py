# Generated by Django 4.1.1 on 2022-11-11 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0004_remove_usuarios_imagen_alter_usuarios_username_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuarios',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='usuarios',
            name='user_permissions',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
        migrations.DeleteModel(
            name='Usuarios',
        ),
    ]