# Generated by Django 5.1 on 2024-09-14 06:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Appmenu', '0004_carrito_nota_alter_carrito_valor_envio_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CuponDescuento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('codigo', models.CharField(max_length=50, unique=True)),
                ('porcentaje', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('valor_fijo', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('valor_minimo_compra', models.IntegerField(default=0)),
                ('fecha_inicio', models.DateTimeField()),
                ('fecha_expiracion', models.DateTimeField()),
                ('usado', models.BooleanField(default=False)),
            ],
        ),
        migrations.DeleteModel(
            name='Descuento',
        ),
        migrations.AlterField(
            model_name='carrito',
            name='nota',
            field=models.TextField(blank=True, default='', max_length=500),
        ),
        migrations.AddField(
            model_name='carrito',
            name='cupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Appmenu.cupondescuento'),
        ),
    ]
