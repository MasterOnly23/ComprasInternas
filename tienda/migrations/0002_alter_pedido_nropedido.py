# Generated by Django 4.1.1 on 2023-01-19 20:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='nroPedido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tienda.orden'),
        ),
    ]
