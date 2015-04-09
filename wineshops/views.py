from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Shop
from .forms import *
from user_profile.forms import EditUserForm

class IndexView(generic.ListView):
    template_name = 'wineshops/index.html'
    context_object_name = 'shop_list'

    def get_queryset(self):
        return Shop.objects.all()

class DetailView(generic.DetailView):
    model = Shop
    template_name = 'wineshops/detail.html'

@login_required
def edit_user(request):
    if request.method == 'POST':
        form = EditUserForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/wineshops/edit/user') # Redirect after POST
        else:
            return HttpResponse('ko')
    else:
        form = EditUserForm(instance=request.user) # An unbound form

    return render(request, 'wineshops/edit_user.html', {
        'form': form,
    })

@login_required
def edit_wineshop(request):
    if request.method == 'POST':
        form = WineshopForm(request.POST)
        if form.is_valid():
            name        = form.cleaned_data('name')
            address     = form.cleaned_data('address')
            city        = form.cleaned_data('city')
            zip_code    = form.cleaned_data('zip_code')
            country     = form.cleaned_data('country')
            description = form.cleaned_data('description')
            phone       = form.cleaned_data('phone')
            mail        = form.cleaned_data('mail')
            web         = form.cleaned_data('web')
            return HttpResponseRedirect('wineshops/edit_wineshop.html') # Redirect after POST
    else:
        form = WineshopForm() # An unbound form

    return render(request, 'wineshops/edit_wineshop.html', {
        'form': form,
    })

@login_required
def edit_catalog(request):
    if request.method == 'POST':
        form = WineshopForm(request.POST)
        if form.is_valid():
            name        = form.cleaned_data('name')
            address     = form.cleaned_data('address')
            city        = form.cleaned_data('city')
            zip_code    = form.cleaned_data('zip_code')
            country     = form.cleaned_data('country')
            description = form.cleaned_data('description')
            phone       = form.cleaned_data('phone')
            mail        = form.cleaned_data('mail')
            web         = form.cleaned_data('web')
            return HttpResponseRedirect('wineshops/edit_catalog.html') # Redirect after POST
    else:
        form = WineshopForm() # An unbound form

    return render(request, 'wineshops/edit_catalog.html', {
        'form': form,
    })

