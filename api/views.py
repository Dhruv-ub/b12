import csv
import io
import statistics
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import UserSerializer, RegisterSerializer, UploadHistorySerializer, MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import UploadHistory


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class HistoryListView(generics.ListAPIView):
    serializer_class = UploadHistorySerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        return UploadHistory.objects.filter(user=self.request.user)

class HistoryDetailView(generics.RetrieveAPIView):
    serializer_class = UploadHistorySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return UploadHistory.objects.filter(user=self.request.user)

class CSVUploadView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        if 'file' not in request.FILES:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        file_obj = request.FILES['file']
        
        try:
            decoded_file = file_obj.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)
            
            data = []
            pressures = []
            temperatures = []
            flowrates = []
            
            for row in reader:
                data.append(row)
                if 'Pressure' in row:
                    pressures.append(float(row['Pressure']))
                if 'Temperature' in row:
                    temperatures.append(float(row['Temperature']))
                # Check for Flowrate first, then fallback to Concentration
                if 'Flowrate' in row:
                    flowrates.append(float(row['Flowrate']))
                elif 'Concentration' in row:
                    flowrates.append(float(row['Concentration']))
            
            if not data:
                return Response({'error': 'Empty CSV'}, status=status.HTTP_400_BAD_REQUEST)

            avg_pressure = statistics.mean(pressures) if pressures else 0
            avg_temperature = statistics.mean(temperatures) if temperatures else 0
            avg_flowrate = statistics.mean(flowrates) if flowrates else 0
            
            # Calculate type distribution
            type_counts = {}
            for row in data:
                if 'Type' in row:
                    equip_type = row['Type']
                    type_counts[equip_type] = type_counts.get(equip_type, 0) + 1

            # Create history entry
            history = UploadHistory.objects.create(
                user=request.user,
                total_count=len(data),
                avg_flowrate=avg_flowrate,
                avg_pressure=avg_pressure,
                avg_temperature=avg_temperature,
                type_distribution=type_counts,
                raw_data=data
            )
            
            serializer = UploadHistorySerializer(history)
            
            return Response({
                'message': 'File uploaded successfully',
                'raw_data': data,
                'summary': serializer.data,
                'history_id': history.id
            })

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
