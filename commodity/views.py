from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Products, Bid, RentalAgreement
from .serializers import UserSignupSerializer, ProductsSerializer, BidSerializer, AcceptBidSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication 


User = get_user_model()



class UserSignupView(APIView):
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "status": "success",
                "message": "User created successfully",
                "payload": {
                    "user_id": user.id
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "error",
            "message": "User could not be created",
            "payload": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class ProductsListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProductsSerializer(data=request.data)
        if serializer.is_valid():
            Products = serializer.save(lender=request.user)
            return Response({
                "status": "success",
                "message": "Products listed successfully",
                "payload": {
                    "Products_id": Products.id,
                    "quote_price_per_month": Products.quote_price_per_month,
                    "created_at": Products.created_at
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "error",
            "message": "Products could not be listed",
            "payload": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)




class PlaceBidView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BidSerializer(data=request.data)
        if serializer.is_valid():
            bid = serializer.save(renter=request.user)
            return Response({
                "status": "success",
                "message": "Bid placed successfully",
                "payload": {
                    "bid_id": bid.id,
                    "Products_id": bid.Products.id,
                    "bid_price_per_month": bid.bid_price_per_month,
                    "created_at": bid.created_at
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "error",
            "message": "Bid could not be placed",
            "payload": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)



class AcceptBidView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AcceptBidSerializer(data=request.data, context={'lender': request.user})
        if serializer.is_valid():
            rental_agreement = serializer.save()
            return Response({
                "status": "success",
                "message": "Bid accepted successfully",
                "payload": {
                    "rental_agreement_id": rental_agreement.id,
                    "Products_id": rental_agreement.Products.id,
                    "renter_id": rental_agreement.renter.id,
                    "rental_start_date": rental_agreement.rental_start_date,
                    "rental_end_date": rental_agreement.rental_end_date
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "error",
            "message": "Bid could not be accepted",
            "payload": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)