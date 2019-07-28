from django.shortcuts import render, get_object_or_404, redirect
from .models import Contact
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q


class HomeView(LoginRequiredMixin, ListView):
    template_name = 'index.html'
    model = Contact
    context_object_name = 'contact'

    def get_queryset(self):
        contact = super().get_queryset()
        return contact.filter(manager=self.request.user)


class DetailView(LoginRequiredMixin, DetailView):
    template_name = 'detail.html'
    model = Contact
#     # queryset = Contact.objects.all()

#     def get_object(self):
#         pk = self.kwargs.get("id")
#         return get_object_or_404(Contact, id)


# def detail(request, id):
#     context = {
#         'contact': get_object_or_404(Contact, pk=id)
#     }
#     return render(request, 'detail.html', context)

class ContactCreateView(LoginRequiredMixin, CreateView):
    model = Contact
    template_name = 'create.html'
    fields = ['name', 'email', 'phone', 'info', 'gender', 'image']

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.manager = self.request.user
        instance.save()
        messages.success(
            self.request, 'Your contact has been successfully created')
        return redirect('app:home')


class ContactUpdateView(LoginRequiredMixin, UpdateView):
    model = Contact
    template_name = 'update.html'
    fields = ['name', 'email', 'phone', 'info', 'gender', 'image']

    def form_valid(self, form):
        instance = form.save()
        messages.success(
            self.request, 'Your contact has been successfully updated')
        return redirect('app:detail', instance.pk)


class ContactDeleteView(LoginRequiredMixin,  DeleteView):
    model = Contact
    template_name = 'delete.html'
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        messages.success(
            self.request, 'Your contact has been successfully deleted')
        return super().delete(self, request, *args, **kwargs)


class SignUpview(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('app:home')


@login_required
def search(request):
    if request.GET:
        ser = request.GET['search']
        search_result = Contact.objects.filter(
            Q(name__icontains=ser) |
            Q(email__icontains=ser) |
            Q(info__icontains=ser) |
            Q(phone__icontains=ser))
        context = {
            'search': ser,
            'res': search_result.filter(manager=request.user),
        }
        return render(request, 'search.html', context)
    else:
        return redirect('home')
