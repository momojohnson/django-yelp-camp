from django.urls import path, include
from . import views
app_name = 'campgrounds'
urlpatterns = [
    path('', views.ListAllCampgroundsView.as_view(), name='list_campgrounds'),
    path('add', views.CreateNewCampgroundView.as_view(), name='add_campground'),
    path('<int:campground_id>/<slug:slug>/', views.CampgroundDetailView.as_view(), name="campground_details"),
    path('<int:campground_id>/<slug:slug>/edit', views.EditCampgroundView.as_view(), name="edit_campground"),
    path('<int:campground_id>/<slug:slug>/delete', views.delete_campground, name="delete_campground"),
    
    
]
