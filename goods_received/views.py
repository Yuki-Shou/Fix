from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
import json
from .models import GoodsReceivedNote


def serialize_grn(g):
    return model_to_dict(g, exclude=['created_at'])


@csrf_exempt
def grn_list(request):
    if request.method == 'GET':
        q = GoodsReceivedNote.objects.all().order_by('-id')
        return JsonResponse([serialize_grn(p) for p in q], safe=False)
    if request.method == 'POST':
        try:
            payload = json.loads(request.body.decode('utf-8'))
        except Exception as e:
            return JsonResponse({'error': f'Invalid JSON: {str(e)}'}, status=400)
        
        g = GoodsReceivedNote.objects.create(
            no=payload.get('no',''),
            date=payload.get('date'),
            linked_po=payload.get('linked_po',''),
            received_by=payload.get('received_by','')
        )
        return JsonResponse(serialize_grn(g), status=201)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def grn_detail(request, pk):
    grn = get_object_or_404(GoodsReceivedNote, pk=pk)
    if request.method == 'GET':
        return JsonResponse(serialize_grn(grn))
    if request.method == 'DELETE':
        grn.delete()
        return JsonResponse({'deleted': True})
    return JsonResponse({'error': 'Method not allowed'}, status=405)
