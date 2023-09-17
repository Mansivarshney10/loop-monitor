from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from .models import Store, StoreStatus, BusinessHours
from loop_monitor.serializers import StoreSerializer, BusinessHoursSerializer, StoreStatusSerializer
import csv
from io import StringIO

@api_view(['GET'])
def home(request):
    return render(request, 'store_monitor/index.html')

@api_view(['POST'])
def trigger_report(request):
    # Logic to compute the report (simplified for the example)
    report_id = "12345"  # Normally, you'd have a more complex system for IDs
    return JsonResponse({'report_id': report_id})

@api_view(['GET'])
def get_report(request, report_id):
    # Logic to fetch the report data based on report_id
    # Fetching all data just for the sake of the example
    stores = Store.objects.all()
    data = StoreSerializer(stores, many=True).data

    csv_data = StringIO()
    writer = csv.writer(csv_data)
    writer.writerow(['store_id', 'timezone_str'])
    for item in data:
        writer.writerow([item['store_id'], item['timezone_str']])

    response = HttpResponse(csv_data.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="report_{report_id}.csv"'
    return response
