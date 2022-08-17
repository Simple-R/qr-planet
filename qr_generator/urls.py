from django.urls import path
from qr_generator import views


app_name = 'qr_generator'

urlpatterns = [
    path('', views.index, name="home"),
]

urlpatterns += [
    path('generate-qr/', views.generate_qr, name='generate_qr'),
    path('share-qr/<str:pk>/', views.share_qr, name='share'),
    path('download-qr/<str:id>/<str:file_type>/', views.download_file, name='download'),
    path('save-qr/<str:id>/', views.save_qr, name='save_qr'),
]

urlpatterns +=[
    path('contact-us/', views.contact_us, name='contact'),
    path('learn-more/', views.learn_more, name="learn_more"), 
]

