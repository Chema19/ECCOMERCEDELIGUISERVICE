# Generated by Django 3.2.9 on 2022-06-18 03:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_cliente_nombre_completo'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientePortal',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('estado', models.CharField(max_length=3)),
                ('fecha_creacion', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='gasto',
            name='colaboradores',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='gasto_colaborador', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='gasto',
            name='tiendas',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='gasto_tienda', to='core.tienda'),
        ),
        migrations.AddField(
            model_name='colaborador',
            name='clientesportales',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='colaborador_clienteportal', to='core.clienteportal'),
        ),
        migrations.AddField(
            model_name='compra',
            name='clientesportales',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='compra_clienteportal', to='core.clienteportal'),
        ),
        migrations.AddField(
            model_name='creditoventa',
            name='clientesportales',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='creditoventa_clienteportal', to='core.clienteportal'),
        ),
        migrations.AddField(
            model_name='entrega',
            name='clientesportales',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='entrega_clienteportal', to='core.clienteportal'),
        ),
        migrations.AddField(
            model_name='gasto',
            name='clientesportales',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='gasto_clienteportal', to='core.clienteportal'),
        ),
        migrations.AddField(
            model_name='movimiento',
            name='clientesportales',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='movimiento_clienteportal', to='core.clienteportal'),
        ),
        migrations.AddField(
            model_name='producto',
            name='clientesportales',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='producto_clienteportal', to='core.clienteportal'),
        ),
        migrations.AddField(
            model_name='venta',
            name='clientesportales',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='venta_clienteportal', to='core.clienteportal'),
        ),
    ]
