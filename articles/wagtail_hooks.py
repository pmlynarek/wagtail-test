from django.utils.translation import gettext as _
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)

from . import models


class ArticleLandingPageAdmin(ModelAdmin):
    model = models.ArticleLandingPage
    search_fields = ("title",)
    list_display = ("title", "slug")


class AuthorAdmin(ModelAdmin):
    model = models.Author
    search_fields = ("name",)
    list_display = ("name",)


class ArticlePageAdmin(ModelAdmin):
    model = models.ArticlePage
    menu_label = "Article"
    search_fields = ("title",)
    list_display = ("title", "author")
    list_filter = ("live", "author")


class ArticlesGroup(ModelAdminGroup):
    menu_label = _("Articles")
    menu_order = 210
    items = (ArticleLandingPageAdmin, AuthorAdmin, ArticlePageAdmin)


modeladmin_register(ArticlesGroup)
