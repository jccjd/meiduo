#!/usr/bin/env python3


import sys

from settings import dev

sys.path.insert(0, '../')

import os

if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'meiduo.settings.dev'

import django
django.setup()

from django.template import loader

from django.conf import settings

# fira code
from goods import models
from contents.utils import get_categories
from goods.utils import get_breadcrumb


def generate_static_sku_detail_html(sku_id):

    sku = models.SKU.objects.get(id=sku_id)

    categories = get_categories()
    breadcrumb = get_breadcrumb(sku.category)

    sku_specs = sku.specs.order_by('spec_id')
    sku_key = []
    for spec in sku_specs:
        sku_key.append(spec.option.id)
    skus = sku.spu.sku_set.all()
    spec_sku_map = {}
    for s in skus:
        s_specs = s.specs.order_by('spec_id')
        key = []
        for spec in s_specs:
            key.append(spec.option.id)
            spec_sku_map[tuple(key)] = s.id
    goods_specs = sku.spu.specs.order_by('id')
    if len(sku_key) < len(goods_specs):
        return
    for index, spec in enumerate(goods_specs):
        key = sku_key[:]
        spec_options = spec.options.all()
        for option in spec_options:
            key[index] = option.id
            option.sku_id = spec_sku_map.get(tuple(key))
        spec.spec_options = spec_options


    context = {
        'categories': categories,
        'breadcrumb': breadcrumb,
        'sku': sku,
        'specs': goods_specs,
    }

    template = loader.get_template('detail.html')
    html_text = template.render(context)
    file_path = os.path.join(dev.STATICFILES_DIRS[0], 'detail/'+str(sku_id)+'.html')

    with open(file_path, 'w') as f:
        f.write(html_text)

if __name__ == '__main__':
    skus = models.SKU.objects.all()
    for sku in skus:
        print(sku.id)
        generate_static_sku_detail_html(sku.id)




