
from django.urls import include, path,re_path
from api import views


urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name = 'register'),
    path('login/', views.LoginAPIView.as_view(), name = 'login'),
    path('user/', views.AuthUserAPIView.as_view(), name = 'user'),
]

urlpatterns += [
    path('<str:category>', views.QRCategoryView.as_view(), name='qr_category'), # Fetch all user QR from a category
    # path('<str:category>/<int:pk>', views.QROneCategoryView.as_view(), name='get_one'), # Fetch one user QR from a category
    path('', views.QRAPIView.as_view(), name='all_user_qr'), # Fetch all user QR
]

# Coming soon ...
# urlpatterns = [
#     path('<int:id>/delete', views.DeleteQRAPIView.as_view(), name='delete_one'), # Delete One user QR from a category    
#     path('<int:id>/category/create/', views), # Create a new QR in a category ... coming soon
#     path('<int:id>/category/edit/', views), # edit a QR in a category ... coming soon
#     path('<int:id>/<str:category/delete', views.), # Delete all user QR from a category
#     path('<str:category>/<int:id>/delete', views.DeleteQRAPIView.as_view(), name='delete_one'), # Delete One user QR from a category
#     path('<int:id>/delete', views.), # Delete all user QR from all categories
# ]