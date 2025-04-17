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

def ad_detail(request, ad_id):
    ad = get_object_or_404(Ad, pk=ad_id)
    return render(request, 'ads/ad_detail.html', {'ad': ad})

@login_required
def create_exchange_proposal(request, ad_id):
    ad_receiver = get_object_or_404(Ad, pk=ad_id)

    if ad_receiver.user == request.user:
        return render(request, 'ads/forbidden.html')

    if request.method == 'POST':
        ad_sender_id = request.POST.get('ad_sender_id')
        comment = request.POST.get('comment')
        ad_sender = get_object_or_404(Ad, pk=ad_sender_id)

        if ad_sender.user != request.user:
            return render(request, 'ads/forbidden.html')

        ExchangeProposal.objects.create(
            ad_sender=ad_sender,
            ad_receiver=ad_receiver,
            comment=comment
        )

        return redirect('ad_list')

    user_ads = Ad.objects.filter(user=request.user)
    return render(request, 'ads/exchange_proposal_form.html', {
        'ad_receiver': ad_receiver,
        'ads': user_ads
    })

    user_ads = Ad.objects.filter(user=request.user).exclude(id=ad_sender.id)
    return render(request, 'ads/exchange_proposal_form.html', {
        'ad_sender': ad_sender,
        'ads': user_ads
    })


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

    success = services.accept_exchange_and_delete_ads(proposal, request.user)

    if not success:
        return render(request, 'ads/forbidden.html')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def reject_exchange_proposal(request, proposal_id):
    proposal = get_object_or_404(ExchangeProposal, pk=proposal_id)

    if proposal.ad_receiver.user == request.user:
        proposal.status = 'rejected'
        proposal.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))