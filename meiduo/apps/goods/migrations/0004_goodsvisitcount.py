# Generated by Django 2.2.5 on 2019-10-19 11:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0003_auto_20191019_1503'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsVisitCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('count', models.IntegerField(default=0, verbose_name='访问量')),
                ('date', models.DateField(auto_now_add=True, verbose_name='统计日期')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsCategory', verbose_name='商品分类')),
            ],
            options={
                'db_table': 'tb_goods_visit',
                'verbose_name_plural': '统计分类商品访问量',
                'verbose_name': '统计分类商品访问量',
            },
        ),
    ]
