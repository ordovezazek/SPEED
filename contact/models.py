from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.core.models import Page
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    PageChooserPanel,
    MultiFieldPanel,
    StreamFieldPanel,
)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.forms.models import (
    AbstractEmailForm,
    AbstractFormField
)

class FormField(AbstractFormField):
    """Contact Page model"""

    page = ParentalKey(
        'ContactPage',
        on_delete=models.CASCADE,
        related_name='form_fields',
        )

class ContactPage(AbstractEmailForm):

    template = "contact/contact_page.html"

    max_count = 1

    #landing test variable
    success = RichTextField(blank=True)

    content = StreamField(
        [
            ("payment_details", blocks.RichTextBlock())
        ],
        null=True,
        blank=True,
    )

    background = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )

    content_panels = AbstractEmailForm.content_panels + [
        ImageChooserPanel('background'),
        
        InlinePanel('form_fields', label='Form Fields'),

        StreamFieldPanel("content", heading="Contact Page Content"),

        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname='from'),
                FieldPanel('to_address', classname='to'),
            ]),
            FieldPanel('subject'),
        ], heading="Email Settings"),

        FieldPanel('success'),
    ]

    #sets slug to 'contact'
    def full_clean(self, *args, **kwargs):
        super(ContactPage, self).full_clean(*args, **kwargs)

        if not self.slug.startswith('contact-us'):
            self.slug = 'contact-us'

    class Meta:
        verbose_name = "Contact Page"
        verbose_name_plural = "Contact Pages"
