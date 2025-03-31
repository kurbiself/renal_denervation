from rest_framework import serializers
from .models import *


class HospitalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hospital
        fields = ("id","fullname", "shortname", "city", "note")


class UnitlSerializer(serializers.ModelSerializer):

    class Meta:
        model = Unit
        fields = ("id","fullname", "shortname")


class PharmacologicalGrouplSerializer(serializers.ModelSerializer):

    class Meta:
        model = PharmacologicalGroup
        fields = ("id","name",)


class ActiveIngredientlSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActiveIngredient
        fields = ("id","name", "pharmacological_group")


class MedicineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Medicine
        fields = ("id","trade_name", "international_name", "active_ingredient")

class CatheterTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CatheterType
        fields = ("id","fullname", "shortname", "note")

class DiseaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Disease
        fields = ("id","fullname", "shortname", "code_ICD_10", "note")


# -------------------------


class AblationSiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = AblationSite
        fields = ("id","surgical_operation", "name", "note")


class SurgicalOperationSerializer(serializers.ModelSerializer):
    type_stage = serializers.CharField()
    ablation_sites = AblationSiteSerializer(many=True, read_only=True)

    class Meta:
        model = SurgicalOperation
        fields = (
            "id",
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
            "id",
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
            "id",
            "name",
            "note",
        )


class CheckPointSerializer(serializers.ModelSerializer):
    operations = SurgicalOperationSerializer(many=True, read_only=True)
    treatments_drugs = TreatmentDrugSerializer(many=True, read_only=True)
    type_point_name = serializers.SerializerMethodField()
    class Meta:
        model = CheckPoint
        fields = (
            "id",
            "patient",
            "type_point",
            "type_point_name",
            "date_of_receipt",
            "date_of_discharge",
            "hospital_id",
            "operations",
            "treatments_drugs",
            "note",
        )
    
    def get_type_point_name(self, obj):
        return obj.type_point.name


class PatientDeseaseSerializer(serializers.ModelSerializer):
    patient_id = serializers.CharField()
    disease_id = serializers.CharField()

    class Meta:
        model = PatientDesease
        fields = (
            "id",
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
        fields = ("id","code", "gender", "birth", "points", "patient_diseases", "note")


class MetricSerializer(serializers.ModelSerializer):
    measurement_type = serializers.CharField()
    unit_for_metric = serializers.CharField()

    class Meta:
        model = Metric
        fields = (
            "id",
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
        fields = ("id","metric_id", "value", "reference", "note")


class MetricsTemplatesSerializer(serializers.ModelSerializer):
    research_template_id = serializers.CharField()
    metric_id = serializers.CharField()

    class Meta:
        model = MetricsTemplates
        fields = ("id","research_template_id", "metric_id", "note")


class ResearchTemplateSerializer(serializers.ModelSerializer):
    metrics_templates = MetricsTemplatesSerializer(many=True, read_only=True)

    class Meta:
        model = ResearchTemplate
        fields = ("id","name", "type_research", "metrics_templates", "note")


class MetricValueSerializer(serializers.ModelSerializer):
    research_id = serializers.CharField()
    metric_id = serializers.CharField()

    class Meta:
        model = MetricValue
        fields = (
            "id",
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
            "id",
            "research_template_id",
            "check_point_id",
            "date",
            "metrics_values",
            "note",
        )
