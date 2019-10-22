from django import http
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, redirect

from django.views import View

from contents.models import ContentCategory
from contents.utils import get_categories
from goods import models
from goods.utils import get_breadcrumb
from verifications import constants


class IndexView(View):
    """首页广告"""

    def get(self, request):
        """提供首页广告界面"""
        # 查询商品频道和分类
        categories = get_categories()

        # 广告数据
        contents = {}
        content_categories = ContentCategory.objects.all()
        for cat in content_categories:
            contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')

        # 渲染模板的上下文
        context = {
            'categories': categories,
            'contents': contents,
        }
        return render(request, 'index.html', context)
