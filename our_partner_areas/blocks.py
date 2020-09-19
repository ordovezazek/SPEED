""" StreamFields live in here """

from wagtail.core import blocks

class TextBlock(blocks.StructBlock):
    """Description"""

    Description = blocks.TextBlock(required=True, help_text="Add text.")

    class Meta: #noqa
        template = "streams/title_and_text.html"
        icon = "edit"
        label = "OPA Description"
