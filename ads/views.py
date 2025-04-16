from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AdForm
from . import services

@login_required
def ad_create(request):
    form = AdForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        services.create_ad(form, request.user)
        return redirect('ad_list')
    return render(request, 'ads/ad_form.html', {'form': form})


@login_required
def ad_edit(request, ad_id):
    ad = services.get_user_ad_or_404(ad_id, request.user)
    if ad is None:
        return render(request, 'ads/forbidden.html')

    form = AdForm(request.POST or None, instance=ad)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('ad_list')

    return render(request, 'ads/ad_form.html', {'form': form})


@login_required
def ad_delete(request, ad_id):
    ad = services.get_user_ad_or_404(ad_id, request.user)
    if ad:
        services.delete_ad(ad)
    return redirect('ad_list')


def ad_list(request):
    ads = services.filter_ads(request.GET)
    return render(request, 'ads/ad_list.html', {'ads': ads})

