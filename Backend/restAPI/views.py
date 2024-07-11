from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from restAPI.models import Stocks
from restAPI.serializers import StocksSerializer

@csrf_exempt
def stocks_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        stocks = Stocks.objects.all()
        serializer = StocksSerializer(stocks, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = StocksSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)