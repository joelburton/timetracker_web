"""Generic form/view utilities."""

import deform
from pyramid.httpexceptions import HTTPFound
from pyramid.traversal import resource_path_tuple


class Form:
    """Convenience mixin for forms."""

    def initial_dict(self, obj):
        """Populate form from ZODB object."""

        return self.flatten(obj.__dict__)

    def update_obj(self, obj, appstruct):
        """Update ZODB object from form."""

        for k, v in self.flatten(appstruct).items():
            setattr(obj, k, v)


class View:
    """Generic view."""

    def __init__(self, request):
        self.request = request
        self.context = request.context

    def breadcrumbs(self):
        curr = self.request.root
        crumbs = [curr]
        for name in resource_path_tuple(self.context)[1:]:
            obj = curr[name]
            crumbs.append(obj)
            curr = obj
        return crumbs


class FormView(View):
    """Generic add/edit view."""

    def __call__(self):
        form = deform.Form(self.form, buttons=('submit',))
        reqts = form.get_widget_resources()

        if 'submit' in self.request.params:
            try:
                appstruct = form.validate(self.request.POST.items())
            except deform.ValidationFailure as e:
                return {"form": e.render(), "reqts": reqts, "context": self.context}

            self.is_valid(appstruct)

            next_url = self.get_success_url()
            return HTTPFound(location=next_url)

        return {"form": form.render(self.get_initial()),
                "reqts": reqts,
                "context": self.context}

    def get_success_url(self):
        """Provide form redirection URL."""

        return self.request.model_url(self.context)

    def get_initial(self):
        """Initial values for form."""

        return self.form.initial_dict(self.context)

    def is_valid(self, appstruct):
        """Save values from form."""

        self.form.update_obj(self.context, appstruct)


