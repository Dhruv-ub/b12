from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .views import (
    MyTokenObtainPairView,
    RegisterView, 
    UserProfileView, 
    CSVUploadView, 
    HistoryListView,
    HistoryDetailView
)

urlpatterns = [
    # Auth routes
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # App routes
    path('upload/', CSVUploadView.as_view(), name='csv-upload'),
    path('history/', HistoryListView.as_view(), name='history-list'),
    path('history/<int:pk>/', HistoryDetailView.as_view(), name='history-detail'),
]
