from django.contrib import admin
from .models import Problem, TestCase

# Register your models here.

class TestCaseInline(admin.TabularInline):
    model = TestCase
    extra = 1

class ProblemAdmin(admin.ModelAdmin):
    inlines = [TestCaseInline]

admin.site.register(Problem, ProblemAdmin)
# admin.site.register(TestCase)

