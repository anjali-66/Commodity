from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Products, Bid, RentalAgreement

User = get_user_model()

# User Signup Serializer
class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'user_type']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            user_type=validated_data['user_type']
        )
        return user

# Product Serializer
class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['item_name', 'item_description', 'quote_price_per_month', 'item_category']

# Bid Serializer
class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ['Products', 'bid_price_per_month', 'bid_duration']

    def validate_bid_price_per_month(self, value):
        Products = self.initial_data.get('Products')
        Products = Products.objects.get(id=Products)
        if value < Products.quote_price_per_month:
            raise serializers.ValidationError("Bid price cannot be less than the quoted price.")
        return value

    def validate(self, data):
        if data['Products'].is_rented:
            raise serializers.ValidationError("This Products is already rented out.")
        return data

# Accept Bid Serializer
class AcceptBidSerializer(serializers.ModelSerializer):
    bid_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = RentalAgreement
        fields = ['bid_id', 'rental_start_date', 'rental_end_date']

    def create(self, validated_data):
        bid = Bid.objects.get(id=validated_data['bid_id'])
        Products = bid.Products

        if Products.lender != self.context['lender']:
            raise serializers.ValidationError("You are not the owner of this Products.")

        Products.is_rented = True
        Products.save()

        rental_agreement = RentalAgreement.objects.create(
            Products=Products,
            renter=bid.renter,
            rental_start_date=validated_data['rental_start_date'],
            rental_end_date=validated_data['rental_end_date'],
        )

        return rental_agreement





