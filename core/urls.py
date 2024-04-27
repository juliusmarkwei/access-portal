from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Access Portal API Documentation ©️",
        default_version="v1",
        description="\
            Our project is a secure access key management system designed to streamline\
                the process of granting and managing access keys for users. It allows\
                    users to request, view, and manage their access keys, while administrators\
                        have the ability to grant, revoke, and monitor access keys.\
                            The system ensures data integrity and security by enforcing\
                                access key validity periods and providing granular control\
                                    over access permissions. Built using Django and Django REST Framework,\
                                        our solution offers a user-friendly interface and robust backend\
                                            functionality to meet the access management needs of modern organizations\
                ",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="julius.markwei@stu.ucc.edu.gh"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("api/v1/django/", admin.site.urls),
    path("api/v1/", include("api.urls", namespace="api")),
    path(
        "api/v1/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
