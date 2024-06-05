from django.db import models
from django.utils import timezone


# Сотрудники
class Worker(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name='Ф.И.О',
                            blank=False,
                            null=False)

    departament = models.ForeignKey('WorkerDepartament',
                                    verbose_name='Отдел',
                                    null=False,
                                    on_delete=models.PROTECT,)

    post = models.ForeignKey('WorkerPost',
                             verbose_name='Должность',
                             null=False,
                             on_delete=models.PROTECT)

    telegram_id = models.ForeignKey('TelegramInfo',
                                    null=True,
                                    on_delete=models.SET_NULL)

    phone_number = models.CharField(max_length=20,
                                    verbose_name='Номер телефона')

    additional_phone_number = models.CharField(max_length=20,
                                               verbose_name='Дополнительный номер телефона')

    birthday = models.DateField(verbose_name='День рождения',
                                default=timezone.now(),
                                blank=False,
                                null=False)

    # Здесь можно добавить отправку писем на почту

    mail = models.EmailField(verbose_name='Почта сотрудника',
                             blank=True,
                             null=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name_plural = 'Сотрудники'
        ordering = ('name',)


class WorkerPost(models.Model):
    title = models.CharField(max_length=255,
                             verbose_name='Название должности',
                             blank=False,
                             null=False)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name_plural = 'Должности'
        ordering = ('title',)


class WorkerDepartament(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name='Отдел',
                            blank=False,
                            null=False)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name_plural = 'Отделы'
        ordering = ('name',)


# Командировки
class BusinessTrip(models.Model):
    city = models.ForeignKey('BusinessTripCity',
                             verbose_name='Город',
                             null=True,
                             on_delete=models.SET_NULL)

    worker = models.ForeignKey('Worker',
                               verbose_name='Сотрудник',
                               null=False,
                               on_delete=models.DO_NOTHING)

    reason = models.ForeignKey('BusinessTripReason',
                               null=False,
                               blank=False,
                               verbose_name='Причина поездки',
                               on_delete=models.DO_NOTHING)

    depart_date = models.DateField(verbose_name='Дата отправки',
                                   default=timezone.now(),
                                   null=False,
                                   blank=False)

    duration = models.IntegerField(verbose_name='Длительность в днях',
                                   default=7,
                                   null=False,
                                   blank=False)

    def __str__(self):
        return f'{self.worker} {self.city} {self.depart_date if self.depart_date else ""}'

    class Meta:
        verbose_name_plural = 'Командировки'


class BusinessTripReason(models.Model):
    reason = models.CharField(max_length=255,
                              unique=True)

    def __str__(self):
        return f'{self.reason}'

    class Meta:
        verbose_name_plural = 'Причины командировок'


class BusinessTripCity(models.Model):
    # Здесь можно добавить синхронизацию с адресным справочником

    city = models.CharField(verbose_name='Город',
                            max_length=255)

    daily_allowance = models.FloatField(verbose_name='Суточные',
                                        null=False,
                                        blank=False,
                                        default=2000)

    def __str__(self):
        return f'{self.city} {self.daily_allowance}'

    class Meta:
        unique_together = ('city', 'daily_allowance')
        verbose_name_plural = 'Город для отправки в командировку'


# Телеграм
class TelegramInfo(models.Model):
    # Здесь можно добавить телеграм бот для отправки документов/напоминаний сотрудникам и клиентам

    telegram_id = models.BigIntegerField(verbose_name='TelegramID (не путать с логином)')

    telegram_login = models.CharField(max_length=255,
                                      verbose_name='Telegram логин')

    def __str__(self):
        return f'{self.telegram_login if self.telegram_login else ""}'

    class Meta:
        verbose_name_plural = 'Данные Telegram'


# Заказы
class Order(models.Model):
    docs = models.ForeignKey('Docs',
                             verbose_name='Документ',
                             null=True,
                             on_delete=models.SET_NULL)

    client = models.ForeignKey('Client',
                               verbose_name='Клиент',
                               null=True,
                               on_delete=models.SET_NULL)

    worker = models.ForeignKey('Worker',
                               verbose_name='Сотрудник',
                               on_delete=models.DO_NOTHING)

    price = models.FloatField(verbose_name='Общая стоимость',
                              default=0)

    def __str__(self):
        return f'{self.docs if self.docs else ""} {self.client if self.client else ""} {self.worker if self.worker else ""} {self.price if self.price else ""}'

    class Meta:
        verbose_name_plural = 'Заказы'


# Документы
class Docs(models.Model):
    file_name = models.CharField(max_length=255,
                                 verbose_name='Название файла',
                                 blank=True)

    file = models.FileField(verbose_name='Файл', upload_to='media/static/')

    file_type = models.ForeignKey('DocsType',
                                  verbose_name='Тип файла',
                                  null=True,
                                  on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.file_name if self.file_name else ""} {self.file_type if self.file_type else ""}'

    class Meta:
        verbose_name_plural = 'Документы'


class DocsType(models.Model):
    type = models.CharField(max_length=255,
                            verbose_name='Тип документа')

    def __str__(self):
        return f'{self.type}'

    class Meta:
        verbose_name_plural = 'Типы документов'


# Информация о клиенте
class Client(models.Model):

    name = models.CharField(max_length=255,
                            verbose_name='Ф.И.О. клиента',
                            blank=False,
                            null=False)

    entity = models.BooleanField(verbose_name='Представляет юр. лицо?')

    company_id = models.ForeignKey('ClientCompany',
                                   verbose_name='Компания клиента',
                                   blank=True,
                                   null=True,
                                   on_delete=models.SET_NULL)

    phone_number = models.CharField(max_length=20,
                                    verbose_name='Номер телефона',)

    additional_phone_number = models.CharField(max_length=20,
                                               verbose_name='Дополнительный номер телефона',)

    telegram_id = models.ForeignKey('TelegramInfo',
                                    blank=True,
                                    null=True,
                                    on_delete=models.SET_NULL)

    # Здесь можно добавить отправку писем на почту

    mail = models.EmailField(verbose_name='Почта клиента',
                             blank=True,
                             null=True)

    def __str__(self):
        return f'{self.name} {self.phone_number if self.phone_number else ""}'

    class Meta:
        verbose_name_plural = 'Клиенты'


class ClientCompany(models.Model):
    title = models.CharField(max_length=255,
                             verbose_name='Название организации',
                             blank=False,
                             null=False)
    inn = models.CharField(max_length=255,
                           verbose_name='ИНН организации',
                           blank=False,
                           null=False)

    def __str__(self):
        return f'{self.title} {self.inn}'

    class Meta:
        verbose_name_plural = 'Организации'


# Информация о товаре/услуге
class Product(models.Model):
    order_id = models.ForeignKey('Order',
                                 verbose_name='Заказ',
                                 blank=False,
                                 null=False,
                                 on_delete=models.CASCADE)

    product_params = models.ForeignKey('ProductParams',
                                       verbose_name='Позиция',
                                       blank=False,
                                       null=False,
                                       on_delete=models.CASCADE)

    count = models.IntegerField(verbose_name='Количество')

    def __str__(self):
        return f'{self.order_id} {self.product_params}'

    class Meta:
        verbose_name_plural = 'Продукты в заказе'


class ProductParams(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name='Название позиции',
                            blank=False,
                            null=False)

    product_type = models.ForeignKey('ProductType',
                                     verbose_name='Тип позиции',
                                     null=True,
                                     on_delete=models.SET_NULL)
    price = models.FloatField(verbose_name='Стоимость',
                              null=False)

    def __str__(self):
        return f'{self.name} {self.price}'

    class Meta:
        verbose_name_plural = 'Товары/услуги'


class ProductType(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name='Тип позиции',
                            blank=False,
                            null=False)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name_plural = 'Типы товаров/услуг'

