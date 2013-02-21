from django.conf.urls.defaults import patterns, include, url
import views
import userTools.views
import itemTools.views
import searchTools.views
import commTools.views
import expiry

urlpatterns = patterns('',
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
    url(r'^my_buys/$', itemTools.views.my_items_buys),
    url(r'^my_sells/$', itemTools.views.my_items_sold),
    url(r'^ongoing_deals/$', itemTools.views.ongoing_deals),

    url(r'^search/$', searchTools.views.search_items),
    url(r'^search_handle/$', searchTools.views.search_handle),
    
    url(r'^item/(\d+)/comm/$', commTools.views.comm_item),
    url(r'^item/(\d+)/comm/([a-z]{1}[a-z0-9_]{2,19})/$', commTools.views.comm_seller_buyer),
    url(r'^item/(\d+)/seal/$', commTools.views.seal),
    url(r'^item/(\d+)/cancel/$', commTools.views.cancel),
    url(r'^item/(\d+)/comm/([a-z]{1}[a-z0-9_]{2,19})/seal/$', commTools.views.seller_seal),

    url(r'^tasks/expiry$', expiry.chk_exp),
    # Testing Purpose
    url(r'^reset/$', views.reset),

)
