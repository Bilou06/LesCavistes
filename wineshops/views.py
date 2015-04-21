# -*- coding: utf8 -*-
import ast

from operator import itemgetter
from django.shortcuts import render, get_object_or_404, render_to_response
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Lower
from django.db.models import Max, Min
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from . import haversine

from .forms import *
from user_profile.forms import EditUserForm
from .searchEngine import get_query


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
        return HttpResponseForbidden()
    else:
        query = Wine.objects.filter(shop_id=shop.id).order_by('area', 'producer')

        # sort
        order = 0
        try:
            order = int(request.GET.get('o'))
            # order of columns is duplicated in html and in js
            parameters = ['','producer','area__region__name','area__name','color__name', 'varietal', 'classification','vintage','capacity', 'price_min', 'price_max']
            if order>0:
                param = parameters[order]
                if order <7:
                    query = query.order_by(Lower(param).asc())
                else:
                    query = query.order_by(param)
            else:
                param = parameters[-order]
                if -order <7:
                    query = query.order_by(Lower(param).desc())
                else:
                    query = query.order_by('-'+param)
        except:
            pass

        # pagination
        paginator = Paginator(query, 20)  # Show 20 forms per page
        page = request.GET.get('page')
        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            objects = paginator.page(1)
        except EmptyPage:
            objects = paginator.page(paginator.num_pages)
        page_query = query.filter(id__in=[object.id for object in objects])
        context = {'objects': objects, 'paginator' : paginator, 'order' : order }

        return render(request, 'wineshops/edit_catalog.html', context)


@login_required
def edit_wine(request, wine_id):
    wine = get_object_or_404(Wine, id=wine_id)

    if (not wine.shop.user == request.user):
        return HttpResponseForbidden()

    if request.method == 'POST':
        wineform = WineForm(request.POST, instance=wine)
        if wineform.is_valid():
            wineform.save()
            return HttpResponseRedirect('/wineshops/edit/catalog')
    else:
        wineform = WineForm(instance=wine)

    return render(request, 'wineshops/edit_wine.html', {'wineform': wineform, 'id': wine_id})


class create_wine(generic.CreateView):
    model = Wine
    fields = ['producer', 'country', 'region', 'area', 'vintage', 'classification', 'color', 'varietal', 'capacity', 'price_min', 'price_max']
    success_url = '/wineshops/edit/catalog'

    def form_valid(self, form):
        form.instance.shop = get_object_or_404(Shop, user=self.request.user)
        return super(create_wine, self).form_valid(form)


@login_required
def confirm_remove(request, wine_ids):
    try:
        index = ast.literal_eval('[' + wine_ids + ']')
        wines = []
        for i in index:
            wine = get_object_or_404(Wine, id=i)
            wines.append(wine)
            if (not wine.shop.user == request.user):
                return HttpResponseForbidden()

        if request.method == 'POST':
            for wine in wines:
                wine.delete()
            return HttpResponseRedirect('/wineshops/edit/catalog')
        else:
            return render(request, 'wineshops/confirm_remove.html', {'wine_ids': wine_ids, 'wines': wines})

    except:
        return HttpResponseForbidden()


def search(request):
    query_what = request.GET['q']
    query_where = request.GET['o']
    try:
        lat = float(request.GET['lat'])
        lng = float(request.GET['lng'])
    except :
        return HttpResponseRedirect('/')

    results = [(shop, haversine.haversine(lng, lat, shop.longitude, shop.latitude)) for shop in Shop.objects.exclude(longitude__isnull=True, latitude__isnull=True).all()]
    results.sort(key=itemgetter(1))
    results = results[:20]
    results = [{'shop': a[0],
                'dist': "%.1f" %a[1],
                'nb': Wine.objects.filter(shop_id=a[0].id).count(),
                'price': Wine.objects.filter(shop_id=a[0].id).aggregate(Min('price_min'), Max('price_max')),
                } for a in results]

    return render_to_response('wineshops/search_results.html',
                          { 'query_what': query_what,
                            'query_where' : query_where,
                            'results': results,
                            'lat' : lat,
                            'lng' : lng},
                          context_instance=RequestContext(request))


'''
def search(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        if (len(query_string)==0 or query_string=='Trouvez votre vin près de chez vous'):
            return HttpResponseRedirect('/')

        entry_query = get_query(query_string, ['producer','area__region__name','area__name','color__name', 'varietal', 'classification','vintage','capacity',])

        found_entries = Wine.objects.filter(entry_query)# .order_by(DISTANCE)

    return render_to_response('wineshops/search_results.html',
                          { 'query_string': query_string, 'found_entries': found_entries },
                          context_instance=RequestContext(request))
                          '''