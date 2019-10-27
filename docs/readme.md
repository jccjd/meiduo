---
date: 2019-10-19
---

### 开发流程
在软件工程的开发流程中分为以下几种开发模型
- 瀑布模型
- 快速原型
- 迭代式开发
- 螺旋式模型
- 敏捷开发模型

具体的流程如下：
### 瀑布模型
> 瀑布模型是最经典的预见性的方法， 严格遵循预先计划的需求分析，设计，编码，集成，测试，和维护的步骤顺序进行。

瀑布模型是至上而下的，是有严格的分级的，这导致项目对于后来的变化难以兼容，后期需求变更的话，很难调整

瀑布式方法在需求不明确时是不可行的
### 快速原型
> 快速原型是一种以最小幅度的规划并迅速地将原型完成的模型，在进行软件开发时，软件规划和软件开发交替同时进行，通常能在没有大量预先规划的情况下，让软件更快完成

### 迭代式开发
> 迭代式开发，也是迭代增量式开发，是一种与传统的瀑布式开发相反的软件开发过程，每次只设计和实现这个产品的一部分， 逐步完成的方法叫迭代开发， 每次设计和实现的一个阶段叫一个迭代


在迭代开发过程中，整个开发工作被组织为一系列的短小的，固定的小项目，被称为一系列的迭代
每次迭代都包括了需求分析，设计，实现和测试。

采用这种方法，开发工作可以在需求被完整的确定之前启动，并在一次迭代中完成系统的一部分功能或业务逻辑的开发工作，在通过客户反馈来细化需求，并开始新一轮的迭代


### 螺旋开发
> 螺旋模型将瀑布模型和快速原型结合起来，强调了其他模型所忽视的风险分析，适合大型复杂的系统,螺旋模型刚开始规模很小，当项目被定义的更好，更稳定时，逐渐展开。

螺旋模型的核心在于不需要在开始的时候就把所有的事情都定义的清清楚楚，先定义最重要的功能，实现后听取客户的意见，之后，进入到下一阶段。如此不断重复，直到产品开发完成

- 制定计划： 确定软件目标，选定实施方案，弄清楚项目开发的限制条件；
- 风险分析： 分析评估所选方案， 考虑如何识别和消除风险
- 实施工程： 实施软件开发和验证
- 客户评价： 评价软件开发和验证

螺旋模型是一套风险驱动的方法体系，因为在每个阶段之前及经常发生循环之前，都必须首先进行风险评估

### 敏捷开发
> 敏捷开发是一种应对快速变化的需求的一种软件开发能力。 相对于非敏捷，更强调程序员团队与业务专家之间的紧密协助，面对面的沟通（比书面文档更加有效）， 频繁交付新的软件版本，紧凑自我组织型的团队，能够很好的适应需求变化的代码编写和团队组织方法，

- 人和交互重于过程和工具
- 可以工作的软件重于求全而完备的文档
- 客户协助重于合同谈判
- 随时应对变化重于循规蹈矩

敏捷开发作为一个整体工作，按短迭代周期工作，每次迭代交付一些成果，适用于较小的团队，40,人以下

-----------------

对于商城项目这显然是一个经典项目，项目需求清晰，十分的可预见，可以采用瀑布模型，

### 开发流程

- 项目立项
- 产品需求分析
- 产品原型设计
- 软件需求分析
-



前端：

- UI界面设计
- 前端页面设计
- 前端代码实现

后端：

- 架构设计
- 数据库设计
- 代码实现
- 单元测试

最后前后端整合，集成测试项目上线

### 架构设计

- 分析可能用到的技术点
- 前后端时候分离
- 前后端使用那些框架
- 后端使用那些框架
- 选择使用什么数据库
- 如何实现缓存
- 时候搭建分布式服务
- 如何管理代码

### 数据库设计
- 数据表的设计至关重要
- 根据项目需求， 设计合适的数据库表
- 数据库表在前期如果设计不合理，后期随需求增加会变得难以维护

### 项目需求分析

**需求分析原因：**

- 可以整体的了解项目的业务流程和主要的业务需求
- 项目中 ，需求驱动开发。既开发人员需要以需求为目标来实现业务逻辑

**需求分析方式：**

- 借助产品原型图分析需求
- 需求分析完后，前端按照产品原型图开发前端页面，后端开发对应的业务及响应处理

### 主要的模块

