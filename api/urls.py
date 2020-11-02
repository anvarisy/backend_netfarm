from rest_framework import routers
from api.views import ApiAllCategory, ApiAllProduct, ApiAllTenant, ApiCart, ApiCheckHalal, ApiLogin, ApiPromo, ApiReferral, ApiRegister, PostApiCart,\
    ApiFavourite
from django.urls import include, path


router = routers.DefaultRouter()
# router.register('category', ApiAllCategory)
# router.register('tenant', ApiAllTenant)
# router.register('product', ApiAllProduct)
urlpatterns = [
    # path('', include(router.urls)),
    # path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('category/',ApiAllCategory.as_view()),
    path('tenant/', ApiAllTenant.as_view()),
    path('product/',ApiAllProduct.as_view()),
    path('check-halal/', ApiCheckHalal.as_view()),
    path('cart/', ApiCart.as_view()),
    path('post-cart/', PostApiCart.as_view()),
    path('register/',ApiRegister.as_view()),
    path('promo/',ApiPromo.as_view()),
    path('login/',ApiLogin.as_view()),
    path('referral/<str:email>',ApiReferral.as_view()),
    path('laris/',ApiFavourite.as_view()),
]