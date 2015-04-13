# -*- coding: utf8 -*-
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseForbidden
from django.contrib.auth.decorators import login_required

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
        form = EditUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/wineshops/edit/user')  # Redirect after POST
        else:
            return HttpResponse('ko')
    else:
        form = EditUserForm(instance=request.user)  # An unbound form

    return render(request, 'wineshops/edit_user.html', {
        'form': form,
    })


@login_required
def edit_wineshop(request):
    shop, created = Shop.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = WineshopForm(request.POST, instance=shop)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/wineshops/edit/wineshop')  # Redirect after POST
    else:
        form = WineshopForm(instance=shop)

    return render(request, 'wineshops/edit_wineshop.html', {
        'form': form,
    })


@login_required
def edit_catalog(request):
    shop = get_object_or_404(Shop, user=request.user)

    if request.method == 'POST':
        formset = ShopFormSet(request.POST, instance=shop)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect('wineshops/edit/catalog') # Redirect after POST
    else:
        formset = ShopFormSet(instance=shop)  # An unbound form

    return render(request, 'wineshops/edit_catalog.html', {
        'shop': shop,
    })

@login_required
def edit_wine(request, wine_id):
    wine = get_object_or_404(Wine, id=wine_id)

    if (not wine.shop.user == request.user):
        raise HttpResponseForbidden()

    if request.method == 'POST':
        wineform = WineForm(request.POST, instance=wine)
        if wineform.is_valid():
            wineform.save()
            return HttpResponseRedirect('/wineshops/edit/catalog')
    else:
        wineform=WineForm(instance=wine)

    return render(request, 'wineshops/edit_wine.html', {'wineform' : wineform, 'id' : wine_id})


class create_wine(generic.CreateView):
    model = Wine
    fields = ['producer', 'area', 'vintage', 'classification', 'color', 'capacity', 'price_min', 'price_max']
    success_url = '/wineshops/edit/catalog'
    def form_valid(self, form):
        form.instance.shop = get_object_or_404(Shop, user=self.request.user)
        return super(create_wine, self).form_valid(form)

