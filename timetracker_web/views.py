"""Views for time tracker app."""
from pyramid.url import resource_url
from pyramid.view import view_config

from .forms import CategorySchema, TaskSchema
from .generic import View, FormView
from .models import Category, Task


@view_config(context=Category,
             renderer='templates/category_detail.jinja2')
class CategoryDetailView(View):
    """Display a category."""

    def __call__(self):
        return {
            "cat": self.context,
            "categories": list(self.context.categories(recurse=False)),
            "tasks": list(self.context.tasks(recurse=False)),
        }


@view_config(context=Task,
             renderer='templates/task_detail.jinja2')
class TaskDetailView(View):
    """Display a task."""

    def __call__(self):
        return {
            "task": self.request.context,
        }


@view_config(name='edit',
             context=Category,
             renderer='templates/edit.jinja2')
class CategoryUpdateView(FormView):
    """Update a category."""

    form = CategorySchema()


@view_config(name='edit',
             context=Task,
             renderer='templates/edit.jinja2')
class TaskUpdateView(FormView):
    """Update a task."""

    form = TaskSchema()


@view_config(name='add-category',
             context=Category,
             renderer='templates/edit.jinja2')
class CategoryAddView(FormView):
    """Add a category."""

    form = CategorySchema()

    def get_initial(self):
        return {}

    def is_valid(self, appstruct):
        self.new = self.context.add_category(title=appstruct['title'],
                                             description=appstruct['description'])

    def get_success_url(self):
        return resource_url(self.new, self.request)


@view_config(name='add-task',
             context=Category,
             renderer='templates/edit.jinja2')
class TaskAddView(FormView):
    """Add a task."""

    form = TaskSchema()

    def get_initial(self):
        return {}

    def is_valid(self, appstruct):
        self.new = self.context.add_task(title=appstruct['title'],
                                         description=appstruct['description'],
                                         mins=appstruct['mins'])

    def get_success_url(self):
        return resource_url(self.new, self.request)
