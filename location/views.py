from statistics import median

import requests
from django.conf import settings

# Create your views here.
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from location.serializers import LocationSerializer


class LocationView(generics.RetrieveAPIView):
    queryset = None
    serializer_class = LocationSerializer
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        """
        :param request: days -> str : Default = 10
        :param args: None
        :param kwargs: city -> str : Required
        :return: {"maximum":xxx,"minimum":yyy,"average":zzz,"median":aaa}
        """
        serializer = self.serializer_class(
            data=request.GET, context=self.get_serializer_context
        )
        serializer.is_valid(raise_exception=True)
        URL = f"{settings.WEATHER_API_BASE_URL}/v1/forecast.json"
        params = {
            "key": settings.WEATHER_API_KEY,
            "q": kwargs.get("city"),
            "days": serializer.data.get("days"),
        }
        result = requests.get(url=URL, params=params)
        if result.status_code == 200:
            data = result.json()
            forecastday = data.get("forecast").get("forecastday")
            max_temp_list = list()
            min_temp_list = list()
            avg_temp_list = list()
            for i, values in enumerate(forecastday):
                max_temp_list.append(values.get("day").get("maxtemp_c"))
                min_temp_list.append(values.get("day").get("mintemp_c"))
                avg_temp_list.append(values.get("day").get("avgtemp_c"))
            processed_data = {
                "maximum": max(max_temp_list),
                "minimum": min(min_temp_list),
                "average": round(sum(avg_temp_list) / len(avg_temp_list), 2),
                "median": round(median(avg_temp_list), 2),
            }
            return Response(processed_data, status=status.HTTP_200_OK)
        else:
            return Response(result.json(), status=status.HTTP_400_BAD_REQUEST)
