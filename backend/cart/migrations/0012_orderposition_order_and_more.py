# Generated by Django 4.2.1 on 2023-06-18 17:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_alter_positions_image'),
        ('cart', '0011_rename_позиция_orderposition_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderposition',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='positions', to='cart.orders', verbose_name='Orders'),
        ),
        migrations.AlterUniqueTogether(
            name='orderposition',
            unique_together={('position', 'order')},
        ),
        migrations.DeleteModel(
            name='PositionInOrder',
        ),
    ]
