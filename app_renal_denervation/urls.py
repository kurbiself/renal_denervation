from django.urls import path, include
from . import views
from .views import (
    PatientsViewSet,
    PatientDeseaseViewSet,
    TypeCheckPointViewSet,
    CheckPointViewSet,
    SurgicalOperationViewSet,
    AblationSiteViewSet,
    TreatmentDrugViewSet,
    MetricViewSet,
    VariantQualitativeViewSet,
    MetricsTemplatesViewSet,
    ResearchTemplateViewSet,
    ResearchViewSet,
    MetricValueViewSet,
    HospitalViewSet,
    DiseaseViewSet,
    UnitViewSet,
    PharmacologicalGroupViewSet,
    ActiveIngredientViewSet,
    MedicineViewSet,
    CatheterTypeViewSet
)
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(prefix="patient", viewset=PatientsViewSet, basename="patient")
router.register(
    prefix="check-points", viewset=CheckPointViewSet, basename="checkpoints"
)
router.register(
    prefix="surgical-operations", viewset=SurgicalOperationViewSet, basename="surgicaloperations"
)
router.register(
    prefix="treatments-drug", viewset=TreatmentDrugViewSet, basename="treatmentsdrug"
)
router.register(
    prefix="metrics", viewset=MetricViewSet, basename="metrics"
)
router.register(
    prefix="variants-qualitative", viewset=VariantQualitativeViewSet, basename="variantsqualitative"
)
router.register(
    prefix="metrics-templates", viewset=MetricsTemplatesViewSet, basename="metricstemplates"
)
router.register(
    prefix="research-templates", viewset=ResearchTemplateViewSet, basename="researchtemplates"
)
router.register(
    prefix="researchs", viewset=ResearchViewSet, basename="researchs"
)
router.register(
    prefix="metrics-values", viewset=MetricValueViewSet, basename="metricsvalues"
)
router.register(
    prefix="patient-diseases", viewset=PatientDeseaseViewSet, basename="patientdiseases"
)
router.register(
    prefix="type-checkpoints", viewset=TypeCheckPointViewSet, basename="typecheckpoints"
)
router.register(
    prefix="ablation-sites", viewset=AblationSiteViewSet, basename="ablationsites"
)
router.register(
    prefix="hospitals", viewset=HospitalViewSet, basename="hospitals"
)
router.register(
    prefix="diseases", viewset=DiseaseViewSet, basename="diseases"
)
router.register(
    prefix="units", viewset=UnitViewSet, basename="units"
)
router.register(
    prefix="pharmacological-groups", viewset=PharmacologicalGroupViewSet, basename="pharmacologicalgroups"
)
router.register(
    prefix="active-ingredients", viewset=ActiveIngredientViewSet, basename="activeingredients"
)
router.register(
    prefix="medicines", viewset=MedicineViewSet, basename="medicines"
)
router.register(
    prefix="catheter-types", viewset=CatheterTypeViewSet, basename="cathetertypes"
)

urlpatterns = [
    path("", include(router.urls)),
]
