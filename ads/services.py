from django.shortcuts import get_object_or_404
from .models import Ad

def create_ad(form, user):
    ad = form.save(commit=False)
    ad.user = user
    ad.save()
    return ad

def get_user_ad_or_404(ad_id, user):
    ad = get_object_or_404(Ad, pk=ad_id)
    if ad.user != user:
        return None
    return ad

def delete_ad(ad):
    ad.delete()

def get_all_ads():
    return Ad.objects.all().order_by('-created_at')

def filter_ads(query_params):
    ads = Ad.objects.all()

    search = query_params.get('search')
    if search:
        ads = ads.filter(title__icontains=search) | ads.filter(description__icontains=search)

    category = query_params.get('category')
    if category:
        ads = ads.filter(category=category)

    condition = query_params.get('condition')
    if condition:
        ads = ads.filter(condition=condition)

    return ads.order_by('-created_at')
