from django.urls import path

# from rest_framework_nested import routers
from . import views

# router = routers.DefaultRouter()

# products_router = routers.NestedDefaultRouter(
#     router, "product", lookup="product"
# )
# products_router.register(
#     "reviews", views.ReviewViewSet, basename="product-reviews"
# )


urlpatterns = [
    path("products/", views.ProductList.as_view()),
    path("products/<int:pk>/", views.ProductDetail.as_view()),
    path("products/<int:pk>/reviews/", views.ReviewList.as_view()),
    path("products/<int:pk>/reviews/<int:id>", views.ReviewDetail.as_view()),
    path("collections/", views.CollectionList.as_view()),
    path(
        "collections/<int:pk>/",
        views.CollectionDetail.as_view(),
        name="collection-detail",
    ),
]
