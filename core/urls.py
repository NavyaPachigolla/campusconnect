from django.urls import path
from . import views

urlpatterns = [

    # Home
    path('home/', views.home, name='home'),

    # Category doubts
    path('category/<int:pk>/', views.category_doubts, name='category_doubts'),

    # Post doubt
    path('post/', views.post_doubt, name='post_doubt'),

    # Doubt detail
    path('doubt/<int:pk>/', views.doubt_detail, name='doubt_detail'),

    # Add answer
    path('doubt/<int:pk>/answer/', views.add_answer, name='add_answer'),

    # Dashboards
    path('junior/', views.junior_dashboard, name='junior_dashboard'),
    path('senior/', views.senior_dashboard, name='senior_dashboard'),

]