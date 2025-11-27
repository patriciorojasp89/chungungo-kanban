from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Board, Column, Task, Tag
from django.shortcuts import get_object_or_404
from django.forms import ModelForm
from .forms import TaskForm
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import json
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages





class BoardListView(LoginRequiredMixin, ListView):
    model = Board
    template_name = "boards/board_list.html"
    context_object_name = "boards"

    def get_queryset(self):
        return Board.objects.filter(owner=self.request.user).order_by("-created_at")

class BoardCreateView(LoginRequiredMixin, CreateView):
    model = Board
    template_name = "boards/board_form.html"
    fields = ["name", "description"]
    success_url = reverse_lazy("board_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class BoardUpdateView(LoginRequiredMixin, UpdateView):
    model = Board
    template_name = "boards/board_form.html"
    fields = ["name", "description"]
    success_url = reverse_lazy("board_list")

    def get_queryset(self):
        return Board.objects.filter(owner=self.request.user)

class BoardDeleteView(LoginRequiredMixin, DeleteView):
    model = Board
    template_name = "boards/board_confirm_delete.html"
    success_url = reverse_lazy("board_list")

    def get_queryset(self):
        return Board.objects.filter(owner=self.request.user)

class BoardDetailView(LoginRequiredMixin, DetailView):
    model = Board
    template_name = "boards/board_detail.html"
    context_object_name = "board"

    def get_queryset(self):
        return Board.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["columns"] = self.object.columns.all().order_by("position")
        return context

class ColumnCreateView(LoginRequiredMixin, CreateView):
    model = Column
    template_name = "boards/column_form.html"
    fields = ["name", "position"]

    def dispatch(self, request, *args, **kwargs):
        self.board = get_object_or_404(
            Board,
            pk=self.kwargs["board_pk"],
            owner=self.request.user,  
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.board = self.board
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("board_detail", kwargs={"pk": self.board.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["board"] = self.board
        return context


class ColumnUpdateView(LoginRequiredMixin, UpdateView):
    model = Column
    template_name = "boards/column_form.html"
    fields = ["name", "position"]

    def get_queryset(self):
        return Column.objects.filter(board__owner=self.request.user)

    def get_success_url(self):
        return reverse_lazy("board_detail", kwargs={"pk": self.object.board.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["board"] = self.object.board
        return context


class ColumnDeleteView(LoginRequiredMixin, DeleteView):
    model = Column
    template_name = "boards/column_confirm_delete.html"

    def get_queryset(self):
        return Column.objects.filter(board__owner=self.request.user)

    def get_success_url(self):
        return reverse_lazy("board_detail", kwargs={"pk": self.object.board.pk})


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = "boards/task_form.html"
    form_class = TaskForm

    def dispatch(self, request, *args, **kwargs):
        self.column = get_object_or_404(
            Column,
            pk=self.kwargs["column_pk"],
            board__owner=self.request.user
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.column = self.column
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("board_detail", kwargs={"pk": self.column.board.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["column"] = self.column
        return context


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = "boards/task_form.html"
    form_class = TaskForm

    def get_queryset(self):
        return Task.objects.filter(column__board__owner=self.request.user)

    def get_success_url(self):
        return reverse_lazy(
            "board_detail",
            kwargs={"pk": self.object.column.board.pk}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["column"] = self.object.column
        return context


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "boards/task_confirm_delete.html"

    def get_queryset(self):
        return Task.objects.filter(column__board__owner=self.request.user)

    def get_success_url(self):
        return reverse_lazy(
            "board_detail",
            kwargs={"pk": self.object.column.board.pk}
        )


class TagListView(LoginRequiredMixin, ListView):
    model = Tag
    template_name = "boards/tag_list.html"
    context_object_name = "tags"

    def get_queryset(self):
        return Tag.objects.filter(owner=self.request.user).order_by("name")


class TagCreateView(LoginRequiredMixin, CreateView):
    model = Tag
    template_name = "boards/tag_form.html"
    fields = ["name", "color"]
    success_url = reverse_lazy("tag_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class TagUpdateView(LoginRequiredMixin, UpdateView):
    model = Tag
    template_name = "boards/tag_form.html"
    fields = ["name", "color"]
    success_url = reverse_lazy("tag_list")

    def get_queryset(self):
       
        return Tag.objects.filter(owner=self.request.user)


class TagDeleteView(LoginRequiredMixin, DeleteView):
    model = Tag
    template_name = "boards/tag_confirm_delete.html"
    success_url = reverse_lazy("tag_list")

    def get_queryset(self):
        return Tag.objects.filter(owner=self.request.user)


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Tu cuenta fue creada correctamente. Ahora puedes iniciar sesión."
            )
            return redirect("login")  # nombre de la URL de django.contrib.auth.urls
    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form": form})



@login_required
@require_POST
def move_task(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return HttpResponseBadRequest("JSON inválido")

    task_id = data.get("task_id")
    column_id = data.get("column_id")
    ordered_task_ids = data.get("ordered_task_ids", [])

    if not task_id or not column_id:
        return HttpResponseBadRequest("Faltan parámetros")

    
    task = get_object_or_404(
        Task,
        pk=task_id,
        column__board__owner=request.user,
    )

    
    new_column = get_object_or_404(
        Column,
        pk=column_id,
        board__owner=request.user,
    )

    
    task.column = new_column
    task.save()

    
    if isinstance(ordered_task_ids, list) and ordered_task_ids:
        for index, t_id in enumerate(ordered_task_ids, start=1):
            try:
                t = Task.objects.get(
                    pk=t_id,
                    column__board__owner=request.user,
                )
                t.position = index
                t.save()
            except Task.DoesNotExist:
                
                continue

    return JsonResponse(
        {
            "status": "ok",
            "task_id": task_id,
            "new_column_id": column_id,
            "ordered_task_ids": ordered_task_ids,
        }
    )
