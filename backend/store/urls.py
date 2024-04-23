from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('accounts', views.AccountViewSet, basename='accounts')
router.register('games', views.GameViewSet, basename='games')
router.register('carts', views.CartViewSet, basename='carts')
router.register('orders', views.OrderViewSet, basename='orders')

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', views.CartItemViewSet, basename='cart-items')

urlpatterns = router.urls + carts_router.urls