# views.py
from rest_framework import viewsets
from core.permissions import *
from .models import *
from .serializers import *


class ThirdPartyContractorViewSet(viewsets.ModelViewSet):
    queryset = ThirdPartyContractor.objects.all()
    serializer_class = ThirdPartyContractorSerializer
    #permission_classes = [IsSystemAdmin]
    #allowed_methods = ['get', 'post', 'delete']


class BillingViewSet(viewsets.ModelViewSet):
    queryset = Billing.objects.all()
    serializer_class = BillingSerializer