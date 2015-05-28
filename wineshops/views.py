# -*- coding: utf-8 -*-
import ast

from operator import itemgetter
from PIL.Image import Image
from django.shortcuts import render, get_object_or_404, render_to_response
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Lower
from django.db.models import Max, Min
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.template import Context, loader
from rest_framework import status

from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer

from . import haversine

from .forms import *
from .models import Country, Region, Area, Color, Capacity
from user_profile.forms import EditUserForm, EditUserProfileForm
from .searchEngine import get_query
from .renderers import JPEGRenderer

import urllib
import json

import logging
from user_profile.models import UserProfile

logger = logging.getLogger(__name__)


class IndexView(generic.ListView):
    template_name = 'wineshops/index.html'
    context_object_name = 'shop_list'

    def get_queryset(self):
        return Shop.objects.all()


@login_required
def edit(request):
    shop, created = Shop.objects.get_or_create(user=request.user)
    if (shop.filled):
        return edit_catalog(request)
    else:
        return edit_wineshop(request)


@login_required
def edit_user(request):
    shop, created = Shop.objects.get_or_create(user=request.user)
    userProfile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        userForm = EditUserForm(request.POST, instance=request.user)
        profileForm = EditUserProfileForm(request.POST, instance=userProfile)
        if userForm.is_valid() and profileForm.is_valid():

            userForm.save()
            profileForm.save()
            return HttpResponseRedirect('/wineshops/edit/user')  # Redirect after POST
        else:
            return HttpResponseRedirect('/wineshops/edit/user')  # todo : add a warning to explain the error
    else:
        userForm = EditUserForm(instance=request.user)  # An unbound form
        profileForm = EditUserProfileForm(instance=userProfile)

    return render(request, 'wineshops/edit_user.html', {
        'userForm': userForm,
        'profileForm': profileForm,
        'filled': shop.filled
    })


@login_required
def edit_wineshop(request):
    shop, created = Shop.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        wineForm = WineshopForm(request.POST, instance=shop)
        image = request.FILES.get('image')

        wineForm.image = image
        if wineForm.is_valid():
            wineForm.instance.image = image
            wineForm.instance.filled = True
            wineForm.save()
            return HttpResponseRedirect('/wineshops/edit/wineshop')  # Redirect after POST
    else:

        if not shop.filled:
            userProfile = UserProfile.objects.get(user=request.user)
            wineForm = WineshopForm(instance=shop, initial={
                'name': userProfile.name,
                'address': userProfile.address,
                'zip_code': userProfile.zip_code,
                'city': userProfile.city,
                'country': userProfile.country,
                'mail': userProfile.user.email,
                })
        else:
            wineForm = WineshopForm(instance=shop)

    return render(request, 'wineshops/edit_wineshop.html', {
        'form': wineForm,
        'filled': shop.filled
    })


@login_required
def edit_catalog(request):
    shop = get_object_or_404(Shop, user=request.user)

    if request.method == 'POST':
        return HttpResponseForbidden()
    else:
        query = Wine.objects.filter(shop_id=shop.id)

    return display_wines(request, 'wineshops/edit_catalog.html', query, {'filled': shop.filled})


def display_wines(request, template, query, context={}):
    query = query.order_by('country__name', 'region__name', 'area__name', 'producer')

    # sort
    order = 0
    try:
        order = int(request.GET.get('o'))
        # order of columns is duplicated in html and in js
        parameters = ['',
                      'producer',
                      'country__name',
                      'region__name',
                      'area__name',
                      'color__name',
                      'varietal',
                      'classification',
                      'vintage',
                      'capacity',
                      'price_min',
                      'price_max',
                      'in_stock']
        if order > 0:
            param = parameters[order]
            if order < 7:
                query = query.order_by(Lower(param).asc())
            else:
                query = query.order_by(param)
        else:
            param = parameters[-order]
            if -order < 7:
                query = query.order_by(Lower(param).desc())
            else:
                query = query.order_by('-' + param)
    except:
        pass

    # pagination
    paginator = Paginator(query.all(), 20)  # Show 20 forms per page
    p = request.GET.get('page')
    try:
        objects = paginator.page(p).object_list
        page = int(p)
    except PageNotAnInteger:
        objects = paginator.page(1).object_list
        page = 1
    except EmptyPage:
        objects = paginator.page(paginator.num_pages).object_list
        page = paginator.num_pages

    c = context.copy()
    c.update({'objects': objects,
              'paginator': paginator,
              'order': order,
              'page': page})

    return render(request, template, c)


