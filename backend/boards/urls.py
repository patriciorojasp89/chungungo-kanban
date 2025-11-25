from django.urls import path
from . import views

urlpatterns = [
    path("", views.BoardListView.as_view(), name="board_list"),
    path("boards/nuevo/", views.BoardCreateView.as_view(), name="board_create"),
    path("boards/<int:pk>/", views.BoardDetailView.as_view(), name="board_detail"),
    path("boards/<int:pk>/editar/", views.BoardUpdateView.as_view(), name="board_edit"),
    path("boards/<int:pk>/eliminar/", views.BoardDeleteView.as_view(), name="board_delete"),
    path("boards/<int:board_pk>/columns/nueva/",views.ColumnCreateView.as_view(),name="column_create"),
    path("columns/<int:pk>/editar/",views.ColumnUpdateView.as_view(),name="column_edit"),
    path("columns/<int:pk>/eliminar/",views.ColumnDeleteView.as_view(),name="column_delete"),
    path("columns/<int:column_pk>/tasks/nueva/",views.TaskCreateView.as_view(),name="task_create"),
    path("tasks/<int:pk>/editar/",views.TaskUpdateView.as_view(),name="task_edit"),
    path("tasks/<int:pk>/eliminar/",views.TaskDeleteView.as_view(),name="task_delete"),
    path("tasks/mover/",views.move_task,name="task_move"),
    path("tags/", views.TagListView.as_view(), name="tag_list"),
    path("tags/nueva/", views.TagCreateView.as_view(), name="tag_create"),
    path("tags/<int:pk>/editar/", views.TagUpdateView.as_view(), name="tag_edit"),
    path("tags/<int:pk>/eliminar/", views.TagDeleteView.as_view(), name="tag_delete"),
]
