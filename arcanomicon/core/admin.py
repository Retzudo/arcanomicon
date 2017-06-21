from django.contrib import admin
from core import models


class AddOnVersionInline(admin.StackedInline):
    model = models.AddOnVersion
    extra = 0


class AddOnAdmin(admin.ModelAdmin):
    inlines = [AddOnVersionInline]


admin.site.register(models.User)
admin.site.register(models.AddOn, AddOnAdmin)
admin.site.register(models.AddOnPage)
admin.site.register(models.Image)