from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("register/", views.register, name="register"),
    path("profile/", views.dashboard, name="profile"),
    path('ads/', views.view_ads, name='view_ads'),
    path("reference/", views.add_reference, name="add_reference"),
    path("withdrawal/", views.withdrawal, name="withdraw_points"),
    # # Login and Logout URLs
    path("login/", views.login_view, name="login_view"),
    path("logout/", views.logout, name="logout"),
    path('notification/', views.notification, name='notification'),
    
    path('pending/', views.status_pending, name='status_pending'),
    path('checking/', views.status_checking, name='status_checking'),
    
    
    # admin area
    path("admin_user_list/", views.admin_user_list, name="admin_user_list"),
    
    path("upload_video/", views.admin_video_upload, name="admin_video_upload"),
    path("videos/", views.admin_video_list, name="admin_video_list"),
    path(
        "send_notification/",
        views.admin_send_notification,
        name="admin_send_notification",
    ),
    
    path(
        "send_notification_list/",
        views.admin_send_notification_list,
        name="admin_send_notification_list",
    ),
    
     path('withdrawals/', views.admin_withdrawal_view, name='admin_withdrawal_view'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
