from django.contrib import admin
from core import models


class AddOnVersionInline(admin.StackedInline):
    model = models.AddOnVersion
    extra = 0


class AddOnPageTabular(admin.TabularInline):
    model = models.AddOnPage


class AddOnScreenshotTabular(admin.TabularInline):
    model = models.Screenshot
    extra = 1


class AddOnAdmin(admin.ModelAdmin):
    inlines = [AddOnVersionInline, AddOnPageTabular, AddOnScreenshotTabular]


admin.site.register(models.User)
admin.site.register(models.AddOn, AddOnAdmin)