@login_required
def edit_wine(request, wine_id):
    shop, created = Shop.objects.get_or_create(user=request.user)
    wine = get_object_or_404(Wine, id=wine_id)

    if not wine.shop.user == request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = WineForm(request.POST, instance=wine)
        if form.is_valid():

            country = form.cleaned_data['country']
            if not country or (
                        form.cleaned_data['country_hidden'] and country.name != form.cleaned_data['country_hidden']):
                country, created = Country.objects.get_or_create(name=form.cleaned_data['country_hidden'],
                                                                 defaults={'custom': True,
                                                                           'name': form.cleaned_data['country_hidden']})
            form.instance.country = country

            region = form.cleaned_data['region']
            if not region or (form.cleaned_data['region_hidden'] and region.name != form.cleaned_data['region_hidden']):
                region, created = Region.objects.get_or_create(name=form.cleaned_data['region_hidden'], country=country,
                                                               defaults={'custom': True,
                                                                         'name': form.cleaned_data['region_hidden'],
                                                                         'country': country})
            elif region.country != country:
                region, created = Region.objects.get_or_create(name=region.name, country=country,
                                                               defaults={'custom': True, 'name': region.name,
                                                                         'country': country})
            form.instance.region = region

            area = form.cleaned_data['area']
            if not area or (form.cleaned_data['area_hidden'] and area.name != form.cleaned_data['area_hidden']):
                area, created = Area.objects.get_or_create(name=form.cleaned_data['area_hidden'], region=region,
                                                           defaults={'custom': True,
                                                                     'name': form.cleaned_data['area_hidden'],
                                                                     'region': region})
            elif area.region != region:
                area, created = Area.objects.get_or_create(name=area.name, region=region,
                                                           defaults={'custom': True, 'name': area.name,
                                                                     'region': region})
            form.instance.area = area

            color = form.cleaned_data['color']
            if not color or (form.cleaned_data['color_hidden'] and color.name != form.cleaned_data['color_hidden']):
                color, created = Color.objects.get_or_create(name=form.cleaned_data['color_hidden'],
                                                             defaults={'custom': True,
                                                                       'name': form.cleaned_data['color_hidden']})
            form.instance.color = color

            capacity = form.cleaned_data['capacity']
            if not capacity or (
                form.cleaned_data['capacity_hidden'] and capacity.volume != form.cleaned_data['capacity_hidden']):
                capacity, created = Capacity.objects.get_or_create(volume=form.cleaned_data['capacity_hidden'],
                                                                   defaults={'custom': True,
                                                                             'volume': form.cleaned_data[
                                                                                 'capacity_hidden']})
            form.instance.capacity = capacity

            form.save()
            return HttpResponseRedirect('/wineshops/edit/catalog')
    else:
        form = WineForm(instance=wine)

    context = {
        'form': form,
        'id': wine_id,
        'title': "Mon vin",
        'countries': _get_user_data(Country, 'country', Country.__str__, request.user),
        'colors': _get_user_data(Color, 'color', Color.__str__, request.user),
        'capacities': _get_user_data(Capacity, 'capacity', Capacity.value, request.user),
        'filled': shop.filled,
    }
    return render(request, 'wineshops/wine_form_update.html', context)


