from django.contrib import admin

from .models import City, Category, Vacancy, Error, Url


class CityAdmin(admin.ModelAdmin):
    prepopulated_fields = ({'slug': ('name',)})
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = ({'slug': ('name',)})
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


class VacancyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')


admin.site.register(City, CityAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(Error)
admin.site.register(Url)
