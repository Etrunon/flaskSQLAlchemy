from Constants.Currencies import suppCurrencies
from marshmallow import ValidationError, validates


@validates('currency')
def validate_currency(self, data):
    if data not in suppCurrencies:
        raise ValidationError('Currency misspelled or not supported yet. Sorry')


@validates('currency')
def validate_service(self, data):
    print(data)
    if data not in suppCurrencies:
        raise ValidationError('Service misspelled or not supported yet. Sorry')