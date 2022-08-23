# qr_gen_project/settings.py

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


from django.contrib.auth import views as auth_views
from django.views.static import serve
from django.contrib import admin
from django.urls import path


schema_view = get_schema_view(
   openapi.Info(
      title="QR Planets API Documentation",
      default_version='v1',
      description="""The Easiest Way to generate, download &amp; share QR Codes Online with QR Planet Code Generator within few minutes.
      Get started today.
      These are the Available Endpoints, Other API Endpoints are coming soon""",
      
      contact=openapi.Contact(email="simplenick01@gmail.com"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
   authentication_classes=[]
)


urlpatterns = [
   path('api/documentation/', schema_view.with_ui('swagger', cache_timeout=0), name='docs'),
   path('qr-gen/api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   path('qr-gen/api/', include('api.urls'), ),
]


urlpatterns += [
    path('', include('qr_generator.urls', namespace='qr_generator'),),
    path('qr-gen/admin/', admin.site.urls),
]

urlpatterns += [
    path('qr-gen/accounts/', include('accounts.urls', namespace='accounts'),),
]

urlpatterns +=[
    path('reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password/password_reset_complete.html'), name='password_reset_complete'),      
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT, }), ]

handler404 = "qr_generator.views.page_not_found"