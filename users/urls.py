from .views import UserViewSet
from rest_framework.routers import SimpleRouter

from .apps import UsersConfig

app_name = UsersConfig.name

router = SimpleRouter()
router.register('', UserViewSet)
urlpatterns = router.urls