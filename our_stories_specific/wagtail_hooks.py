from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import Comment

class CommentAdmin(ModelAdmin):
    model = Comment
    menu_label = "Comments"
    menu_icon = "form"
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("post", "name", "body")
    list_filter = ("post", "name")
    search_fields = ("post", "name", "body")

modeladmin_register(CommentAdmin)
