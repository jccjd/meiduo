# Generated by Django 2.2.5 on 2019-10-22 02:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('trade_id', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='支付编号')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.OrderInfo', verbose_name='订单')),
            ],
            options={
                'verbose_name_plural': '支付信息',
                'db_table': 'tb_payment',
                'verbose_name': '支付信息',
            },
        ),
    ]