from django.urls import path
from .views import (
    FormulaireListView,
    FormulaireCreateView,
    FormulaireUpdateView,
    FormulaireDeleteView,
    RapportListView,
    RapportCreateView,
    RapportUpdateView,
    RapportDeleteView
)

urlpatterns = [
    path('formulaires/', FormulaireListView.as_view(), name='formulaire-list'),
    path('formulaires-nouveau/', FormulaireCreateView.as_view(), name='formulaire-create'),
    path('formulaires/<int:pk>/modifier/', FormulaireUpdateView.as_view(), name='formulaire-update'),
    path('formulaires/<int:pk>/supprimer/', FormulaireDeleteView.as_view(), name='formulaire-delete'),
    
    path('rapports/', RapportListView.as_view(), name='rapport-list'),
    path('rapports-nouveau/', RapportCreateView.as_view(), name='rapport-create'),
    path('rapports/<int:pk>/modifier/', RapportUpdateView.as_view(), name='rapport-update'),
    path('rapports/<int:pk>/supprimer/', RapportDeleteView.as_view(), name='rapport-delete'),
]
