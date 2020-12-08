'''
项目管理url
'''

from django.conf.urls import url
from app01.views import wiki, file, setting, issues, dashboard, statistics

urlpatterns = [
    url(r'^wiki/$', wiki.wiki, name='wiki'),
    url(r'^wiki-add/$', wiki.wiki_add, name='wiki_add'),
    url(r'^wiki-catalog/$', wiki.wiki_catalog, name='wiki_catalog'),
    url(r'^wiki-delete/(?P<wiki_id>\d+)/$', wiki.wiki_delete, name='wiki_delete'),


    url(r'^file/$', file.file, name='file'),
    url(r'^setting/$', setting.setting, name='setting'),
    url(r'^issues/$', issues.issues, name='issues'),
    url(r'^dashboard/$', dashboard.dashboard, name='dashboard'),
    url(r'^statistics/$', statistics.statistics, name='statistics'),
]
