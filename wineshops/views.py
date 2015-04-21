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
from .models import Country, Region, Area
from user_profile.forms import EditUserForm
from .searchEngine import get_query

import logging


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
        form = WineForm(request.POST, instance=wine)
        if form.is_valid():

            country = form.cleaned_data['country']
            if not country or( form.cleaned_data['country_hidden'] and country.name != form.cleaned_data['country_hidden']):
                country, created = Country.objects.get_or_create(name=form.cleaned_data['country_hidden'], defaults={'custom':True, 'name':form.cleaned_data['country_hidden'] })
            form.instance.country = country

            region = form.cleaned_data['region']
            if not region or (form.cleaned_data['region_hidden'] and region.name != form.cleaned_data['region_hidden']):
                region, created = Region.objects.get_or_create(name=form.cleaned_data['region_hidden'], country=country, defaults={'custom':True, 'name':form.cleaned_data['region_hidden'], 'country':country })
            elif region.country != country:
                region, created = Region.objects.get_or_create(name=region.name, country=country, defaults={'custom':True, 'name':region.name, 'country':country })
            form.instance.region = region

            area = form.cleaned_data['area']
            if not area or(form.cleaned_data['area_hidden'] and area.name != form.cleaned_data['area_hidden']):
                area, created = Area.objects.get_or_create(name=form.cleaned_data['area_hidden'], region=region, defaults={'custom':True, 'name':form.cleaned_data['area_hidden'], 'region':region })
            elif region.country != country:
                area, created = Area.objects.get_or_create(name=area.name, region=region, defaults={'custom':True, 'name':area.name, 'region':region })
            form.instance.area = area

            form.save()
            return HttpResponseRedirect('/wineshops/edit/catalog')
    else:
        form = WineForm(instance=wine)

    generic_countries = set(Country.objects.filter(custom=False).all())
    user_countries_ids = set(Wine.objects.filter(shop__user=request.user).values_list('country', flat=True).distinct())
    user_countries = Country.objects.filter(pk__in=user_countries_ids)
    countries = list(generic_countries.union(user_countries))
    countries.sort(key=Country.__str__)

    context = {
        'form': form,
        'id': wine_id,
        'title' : "Mon vin",
        'countries' : countries,
        }
    return render(request, 'wineshops/wine_form.html', context )




class create_wine(generic.CreateView):
    form_class = WineForm
    template_name = 'wineshops/wine_form.html'
    success_url = '/wineshops/edit/catalog'


    def form_valid(self, form):
        form.instance.shop = get_object_or_404(Shop, user=self.request.user)

        country = form.cleaned_data['country']
        if not country and form.cleaned_data['country_hidden']:
            country, created = Country.objects.get_or_create(name=form.cleaned_data['country_hidden'], defaults={'custom':True, 'name':form.cleaned_data['country_hidden'] })
        form.instance.country = country

        region = form.cleaned_data['region']
        if not region:
            if form.cleaned_data['region_hidden']:
                region, created = Region.objects.get_or_create(name=form.cleaned_data['region_hidden'], country=country, defaults={'custom':True, 'name':form.cleaned_data['region_hidden'], 'country':country })
        elif region.country != country:
            region, created = Region.objects.get_or_create(name=region.name, country=country, defaults={'custom':True, 'name':region.name, 'country':country })
        form.instance.region = region

        area = form.cleaned_data['area']
        if not area:
            if form.cleaned_data['area_hidden']:
                area, created = Area.objects.get_or_create(name=form.cleaned_data['area_hidden'], region=region, defaults={'custom':True, 'name':form.cleaned_data['area_hidden'], 'region':region })
        elif region.country != country:
            area, created = Area.objects.get_or_create(name=area.name, region=region, defaults={'custom':True, 'name':area.name, 'region':region })
        form.instance.area = area

        return super(create_wine, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super(create_wine, self).get_context_data(**kwargs)
        generic_countries = set(Country.objects.filter(custom=False).all())
        user_countries_ids = set(Wine.objects.filter(shop__user=self.request.user).values_list('country', flat=True).distinct())
        user_countries = Country.objects.filter(pk__in=user_countries_ids)
        countries = list(generic_countries.union(user_countries))
        countries.sort(key=Country.__str__)
        ctx['countries'] = countries

        ctx['title'] = 'Ajouter un vin'
        return ctx


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



def regions(request):
    country_id = None
    if request.method == 'GET':
        country_id = request.GET.get('country_id', -1)
    regions = []
    if country_id:
        generic_regions = set(Region.objects.filter(country_id=country_id,custom=False).all())
        user_regions_ids = set(Wine.objects.filter(shop__user=request.user).values_list('region', flat=True).distinct())
        user_regions = Region.objects.filter(pk__in=user_regions_ids)
        regions = list(generic_regions.union(user_regions))
        regions.sort(key=Country.__str__)

    return HttpResponse('|'.join([r.name+'#'+str(r.id) for r in regions]))


def areas(request):
    region_id = None
    if request.method == 'GET':
        region_id = request.GET.get('region_id', -1)
    areas = []
    if region_id:
        generic_areas = set(Area.objects.filter(region_id=region_id,custom=False).all())
        user_areas_ids = set(Wine.objects.filter(shop__user=request.user).values_list('area', flat=True).distinct())
        user_areas = Area.objects.filter(pk__in=user_areas_ids)
        areas = list(generic_areas.union(user_areas))
        areas.sort(key=Country.__str__)

    return HttpResponse('|'.join([r.name+'#'+str(r.id) for r in areas]))

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