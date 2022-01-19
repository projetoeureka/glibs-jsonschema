import pytest

from glibs.jsonschema import validate, SchemaValidationError

import _schemas


def test_validation_error_on_instance():
    with pytest.raises(SchemaValidationError) as exc_info1:
        validate({}, _schemas.EXPECTED_SCHEMA)

    assert exc_info1.value.errors == {"<instance>": "{} is not of type 'array'"}

    with pytest.raises(SchemaValidationError) as exc_info2:
        validate([{}], _schemas.REQUIRED_ARRAY_SCHEMA)

    assert exc_info2.value.errors == {
        "0.property_one": "'property_one' is a required property"
    }


def test_required_properties():
    with pytest.raises(SchemaValidationError) as exc_info:
        validate({}, _schemas.REQUIRED_SCHEMA)

    assert exc_info.value.errors == {
        "property_one": "'property_one' is a required property",
        "property_two": "'property_two' is a required property",
    }


def test_compound_required_properties():
    with pytest.raises(SchemaValidationError) as exc_info:
        validate({"property_one": "something"}, _schemas.COMPOUND_REQUIRED_SCHEMA)

    assert exc_info.value.errors == {
        "property_three": "'property_three' is a required property",
        "property_two": "'property_two' is a required property",
    }


def test_error_with_additional_properties():
    with pytest.raises(SchemaValidationError) as exc_info:
        validate(
            {"property_one": "one", "property_two": "exams", "property_three": "three"},
            _schemas.REQUIRED_SCHEMA,
        )

    assert exc_info.value.errors == {"property_three": "Unrecognized property"}


def test_success():
    assert validate(["a"], _schemas.EXPECTED_SCHEMA) is None


def test_success_with_compound_schema():
    assert (
        validate(
            {"property_one": "something", "property_two": "another thing"},
            _schemas.COMPOUND_REQUIRED_SCHEMA,
        )
        is None
    )


def test_success_with_polymorphic_schemas():
    assert (
        validate(
            {
                "items": [
                    {
                        "type": "banana",
                        "weight": 1.2,
                        "ripe": True,
                    },
                    {
                        "type": "monkey",
                        "weight": 5.5,
                        "age": 13,
                    },
                ]
            },
            _schemas.POLYMORPHIC_SCHEMA,
        )
        is None
    )


def test_error_with_polymorphic_schema():
    with pytest.raises(SchemaValidationError) as exc_info1:
        validate(
            {
                "items": [
                    {
                        "type": "banana",
                        "weight": 1.2,
                        "ripe": True,
                    },
                    {
                        "type": "monkey",
                        "weight": 5.5,
                        "age": 13,
                        "dead": False,
                    },
                ]
            },
            _schemas.POLYMORPHIC_SCHEMA,
        )

    assert exc_info1.value.errors == {
        "items[1].age": "Unrecognized property",
        "items[1].dead": "Unrecognized property",
        "items[1].ripe": "'ripe' is a required property",
        "items[1].type": "'monkey' is not one of ['banana']",
    }

    with pytest.raises(SchemaValidationError) as exc_info2:
        validate(
            {
                "items": [
                    {
                        "type": "banana",
                        "weight": 1.2,
                        "ripe": True,
                    },
                    {
                        "type": "monkeyy",
                        "weight": 5.5,
                        "age": 13,
                    },
                ]
            },
            _schemas.POLYMORPHIC_SCHEMA,
        )

    assert exc_info2.value.errors == {
        "items[1].age": "Unrecognized property",
        "items[1].ripe": "'ripe' is a required property",
        "items[1].type": "'monkeyy' is not one of ['monkey']",
    }

    with pytest.raises(SchemaValidationError) as exc_info3:
        validate(
            {
                "items": [
                    {
                        "type": "banana",
                        "weight": 1.2,
                        "ripe": True,
                    },
                    {
                        "type": "monkey",
                        "weight": 5.5,
                    },
                ]
            },
            _schemas.POLYMORPHIC_SCHEMA,
        )

    assert exc_info3.value.errors == {
        "items[1].age": "'age' is a required property",
        "items[1].ripe": "'ripe' is a required property",
        "items[1].type": "'monkey' is not one of ['banana']",
    }


# class TestFlaskSchemaValidation(_BaseSchemaValidationTest):

#     def setUp(self):
#         self.app = flask.Flask(__name__)

#         @self.app.route("/test", methods=["POST"])
#         @schema_validation.flask_validation(EXPECTED_SCHEMA)
#         def route():
#             return "ok"

#         @self.app.route("/test2", methods=["POST"])
#         @schema_validation.flask_validation(REQUIRED_SCHEMA)
#         def route2():
#             return "ok"

#         @self.app.route("/test3", methods=["POST"])
#         @schema_validation.flask_validation(ADDITIONAL_PROPERTIES_SCHEMA)
#         def route3():
#             return "ok"

#         @self.app.route("/test4", methods=["POST"])
#         @schema_validation.flask_validation(COMPOUND_REQUIRED_SCHEMA)
#         def route4():
#             return "ok"

#         @self.app.route("/test5", methods=["POST"])
#         @schema_validation.flask_validation(POLYMORPHIC_SCHEMA)
#         def route5():
#             return "ok"

#     def post(self, url, data, expect_errors, **kwargs):
#         with self.app.test_client() as test_client:
#             return test_client.post(url, data=data, **kwargs)
