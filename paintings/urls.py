from django.urls import path

from . import views

urlpatterns = [
    path('', views.ProductsView.as_view()),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('review/<int:pk>/', views.NewReview.as_view(), name='new_review'),
    path('author/<str:slug>/', views.AuthorView.as_view(), name='author_detail'),
]
