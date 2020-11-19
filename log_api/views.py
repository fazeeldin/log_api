from log_api.serializers import LoggerSerializer
from log_api.models import Logger
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import datetime
from django.db.models import Count
import re
from dateutil.relativedelta import relativedelta
# Create your views here.

class LoggerAPIView(APIView):
   
    def get(self, request):
        logs = Logger.objects.all()
        serializer = LoggerSerializer(logs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LoggerSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class LoggerDateDetails(APIView):
    
    def get_object(self, date):
        try:
            return Logger.objects.filter(date=date)
        except Logger.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def get(self, request, date):
        date_field = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
        logs = self.get_object(date_field)
        hourly_freq = Logger.objects.filter(date__lte=date_field).extra({'date-hour': 'strftime("%%d-%%H", date)'
                                                                         }
                                                                        ).order_by().values('date-hour').annotate(count=Count('info')
                                                                        )
        #serializer = LoggerSerializer(logs, many=True)
        return Response({"No of logs on {} time".format(date_field): len(logs), "Hour-wise frequency" : {hourly_freq}})
    
    
    
class LoggerDateRangeDetails(APIView):
    
    def get_object(self, start_date, end_date):
        try:
            return Logger.objects.filter(date__range = (start_date, end_date))
        except Logger.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def fetch_delta_date(self, date_range):
        if "month" in date_range.casefold():
            month, = map(int, re.findall(r'[0-9]+', date_range))
            day, year = 0, 0
        elif "day" in date_range.casefold():
            day, = map(int, re.findall(r'[0-9]+', date_range))
            month, year = 0, 0
        elif "year" in date_range.casefold():
            year, = map(int, re.findall(r'[0-9]+', date_range))
            day, month = 0, 0
        return month, day, year
    
    def get(self, request, date, date_range):
        month, day, year = self.fetch_delta_date(date_range)
        
        start_date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
        end_date = start_date + relativedelta(months=month, years=year, days=day)
        
        logs = self.get_object(start_date, end_date)
        
        hourly_freq = Logger.objects.filter(date__gte=start_date,
                                            date__lte=end_date).extra({'date-hour': 'strftime("%%d-%%H", date)'
                                                                         }
                                                                        ).order_by().values('date-hour').annotate(count=Count('info')
                                                                        )
        
        return Response({"No of logs from {} time".format(start_date): len(logs), "Hour Wise Frequency" : {hourly_freq}})
        
        