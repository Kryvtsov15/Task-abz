from django.shortcuts import render
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.views.generic.base import View
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import login, logout
from .models import Human
from django.views.generic import TemplateView
from django.db.models import Q
import json


# Create your views here.
def base(request):
    return render(request, "base.html")

def list_of_persons(request):
    return render(request, "list_of_persons.html")



class List(TemplateView):
    template_name = "info_persons.html"
    def get(self, request, param = 'full_name'):
        if request.user.is_authenticated:
            if param == "full_name":
                all_humans = Human.objects.order_by("full_name")
            elif param == "position":
                all_humans = Human.objects.order_by("position")
            elif param == "employment_date":
                all_humans = Human.objects.order_by("employment_date")
            elif param == "salary":
                all_humans = Human.objects.order_by("salary")
            elif param == "parent":
                all_humans = Human.objects.order_by("parent")
            ctx = {
                "all_humans": list(all_humans)
            }
            return render(request , self.template_name , ctx)
        else:
            return render(request, self.template_name, {})


    def post(self, request):
        if request.user.is_authenticated:
            query = request.POST['search']
            result_list = Human.search_manager.search(query)

            if result_list.count() != 0:
                context = {
                    'result_list': result_list,

                    'query': query,
                }
            else:
                context ={
                    'empty': "Ничего не найдено :(",
                    'query': query,
                }
            return render(request , 'result.html' , context)
        else:
            return render(request, 'result.html', {})



class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "/login/"
    template_name = "register.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(RegisterFormView, self).form_invalid(form)

class LoginFormView(FormView):
    form_class = AuthenticationForm
    success_url = "/"
    template_name = "login.html"

    def form_valid(self, form):
        self.user = form.get_user()

        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)

class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")

def show_human(request):
    return render(request, "list_of_person.html", {'human': Human.objects.all()})

class MainView(TemplateView):
    template_name = "list_of_persons.html"

    def get(self, request):
            humans = Human.objects.all()
            ctx = {}
            ctx['human'] = humans
            return render(request,self.template_name, ctx)

    def show_human(request):
        return render(request, "list_of_person.html", {'human': Human.objects.all()})