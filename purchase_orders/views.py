import json
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from .models import PurchaseOrder, POItem


def serialize_po(po):
    data = model_to_dict(po, exclude=['created_at'])
    data['items'] = [model_to_dict(it, exclude=[]) for it in po.items.all()]
    return data


@csrf_exempt
def po_list(request):
    if request.method == 'GET':
        q = PurchaseOrder.objects.all().order_by('-id')
        return JsonResponse([serialize_po(p) for p in q], safe=False)

    if request.method == 'POST':
        try:
            payload = json.loads(request.body.decode('utf-8'))
        except Exception as e:
            return JsonResponse({'error': f'Invalid JSON: {str(e)}'}, status=400)

        po = PurchaseOrder.objects.create(
            no=payload.get('no',''),
            date=payload.get('date'),
            dept=payload.get('dept',''),
            supplier=payload.get('supplier',''),
            tin=payload.get('tin',''),
            address=payload.get('address',''),
            contact_person=payload.get('contact_person',''),
            contact_number=payload.get('contact_number',''),
            total=payload.get('total') or 0,
            prepared_by=payload.get('prepared_by',''),
            checked_by=payload.get('checked_by',''),
            approved_by=payload.get('approved_by',''),
        )
        for it in payload.get('items',[]):
            POItem.objects.create(
                po=po,
                qty=it.get('qty') or 0,
                unit=it.get('unit',''),
                description=it.get('description',''),
                unit_cost=it.get('unit_cost') or 0,
                total=it.get('total') or 0,
            )
        return JsonResponse(serialize_po(po), status=201)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def po_detail(request, pk):
    po = get_object_or_404(PurchaseOrder, pk=pk)
    if request.method == 'GET':
        return JsonResponse(serialize_po(po))
    if request.method == 'DELETE':
        po.delete()
        return JsonResponse({'deleted': True})
    return JsonResponse({'error': 'Method not allowed'}, status=405)
