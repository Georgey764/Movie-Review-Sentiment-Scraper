from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from restAPI.models import Stocks
from restAPI.serializers import StocksSerializer
from WebScraping.webscrape import ScrapeReviews

@csrf_exempt
def stocks_list(request):
    """
    endpoint for stocks
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

@csrf_exempt
def get_sentiment(request):
    """
    endpoint to get total number of reviews scraped for the movie
    """
    if request.method == 'GET':
        query = request.GET.get("q", None)
        mode = request.GET.get('mode', 'all')
        review_num = request.GET.get('num', None)

        if not query:
            return JsonResponse({"error_message": "Query parameter not present"}, status=400)
        if mode.lower() not in {'all', 'single'}:
            return JsonResponse({"error_message": "Mode should be either 'all' or 'single'"}, status=400)
        
        scraper = ScrapeReviews(query)

        if mode.lower() == "single":
            if review_num == None:
                return JsonResponse({"error_message": "parameter num is required in single mode"}, status=400)
            sentiments = scraper.get_review_sentiment(review_num)
            return JsonResponse(sentiments, status=200, safe=False)
        else:
            sentiments = scraper.get_total_sentiment()
            return JsonResponse(sentiments, status=200, safe=False)