class create_wine(generic.CreateView):
    form_class = WineForm
    template_name = 'wineshops/wine_form_create.html'

    button_create_and_return = "Enregister et retourner au catalogue"
    button_create_and_again = "Enregister et ajouter un nouveau"

    def get_success_url(self):
        if self.request.POST.get('direction') == self.button_create_and_return:
            return '/wineshops/edit/catalog'
        elif self.request.POST.get('direction') == self.button_create_and_again:
            return '/wineshops/create/wine/'
        logger.warning('unexpected redirection value in create_wine :' + self.request.POST.get('direction'))
        return '/wineshops/edit/catalog'


    def form_valid(self, form):
        form.instance.shop = get_object_or_404(Shop, user=self.request.user)

        country = form.cleaned_data['country']
        if not country:
            if form.cleaned_data['country_hidden']:
                country, created = Country.objects.get_or_create(name=form.cleaned_data['country_hidden'],
                                                                 defaults={'custom': True,
                                                                           'name': form.cleaned_data['country_hidden']})
        form.instance.country = country

        region = form.cleaned_data['region']
        if not region:
            if form.cleaned_data['region_hidden']:
                region, created = Region.objects.get_or_create(name=form.cleaned_data['region_hidden'], country=country,
                                                               defaults={'custom': True,
                                                                         'name': form.cleaned_data['region_hidden'],
                                                                         'country': country})
        elif region.country != country:
            region, created = Region.objects.get_or_create(name=region.name, country=country,
                                                           defaults={'custom': True, 'name': region.name,
                                                                     'country': country})
        form.instance.region = region

        area = form.cleaned_data['area']
        if not area:
            if form.cleaned_data['area_hidden']:
                area, created = Area.objects.get_or_create(name=form.cleaned_data['area_hidden'], region=region,
                                                           defaults={'custom': True,
                                                                     'name': form.cleaned_data['area_hidden'],
                                                                     'region': region})
        elif area.region != region:
            area, created = Area.objects.get_or_create(name=area.name, region=region,
                                                       defaults={'custom': True, 'name': area.name, 'region': region})
        form.instance.area = area

        color = form.cleaned_data['color']
        if not color:
            if form.cleaned_data['color_hidden']:
                color, created = Color.objects.get_or_create(name=form.cleaned_data['color_hidden'],
                                                         defaults={'custom': True,
                                                                   'name': form.cleaned_data['color_hidden']})
        form.instance.color = color

        capacity = form.cleaned_data['capacity']
        if not capacity:
            if form.cleaned_data['capacity_hidden']:
                capacity, created = Capacity.objects.get_or_create(volume=form.cleaned_data['capacity_hidden'],
                                                               defaults={'custom': True,
                                                                         'volume': form.cleaned_data[
                                                                             'capacity_hidden']})
        form.instance.capacity = capacity

        return super(create_wine, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super(create_wine, self).get_context_data(**kwargs)
        generic_countries = set(Country.objects.filter(custom=False).all())
        user_countries_ids = set(
            Wine.objects.filter(shop__user=self.request.user).values_list('country', flat=True).distinct())
        user_countries = Country.objects.filter(pk__in=user_countries_ids)
        countries = list(generic_countries.union(user_countries))
        countries.sort(key=Country.__str__)
        ctx['countries'] = _get_user_data(Country, 'country', Country.__str__, self.request.user)
        ctx['colors'] = _get_user_data(Color, 'color', Color.__str__, self.request.user)
        ctx['capacities'] = _get_user_data(Capacity, 'capacity', Capacity.value, self.request.user)

        shop, created = Shop.objects.get_or_create(user=self.request.user)
        ctx['filled'] = shop.filled,

        ctx['title'] = 'Ajouter un vin'

        ctx['button_create_and_return'] = self.button_create_and_return
        ctx['button_create_and_again'] = self.button_create_and_again
        return ctx


def _get_user_data(data, field, sortkey, user):
    generic_objects = set(data.objects.filter(custom=False).all())
    user_objects_ids = set(Wine.objects.filter(shop__user=user).values_list(field, flat=True).distinct())
    user_objects = data.objects.filter(pk__in=user_objects_ids)
    objects = list(generic_objects.union(user_objects))
    objects.sort(key=sortkey)
    return objects


@login_required
def confirm_remove(request, wine_ids):
    try:
        index = ast.literal_eval('[' + wine_ids + ']')
        wines = []
        for i in index:
            wine = get_object_or_404(Wine, id=i)
            wines.append(wine)
            if not wine.shop.user == request.user:
                return HttpResponseForbidden()

        if request.method == 'POST':
            for wine in wines:
                wine.delete()
            return HttpResponseRedirect('/wineshops/edit/catalog')
        else:
            return render(request, 'wineshops/confirm_remove.html', {'wine_ids': wine_ids, 'wines': wines})

    except:
        return HttpResponseForbidden()


@login_required
def out_wines(request, wine_ids):
    return in_out_wines(request, wine_ids, False)


@login_required
def in_wines(request, wine_ids):
    return in_out_wines(request, wine_ids, True)


def in_out_wines(request, wine_ids, status):
    try:
        index = ast.literal_eval('[' + wine_ids + ']')
        wines = []
        for i in index:
            wine = get_object_or_404(Wine, id=i)
            wines.append(wine)
            if not wine.shop.user == request.user:
                return HttpResponseForbidden()

        if request.method == 'GET':
            for wine in wines:
                wine.in_stock = status
                wine.save()

        return HttpResponse('ok')

    except:
        return HttpResponseForbidden()


def search(request):
    query_what = request.GET.get('q')
    query_where = request.GET.get('o')
    try:
        lat = float(request.GET['lat'])
        lng = float(request.GET['lng'])
    except:
        return HttpResponseRedirect('/')

    do_search = (len(query_what) != 0 and query_what != 'Trouvez votre vin près de chez vous')

    wine_objects = Wine.objects
    if do_search:
        wine_objects = wine_objects.filter(get_query(query_what,
                                                     ['producer', 'country__name', 'region__name', 'area__name',
                                                      'color__name', 'varietal', 'classification', 'vintage',
                                                      'capacity__volume', ]))

    results = [(shop, haversine.haversine(lng, lat, shop.longitude, shop.latitude)) for shop in
               Shop.objects.exclude(filled=False, longitude__isnull=True, latitude__isnull=True).all()]
    results.sort(key=itemgetter(1))
    results = [{'shop': a[0],
                'dist': "%.1f" % a[1],
                'nb': wine_objects.filter(in_stock=True, shop_id=a[0].id).count(),
                'price': wine_objects.filter(in_stock=True, shop_id=a[0].id).aggregate(Min('price_min'),
                                                                                       Max('price_max')),
                } for a in results]

    if do_search:
        results = [a for a in results if a['nb'] != 0]
    results = results[:20]

    return render_to_response('wineshops/search_results.html',
                              {'query_what': query_what,
                               'query_where': query_where,
                               'results': results,
                               'lat': lat,
                               'lng': lng,
                               'what_criteria': do_search},
                              context_instance=RequestContext(request))


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def get_wine_shops(request):
    """
    A view that returns the wine shops
    """

    try:
        query_what = request.GET.get('q')
        lat = float(request.GET['lat'])
        lng = float(request.GET['lng'])
        already_loaded = int(request.GET['c'])
    except ValueError:
        logger.warning(ValueError)
        return HttpResponse(json.dumps([]), content_type='application/json')

    do_search = (len(query_what) != 0)

    wine_objects = Wine.objects
    if do_search:
        wine_objects = wine_objects.filter(get_query(query_what,
                                                     ['producer', 'country__name', 'region__name', 'area__name',
                                                      'color__name', 'varietal', 'classification', 'vintage',
                                                      'capacity__volume', ]))

    results = [(shop, haversine.haversine(lng, lat, shop.longitude, shop.latitude)) for shop in
               Shop.objects.exclude(filled=False, longitude__isnull=True, latitude__isnull=True).all()]
    results.sort(key=itemgetter(1))
    results = [{'name': a[0].name,
                'id': a[0].id,
                'address': a[0].address + ', ' + str(a[0].zip_code) + ' ' + a[0].city,
                'phone': a[0].phone,
                'mail': a[0].mail,
                'web': a[0].web,
                'desc': a[0].description,
                'lat': a[0].latitude,
                'lng': a[0].longitude,
                'dist': "%.1f" % a[1],
                'nb': wine_objects.filter(in_stock=True, shop_id=a[0].id).count(),
                'price': wine_objects.filter(in_stock=True, shop_id=a[0].id).aggregate(Min('price_min'),
                                                                                       Max('price_max')),
                } for a in results]

    if do_search:
        results = [a for a in results if a['nb'] != 0]

    nb_results = len(results)
    per_page = 10
    results = results[already_loaded: already_loaded + per_page]
    return Response([nb_results] + results)




@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def get_wines(request):
    """
    A view that returns the wine shops
    """

    try:
        query_what = request.GET.get('q')
        shop_id = int(request.GET.get('shop'))
        already_loaded = int(request.GET['c'])
    except ValueError:
        logger.warning(ValueError)
        return HttpResponse(json.dumps([]), content_type='application/json')

    do_search = (len(query_what) != 0)

    wine_objects = Wine.objects.filter(shop_id=shop_id).filter(in_stock=True)
    if do_search:
        wine_objects = wine_objects.filter(get_query(query_what,
                                                     ['producer', 'country__name', 'region__name', 'area__name',
                                                      'color__name', 'varietal', 'classification', 'vintage',
                                                      'capacity__volume', ]))

    wine_objects = wine_objects.order_by('country__name', 'region__name', 'area__name', 'producer')

    results = [{'producer': a.producer,
                'country': a.country.name if a.country else "",
                'region': a.region.name if a.region else "",
                'area': a.area.name if a.area else "",
                'classification': a.classification,
                'color': a.color.name if a.color else "",
                'varietal': a.varietal,
                'vintage': a.vintage,
                'capacity': a.capacity.volume if a.capacity else 0,
                'price_min': a.price_min,
                'price_max': a.price_max,
                } for a in wine_objects]

    nb_results = len(results)
    per_page = 10
    results = results[already_loaded: already_loaded + per_page]
    return Response([nb_results] + results)




@api_view(['GET'])
@renderer_classes((JPEGRenderer,))
def get_wineshop_image(request, shop_id):
    """
    A view that returns the shop image
    """
    shop = get_object_or_404(Shop, id=shop_id)

    if shop.image:
        image_data = shop.image.read()
        return Response(image_data)
    else:
        return Response(None, status=status.HTTP_404_NOT_FOUND)


def regions(request):
    country_id = None
    if request.method == 'GET':
        country_id = request.GET.get('country_id', -1)

    if country_id:
        generic_regions = set(Region.objects.filter(country_id=country_id, custom=False).all())
        user_regions_ids = set(Wine.objects.filter(shop__user=request.user, country_id=country_id).values_list('region',
                                                                                                               flat=True).distinct())
        user_regions = Region.objects.filter(pk__in=user_regions_ids)
        regions = list(generic_regions.union(user_regions))
        regions.sort(key=Country.__str__)
    else:
        regions = []

    return HttpResponse(json.dumps([{'name': r.name, '#': str(r.id)} for r in regions]))


def areas(request):
    region_id = None
    if request.method == 'GET':
        region_id = request.GET.get('region_id', -1)
    areas = []
    if region_id:
        generic_areas = set(Area.objects.filter(region_id=region_id, custom=False).all())
        user_areas_ids = set(
            Wine.objects.filter(shop__user=request.user, region_id=region_id).values_list('area', flat=True).distinct())
        user_areas = Area.objects.filter(pk__in=user_areas_ids)
        areas = list(generic_areas.union(user_areas))
        areas.sort(key=Country.__str__)

    return HttpResponse(json.dumps([{'name': r.name, '#': str(r.id)} for r in areas]))


def filtered_catalog(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id)

    if request.method == 'POST':
        return HttpResponseForbidden()

    query_what = request.GET.get('q')
    do_search = (len(query_what) != 0 and query_what != 'Trouvez votre vin près de chez vous')

    query = Wine.objects.filter(shop_id=shop.id)
    if do_search:
        query = query.filter(get_query(query_what, ['producer', 'country__name', 'region__name', 'area__name',
                                                    'color__name', 'varietal', 'classification', 'vintage',
                                                    'capacity__volume', ]))
    back = request.GET.get('back')

    if back == None:
        back_url = request.META.get('HTTP_REFERER', '/')
        back = urllib.parse.quote(back_url)
    else:
        back_url = back
        back = urllib.parse.quote(back_url)

    return display_wines(request,
                         'wineshops/show_catalog.html',
                         query,
                         {'query_what': query_what,
                          'shop_id': shop_id,
                          'shop': shop,
                          'what_criteria': do_search,
                          'back': back,
                          'back_url': back_url})



##
# Handle 404 Errors
# @param request WSGIRequest list with all HTTP Request
def error404(request):

    # 1. Load models for this view
    #from idgsupply.models import My404Method

    # 2. Generate Content for this view
    template = loader.get_template('404.htm')
    context = Context({
        'message': 'All: %s' % request,
        })

    # 3. Return Template for this view + Data
    return HttpResponse(content=template.render(context), content_type='text/html; charset=utf-8', status=404)