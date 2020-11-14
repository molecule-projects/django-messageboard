from django.urls import path

from .views import messageboard_list_view, messageboard_detail_view, messageboard_comment_to_message_view

app_name = 'messageboard'

urlpatterns = [
    path('comment/<int:pk>/', messageboard_comment_to_message_view, name='comment'),
    path('<int:pk>/', messageboard_detail_view, name='detail'),
    path('', messageboard_list_view, name='list'),
]