|    模块    |                       功能                       |
| :--------: | :----------------------------------------------: |
|    验证    |                图形验证，短信验证                |
|    用户    |               注册，登录，用户中心               |
| 第三方登录 |                        QQ                        |
|  首页广告  |                     首页广告                     |
|    商品    |           商品列表，商品搜索，商品详情           |
|   购物车   |              购物车管理，购物车合并              |
|    订单    |                确认订单，提交订单                |
|    支付    |             支付宝支付，订单商品评价             |
|  MIS系统   | 数据统计，用户管理，权限管理，商品管理，订单管理 |

### 项目开发模式

|   选项   |   技术选型   |
| :------: | :----------: |
| 开发模式 | 前后端不分离 |
| 后端架构 |    Django    |
| 前端架构 |    Vue.js    |

### 项目运行机制

- 代理服务： Nginx服务器（反向代理）
- 静态服务：Nginx服务器（静态首页，商品详情页）
- 动态服务：uwsgi服务器（处理业务场景）
- 后端服务：Mysql, Redis, Celery, RabbitMQ, Docker, FastDFS, Elasticsearch, Crontab
- 外部接口：容联云，QQ ， 支付宝

### 数据相关存储

**Redis:**

使用`redis`存储有关一次性数据或者非常驻数据

- 存储session
- 注册或登录时的验证码
- 用户的浏览历史记录

Mysql:

关于数据库的表设计

主要的表有`user`表

|        字段        |     类型     |     Null     |
| :----------------: | :----------: | :----------: |
|         id         |   int(11)    |   not null   |
|      password      | varchar(128) |   not null   |
|     last_login     | datetime(6)  | default null |
|    is_superuser    |  tinyint(1)  |   not null   |
|      username      | varchar(150) |   not null   |
|     first_name     | varchar(30)  |   not null   |
|     last_name      | varchar(150) |   not null   |
|       email        | varchar(254) |   not null   |
|      is_staff      |  tinyint(1)  |   not null   |
|     is_active      |  tinyint(1)  |   not null   |
|    date_joined     | datetime(6)  |   not null   |
|       mobile       | varchar(11)  |   not null   |
|    email_actice    |  tinyint(1)  |   not null   |
| default_address_id |   int(11)    | default null |

> lannister always pays has debts
>
> Valar Dohaeris
>
> Valar Morghulis

与`user`表相关,有外键关联的有 `address`, 和`order_info`(订单基本信息)表

**address**

|    字段     |    类型     |   null   |
| :---------: | :---------: | :------: |
|     id      |   int(11)   | not null |
|    title    | varchar(20) | not null |
|  receiver   | varchar(20) | not null |
|    place    | varchar(50) | not null |
|   mobile    | varchar(11) | not null |
|     tel     | varchar(20) |   null   |
|    email    | varchar(30) |   null   |
| is_deleted  | tinyint(1)  | not null |
|   city_id   |   int(11)   | not null |
| district_id |   int(11)   | not null |
| province_id |   int(11)   | not null |
|   user_id   |   int(11)   | not null |

**order_info**

|     字段     |     类型      |   null   |
| :----------: | :-----------: | :------: |
|   order_id   |  datetime(6)  | not null |
| total_count  |    int(11)    | not null |
| total_amount | decimal(10,2) | not null |
|   freight    | decimal(10,2) | not null |
|  pay_method  |  smallint(6)  | not null |
|    status    |  smallint(6)  | not null |
|  address_id  |    int(11)    | not null |
|   user_id    |    int(11)    | not null |
|              |               |          |

`order_info`和`user`,`address`表均有外键关联，每个用户都有对应的订单信息（order_info）和地址信息(address),地址信息有关的表有`areas`省市县表, 并且在查询省市地址时该表是自关联的

**areas**

|          字段           |    类型     |   null   |
| :---------------------: | :---------: | :------: |
|           id            |   int(11)   | not null |
|          name           | varchar(20) | not null |
| parent_id(上级行政区划) |   int(11)   |   null   |

`order_info`每个订单信息表对应相关的支付信息，可以提取出一个支付表`payment`表

**payment**

|        字段        |     类型     |   null   |
| :----------------: | :----------: | :------: |
|         id         |   int(11)    | not null |
|   trade_id(订单)   | varchar(100) | not null |
| order_id(支付编号) | varchar(64)  | not null |

与订单信息`order_info`还有订单的具体商品`order_good`表，该表中有订单商品的具体信息，数量，价格和对商品的评价信息，客户打分数，是否匿名评价，是否评价了，其外键关联了商品的更具体的信息`sku`表库存量单位

**order_good**

