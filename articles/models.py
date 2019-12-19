from wagtail.core.fields import RichTextField
from modelcluster.fields import ParentalKey

from wagtail.contrib.routable_page.models import route
from django.shortcuts import redirect
from wagtail.search import index
from rest_framework import serializers
from django.db import models
from django.utils.translation import ugettext_lazy as _
from wagtail.api import APIField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    ObjectList,
    StreamFieldPanel,
    TabbedInterface,
)
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page, Orderable
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.models import Image
from wagtail.images.api.fields import ImageRenditionField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet


class ArticleLandingPage(Page):
    pass


@register_snippet
class Author(models.Model):
    name = models.CharField(_("Name"), max_length=100)

    avatar = models.ForeignKey(
        Image, on_delete=models.PROTECT, related_name="+", verbose_name=_("Avatar")
    )
    description = RichTextField(_("Description"), features=["ul"])

    api_fields = [
        APIField("name"),
        APIField("avatar"),
        APIField("description"),
        APIField(
            "avatar_thumbnail",
            serializer=ImageRenditionField("fill-30x30", source="avatar"),
        ),
    ]

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
        ImageChooserPanel("avatar"),
    ]

    def __str__(self):
        return self.name

    autocomplete_search_field = "name"

    def autocomplete_label(self):
        return self.name


class ArticlePage(Page):
    parent_page_types = ["articles.ArticleLandingPage"]
    # Page class
    # https://github.com/wagtail/wagtail/blob/v2.7/wagtail/core/models.py
    # [
    #     "title",
    #     "draft_title",
    #     "slug",
    #     "content_type",
    #     "live",
    #     "has_unpublished_changes",
    #     "url_path",
    #     "owner",
    #     "seo_title",
    #     "show_in_menus_default",
    #     "show_in_menus",
    #     "search_description",
    #     "go_live_at",
    #     "expire_at",
    #     "expired",
    #     "locked",
    #     "first_published_at",
    #     "last_published_at",
    #     "latest_revision_created_at",
    #     "live_revision",
    # ]

    # fields
    body = StreamField(
        [
            ("paragraph", blocks.RichTextBlock()),
            ("raw_html", blocks.RawHTMLBlock()),
            ("quote", blocks.BlockQuoteBlock()),
            ("image", ImageChooserBlock()),
        ],
        verbose_name=_("Body"),
    )
    author = models.ForeignKey(
        Author,
        related_name="articles",
        on_delete=models.PROTECT,
        verbose_name=_("Author"),
    )

    # Additional validation in CMS
    # base_form_class = GalleryImageWagtailAdminPageForm
    # def clean(self):
    #     pass

    # methods & properties
    def get_title(self):
        return self.title

    @property
    def custom_title(self):
        return self.title

    # routing
    @route(r"^$")
    def base_route(self, request):
        return redirect("https://sunscrapers.com/")

    # CMS Tabs
    content_panels = Page.content_panels + [
        InlinePanel("related_links", label="Related links", min_num=1, max_num=2),
        SnippetChooserPanel("author"),
    ]

    body_panel = [StreamFieldPanel("body")]
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading=_("Content")),
            ObjectList(body_panel, heading=_("Body")),
        ]
    )

    # API fields - which should be public
    api_fields = [
        APIField("title"),
        APIField("slug"),
        APIField("author"),
        APIField("body"),  # not rendered to plain html
        APIField(
            "custom_title", serializer=serializers.CharField(source="get_title")
        ),  # watch out for additional queries to database here - prefetch by default doesn't work
        # APIField(
        #     "videos",
        #     serializer=VideoSerializer(many=True, source="original_post_videos"),
        # ),
    ]

    # indexing data in Elasticsearch
    # make sure that related models trigger indexing on this model
    # and make sure that your data are up to date(Bug - I had to save something twice)
    # curl http://elastic:9200/wagtail__wagtailcore_page/_search
    # WAGTAILSEARCH_BACKENDS = {
    #     "default": {
    #         "BACKEND": "wagtail.search.backends.elasticsearch6",
    #         "URLS": [os.getenv("ELASTICSEARCH_URL")],
    #         "INDEX_SETTINGS": {"settings": {"index": {"number_of_shards": 1}}},
    #     }
    # }
    search_fields = Page.search_fields + [
        index.AutocompleteField("title"),
        index.FilterField("slug"),  # keyword in elasticsearch
        index.SearchField("custom_title"),
    ]


class ArticlePageRelatedLink(Orderable):
    page = ParentalKey(
        ArticlePage, on_delete=models.CASCADE, related_name="related_links"
    )
    name = models.CharField(max_length=255)
    url = models.URLField()

    panels = [FieldPanel("name"), FieldPanel("url")]
