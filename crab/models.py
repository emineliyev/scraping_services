from django.db import models
import jsonfield


def default_urls():
    return {
        "boss": "",
        "elan": ""
    }


class City(models.Model):
    name = models.CharField(max_length=60, verbose_name='Şəhər adı', unique=True)
    slug = models.SlugField(max_length=60, unique=True, verbose_name='Slaq adı')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Şəhər'
        verbose_name_plural = 'Şəhər'
        ordering = ['name']


class Category(models.Model):
    name = models.CharField(max_length=60, verbose_name='Kateqoriya adı')
    slug = models.SlugField(max_length=60, unique=True, verbose_name='Slaq adı')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Kateqoriya'
        verbose_name_plural = 'Kateqoriya'
        ordering = ['name']


class Vacancy(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=250, verbose_name='Vakansiya adı')
    company = models.CharField(max_length=250, verbose_name='İş verən şirkət')
    description = models.TextField(verbose_name='Açıqlama')
    salary = models.CharField(max_length=60, verbose_name='Maaş')
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Şəhər')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Kateqoriya')
    create_at = models.DateField(auto_now_add=True, verbose_name='Yükləmə tarixi')

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Vakansiya'
        verbose_name_plural = 'Vakansiya'
        ordering = ['-create_at']


class Error(models.Model):
    create_at = models.DateField(auto_now_add=True, verbose_name='Xətanın tarixi')
    data = jsonfield.JSONField()

    def __str__(self):
        return f"{self.create_at}"


class Url(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Şəhər')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Kateqoriya')
    url_data = jsonfield.JSONField(default=default_urls)

    def __str__(self):
        return f"Url"

    class Meta:
        unique_together = ("city", "category")
        verbose_name = 'Url'
        verbose_name_plural = 'Url'