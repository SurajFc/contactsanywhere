from django.urls import path
from . import views
app_name = 'app'

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    #path("detail/<int:id>/", views.detail, name="detail"),
    path('detail/<int:pk>/', views.DetailView.as_view(), name="detail"),
    path('search/', views.search, name="search"),
    path('add/', views.ContactCreateView.as_view(), name="create"),
    path('update/<int:pk>', views.ContactUpdateView.as_view(), name="update"),
    path('delete/<int:pk>', views.ContactDeleteView.as_view(), name="delete"),
    path('signup/', views.SignUpview.as_view(), name='signup')
]
