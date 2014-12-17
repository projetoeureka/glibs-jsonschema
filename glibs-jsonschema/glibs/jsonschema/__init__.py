import jsonschema
import functools


class SchemaValidationError(Exception):

    def __init__(self, errors):
        super(SchemaValidationError, self).__init__("Error validating the schema")
        self.errors = errors


def validate_schema(json, schema):
    errors = {}
    validator = jsonschema.Draft4Validator(schema)

    for error in sorted(validator.iter_errors(json), key=str):
        if error.path:
            errors[error.path[0]] = error.message
        else:
            errors["root"] = "{}{};".format(errors.get("root", ""), error.message)

    if errors:
        raise SchemaValidationError(errors)


def schema(schema, json_provider):
    def decorator(f):
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            validate_schema(json_provider(), schema)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
