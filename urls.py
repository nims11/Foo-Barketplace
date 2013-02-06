from django.conf.urls.defaults import patterns, include, url
import views
import userTools.views
import itemTools.views
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.home),
    url(r'^myprofile/$', userTools.views.user_info),
    url(r'^myprofile/edit/$', userTools.views.edit_profile),
    url(r'^myprofile/delete/$', userTools.views.del_profile),
    url(r'^user/([a-z]{1}[a-z0-9_]{2,19})/$', userTools.views.view_profile),
    url(r'^admin/$', userTools.views.admin_panel_home),
    url(r'^admin/user/deact/([a-z]{1}[a-z0-9_]{2,19})/$', userTools.views.deact_profile),
    url(r'^admin/user/act/([a-z]{1}[a-z0-9_]{2,19})/$', userTools.views.act_profile),
    url(r'^admin/add/$', userTools.views.admin_add),
    url(r'^admin/deact_users/$', userTools.views.deact_users),
    url(r'^sell/$', itemTools.views.sell),
    url(r'^buy/$', itemTools.views.buy),
    url(r'^item/$', itemTools.views.item_view),
    url(r'^item/(\d+)/delete/$', itemTools.views.item_delete),
    url(r'^item/(\d+)/edit/$', itemTools.views.item_edit),
    url(r'^my_items/$', itemTools.views.my_items),
    # url(r'^hackcode13/', include('hackcode13.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
