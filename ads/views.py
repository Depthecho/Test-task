from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.core.checks import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import AdForm
from .models import Ad, ExchangeProposal
from . import services

@login_required
@login_required
def ad_create(request):
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return redirect('ad_list')
    else:
        form = AdForm()
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
    all_ads = services.filter_ads(request.GET)
    user_ads = all_ads.filter(user=request.user) if request.user.is_authenticated else Ad.objects.none()
    other_ads = all_ads.exclude(user=request.user) if request.user.is_authenticated else all_ads

    categories = Ad.objects.values_list('category', flat=True).distinct()
    conditions = Ad.CONDITION_CHOICES

    return render(request, 'ads/ad_list.html', {
        'user_ads': user_ads,
        'other_ads': other_ads,
        'categories': categories,
        'conditions': conditions
    })

@login_required
def create_exchange_proposal(request, ad_id):
    ad_sender = get_object_or_404(Ad, pk=ad_id)

    if request.method == 'POST':
        ad_receiver_id = request.POST.get('ad_receiver_id')
        comment = request.POST.get('comment')
        ad_receiver = get_object_or_404(Ad, pk=ad_receiver_id)

        exchange_proposal = ExchangeProposal.objects.create(
            ad_sender=ad_sender,
            ad_receiver=ad_receiver,
            comment=comment
        )

        return redirect('ad_list')

    ads = Ad.objects.exclude(id=ad_sender.id)
    return render(request, 'ads/exchange_proposal_form.html', {'ad_sender': ad_sender, 'ads': ads})


@login_required
def exchange_proposals_list(request):
    user_ads = request.user.ads.all()

    sent_proposals = ExchangeProposal.objects.filter(ad_sender__in=user_ads)

    received_proposals = ExchangeProposal.objects.filter(ad_receiver__in=user_ads)

    return render(request, 'ads/exchange_proposals_list.html', {
        'sent_proposals': sent_proposals,
        'received_proposals': received_proposals
    })


@login_required
def accept_exchange_proposal(request, proposal_id):
    proposal = get_object_or_404(ExchangeProposal, pk=proposal_id)

    if proposal.ad_receiver.user == request.user:
        proposal.status = 'accepted'
        proposal.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def reject_exchange_proposal(request, proposal_id):
    proposal = get_object_or_404(ExchangeProposal, pk=proposal_id)

    if proposal.ad_receiver.user == request.user:
        proposal.status = 'rejected'
        proposal.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))