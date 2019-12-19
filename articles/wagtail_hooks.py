import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import (
    InlineStyleElementHandler,
)
from wagtail.core import hooks
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


@hooks.register("register_rich_text_features")
def register_underline_feature(features):
    feature_name = "underline"
    type_ = "UNDERLINE"

    control = {"type": type_, "label": "U", "description": "underline"}

    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        "from_database_format": {
            'span[style="text-decoration: underline"]': InlineStyleElementHandler(type_)
        },
        "to_database_format": {
            "style_map": {type_: 'span style="text-decoration: underline"'}
        },
    }

    features.register_converter_rule("contentstate", feature_name, db_conversion)
