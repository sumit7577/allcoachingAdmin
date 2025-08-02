from django.shortcuts import render
from rest_framework.generics import ListAPIView
from user.auth import CustomAuthentication,IsAuthAndTeacher
from analytics.serialaizer import *
from app.models import Order
from django.db.models.functions import TruncMonth
from django.db.models import Count
from collections import defaultdict
from rest_framework.response import Response
from django.utils.timezone import now
import calendar


# Create your views here.
class InstituteSales(ListAPIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthAndTeacher]
    serializer_class = SalesSerializer
    
    def list(self, request, *args, **kwargs):
        institute = request.user.institute
        current_date = now()

        # Get year from query param or default to current year
        year = request.query_params.get("year")
        try:
            year = int(year)
        except (TypeError, ValueError):
            year = current_date.year

        max_month = current_date.month if year == current_date.year else 12
        months = [calendar.month_abbr[i] for i in range(1, max_month + 1)]  
        month_map = {i + 1: i for i in range(len(months))}  # Jan -> 0, ..., Aug -> 7

        orders = (
            Order.objects.filter(
                course__institute=institute,
                status="COMPLETED",
                created_at__year=year,
                created_at__month__lte=max_month
            )
            .annotate(month=TruncMonth("created_at"))
            .values("course__name", "created_at__month")
            .annotate(count=Count("id"))
        )

        course_sales = defaultdict(lambda: [0] * max_month)  # 8 months from Jan to Aug

        for item in orders:
            course_title = item["course__name"]
            month_num = item["created_at__month"]
            if month_num in month_map:
                idx = month_map[month_num]
                course_sales[course_title][idx] = item["count"]

        series = [{"name": title, "data": data} for title, data in course_sales.items()]

        return Response({
            "categories": months,
            "series": series
        })


class InstituteTransactions(ListAPIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthAndTeacher]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.select_related("course","user").filter(course__institute__user=self.request.user).order_by("-id")