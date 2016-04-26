from marshmallow import fields, ValidationError
import json


class Jsonlist(fields.Field):
    def _deserialize(self, value, attr, obj):
        if value is None or value is "":
            raise ValidationError("Invalid JSON")
        if type(value) is str:
            return json.loads(value)
        return value

