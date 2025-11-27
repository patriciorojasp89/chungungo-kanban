from django.urls import path
from .views import (
    BoardListView,
    BoardCreateView,
    BoardDetailView,
    BoardUpdateView,
    BoardDeleteView,
    ColumnCreateView,
    ColumnUpdateView,
    ColumnDeleteView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    TagListView,
    TagCreateView,
    TagUpdateView,
    TagDeleteView,
    move_task,
)

urlpatterns = [
    # LISTA DE TABLEROS
    path("", BoardListView.as_view(), name="board_list"),

    # CREAR TABLERO NUEVO
    path("nuevo/", BoardCreateView.as_view(), name="board_create"),

    # DETALLE DE TABLERO
    path("<int:pk>/", BoardDetailView.as_view(), name="board_detail"),

    # EDITAR / ELIMINAR TABLERO
    path("<int:pk>/editar/", BoardUpdateView.as_view(), name="board_edit"),
    path("<int:pk>/eliminar/", BoardDeleteView.as_view(), name="board_delete"),

    # COLUMNAS
    path("<int:board_pk>/columns/nueva/", ColumnCreateView.as_view(), name="column_create"),
    path("columns/<int:pk>/editar/", ColumnUpdateView.as_view(), name="column_edit"),
    path("columns/<int:pk>/eliminar/", ColumnDeleteView.as_view(), name="column_delete"),

    # TAREAS
    path("columns/<int:column_pk>/tasks/nueva/", TaskCreateView.as_view(), name="task_create"),
    path("tasks/<int:pk>/editar/", TaskUpdateView.as_view(), name="task_edit"),
    path("tasks/<int:pk>/eliminar/", TaskDeleteView.as_view(), name="task_delete"),
    path("tasks/mover/", move_task, name="task_move"),

    # TAGS
    path("tags/", TagListView.as_view(), name="tag_list"),
    path("tags/nueva/", TagCreateView.as_view(), name="tag_create"),
    path("tags/<int:pk>/editar/", TagUpdateView.as_view(), name="tag_edit"),
    path("tags/<int:pk>/eliminar/", TagDeleteView.as_view(), name="tag_delete"),
]

