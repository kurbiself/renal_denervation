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
        # patient_filter = self.request.query_params.get("patient_id")
        # disease_filter = self.request.query_params.get("disease_name")
        # if patient_filter:
        #     patient_desease = patient_desease.filter(patient_id=patient_filter)
        # if disease_filter:
        #     patient_desease = patient_desease.filter(
        #         disease_id__fullname__istartswith=disease_filter
        #     )
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
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        surgical_operations = SurgicalOperation.objects.all()

        check_point_id_filter = self.request.query_params.get("check_point_id")
        if check_point_id_filter:
            surgical_operations = surgical_operations.filter(
                check_point_id=check_point_id_filter
            )

        return surgical_operations


class AblationSiteViewSet(viewsets.ModelViewSet):
    serializer_class = AblationSiteSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        ablation_sites = AblationSite.objects.all()
        return ablation_sites


class TreatmentDrugViewSet(viewsets.ModelViewSet):
    serializer_class = TreatmentDrugSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        treatments_drug = TreatmentDrug.objects.all()
        check_point_id_filter = self.request.query_params.get("check_point_id")
        if check_point_id_filter:
            treatments_drug = treatments_drug.filter(
                check_point_id=check_point_id_filter
            )
        return treatments_drug


class MetricViewSet(viewsets.ModelViewSet):
    serializer_class = MetricSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        metrics = Metric.objects.all()
        return metrics


class VariantQualitativeViewSet(viewsets.ModelViewSet):
    serializer_class = VariantQualitativeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        variants_qualitative = VariantQualitative.objects.all()
        metric_id_filter = self.request.query_params.get("metric_id")
        reference_filter = self.request.query_params.get("reference")
        if metric_id_filter:
            variants_qualitative = variants_qualitative.filter(
                metric_id=metric_id_filter
            )
        if reference_filter:
            variants_qualitative = variants_qualitative.filter(
                reference=reference_filter
            )
        return variants_qualitative


class MetricsTemplatesViewSet(viewsets.ModelViewSet):
    serializer_class = MetricsTemplatesSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        metrics_templates = MetricsTemplates.objects.all()
        metric_id_filter = self.request.query_params.get("metric_id")
        research_template_id_filter = self.request.query_params.get(
            "research_template_id"
        )
        if metric_id_filter:
            metrics_templates = metrics_templates.filter(metric_id=metric_id_filter)
        if research_template_id_filter:
            metrics_templates = metrics_templates.filter(
                research_template_id=research_template_id_filter
            )
        return metrics_templates


class ResearchTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = ResearchTemplateSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        research_templates = ResearchTemplate.objects.all()
        return research_templates


class ResearchViewSet(viewsets.ModelViewSet):
    serializer_class = ResearchSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):

        researchs = Research.objects.all()
        check_point_id_filter = self.request.query_params.get("check_point_id")
        research_template_id_filter = self.request.query_params.get(
            "research_template_id"
        )
        if check_point_id_filter:
            researchs = researchs.filter(check_point_id=check_point_id_filter)
        if research_template_id_filter:
            researchs = researchs.filter(
                research_template_id=research_template_id_filter
            )
        return researchs


class MetricValueViewSet(viewsets.ModelViewSet):
    serializer_class = MetricValueSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        metrics_values = MetricValue.objects.all()
        research_id_filter = self.request.query_params.get("research_id")
        if research_id_filter:
            metrics_values = metrics_values.filter(research_id=research_id_filter)

        return metrics_values


class HospitalViewSet(viewsets.ModelViewSet):
    serializer_class = HospitalSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        hospitals = Hospital.objects.all()
        return hospitals


class DiseaseViewSet(viewsets.ModelViewSet):
    serializer_class = DiseaseSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

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
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        units = Unit.objects.all()
        return units


class PharmacologicalGroupViewSet(viewsets.ModelViewSet):
    serializer_class = PharmacologicalGrouplSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        pharmacological_groups = PharmacologicalGroup.objects.all()
        return pharmacological_groups


class ActiveIngredientViewSet(viewsets.ModelViewSet):
    serializer_class = ActiveIngredientlSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        active_ingredients = ActiveIngredient.objects.all()
        return active_ingredients


class MedicineViewSet(viewsets.ModelViewSet):
    serializer_class = MedicineSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        medicines = Medicine.objects.all()
        return medicines


class CatheterTypeViewSet(viewsets.ModelViewSet):
    serializer_class = CatheterTypeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        catheter_types = CatheterType.objects.all()
        return catheter_types