|       字段        |     类型      |   null   |
| :---------------: | :-----------: | :------: |
|        id         |    int(11)    | not null |
|       count       |    int(11)    | not null |
|       price       | decimal(10,2) | not null |
| comment(评价信息) |   longtext    | not null |
|       score       |  smallint(6)  | not null |
|   is_anonymous    |  tinyint(1)   | not null |
|   is_commented    |  tinyint(1)   | not null |
|     order_id      |  varchar(64)  | not null |
|      sku_id       |    int(11)    | not null |

对于`SKU`它是stock keeping Unit(库存量单位)

>  可以是以件，盒为单位，是物理上不可分割的最小存货单元,通俗的讲，SKU是指一款商品，，每款都有一个SKU，便于电商识别商品,例如：`iPhone 11 全网通 黑色 256G`就是一个SKU,它表示了一个具体的规格，颜色等信息

`SKU`有具体的名称，副标题，从属类别，单价，进价，市场价，库存，销售，评价数，是否上架，商品图片

**sku**

|     字段      |      类型      |   null   |
| :-----------: | :------------: | :------: |
|      id       |    int(11)     | not null |
|     name      |  varchar(50)   | not null |
|    caption    |  varchar(100)  | not null |
|     price     | decimal(10, 2) | not null |
|  cost_price   | decimal(10, 2) | not null |
| market_price  | decimal(10, 2) | not null |
|     stock     |    int(11)     | not null |
|     sales     |    int(11)     | not null |
|   comments    |    int(11)     | not null |
|  is_launched  |   tinyint(1)   | not null |
| default_image |  varchar(200)  |   null   |
|  category_id  |    int(11)     | not null |
|    spu_id     |    int(11)     | not null |

可以看到`sku`表依然没有表达完整的商品信息，其外键关联，又分成表`goods_category`(商品类别)，`spu`（标准产品），`sku_image`

**goods_category**

|   字段    |    类型     |   Null   |
| :-------: | :---------: | :------: |
|    id     |   int(11)   | not null |
|   name    | varchar(10) | not null |
| parent_id |   int(11)   |   null   |

**sku_image**

|  字段  |     类型     |   Null   |
| :----: | :----------: | :------: |
|   id   |   int(11)    | not null |
| image  | varchar(100) | not null |
| sku_id |   int(11)    | not null |

其中的spu是标准产品的单位`Standard Product Unit`

> SPU是商品信息聚合的最小单位，是一组可复用，易检索的标准化信息的集合，该集合描述了一个产品的特性。通俗的讲，属性值，特性相同的商品就可以归类到一类SPU。列入：iPhone 11就是一个SPU，没有具体的信息只是一个分类

spu包含名称，品牌，三级类别，销量，评价数，详细介绍，包装信息，售后服务等信息

**spu**

|     字段     |    类型     |   Null   |
| :----------: | :---------: | :------: |
|      id      |   int(11)   | not null |
|     name     | varchar(50) | not null |
|    sales     |   int(11)   | not null |
|   comments   |   int(11)   | not null |
|   brand_id   |   int(11)   | not null |
| category1_id |   int(11)   | not null |
| category2_id |   int(11)   | not null |
| category3_id |   int(11)   | not null |
| desc_detail  |  longtext   | not null |
|  desc_pack   |  longtext   | not null |
| desc_service |  longtest   | not null |

与spu相关的表`brand`是相关啊品牌表，相当于是spu的父表，提供相关的品牌信息

**band**

|           字段           |     类型     |   Null   |
| :----------------------: | :----------: | :------: |
|            id            |   int(11)    | not null |
|           name           | varchar(20)  | not null |
|           logo           | varchar(100) | not null |
| first_letter(品牌首字母) |  varchar(1)  | not null |

这些是项目中的主要数据表，及其对应关系，总的来说就是根据用户行为，商品行为，进行的分表，一个用户需要有基本的信息，`user`,购物需要有订单信息`order_info`,和住址`address`，当然给用户的订单发货也需要`address`，订单要被支付`payment`订单的具体内容`order_goods`,

而商家所提供的商品需要对商品进行管理`good_category`商品类别，如手机，家电之类，在对应具体的什么商品`spu`如''手机-->app'',在详细点需要sku, "手机->app->华为"，整个大致的流程如此，当然还有其他功能扩展表，如`good_visi`对商品类别 `good_category`监控，`spu`需要有品牌`brand`表。






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


### pip package

    pip install djangorestframework

### Haystack扩展建立索引

    pip install django-haystack
    pip install elasticsearch
    pip install django_crontab

    pip install python-alipay-sdk --upgrade
