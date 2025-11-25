from django.contrib import admin
from .models import Board, Column, Tag, Task


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner", "created_at")
    list_filter = ("owner",)
    search_fields = ("name",)


@admin.register(Column)
class ColumnAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "board", "position")
    list_filter = ("board",)
    ordering = ("board", "position")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner", "color")
    list_filter = ("owner",)
    search_fields = ("name",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "column", "priority", "due_date", "created_at")
    list_filter = ("priority", "due_date", "column")
    search_fields = ("title",)
    ordering = ("column", "position")
    filter_horizontal = ("tags",)
