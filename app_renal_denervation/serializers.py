from rest_framework import serializers
from .models import *


class HospitalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hospital
        fields = ("id", "fullname", "shortname", "city", "note")


class UnitlSerializer(serializers.ModelSerializer):

    class Meta:
        model = Unit
        fields = ("id", "fullname", "shortname")


class PharmacologicalGrouplSerializer(serializers.ModelSerializer):

    class Meta:
        model = PharmacologicalGroup
        fields = (
            "id",
            "name",
        )


class ActiveIngredientlSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActiveIngredient
        fields = ("id", "name", "pharmacological_group")


class MedicineSerializer(serializers.ModelSerializer):

    active_ingredient_name = serializers.SerializerMethodField()
    pharmacological_group_name = serializers.SerializerMethodField()
    pharmacological_group_id = serializers.SerializerMethodField()

    class Meta:
        model = Medicine
        fields = (
            "id",
            "trade_name",
            "international_name",
            "active_ingredient",
            "active_ingredient_name",
            "pharmacological_group_id",
            "pharmacological_group_name",
        )

    def get_active_ingredient_name(self, obj):
        return obj.active_ingredient.name

    def get_pharmacological_group_name(self, obj):
        return obj.active_ingredient.pharmacological_group.name

    def get_pharmacological_group_id(self, obj):
        return obj.active_ingredient.pharmacological_group.id


class CatheterTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CatheterType
        fields = ("id", "fullname", "shortname", "note")


class DiseaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Disease
        fields = ("id", "fullname", "shortname", "code_ICD_10", "note")


# -------------------------


class AblationSiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = AblationSite
        fields = ("id", "surgical_operation", "name", "note")


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
    medicine_name = serializers.SerializerMethodField()

    class Meta:
        model = TreatmentDrug
        fields = (
            "id",
            "check_point_id",
            "medicine",
            "medicine_name",
            "note",
            "dose",
            "type_stage",
            "taking_medicine_morning",
            "taking_medicine_day",
            "taking_medicine_evening",
            "taking_medicine_night",
        )
    def get_medicine_name(self, obj):
        return obj.medicine.international_name


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
    disease_id_fullname = serializers.SerializerMethodField()
    disease_id_shortname = serializers.SerializerMethodField()

    class Meta:
        model = PatientDesease
        fields = (
            "id",
            "patient_id",
            "disease_id",
            "disease_id_fullname",
            "disease_id_shortname",
            "year_start_disease",
            "note",
            "classification_disease",
        )

    def get_disease_id_fullname(self, obj):
        return obj.disease_id.fullname

    def get_disease_id_shortname(self, obj):
        return obj.disease_id.shortname


class PatientSerializer(serializers.ModelSerializer):
    points = CheckPointSerializer(many=True, read_only=True)
    patient_diseases = PatientDeseaseSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = ("id", "code", "gender", "birth", "points", "patient_diseases", "note")


class VariantQualitativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantQualitative
        fields = ("id", "metric_id", "value", "reference", "note")


class MetricSerializer(serializers.ModelSerializer):
    measurement_type = serializers.CharField()
    unit_for_metric_shortname = serializers.SerializerMethodField()
    variants_qualitative = VariantQualitativeSerializer(many=True, read_only=True)

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
            "unit_for_metric_shortname",
            "variants_qualitative",
            "note",
        )

    def get_unit_for_metric_shortname(self, obj):
        return str(obj.unit_for_metric)


class MetricsTemplatesSerializer(serializers.ModelSerializer):
    metric_data = serializers.SerializerMethodField()

    class Meta:
        model = MetricsTemplates
        fields = ("id", "research_template_id", "metric_id", "metric_data", "note")

    def get_metric_data(self, obj):
        return MetricSerializer(obj.metric_id).data


class ResearchTemplateSerializer(serializers.ModelSerializer):
    metrics_templates = MetricsTemplatesSerializer(many=True, read_only=True)

    class Meta:
        model = ResearchTemplate
        fields = (
            "id",
            "name",
            "type_research",
            "metrics_templates",
            "obligation_of_research",
            "note",
        )


class MetricValueSerializer(serializers.ModelSerializer):
    metric_id_data = serializers.SerializerMethodField()

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
            "metric_id_data",
            "note",
        )

    def get_metric_id_data(self, obj):
        return MetricSerializer(obj.metric_id).data


class ResearchSerializer(serializers.ModelSerializer):
    research_template_name = serializers.SerializerMethodField()
    check_point_name = serializers.SerializerMethodField()
    metrics_values = MetricValueSerializer(many=True, read_only=True)

    
    class Meta:
        model = Research
        fields = (
            "id",
            "research_template_id",
            "research_template_name",
            "check_point_id",
            "check_point_name",
            "date",
            "metrics_values",
            "note",
        )

    def get_research_template_name(self, obj):
        return obj.research_template_id.name

    def get_check_point_name(self, obj):
        return str(obj.check_point_id)
