from rest_framework import routers
from api.views import APiAddBookmark, ApiAllCategory, ApiAllProduct,\
     ApiAllTenant, ApiBookmark, ApiCart, ApiCheckHalal, ApiDeleteBookmark, ApiFavourite, \
         ApiLogin, ApiPayCod, ApiPromo, ApiReferral, ApiRegister, ApiTest, ApiUpdate, PostApiCart
from django.urls import include, path


# router = routers.DefaultRouter()
# router.register('category/', ApiAllCategory,basename='category')
# router.register('tenant/', ApiAllTenant,basename='tenant')
# router.register('product/', ApiAllProduct,basename='product')
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
    path('bookmark/',ApiBookmark.as_view()),
    path('add-bookmark/',APiAddBookmark.as_view()),
    path('del-bookmark/',ApiDeleteBookmark.as_view()),
    path('paycod/',ApiPayCod.as_view()),
    path('id-cart/',ApiTest.as_view()),
    path('update-cart/<str:pk>/',ApiUpdate.as_view())
]