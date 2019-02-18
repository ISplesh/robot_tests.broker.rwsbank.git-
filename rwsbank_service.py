#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
import pytz
import urllib
import os


tz = str(datetime.now(pytz.timezone('Europe/Kiev')))[26:]


def prepare_tender_data(role, data):
    if role == 'tender_owner':
        data['data']['procuringEntity']['name'] = u'Ubisoft'
    return data


def convert_date_from_item(date):
    date = datetime.strptime(date, '%d/%m/%Y %H:%M:%S').strftime('%Y-%m-%d')
    return '{}T00:00:00{}'.format(date, tz)


def adapt_paid_date(sign_date, date_paid):
    time = sign_date[-8:]
    date = datetime.strptime(date_paid, '%Y-%m-%d')
    return '{} {}'.format(datetime.strftime(date, '%d/%m/%Y'), time)


def convert_date(date):
    date = datetime.strptime(date, '%d/%m/%Y %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%S.%f')
    return '{}{}'.format(date, tz)


def convert_date_for_item(date):
    date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S{}'.format(tz)).strftime('%d/%m/%Y %H:%M')
    return '{}'.format(date)


def convert_date_for_auction(date):
    date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f{}'.format(tz)).strftime('%d/%m/%Y %H:%M')
    return '{}'.format(date)

def convert_date_for_datePaid(date):
    date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f{}'.format(tz)).strftime('%d/%m/%Y %H:%M:%S')
    return date


def dgf_decision_date_from_site(date):
    return u'{}-{}-{}'.format(date[-4:], date[-7:-5], date[-10:-8])


def dgf_decision_date_for_site(date):
    return u'{}/{}/{}'.format(date[-2:], date[-5:-3], date[-10:-6])


def adapted_dictionary(value):
    return{
        u'Класифікація згідно CAV': 'CAV',
        u'Класифікація згідно CAV-PS': 'CAV-PS',
        u'Класифікація згідно CPV': 'CPV',
        u'Аукцiон': 'active.auction',
        u'Аукціон': 'active.auction',
        u'Очiкування пропозицiй': 'active.tendering',
        u'Торги не відбулися': 'unsuccessful',
        u'Аукціон не відбувся': 'unsuccessful',
        u'Продаж завершений': 'complete',
        u'Торги скасовано': 'cancelled',
        u'Аукціон відмінено': 'cancelled',
        u'Квалiфiкацiя переможця': 'active.qualification',
        u'Прийняття заяв на участь': 'active.qualification',
        u'Очікується опублікування протоколу': 'active.qualification',
        u'Очікується рішення': 'pending.waiting',
        u'Очікується протокол': 'pending',
        u'Рішення скасоване': 'unsuccessful',
        u'Відмова від очікування': 'cancelled',
        u'Очікується рішення про викуп': 'pending.admission',
        u'Переможець': 'active',
        u'об’єкт реєструється': u'registering',
        u'об’єкт зареєстровано': u'complete',
        u'Об’єкт зареєстровано': u'complete',
        u'Опубліковано': u'pending',
        u'Актив завершено': u'complete',
        u'Публікація інформаційного повідомлення': u'composing',
        u'Перевірка доступності об’єкту': u'verification',
        u'lot.status.pending.deleted': u'pending.deleted',
        u'Об’єкт виключено': u'deleted',
        u'Інформація': u'informationDetails',
        u'об’єктів малої приватизації - аукціон': u'sellout.english',
        u'Заплановано': u'scheduled',
        u'Виконано': u'met',
        u'Не виконано': u'notMet',
        u'Завершений': u'terminated',
        u'Не успішний': u'unsuccessful',
        u'Очікується оплата.': u'active.confirmation',
        u'Очікується оплата': u'active.payment',
        u'Договір оплачено. Очікується наказ': u'active.approval',
        u'Період виконання умов продажу (період оскарження)': u'active',
        u"Приватизація об’єкта завершена.": u'pending.terminated',
        u"Приватизація об’єкта неуспішна.": u'pending.unsuccessful',
        u"Приватизація об’єкта завершена": u'terminated',
        u"Приватизація об’єкта неуспішна": u'unsuccessful'
    }.get(value, value)


def adapt_data(field, value):
    if field == 'tenderAttempts':
        value = int(value)
    elif 'dutchSteps' in field:
        value = int(value)
    elif field == 'value.amount':
        value = float(value)
    elif field == 'minimalStep.amount':
        value = float(value.split(' ')[0])
    elif field == 'guarantee.amount':
        value = float(value.split(' ')[0])
    elif field == 'quantity':
        value = float(value.replace(',', '.'))
    elif field == 'minNumberOfQualifiedBids':
        value = int(value)
    elif 'contractPeriod' in field:
        value = convert_date_from_item(value)
    elif 'tenderPeriod' in field or 'auctionPeriod' in field or 'datePaid' in field:
        value = convert_date(value)
    elif 'dgfDecisionDate' in field:
        value = dgf_decision_date_from_site(value)
    elif 'dgfDecisionID' in field:
        value = value[-6:]
    else:
        value = adapted_dictionary(value)
    return value


def download_file(url, filename, folder):
    urllib.urlretrieve(url, ('{}/{}'.format(folder, filename)))


def my_file_path():
    return os.path.join(os.getcwd(), 'src', 'robot_tests.broker.rwsbank', 'Doc.pdf')


