from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.renderers import JSONRenderer
from rest_framework.exceptions import APIException
from oauth2_provider.contrib.rest_framework import (
    TokenHasReadWriteScope, OAuth2Authentication
)
from django_pandas.io import read_frame
from basic.tracker import get_tracker_data
from my_app.ifrs16 import calculate
from my_app.models import Contract, Cost
from my_app.serializers import CostSerializer


class TrackerAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, _request):
        data = get_tracker_data()
        return Response(data)


class LiabilityAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        query_params = request.query_params
        print(query_params)
        try:
            record_id = query_params['id']
            contract = Contract.objects.get(id=record_id)
            payments = contract.contractpayment_set.values_list(
                'amount', flat=True
            )
            print(payments)
            dates = contract.contractpayment_set.values_list('date', flat=True)
            print(dates)
            actuals = contract.contractpayment_set.values_list(
                'actual_expected', flat=True
            )
            print(actuals)
            data = calculate(
                payments=list(payments), dates=list(dates),
                actuals=list(actuals), as_records=False
            )
            npv = contract.npv
            liability = data['Liability']
            liability.insert(0, npv)
            print(liability)
            datasets = [
                {'label': 'Liability (IFRS16)', 'series': liability}
            ]
            labels = ['Period '+str(i) for i in range(len(liability))]
            data = {'labels': labels, 'datasets': datasets}
            return Response(data)
        except Exception as exc:
            print(exc)
            raise APIException('Something went wrong') from exc


class ExampleAPIView(APIView):
    authentication_classes = [OAuth2Authentication]
    authentication_classes = []
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    permission_classes = []
    renderer_classes = [JSONRenderer]

    def get(self):
        def is_blank(value):
            if value is None or value == "":
                return True
            else:
                return False
        kwargs = {k: v for k, v in self.request.query_params.items()
                  if not is_blank(v)}
        print('All kwargs: ' + str(kwargs))

        filter_list = ['building__region', 'cost_type', 'start']
        filter_kwargs = {k: v for k, v in kwargs.items() if k in filter_list}
        print('Filter kwargs: ' + str(filter_kwargs))

        calculate_list = ['groupby']
        calculate_kwargs = {k: v for k,
                            v in kwargs.items() if k in calculate_list}
        print('Calculate kwargs: ' + str(calculate_kwargs))

        if filter_kwargs is not None:
            queryset = Cost.objects.filter(**filter_kwargs)
        else:
            queryset = Cost.objects.all()

        # if not is_blank(self.request.query_params.get('groupby')):
        #     groupby_kwarg = self.request.query_params.get('groupby')
        # else:
        #     groupby_kwarg = False

        print('Calculating...')
        dummy = True
        if dummy:
            data = calculate(**calculate_kwargs)
        else:
            df = read_frame(queryset)
            print(df)
            serializer = CostSerializer(queryset, many=True)
            data = serializer.data

        return Response(data)
