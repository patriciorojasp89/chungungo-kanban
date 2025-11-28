from django import forms
from .models import Board, Column, Tag, Task



# -------------------------------------
# TABLEROS
# -------------------------------------
class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ["name", "description"]

        labels = {
            "name": "Nombre del tablero",
            "description": "Descripción",
        }

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
        }


# -------------------------------------
# COLUMNAS
# -------------------------------------
class ColumnForm(forms.ModelForm):
    class Meta:
        model = Column
        fields = ["name"]

        labels = {
            "name": "Nombre de la columna",
        }

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }


# -------------------------------------
# ETIQUETAS (tags)
# -------------------------------------
class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name", "color"]

        labels = {
            "name": "Nombre de la etiqueta",
            "color": "Color",
        }

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "color": forms.TextInput(attrs={"class": "form-control", "type": "color"}),
        }


# -------------------------------------
# TAREAS
# -------------------------------------
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "priority", "due_date", "tags"]

        labels = {
            "title": "Título",
            "description": "Descripción",
            "priority": "Prioridad",
            "due_date": "Fecha de vencimiento",
            "tags": "Etiquetas",
        }

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "priority": forms.Select(attrs={"class": "form-control"}),
            "due_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "tags": forms.SelectMultiple(attrs={"class": "form-control"}),
        }
