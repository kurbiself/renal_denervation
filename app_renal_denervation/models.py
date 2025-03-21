from django.db import models
from django.contrib.auth import get_user_model
from model_utils import Choices
from django.utils.timezone import datetime


User = get_user_model()


# ---------------------Cправочники-------------------------------
class Hospital(models.Model):  # Лечебно-профилактическое учреждение
    fullname = models.CharField(
        max_length=256,
        unique=True,
        verbose_name="Полное название лечебно-профилактического учреждения",
    )
    shortname = models.CharField(
        max_length=256,
        verbose_name="Аббревиатура лечебно-профилактического учреждения",
        null=True,
        blank=True,
    )
    city = models.CharField(
        max_length=128, verbose_name="Город местонахождения ЛПУ", null=True, blank=True
    )
    note = models.CharField(
        max_length=1024, verbose_name="Примечание", blank=True, null=True
    )

    def __str__(self):
        return self.shortname

    class Meta:
        verbose_name = "Лечебно-профилактическое учреждение"
        verbose_name_plural = "Лечебно-профилактические учреждения"


class Unit(models.Model):
    fullname = models.CharField(
        max_length=256,
        unique=True,
        verbose_name="Название единиц измерения",
        null=True,
        blank=True,
    )
    shortname = models.CharField(
        max_length=256,
        verbose_name="Обозначение единиц изменения",
    )

    def __str__(self):
        return self.shortname

    class Meta:
        verbose_name = "Единица измерений"
        verbose_name_plural = "Единицы измерений"


