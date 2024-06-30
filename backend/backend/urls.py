from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("account.urls")),
    path("api/vdocon/", include("vdocon.urls")),
    # path("api/search/", include("search.urls")),
    # path('api/notifications/', include('notification.urls')),
]