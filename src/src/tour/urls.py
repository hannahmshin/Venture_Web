#urls.py for tourapp
from django.conf.urls import url
from django.contrib import admin
from .views import (
    main_page,
    about_page,
    search_page,
    my_page,
    create_page,
    profile_page,
    create_page_yourtour,
    create_page_create,
    profile_page_preferences,
    tour_detail_page,
    create_page_stop_1,
    create_page_stop_2,
    create_page_stop_3,
    create_page_review,
    create_in_progress,
    finish_review,
    clear_the_form,
    delete_tour_instance,
    eidt_tour_instance,
   
)

urlpatterns = [
    url(r'^$', main_page, name="main"), 
    url(r'^about/$', about_page, name="about"),
    url(r'^search/$', search_page, name="search"),
    url(r'^mypage/', my_page, name="mypage"),
    url(r'^create/$', create_page, name="create"),
    url(r'^profile/', profile_page, name="profile"),
    url(r'^create/your_tours', create_page_yourtour, name="create_yourtours"),
    url(r'^create/create_tours/$', create_page_create, name="create_create"),
    url(r'^create/create_tours/inprogress/$',create_in_progress, name="inprogress"),
    url(r'^create/create_tours/stop1/', create_page_stop_1, name="create_stop1"),
    url(r'^create/create_tours/stop2/', create_page_stop_2, name="create_stop2"),
    url(r'^create/create_tours/stop3/', create_page_stop_3, name="create_stop3"),
    url(r'^create/create_tours/review/', create_page_review, name="review"),
    url(r'^create/create_tours/finish/', finish_review, name="finish_review"),
    url(r'^profile_preference/', profile_page_preferences, name="preferences"),
    url(r'^create/clear_form', clear_the_form, name="clear_form"),

  
    #Delete tour url
    url(r'^tours/(?P<slug>[^\.]+)/delete/', delete_tour_instance, name="delete_tour"),
    #Edit tour instance
    url(r'^tours/(?P<slug>[^\.]+)/edit/', eidt_tour_instance, name="edit_tour"),
    #This is for tour_detail page for specific tours
    url(r'^tours/(?P<slug>[^\.]+)/$', tour_detail_page, name="tour_detail"),
    #url(r'^(?P<id>\d+)/edit/$', post_update, name="update"),
    # url(r'^create/$', post_create),
    # url(r'^(?P<id>\d+)/$', post_detail, name = "detail"),
    # url(r'^(?P<id>\d+)/edit/$', post_update, name="update"),
    # url(r'^(?P<id>\d+)/delete/$', post_delete),
]
