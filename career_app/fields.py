"""Custom fields for SQLite compatibility."""
import json
from django.db import models


class JSONTextField(models.TextField):
    """Stores JSON as text for SQLite compatibility."""
    def from_db_value(self, value, expression, connection):
        if value is None or value == "":
            return []
        try:
            return json.loads(value)
        except (TypeError, json.JSONDecodeError):
            return []

    def get_prep_value(self, value):
        if value is None:
            return "[]"
        return json.dumps(value) if not isinstance(value, str) else value
