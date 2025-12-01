import json
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from .models import PurchaseRequisition, PRItem


def serialize_pr(pr):
    data = model_to_dict(pr, exclude=['created_at'])
    data['items'] = [model_to_dict(it, exclude=[]) for it in pr.items.all()]
    return data


@csrf_exempt
def pr_list(request):
    if request.method == 'GET':
        q = PurchaseRequisition.objects.all().order_by('-id')
        return JsonResponse([serialize_pr(p) for p in q], safe=False)

    if request.method == 'POST':
        try:
            payload = json.loads(request.body.decode('utf-8'))
        except Exception as e:
            return JsonResponse({'error': f'Invalid JSON: {str(e)}'}, status=400)

        pr = PurchaseRequisition.objects.create(
            no=payload.get('no',''),
            date=payload.get('date'),
            requester=payload.get('requester',''),
            dept=payload.get('dept',''),
            date_needed=payload.get('date_needed') or None,
            remarks=payload.get('remarks',''),
            requested_by=payload.get('requested_by',''),
            checked_by=payload.get('checked_by',''),
            recommend_approval=payload.get('recommend_approval',''),
            approved_by=payload.get('approved_by',''),
        )
        for it in payload.get('items',[]):
            PRItem.objects.create(
                pr=pr,
                stk=it.get('stk',''),
                qty=it.get('qty') or 0,
                unit=it.get('unit',''),
                desc=it.get('desc',''),
                remark=it.get('remark',''),
            )
        return JsonResponse(serialize_pr(pr), status=201)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def pr_detail(request, pk):
    pr = get_object_or_404(PurchaseRequisition, pk=pk)
    if request.method == 'GET':
        return JsonResponse(serialize_pr(pr))
    if request.method == 'DELETE':
        pr.delete()
        return JsonResponse({'deleted': True})

    # Support full update (PUT) and partial update (PATCH) via JSON payload
    if request.method in ('PUT', 'PATCH'):
        try:
            payload = json.loads(request.body.decode('utf-8'))
        except Exception as e:
            return JsonResponse({'error': f'Invalid JSON: {str(e)}'}, status=400)

        # update scalar fields
        for field in ('no', 'date', 'requester', 'dept', 'date_needed', 'remarks', 'requested_by', 'checked_by', 'recommend_approval', 'approved_by'):
            if field in payload:
                setattr(pr, field, payload.get(field))

        pr.save()

        # replace items if provided
        if 'items' in payload:
            # remove existing items and recreate
            pr.items.all().delete()
            for it in payload.get('items', []):
                PRItem.objects.create(
                    pr=pr,
                    stk=it.get('stk',''),
                    qty=it.get('qty') or 0,
                    unit=it.get('unit',''),
                    desc=it.get('desc',''),
                    remark=it.get('remark',''),
                )

        return JsonResponse(serialize_pr(pr))

    return JsonResponse({'error': 'Method not allowed'}, status=405)
