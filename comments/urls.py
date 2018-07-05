from django.urls import path
from . import views

app_name = 'comment'

urlpatterns = [
    path('add', views.CreateNewCommentView.as_view(), name='add_new_comment'),
    path('<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('<int:comment_id>/edit/', views.UpdateCommentView.as_view(), name='edit_comment'),
    
]
