import os
import random

from django.db import models
from model_utils.models import TimeStampedModel

from extuser.models import ExtUser
from tequilla import settings


class Metro(TimeStampedModel):
    """
    Станция метро.
    Клубы привязываются к станции метро.
    """
    name = models.CharField('Название', max_length=255)
    old_id = models.PositiveIntegerField(
        'ID из старой системы',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class City(TimeStampedModel):
    """
    Город.
    Клубы привязываются к городу.
    """
    name = models.CharField('Название', max_length=255)

    def __str__(self):
        return self.name


class ClubType(TimeStampedModel):
    """
    Тип заведения
    Клубы связаны с типами заведения.
    """
    name = models.CharField('Название', max_length=255)
    old_id = models.PositiveIntegerField(
        'ID из старой системы',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


class DayOfWeek(TimeStampedModel):
    """
    Дни недели.
    Клубы связаны с днями недели.
    """
    name = models.CharField('Название', max_length=30)
    short_name = models.CharField('Короткое название', max_length=3)
    num = models.PositiveSmallIntegerField('Номер')

    def __str__(self):
        return self.name


class Club(TimeStampedModel):

    BEAKER_CHOICE = 'beaker'
    SHOT_CHOICE = 'shot'
    FORMULA_CHOICES = (
        (BEAKER_CHOICE, 'Для мензурки'),
        (SHOT_CHOICE, 'Для шотов'),
    )

    SIZE_40_CHOICE = 40
    SIZE_50_CHOICE = 50
    SIZE_CHOICES = (
        (SIZE_40_CHOICE, '40 мл.'),
        (SIZE_50_CHOICE, '50 мл.')
    )

    is_active = models.BooleanField('Активен', default=False)
    name = models.CharField('Название', max_length=255)
    old_id = models.PositiveIntegerField('ID из старой системы', blank=True, null=True)
    order = models.PositiveIntegerField('Позиция', default=0)
    metro = models.ForeignKey(Metro, blank=True, null=True, verbose_name='Станция метро')
    street = models.CharField('Улица', max_length=255)
    house = models.CharField('Дом', max_length=255)
    site = models.CharField('Сайт', max_length=255, blank=True)
    city = models.ForeignKey(City, verbose_name='Город', blank=True, null=True)
    type = models.ManyToManyField(ClubType, verbose_name='Тип заведения', blank=True)
    days_of_week = models.ManyToManyField(DayOfWeek, blank=True, verbose_name='Дни недели')
    description = models.TextField('Описание', blank=True, null=True)
    features = models.TextField('Особенности', blank=True, null=True)
    discount_conditions = models.TextField('Условия скидки', blank=True, null=True)
    drinks = models.TextField('Напитки', blank=True, null=True)
    count_shots = models.CharField('Норма шотов', max_length=255, blank=True, null=True)
    start_time = models.CharField('Время начала работы', max_length=6, default='00:00')
    end_time = models.CharField('Время окончания работы', max_length=6, default='00:00')
    w_start_time = models.CharField('Время начала работы на выходных', max_length=6, default='00:00')
    w_end_time = models.CharField('Время окончания работы на выходных', max_length=6, default='00:00')
    contact_person = models.TextField('Контактное лицо', blank=True, null=True)
    formula = models.CharField('Формула рассчета', max_length=10, choices=FORMULA_CHOICES, default=SHOT_CHOICE)
    size_for_calc = models.PositiveSmallIntegerField(
        'Размер мензурок (для калькулятора)', choices=SIZE_CHOICES, blank=True, null=True)
    coordinator = models.ForeignKey(
        ExtUser, verbose_name='Координатор', related_name='coordinate_clubs', blank=True, null=True
    )
    rate = models.CharField('Рейтинг', default='0', max_length=5)
    employee = models.ManyToManyField(ExtUser, verbose_name='Сотрудники', blank=True, related_name='clubs')
    photo = models.ImageField('Фотография', blank=True, null=True, upload_to="club")

    def get_default_photo(self):
        return settings.DEFAULT_CLUB_PHOTO

    def __str__(self):
        return self.name + (' (м.' + self.metro.name + ', ' if self.metro is not None else ' (') + \
               self.street + ', ' + self.house + ')'

    def get_address(self):
        return ('м.' + self.metro.name + ', ' if self.metro is not None else ' ') + self.street + ', ' + self.house

    class Meta:
        ordering = ('order',)


class Drink(TimeStampedModel):
    """
    Напитки в заведении
    """
    name = models.CharField(max_length=255, verbose_name='Название')
    price_in_bar = models.IntegerField(verbose_name='Цена в баре')
    price_for_sale = models.IntegerField(verbose_name='Цена продажи')
    club = models.ForeignKey(Club, verbose_name='Заведение')

    def __str__(self):
        return self.name
