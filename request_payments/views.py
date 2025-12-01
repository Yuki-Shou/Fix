from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from .models import RequestPayment


def serialize_rp(rp):
    data = model_to_dict(rp, exclude=['created_at'])
    if rp.invoice:
        data['invoice_url'] = rp.invoice.url
    return data


@csrf_exempt
def rp_list(request):
    if request.method == 'GET':
        q = RequestPayment.objects.all().order_by('-id')
        return JsonResponse([serialize_rp(p) for p in q], safe=False)

    if request.method == 'POST':
        # handle multipart/form-data for invoice file
        no = request.POST.get('no','')
        date = request.POST.get('date')
        rp = RequestPayment.objects.create(
            no=no,
            date=date,
            payee=request.POST.get('payee',''),
            tin=request.POST.get('tin',''),
            action_required=request.POST.get('action_required',''),
            mode_of_payment=request.POST.get('mode_of_payment',''),
            payment_for=request.POST.get('payment_for',''),
            amount=request.POST.get('amount') or 0,
            remarks=request.POST.get('remarks',''),
            requested_by=request.POST.get('requested_by',''),
            checked_by=request.POST.get('checked_by',''),
            recommend_approval=request.POST.get('recommend_approval',''),
            approved_by=request.POST.get('approved_by',''),
        )
        if 'invoice' in request.FILES:
            rp.invoice = request.FILES['invoice']
            rp.save()
        return JsonResponse(serialize_rp(rp), status=201)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def rp_detail(request, pk):
    rp = get_object_or_404(RequestPayment, pk=pk)
    if request.method == 'GET':
        return JsonResponse(serialize_rp(rp))
    if request.method == 'DELETE':
        rp.delete()
        return JsonResponse({'deleted': True})
    return JsonResponse({'error': 'Method not allowed'}, status=405)
