from django.shortcuts import render
from .models import (
    Hospital,
    Disease,
    Unit,
    PharmacologicalGroup,
    ActiveIngredient,
    Medicine,
    CatheterType,
    Patient,
    PatientDesease,
    TypeCheckPoint,
    CheckPoint,
    SurgicalOperation,
    AblationSite,
    TreatmentDrug,
    Metric,
    VariantQualitative,
    MetricsTemplates,
    ResearchTemplate,
    MetricValue,
    Research,
)
from .serializers import (
    HospitalSerializer,
    DiseaseSerializer,
    UnitlSerializer,
    PharmacologicalGrouplSerializer,
    ActiveIngredientlSerializer,
    MedicineSerializer,
    CatheterTypeSerializer,
    PatientSerializer,
    PatientDeseaseSerializer,
    TypeCheckPointSerializer,
    CheckPointSerializer,
    AblationSiteSerializer,
    SurgicalOperationSerializer,
    TreatmentDrugSerializer,
    MetricSerializer,
    VariantQualitativeSerializer,
    MetricsTemplatesSerializer,
    ResearchTemplateSerializer,
    MetricValueSerializer,
    ResearchSerializer,
)
from rest_framework import generics, viewsets, permissions
from rest_framework.parsers import JSONParser


class PatientsViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        patients = Patient.objects.all()
        code_filter = self.request.query_params.get("code")
        gender_filter = self.request.query_params.get("gender")
        birth_filter = self.request.query_params.get("birth")
        if code_filter:
            patients = patients.filter(code=code_filter)
        if gender_filter:
            patients = patients.filter(
                gender__icontains=gender_filter
            )  # искать по "жен", а не по целому слову "Женский"
        if birth_filter:
            patients = patients.filter(birth=birth_filter)

        return patients


class PatientDeseaseViewSet(viewsets.ModelViewSet):
    serializer_class = PatientDeseaseSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        patient_desease = PatientDesease.objects.all()
        patient_filter = self.request.query_params.get("patient_id")
        disease_filter = self.request.query_params.get("disease_name")
        if patient_filter:
            patient_desease = patient_desease.filter(patient_id=patient_filter)
        if disease_filter:
            patient_desease = patient_desease.filter(
                disease_id__fullname__istartswith=disease_filter
            )
        return patient_desease


class TypeCheckPointViewSet(viewsets.ModelViewSet):
    serializer_class = TypeCheckPointSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    def get_queryset(self):
        type_checkpoints = TypeCheckPoint.objects.all()
        name_filter = self.request.query_params.get("name")
        if name_filter:
            type_checkpoints = type_checkpoints.filter(name__icontains=name_filter)
        return type_checkpoints


class CheckPointViewSet(viewsets.ModelViewSet):
    serializer_class = CheckPointSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        check_points = CheckPoint.objects.all()
        patient_filter = self.request.query_params.get("patient")
        type_point_filter = self.request.query_params.get("type_point")
        date_of_receipt_filter_year = self.request.query_params.get(
            "date_of_receipt_year"
        )
        date_of_discharge_filter_year = self.request.query_params.get(
            "date_of_discharge_year"
        )

        if patient_filter:
            check_points = check_points.filter(patient=patient_filter)
        if type_point_filter:
            check_points = check_points.filter(type_point=type_point_filter)
        if date_of_receipt_filter_year:
            check_points = check_points.filter(
                date_of_receipt__year=date_of_receipt_filter_year
            )
        if date_of_discharge_filter_year:
            check_points = check_points.filter(
                date_of_discharge__year=date_of_discharge_filter_year
            )
        return check_points


class SurgicalOperationViewSet(viewsets.ModelViewSet):
    serializer_class = SurgicalOperationSerializer

    def get_queryset(self):
        surgical_operations = SurgicalOperation.objects.all()
        return surgical_operations


class AblationSiteViewSet(viewsets.ModelViewSet):
    serializer_class = AblationSiteSerializer

    def get_queryset(self):
        ablation_sites = AblationSite.objects.all()
        return ablation_sites


class TreatmentDrugViewSet(viewsets.ModelViewSet):
    serializer_class = TreatmentDrugSerializer

    def get_queryset(self):
        treatments_drug = TreatmentDrug.objects.all()
        return treatments_drug


class MetricViewSet(viewsets.ModelViewSet):
    serializer_class = MetricSerializer

    def get_queryset(self):
        metrics = Metric.objects.all()
        return metrics


class MetricViewSet(viewsets.ModelViewSet):
    serializer_class = MetricSerializer

    def get_queryset(self):
        metrics = Metric.objects.all()
        return metrics


class VariantQualitativeViewSet(viewsets.ModelViewSet):
    serializer_class = VariantQualitativeSerializer

    def get_queryset(self):
        variants_qualitative = VariantQualitative.objects.all()
        return variants_qualitative


class MetricsTemplatesViewSet(viewsets.ModelViewSet):
    serializer_class = MetricsTemplatesSerializer

    def get_queryset(self):
        metrics_templates = MetricsTemplates.objects.all()
        return metrics_templates


class ResearchTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = ResearchTemplateSerializer

    def get_queryset(self):
        research_templates = ResearchTemplate.objects.all()
        return research_templates


class ResearchViewSet(viewsets.ModelViewSet):
    serializer_class = ResearchSerializer

    def get_queryset(self):
        researchs = Research.objects.all()
        return researchs


class MetricValueViewSet(viewsets.ModelViewSet):
    serializer_class = MetricValueSerializer

    def get_queryset(self):
        metrics_values = MetricValue.objects.all()
        return metrics_values


class HospitalViewSet(viewsets.ModelViewSet):
    serializer_class = HospitalSerializer

    def get_queryset(self):
        hospitals = Hospital.objects.all()
        return hospitals


class DiseaseViewSet(viewsets.ModelViewSet):
    serializer_class = DiseaseSerializer

    def get_queryset(self):
        diseases = Disease.objects.all()

        shortname_filter = self.request.query_params.get("disease_shortname")
        fullname_filter = self.request.query_params.get("disease_fullname")
        code_ICD_10_filter = self.request.query_params.get("code_ICD_10")
        if fullname_filter:
            diseases = diseases.filter(fullname__icontains=fullname_filter)
        if shortname_filter:
            diseases = diseases.filter(shortname__icontains=shortname_filter)
        if code_ICD_10_filter:
            diseases = diseases.filter(code_ICD_10__icontains=code_ICD_10_filter)
        return diseases


class UnitViewSet(viewsets.ModelViewSet):
    serializer_class = UnitlSerializer

    def get_queryset(self):
        units = Unit.objects.all()
        return units


class PharmacologicalGroupViewSet(viewsets.ModelViewSet):
    serializer_class = PharmacologicalGrouplSerializer

    def get_queryset(self):
        pharmacological_groups = PharmacologicalGroup.objects.all()
        return pharmacological_groups


class ActiveIngredientViewSet(viewsets.ModelViewSet):
    serializer_class = ActiveIngredientlSerializer

    def get_queryset(self):
        active_ingredients = ActiveIngredient.objects.all()
        return active_ingredients


class MedicineViewSet(viewsets.ModelViewSet):
    serializer_class = MedicineSerializer

    def get_queryset(self):
        medicines = Medicine.objects.all()
        return medicines


class CatheterTypeViewSet(viewsets.ModelViewSet):
    serializer_class = CatheterTypeSerializer

    def get_queryset(self):
        catheter_types = CatheterType.objects.all()
        return catheter_types
