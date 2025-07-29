from django.shortcuts import render
from user.auth import CustomAuthentication,IsAuthAndTeacher
from rest_framework.generics import *
from institute.serializer import *
from app.models import Institute,Course,Category
from rest_framework.response import Response
from django.db.models import Count 
from rest_framework.pagination import PageNumberPagination
from app.Razorpay import RazorPay
from rest_framework.views import APIView
from rest_framework import status

# Create your views here.
class InstituteViews(RetrieveUpdateAPIView):
    serializer_class = InstituteSerialzier
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthAndTeacher]
    
    def get_object(self):
        if self.get_queryset() == None:
            return self.request.user.institute
        return self.get_queryset()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = InstituteReadSerializer(instance)
        return Response(serializer.data)

    def get_queryset(self):
        return Institute.objects.select_related("user", "category")\
                .annotate(follower_count=Count("users"))\
                .filter(user=self.request.user).first()
    

class InstituteCategoryViews(ListCreateAPIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthAndTeacher]
    serializer_class = CategorySerializer
    pagination_class = None

    def get_queryset(self):
        return Category.objects.all().order_by("name")
    

class InstituteFreeContentViews(ListAPIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthAndTeacher]
    serializer_class = CourseReadSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Course.objects.select_related("category").prefetch_related("banners").annotate(enrolled_count=Count("users")).filter(institute__user=self.request.user,price=0).order_by("-created_at")
    

class InstituteLinkAccount(APIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthAndTeacher]

    def post(self, request, *args, **kwargs):
        institute = get_object_or_404(Institute, user=request.user)

        payload = {
            "email": institute.user.email,
            "phone": institute.user.phone,
            "type": "route",
            "legal_business_name": institute.name,
            "business_type": "educational_institutes",
            "contact_name": institute.director_name,
            "profile": {
                "category": "education",
                "subcategory": "elearning",
                "addresses": {
                    "registered": {
                        "street1": "16 havelia",
                        "street2":"jhaunsi",
                        "city": "Prayagraj",
                        "state": "Uttar Pradesh",
                        "postal_code": "211019",
                        "country": "IN"
                    }
                }
            },
        }

        razorpay = RazorPay("https://api.razorpay.com/v2/accounts", payload=payload)
        response = razorpay.makeRequest()
        if(response.get("status")):
            institute.account_link = response.get("data")
            institute.save()
            return Response({"success": True, "data": response.get("data")}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": False, "message": response.get("error")}, status=status.HTTP_400_BAD_REQUEST)
        

class InstituteVerifyAccount(APIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthAndTeacher]

    def post(self, request, *args, **kwargs):
        institute = get_object_or_404(Institute, user=request.user)

        payload = {
            "product_name":"route",
            "tnc_accepted":True,
        }

        razorpay = RazorPay(f"https://api.razorpay.com/v2/accounts/{institute.account_link.get("id")}/products/", payload=payload)
        response = razorpay.makeRequest()
        if(response.get("status")):
            institute.account_detail = response.get("data")
            institute.save()
            return Response({"success": True, "data": response.get("data")}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": False, "message": response.get("error")}, status=status.HTTP_400_BAD_REQUEST)
        

class InstituteAddBankAccount(APIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthAndTeacher]

    def post(self, request, *args, **kwargs):
        institute = get_object_or_404(Institute, user=request.user)
        serializer = BankAccountSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data

        payload = {
            "tnc_accepted": True,
            "settlements":{
                "account_number": data["account_number"],
                "ifsc_code": data["ifsc_code"],
                "beneficiary_name": data["beneficiary_name"],
            },
        }

        razorpay = RazorPay(f"https://api.razorpay.com/v2/accounts/{institute.account_link.get("id")}/products/{institute.account_detail.get("id")}", payload=payload)
        response = razorpay.makeRequest(method="patch")
        if(response.get("status")):
            institute.account_detail = response.get("data")
            institute.save()
            return Response({"success": True, "data": response.get("data")}, status=status.HTTP_201_CREATED)
        else:
            print(response)
            return Response({"success": False, "message": response.get("error")}, status=status.HTTP_400_BAD_REQUEST)
