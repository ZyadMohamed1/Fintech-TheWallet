from django.db.models import manager
from django.http import response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PaymentSerializer
from .models import Payment
from api import serializers
import hashlib
import requests
import json


@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint' : '/django_project/',
            'method' : 'GET',
            'body' : None,
            'description' : 'Return an array'
        },
        {
            'Endpoint' : '/django_project/id',
            'method' : 'GET',
            'body' : None,
            'description' : 'Return an object'
        },
        {
            'Endpoint' : '/django_project/create/',
            'method' : 'POST',
            'body' : {
                    "merchantCode": "1tSa6uxz2nTwlaAmt38enA==",
                    "customerName": "example",
                    "customerMobile": "01234567891",
                    "customerEmail": "example@gmail.com",
                    "customerProfileId": "777777",
                    "merchantRefNum": "2312465464",
                    "amount": "580.55",
                    "paymentExpiry" : "1631138400000",
                    "currencyCode": "EGP",
                    "language" : "en-gb",
                    "chargeItems": [
                        {
                        "itemId": "897fa8e81be26df25db592e81c31c",
                        "description": "Item Descriptoin",
                        "price": "580.55",
                        "quantity": "1"
                        }
                    ],
                    "signature": "2ca4c078ab0d4c50ba90e31b3b0339d4d4ae5b32f97092dd9e9c07888c7eef36",
                    "paymentMethod": "PAYATFAWRY",
                    "description": "Example Description"
                },
            'description' : 'Create a payment'
        },
        {
            'Endpoint' : '/django_project/id/update/',
            'method' : 'PUT',
            'body' : {'body' : ""},
            'description' : 'Update data'
        },
        {
            'Endpoint' : '/django_project/id/delete/',
            'method' : 'DELETE',
            'body' : None,
            'description' : 'DELETE'
        },
    ]
    return Response(routes)



# FawryPay Pay at Fawry API Endpoint
URL = "https://atfawry.fawrystaging.com/ECommerceWeb/Fawry/payments/charge"


# Payment Data
merchantCode    = '1tSa6uxz2nTwlaAmt38enA=='
merchantRefNum  = '99900642041'
merchant_cust_prof_id  = '458626698'
payment_method = 'PAYATFAWRY'
amount = '580.55'
merchant_sec_key =  '259af31fc2f74453b3a55739b21ae9ef'  #For the sake of demonstration
signature = hashlib.sha256(str(merchantCode + merchantRefNum + merchant_cust_prof_id + payment_method + amount + merchant_sec_key).encode('utf-8')).hexdigest()



# defining a params dict for the parameters to be sent to the API
PaymentData = {
    'merchantCode' : merchantCode,
    'merchantRefNum' : merchantRefNum,
    'customerName' : 'Ahmed Ali',
    'customerMobile' : '01234567891',
    'customerEmail' : 'example@gmail.com',
    'customerProfileId' : '777777',
    'amount' : '580.55',
    'paymentExpiry' : '1631138400000',
    'currencyCode' : 'EGP',
    'language' : 'en-gb',
    'chargeItems' : {
                          'itemId' : '897fa8e81be26df25db592e81c31c',
                          'description' : 'Item Description',
                          'price' : '580.55',
                          'quantity' : '1'
                      },
    'signature' : signature,
    'payment_method' : payment_method,
    'description': 'example description'
}



# sending post request and saving the response as response object
status_request = requests.post(url = URL, params = json.dumps(PaymentData))

# extracting data in json format
status_response = status_request.json()




@api_view(['GET'])
def getPayments(request):
    payments = Payment.objects.all()
    serializer = PaymentSerializer(payments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getPayment(request, pk):
    payment = Payment.objects.get(id=pk)
    serializer = PaymentSerializer(payment, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def createPayment(request):
    data = request.data

    payment = Payment.objects.create(
        body = data['body']
    )
    serializer = PaymentSerializer(payment, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
def updatePayment(request, pk):
    data = request.data

    payment = Payment.objects.get(id=pk)

    
    serializer = PaymentSerializer(payment, data=request.data)
    if serializer.is_valid():
        serializer.save()
    

    return Response(serializer.data)

@api_view(['DELETE'])
def deletePayment(request, pk):

    payment = Payment.objects.get(id=pk)
    payment.delete()

    return Response('Payement is deleted')
