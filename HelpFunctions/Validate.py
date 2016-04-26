from Constants.Constants import suppCurrencies, suppServices
from marshmallow import ValidationError, validates


def validate_currency(data):
    if data not in suppCurrencies:
        raise ValidationError('Currency misspelled or not supported yet. Sorry')


def validate_service(data):
    for serv in data:
        print(serv)
        if serv not in suppServices:
            raise ValidationError('Service misspelled or not supported yet. Sorry')
