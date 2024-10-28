from django.urls import path
from .views import FormulaireListView, FormulaireCreateView, RapportListView, RapportCreateView

urlpatterns = [
    path('formulaires/', FormulaireListView.as_view(), name='formulaire-list'),
    path('formulaires-nouveau/', FormulaireCreateView.as_view(), name='formulaire-create'),
    path('rapports/', RapportListView.as_view(), name='rapport-list'),
    path('rapports/nouveau/', RapportCreateView.as_view(), name='rapport-create'),
]
