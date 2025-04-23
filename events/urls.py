from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('list/', views.event_list, name='event_list'),
    path('create/', views.create_event, name='create_event'),
    path('<int:event_id>/', views.event_detail, name='event_detail'),
    path('<int:event_id>/edit/', views.edit_event, name='edit_event'),
    path('<int:event_id>/delete/', views.delete_event, name='delete_event'),
    path('<int:event_id>/invite/', views.send_invitations, name='send_invitations'),
    path('rsvp/<int:event_id>/<str:response>/', views.rsvp_event, name='rsvp_event'),
    path('add_contact/', views.add_contact, name='add_contact'),
    path('<int:event_id>/create_post/', views.create_post, name='create_post'),
    path('notifications/', views.notifications_list, name='notifications_list'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('profile/', views.profile_view, name='profile'),

]
