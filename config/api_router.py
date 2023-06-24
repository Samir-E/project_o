from django.urls import include, path

app_name = "api"


# urls from apps
urlpatterns = [
    path(r'menu/', include('backend.menu.urls')),
    path(r'feedback/', include('backend.feedback.urls')),
    path(r'cart/', include('backend.cart.urls')),
    path(r'booking/', include('backend.booking.urls')),

    # path(r'auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path(r'auth/', include('djoser.urls.authtoken')),
]
