"""DRF URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls


# 基于类的视图，使用混合，一定要在后面加：as_view()方法！否则缺少参数：
urlpatterns = [
    path('admin/', admin.site.urls),
    path('doc/', include_docs_urls(title='HQQ')),

    path('user/', include('hqq_user.web.user_urls')),
    path('topic/', include('hqq_topic.web.topic_urls')),
    path('usertopic/', include('hqq_usertopic.web.usertopic_urls')),
    path('directchat/', include('hqq_directchat.web.directchat_urls')),
    path('group/', include('hqq_group.web.group_urls')),
    path('forum/', include('hqq_forum.web.forum_urls')),
    path('system/', include('hqq_system.web.system_urls')),
    path('dialog/', include('hqq_dialog.web.dialog_urls')),
    path('qiniu/', include('hqq_qiniu.qiniu_urls')),
    path('search/', include('hqq_search.web.search_urls')),
    path('blacklist/', include('hqq_blacklist.web.blacklist_urls')),
    path('rongyun/', include('hqq_rongyun.web.rongyun_urls')),
    path('report/', include('hqq_report.web.report_urls')),
    path('complaint/', include('hqq_complaint.web.complaint_urls')),
    path('coterie/', include('hqq_coterie.web.coterie_urls')),
    path('news/', include('hqq_news.web.news_urls')),
    path('notice/', include('hqq_notice.web.notice_url')),
    path('dating/', include('hqq_dating.web.dating_urls')),
    path('admin/', include('hqq_admin.web.admin_urls')),
    path('admin/', include('hqq_admin.web.statistic_urls')),

]
