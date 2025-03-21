from rest_framework import serializers
from .models import *


class HospitalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hospital
        fields = ("fullname", "shortname", "city", "note")


class UnitlSerializer(serializers.ModelSerializer):

    class Meta:
        model = Unit
        fields = ("fullname", "shortname")


class PharmacologicalGrouplSerializer(serializers.ModelSerializer):

    class Meta:
        model = PharmacologicalGroup
        fields = ("name",)


class ActiveIngredientlSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActiveIngredient
        fields = ("name", "pharmacological_group")


class MedicineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Medicine
        fields = ("trade_name", "international_name", "active_ingredient")

class CatheterTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CatheterType
        fields = ("fullname", "shortname", "note")

class DiseaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Disease
        fields = ("fullname", "shortname", "code_ICD_10", "note")


# -------------------------


class AblationSiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = AblationSite
        fields = ("surgical_operation", "name", "note")


class SurgicalOperationSerializer(serializers.ModelSerializer):
    type_stage = serializers.CharField()
    ablation_sites = AblationSiteSerializer(many=True, read_only=True)

    class Meta:
        model = SurgicalOperation
        fields = (
            "check_point_id",
            "catheter",
            "name",
            "date",
            "type_stage",
            "ablation_sites",
            "number_of_ablation_points",
            "note",
        )


class TreatmentDrugSerializer(serializers.ModelSerializer):
    type_stage = serializers.CharField()

    class Meta:
        model = TreatmentDrug
        fields = (
            "check_point_id",
            "medicine",
            "note",
            "dose",
            "type_stage",
            "taking_medicine_morning",
            "taking_medicine_day",
            "taking_medicine_evening",
            "taking_medicine_night",
        )


class TypeCheckPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeCheckPoint
        fields = (
            "name",
            "note",
        )


class CheckPointSerializer(serializers.ModelSerializer):
    operations = SurgicalOperationSerializer(many=True, read_only=True)
    treatments_drugs = TreatmentDrugSerializer(many=True, read_only=True)
    type_point = serializers.CharField()

    class Meta:
        model = CheckPoint
        fields = (
            "patient",
            "type_point",
            "date_of_receipt",
            "date_of_discharge",
            "hospital_id",
            "operations",
            "treatments_drugs",
            "note",
        )


class PatientDeseaseSerializer(serializers.ModelSerializer):
    patient_id = serializers.CharField()
    disease_id = serializers.CharField()

    class Meta:
        model = PatientDesease
        fields = (
            "patient_id",
            "disease_id",
            "year_start_disease",
            "note",
            "classification_disease",
        )


class PatientSerializer(serializers.ModelSerializer):
    points = CheckPointSerializer(many=True, read_only=True)
    patient_diseases = PatientDeseaseSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = ("code", "gender", "birth", "points", "patient_diseases", "note")


class MetricSerializer(serializers.ModelSerializer):
    measurement_type = serializers.CharField()
    unit_for_metric = serializers.CharField()

    class Meta:
        model = Metric
        fields = (
            "measurement_type",
            "fullname",
            "shortname",
            "reference_max_numerical",
            "reference_min_numerical",
            "reference_binary",
            "unit_for_metric",
            "note",
        )


class VariantQualitativeSerializer(serializers.ModelSerializer):
    metric_id = serializers.CharField()

    class Meta:
        model = VariantQualitative
        fields = ("metric_id", "value", "reference", "note")


class MetricsTemplatesSerializer(serializers.ModelSerializer):
    research_template_id = serializers.CharField()
    metric_id = serializers.CharField()

    class Meta:
        model = MetricsTemplates
        fields = ("research_template_id", "metric_id", "note")


class ResearchTemplateSerializer(serializers.ModelSerializer):
    metrics_templates = MetricsTemplatesSerializer(many=True, read_only=True)

    class Meta:
        model = ResearchTemplate
        fields = ("name", "type_research", "metrics_templates", "note")


class MetricValueSerializer(serializers.ModelSerializer):
    research_id = serializers.CharField()
    metric_id = serializers.CharField()

    class Meta:
        model = MetricValue
        fields = (
            "research_id",
            "metric_id",
            "value_qualitative_id",
            "value_numerical",
            "value_binary",
            "value_descriptive",
            "note",
        )


class ResearchSerializer(serializers.ModelSerializer):
    research_template_id = serializers.CharField()
    check_point_id = serializers.CharField()
    metrics_values = MetricValueSerializer(many=True, read_only=True)

    class Meta:
        model = Research
        fields = (
            "research_template_id",
            "check_point_id",
            "date",
            "metrics_values",
            "note",
        )
