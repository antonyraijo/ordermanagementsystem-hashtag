from django.urls import path, include
from rest_framework.routers import SimpleRouter

from accounts.views import ConsumerCreationView, LoginView

router = SimpleRouter()
router.register('consumer-creation', ConsumerCreationView)
urlpatterns = [
        path('', include(router.urls)),
        path('login/', LoginView.as_view(), name='login'),
] + router.urls