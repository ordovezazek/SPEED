# from django.db import models
#
# from modelcluster.fields import ParentalKey
#
# from wagtail.core.models import Page, Orderable
# from wagtail.core.fields import RichTextField, StreamField
# from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, StreamFieldPanel
# from wagtail.images.edit_handlers import ImageChooserPanel
# from wagtail.search import index
# from .blocks import BaseStreamBlock

from __future__ import unicode_literals

from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
    StreamFieldPanel,
)
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Collection, Page, Orderable
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

# Create your models here.


class AboutPage(Page):
    template = 'aboutus/about.html'

    max_count = 1

    background = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )

    date = models.DateField("Post date")
    body = StreamField([
        ('heading', blocks.RichTextBlock()),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ])

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        ImageChooserPanel('background'),
        FieldPanel('date'),
        StreamFieldPanel('body'),
    ]


class AboutPageRelatedLink(Orderable):
    page = ParentalKey(AboutPage, on_delete=models.CASCADE, related_name='related_links')
    name = models.CharField(max_length=255)
    url = models.URLField()

    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
    ]
