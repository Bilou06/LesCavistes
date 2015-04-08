from django.shortcuts import render
from django.views import generic

from .models import Shop


class IndexView(generic.ListView):
    template_name = 'wineshops/index.html'
    context_object_name = 'shop_list'

    def get_queryset(self):
        return Shop.objects.all()

class DetailView(generic.DetailView):
    model = Shop
    template_name = 'wineshops/detail.html'


def edit(request):#TODO
    shops = []
    context = {'shop_list':shops,}
    return render(request, 'wineshops/index.html', context)


