from traceback import print_tb
from zlib import DEF_BUF_SIZE
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from api_basic import serializers
from api_basic.models import Article
from api_basic.models import zulassungen
from api_basic.serializers import ArticleSerializer
from api_basic.serializers import ZulassungenSerializer
from api_basic.serializers import MarkenSerializer
from django.db.models import Sum
import pandas as pd

@csrf_exempt
def marken_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        marken = zulassungen.objects.values('marke').distinct()
        serializer = MarkenSerializer(marken, many=True)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def zulassungen_list(request,marken):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        #objzulassungen = zulassungen.objects.all()
        split_marken = marken.split(';')
        queryList = []
        count = 0
        append_data = []
        for marke in split_marken:
            objzulassungen=zulassungen.objects.filter(marke=marke)
            queryList = list(objzulassungen.values())
            df_temp = pd.DataFrame(queryList)
            append_data.append(df_temp)
        appended_data = pd.concat(append_data)
        data_sorted=appended_data.sort_values(by=['monat'])
        uniqueValues = data_sorted['monat'].unique()
        g = appended_data.groupby(['jahr','monat', 'marke'])['anzahl'].sum().reset_index()
        temp_dict={}
        format_list=[]
        for unique in uniqueValues:
            temp_dict={}
            rslt_df = g[g['monat'] == unique]
            datadict = rslt_df.to_dict('records')
            zeitpunkt = str(datadict[0]["jahr"]) + "_" + str(datadict[0]["monat"])
            temp_dict["jahr"]= zeitpunkt
            for item in datadict:
                temp_dict[item["marke"]]= item["anzahl"]
            #    temp_dict[item["marke"]] = item["anzahl"]
            #    print(temp_dict)
            format_list.append(temp_dict)
        #serializer = ZulassungenSerializer(objzulassungen, many=True)
        serializer = ZulassungenSerializer(objzulassungen, many=True)
        return JsonResponse(format_list, safe=False)
    elif request.method == 'POST':
        data = request.POST
        print(data)
        serializer = ZulassungenSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)

@csrf_exempt
def aritcle_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        
        data = JSONParser().parse(request)
        serializer = ArticleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def article_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        article = ArticleSerializer(article)
        return JsonResponse(article.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ArticleSerializer(article, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        article.delete()
        return HttpResponse(status=204)


