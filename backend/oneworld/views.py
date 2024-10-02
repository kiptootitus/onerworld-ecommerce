from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import FormView
from django.views.generic import RedirectView
from django.views.generic import ArchiveIndexView



class UserRegesterGenericView(CreateView):

    def form_valid(self, form):
        form.save()
        return super(UserRegesterGenericView, self).form_valid(form)