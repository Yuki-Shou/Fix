from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from .models import RequestPayment
import traceback


def serialize_rp(rp):
    # Exclude the raw FileField from model_to_dict so JSON serialization
    # does not attempt to encode a FieldFile object (which is not JSON serializable).
    data = model_to_dict(rp, exclude=['created_at', 'invoice'])
    # If an invoice file exists, expose its URL (string) instead.
    try:
        if rp.invoice and hasattr(rp.invoice, 'url'):
            data['invoice_url'] = rp.invoice.url
    except Exception:
        # defensive: if accessing .url fails, do not break serialization
        data['invoice_url'] = None
    return data


@csrf_exempt
def rp_list(request):
    if request.method == 'GET':
        q = RequestPayment.objects.all().order_by('-id')
        return JsonResponse([serialize_rp(p) for p in q], safe=False)

    if request.method == 'POST':
        try:
            # Accept either multipart/form-data (with files) or application/json
            if request.content_type and request.content_type.startswith('application/json'):
                try:
                    import json as _json
                    payload = _json.loads(request.body.decode('utf-8'))
                except Exception as e:
                    return JsonResponse({'error': f'Invalid JSON: {str(e)}'}, status=400)

                no = payload.get('no','')
                date = payload.get('date')
                rp = RequestPayment.objects.create(
                    no=no,
                    date=date,
                    payee=payload.get('payee',''),
                    tin=payload.get('tin',''),
                    action_required=payload.get('action_required',''),
                    mode_of_payment=payload.get('mode_of_payment',''),
                    payment_for=payload.get('payment_for',''),
                    amount=payload.get('amount') or 0,
                    remarks=payload.get('remarks',''),
                    requested_by=payload.get('requested_by',''),
                    checked_by=payload.get('checked_by',''),
                    recommend_approval=payload.get('recommend_approval',''),
                    approved_by=payload.get('approved_by',''),
                )
                return JsonResponse(serialize_rp(rp), status=201)

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
        except Exception as e:
            tb = traceback.format_exc()
            return JsonResponse({'error': str(e), 'traceback': tb}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def rp_detail(request, pk):
    rp = get_object_or_404(RequestPayment, pk=pk)
    if request.method == 'GET':
        return JsonResponse(serialize_rp(rp))
    if request.method == 'DELETE':
        rp.delete()
        return JsonResponse({'deleted': True})
    # Support partial/full update via JSON payload (PATCH/PUT)
    if request.method in ('PUT', 'PATCH'):
        try:
            import json as _json
            payload = _json.loads(request.body.decode('utf-8'))
        except Exception as e:
            return JsonResponse({'error': f'Invalid JSON: {str(e)}'}, status=400)

        for field in ('no','date','payee','tin','action_required','mode_of_payment','payment_for','amount','remarks','requested_by','checked_by','recommend_approval','approved_by'):
            if field in payload:
                setattr(rp, field, payload.get(field))
        rp.save()
        return JsonResponse(serialize_rp(rp))

    return JsonResponse({'error': 'Method not allowed'}, status=405)
