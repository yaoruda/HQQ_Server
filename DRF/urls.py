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
    path('hqq_user/', include('hqq_user.urls')),
    path('topic/', include('topic.urls')),
    path('admin/', admin.site.urls),
    path('doc/', include_docs_urls(title='HQQ')),
]
