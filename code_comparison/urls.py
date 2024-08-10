"""
URL configuration for CodeCheck project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from .views import CodeComparisonView, code_comparison_history, code_comparison_history_new

urlpatterns = [
    path('api/group/', CodeComparisonView.as_view(), name='group_comparison'),
    path('api/comparison/', CodeComparisonView.as_view(), name='code_comparison'),
    path('api/history/', code_comparison_history, name='code_comparison_history'),
    path('api/history_new/', code_comparison_history_new, name='code_comparison_history_new'),
    path('api/get_groups/', views.get_groups, name='get_groups'),
    path('submissions/<int:submission_id>', views.submission_details, name='submission_details'),
    path('api/mark_plagiarism/', views.mark_plagiarism, name='mark_plagiarism'),
]
