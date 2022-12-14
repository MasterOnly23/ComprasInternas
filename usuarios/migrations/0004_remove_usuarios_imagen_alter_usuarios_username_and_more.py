# Generated by Django 4.1.1 on 2022-10-24 17:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_alter_usuarios_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuarios',
            name='imagen',
        ),
        migrations.AlterField(
            model_name='usuarios',
            name='username',
            field=models.CharField(max_length=50, verbose_name='Repetir email'),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, default='default.png', upload_to='avatares')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