class PharmacologicalGroup(models.Model):
    name = models.CharField(
        max_length=256, verbose_name="Название фармакологической группы"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Фармакологическая группа"
        verbose_name_plural = "Фармакологические группы"


class ActiveIngredient(models.Model):
    name = models.CharField(max_length=256, verbose_name="Название активного вещества")
    pharmacological_group = models.ForeignKey(
        PharmacologicalGroup,
        on_delete=models.CASCADE,
        verbose_name="Фармакологическая группа",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Активное вещество"
        verbose_name_plural = "Активные вещества"


class Medicine(models.Model):
    active_ingredient = models.ForeignKey(
        ActiveIngredient, verbose_name="Активное вещество", on_delete=models.CASCADE
    )
    trade_name = models.CharField(
        max_length=256, unique=True, verbose_name="Торговое наименование"
    )
    international_name = models.CharField(
        max_length=256, verbose_name="Международное непантентованное название"
    )

    def __str__(self):
        return self.trade_name

    class Meta:
        verbose_name = "Лекарство"
        verbose_name_plural = "Лекарства"


class CatheterType(models.Model):  # ?
    fullname = models.CharField(max_length=256, verbose_name="Название катетера")
    shortname = models.CharField(
        max_length=256,
        verbose_name="Сокращённое название катетера",
        null=True,
        blank=True,
    )
    note = models.CharField(
        max_length=1024, verbose_name="Примечание", blank=True, null=True
    )

    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name = "Катетер"
        verbose_name_plural = "Катетеры"


class Disease(models.Model):
    fullname = models.CharField(max_length=256, verbose_name="Название заболевания")
    shortname = models.CharField(
        max_length=256, verbose_name="Краткое название заболевания", null=True, blank=True
    )
    code_ICD_10 = models.CharField(max_length=16, verbose_name="Код МКБ 10", null=True, blank=True)
    note = models.CharField(
        max_length=1024, verbose_name="Примечание", blank=True, null=True
    )

    def __str__(self):
        return f"{self.fullname} ({self.code_ICD_10})"

    class Meta:
        verbose_name = "Заболевание"
        verbose_name_plural = "Заболевания"


# -------------------------------------------------------------


class Patient(models.Model):

    code = models.CharField(
        max_length=128, verbose_name="Идентификатор пациента", unique=True
    )
    GenderType = Choices("Мужской", "Женский")
    gender = models.CharField(choices=GenderType, verbose_name="Пол пациента")
    birth = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    note = models.CharField(
        max_length=1024, verbose_name="Примечание", blank=True, null=True
    )

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Пациент"
        verbose_name_plural = "Пациенты"


class PatientDesease(models.Model):
    patient_id = models.ForeignKey(
        Patient, related_name="patient_diseases", on_delete=models.CASCADE
    )
    disease_id = models.ForeignKey(
        Disease,
        verbose_name="Заболевание пациента",
        null=True,
        related_name="patient_diseases",
        on_delete=models.CASCADE,
    )
    year_start_disease = models.IntegerField(verbose_name="Год начала заболевания")
    note = models.CharField(
        max_length=1024, verbose_name="Примечание", blank=True, null=True
    )
    ClassificationDisease = Choices("Основное", "Сопуствующее")
    classification_disease = models.CharField(
        choices=ClassificationDisease, verbose_name="Тип значимости заболевания"
    )

    def __str__(self):
        return f"{self.disease_id} ({self.classification_disease})"

    class Meta:
        verbose_name = "Заболевание пациента"
        verbose_name_plural = "Заболевания пациента"


class TypeCheckPoint(models.Model):
    name = models.CharField(max_length=256, verbose_name="Название контрольной точки")
    note = models.CharField(
        max_length=1024, verbose_name="Примечание", blank=True, null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип контрольной точки"
        verbose_name_plural = "Типы контрольных точек"


class CheckPoint(models.Model):
    patient = models.ForeignKey(
        Patient,
        related_name="points",
        on_delete=models.CASCADE,
        verbose_name="ID пациента",
    )
    hospital_id = models.ForeignKey(
        Hospital, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="ЛПУ"
    )

    type_point = models.ForeignKey(
        TypeCheckPoint,
        related_name="points",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Тип контрольной точки",
    )

    date_of_receipt = models.DateField(
        null=True, blank=True, verbose_name="Дата поступления"
    )
    date_of_discharge = models.DateField(
        null=True, blank=True, verbose_name="Дата выписки"
    )
    note = models.CharField(
        max_length=1024, verbose_name="Примечание", blank=True, null=True
    )

    def __str__(self):
        return f"{self.patient} - {self.type_point}"

    class Meta:
        verbose_name = "Контрольная точка"
        verbose_name_plural = "Контрольные точки"


class SurgicalOperation(models.Model):
    TypeStage = Choices("Операция", "Повторная операция")

    check_point_id = models.ForeignKey(
        CheckPoint,
        related_name="operations",
        on_delete=models.CASCADE,
        verbose_name="ID контрольной точки",
    )
    catheter = models.ForeignKey(
        CatheterType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Тип катетера",
    )
    name = models.CharField(
        max_length=128, verbose_name="Название оперативного вмешательства"
    )
    number_of_ablation_points = models.IntegerField(
        verbose_name="Количество точек абляции"
    )
    date = models.DateField(verbose_name="Дата оперативного вмешательства")

    type_stage = models.CharField(choices=TypeStage, verbose_name="Тип лечения")
    note = models.CharField(
        max_length=1024, verbose_name="Примечание", blank=True, null=True
    )

    def __str__(self):
        return f"{self.type_stage} - {self.name}"

    class Meta:
        verbose_name = "Оперативное вмешательство"
        verbose_name_plural = "Оперативные вмешательства"


class AblationSite(models.Model):
    surgical_operation = models.ForeignKey(
        SurgicalOperation,
        related_name="ablation_sites",
        on_delete=models.CASCADE,
        verbose_name="ID операции",
    )
    name = models.CharField(max_length=256, verbose_name="Название места абляции")
    note = models.CharField(
        max_length=1024, verbose_name="Примечание", blank=True, null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Место абляиции"
        verbose_name_plural = "Места абляции"


class TreatmentDrug(models.Model):
    check_point_id = models.ForeignKey(
        CheckPoint,
        related_name="treatments_drugs",
        on_delete=models.CASCADE,
        verbose_name="ID контрольной точки",
    )
    medicine = models.ForeignKey(
        Medicine, on_delete=models.CASCADE, verbose_name="Лекарство"
    )
    TypeStage = Choices("Фармакотерапия")
    type_stage = models.CharField(choices=TypeStage, verbose_name="Тип лечения")
    dose = models.FloatField(null=True, blank=True, verbose_name="Доза")
    taking_medicine_morning = models.BooleanField(verbose_name="Приём утром")
    taking_medicine_day = models.BooleanField(verbose_name="Приём днём")
    taking_medicine_evening = models.BooleanField(verbose_name="Приём вечером")
    taking_medicine_night = models.BooleanField(verbose_name="Приём на ночь")
    note = models.CharField(
        max_length=1024, verbose_name="Примечание", blank=True, null=True
    )

    def __str__(self):
        return f"{self.medicine}"

    class Meta:
        verbose_name = "Фармакотерапия"
        verbose_name_plural = "Фармакотерапии"


class Metric(models.Model):
    MeasurementType = Choices(
        "количественный", "качественный", "бинарный", "описательный"
    )
    measurement_type = models.CharField(
        choices=MeasurementType, verbose_name="Тип измерямеого признака"
    )
    fullname = models.CharField(max_length=256, verbose_name="Название показателя")
    shortname = models.CharField(
        max_length=256, verbose_name="Краткое название показателя", null=True
    )
    reference_max_numerical = models.IntegerField(
        verbose_name="Референсное значение по верхней границе количественного признака",
        null=True,
        blank=True,
    )
    reference_min_numerical = models.IntegerField(
        verbose_name="Референсное значение по нижней границе количественного признака",
        null=True,
        blank=True,
    )
    reference_binary = models.BooleanField(
        verbose_name="Референсное значение для бинарного признака",
        null=True,
        blank=True,
    )
    unit_for_metric = models.ForeignKey(
        Unit,
        related_name="metrics",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Единицы измерения",
    )
    note = models.CharField(
        max_length=1024, verbose_name="Примечание", blank=True, null=True
    )

    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name = "Показатель исследования"
        verbose_name_plural = "Показатели исследований"

    # референсные показатель для качественного признака есть в самой модели VariantQualitative
    # и определяется в измеряемом показателе


class VariantQualitative(models.Model):
    metric_id = models.ForeignKey(
        Metric,
        on_delete=models.CASCADE,
        related_name="variants_qualitative",
        verbose_name="Показатель",
    )  # вариант признрака относится к определённому показателю (цвет кожнымх покровов к коже и т.д.)
    value = models.CharField(max_length=256, verbose_name="Вариант признака")
    reference = models.BooleanField(
        verbose_name="Допустимое значение"
    )  # норма/не норма
    note = models.CharField(
        max_length=1024, verbose_name="Примечание", blank=True, null=True
    )

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = "Вариант качественного признака"
        verbose_name_plural = "Варианты качественного признака"


class ResearchTemplate(models.Model):
    ResearchType = Choices("Лабораторное", "Инструментальное")
    ObligationOfResearch = Choices("Обязательное", "Необязательное")
    name = models.CharField(max_length=256, verbose_name="Название")
    type_research = models.CharField(
        choices=ResearchType, null=True, blank=True, verbose_name="Тип исследования"
    )
    obligation_of_research = models.CharField(
        choices=ObligationOfResearch, verbose_name="Важность исследования"
    )
    note = models.CharField(
        max_length=1024, verbose_name="Примечание", blank=True, null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Шаблон исследования"
        verbose_name_plural = "Шаблоны исследований"


class MetricsTemplates(models.Model):
    research_template_id = models.ForeignKey(
        ResearchTemplate,
        on_delete=models.CASCADE,
        related_name="metrics_templates",
        verbose_name="Шаблон исследования",
    )
    metric_id = models.ForeignKey(
        Metric, on_delete=models.CASCADE, verbose_name="Показатель"
    )
    note = models.CharField(
        max_length=1024, verbose_name="Примечание", blank=True, null=True
    )

    def __str__(self):
        return f"{self.metric_id.shortname} ({self.research_template_id.name })"

    class Meta:
        verbose_name = "Шаблон показателя"
        verbose_name_plural = "Шаблоны показателей"


class Research(models.Model):
    research_template_id = models.ForeignKey(
        ResearchTemplate, on_delete=models.CASCADE, verbose_name="Шаблон исследования"
    )
    check_point_id = models.ForeignKey(
        CheckPoint,
        on_delete=models.CASCADE,
        verbose_name="Контрольная точка исследования",
    )
    date = models.DateField(
        verbose_name="Дата проводимого исследования", null=True, blank=True
    )
    note = models.CharField(
        max_length=1024, verbose_name="Примечание", blank=True, null=True
    )

    def __str__(self):
        return f"{self.check_point_id} - {self.research_template_id}"

    class Meta:
        verbose_name = "Исследование"
        verbose_name_plural = "Исследования"


class MetricValue(models.Model):
    research_id = models.ForeignKey(
        Research,
        on_delete=models.CASCADE,
        related_name="metrics_values",
        verbose_name="Исследование",
    )
    metric_id = models.ForeignKey(Metric, on_delete=models.CASCADE)
    value_qualitative_id = models.ManyToManyField(
        VariantQualitative,
        verbose_name="Значение качественногоо признака",
        blank=True,
        null=True,
    )  # Определили связь многие ко многим
    value_numerical = models.IntegerField(
        verbose_name="Значение количественного признака", blank=True, null=True
    )
    value_binary = models.BooleanField(
        verbose_name="Значение бинарного признака", blank=True, null=True
    )
    value_descriptive = models.CharField(
        max_length=1024,
        verbose_name="Значение описательного признака",
        blank=True,
        null=True,
    )
    note = models.CharField(
        max_length=1024, verbose_name="Примечание", blank=True, null=True
    )

    def __str__(self):
        return f"{self.research_id} - {self.metric_id}"

    class Meta:
        verbose_name = "Значение показателя"
        verbose_name_plural = "Значения показателей"
