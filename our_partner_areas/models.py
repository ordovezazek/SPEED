from __future__ import unicode_literals
from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.search import index

from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from wagtail.core.models import Page, Orderable, Collection
from wagtail.core.fields import RichTextField, StreamField

from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock

from wagtail.core import blocks
from django_extensions.db.fields import AutoSlugField

from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    PageChooserPanel,
    MultiFieldPanel,
    StreamFieldPanel,
)

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wagtail.search.models import Query

class OurPartnerAreas(Page):

    template = "ourpartnerareas/our_partner_areas.html"

    max_count = 1

    background = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )

    desc = StreamField(
        [
            ("Description", blocks.RichTextBlock())
        ],
        null=True,
        blank=True,
    )

    search_fields = Page.search_fields + [
        index.SearchField('desc'),
    ]

    content_panels = Page.content_panels + [
        ImageChooserPanel('background'),
        StreamFieldPanel('desc', heading="Contact Page Content"),
        MultiFieldPanel(
            [
                InlinePanel("partner_area", label="Partner", min_num=1, max_num=36)
            ],
            heading="Partner(s)"
        ),
    ]

    # Pagination for the index page. We use the `django.core.paginator` as any
    # standard Django app would, but the difference here being we have it as a
    # method on the model rather than within a view function
    def paginate(self, request, *args):
        page = request.GET.get('page')
        areas = args[0]

        paginator = Paginator(areas, 6)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        return pages

    def get_context(self, request):
        context = super(OurPartnerAreas, self).get_context(request)
        context['partner_areas'] = self.paginate(request, self.partner_area.all())

        return context

    # Specifies what content types can exist as children of BlogPage.
    # Empty list means that no child content types are allowed.
    # subpage_types = ['our_partner_areas.PageModal']

    class Meta:
        # abstract = True
        verbose_name = "Our Partner Areas Page"

class PartnerArea(models.Model):

    name = models.CharField(max_length=100)
    description = RichTextField(blank=True)
    link = models.URLField(blank=True, null=True)
    background = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.CASCADE,
        null=True,
        blank=False,
        related_name="+",
    )

    panels = [
        ImageChooserPanel('background'),
        MultiFieldPanel(
            [
                FieldPanel("name"),
                ImageChooserPanel("image"),
            ],
            heading="Partner Area (Name & Image)",
        ),
        MultiFieldPanel(
            [
                FieldPanel("description"),
                FieldPanel("link"),
            ],
            heading="Partner Details",
        ),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Partner Area"
        verbose_name_plural = "Partner Areas"

register_snippet(PartnerArea)

class PartnerAreaOrderable(Orderable):

    page = ParentalKey("our_partner_areas.OurPartnerAreas", related_name="partner_area")
    partner = models.ForeignKey(
        "our_partner_areas.PartnerArea",
        on_delete=models.CASCADE,
    )

    panels = [
        SnippetChooserPanel("partner")
    ]
