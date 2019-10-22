---
data: 2019-10-19
---

### Q&A

> **Q:**
关于路由问题

django 的路由,一般当app多的时候多是使用二级路由,在二级路由使用的过程中,出现了一个问题当,在根目录下的`urls`里面的url路径居然和定义的位置先后有关,具体的过程就是,当一个app,如下的`goods app` 当放在最下面的时候,从路由访问是找不到的,只有当该路由往上移才能找到路由


    urlpatterns = [
        url(r'^admin/', admin.site.urls),
        url(r'^', include('meiduo.apps.goods.urls')),
        url(r'^', include('meiduo.apps.users.urls')),
        url(r'^', include('meiduo.apps.verifications.urls')),
        url(r'^', include('meiduo.apps.areas.urls')),
        url(r'^', include('meiduo.apps.contents.urls')),
        url(r'^search/', include('haystack.urls')),
    ]

~~我猜想大致的问题是由于匹配的问题`r'^'`开头的时候其他几个app也是相同的当`app`多的时候就出现匹配混乱,但是测了一下并不是这样的~~

### python-tool

`Ctrl + Alt + u` 多项修改

`Ctrl + Alt + g` 进入函数


### pycharm 快捷键

`Ctrl + shift + Enter`  补全分号

`Ctrl + Shift + I ` 查看快速定义
`ctrl+ g` 光标移动到指定行(弹出框指定行数)
