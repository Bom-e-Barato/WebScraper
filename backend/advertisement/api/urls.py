from django.urls import path
from advertisement.api.views import(
    add_ad_view,
    update_ad_img_view,
    get_all_ads_view,
    get_promoted_ads_view,
)

app_name = "advertisement"

urlpatterns = [
    path("add_advertisement", add_ad_view, name="add_advertisement"),
    path("update_advertisement_img/<int:id>", update_ad_img_view, name="update_advertisement_img"),
    path("get_all_ads", get_all_ads_view, name="get_all_ads"),
    path("get_promoted_ads", get_promoted_ads_view, name="get_promoted_ads"),
]