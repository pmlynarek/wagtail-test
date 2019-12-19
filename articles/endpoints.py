from django_filters.rest_framework import DjangoFilterBackend
from articles.models import ArticlePage
from wagtail.api.v2.endpoints import BaseAPIEndpoint
from wagtail.api.v2.filters import FieldsFilter, OrderingFilter, SearchFilter
from rest_framework.authentication import TokenAuthentication


class ArticlePageEndpoint(BaseAPIEndpoint):
    model = ArticlePage
    filter_backends = (DjangoFilterBackend, FieldsFilter, OrderingFilter, SearchFilter)
    authentication_classes = [TokenAuthentication]
    # filter_fields = (
    #     "author__name",
    # )
    # known_query_parameters = BaseAPIEndpoint.known_query_parameters.union(filter_fields)
