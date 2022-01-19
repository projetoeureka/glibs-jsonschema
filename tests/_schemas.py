EXPECTED_SCHEMA = {
    "type": "array",
    "uniqueItems": True,
    "items": {"type": "string"},
}

REQUIRED_SCHEMA = {
    "type": "object",
    "properties": {
        "property_one": {
            "type": "string",
        },
        "property_two": {
            "enum": ["exams", "all_items_and_learning_objects"],
        },
    },
    "required": ["property_one", "property_two"],
    "additionalProperties": False,
}

REQUIRED_ARRAY_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": REQUIRED_SCHEMA["properties"],
        "required": ["property_one"],
    },
    "minItems": 1,
}

COMPOUND_REQUIRED_SCHEMA = {
    "type": "object",
    "properties": {
        "property_one": {
            "type": "string",
        },
        "property_two": {
            "type": "string",
        },
        "property_three": {
            "type": "string",
        },
    },
    "required": ["property_one"],
    "oneOf": [
        {"required": ["property_two"]},
        {"required": ["property_three"]},
    ],
}

POLYMORPHIC_SCHEMA = {
    "type": "object",
    "properties": {
        "items": {
            "type": "array",
            "items": {
                "anyOf": [
                    {
                        "type": "object",
                        "properties": {
                            "type": {"type": "string", "enum": ["banana"]},
                            "weight": {"type": "number"},
                            "ripe": {"type": "boolean"},
                        },
                        "additionalProperties": False,
                        "required": ["type", "weight", "ripe"],
                    },
                    {
                        "type": "object",
                        "properties": {
                            "type": {"type": "string", "enum": ["monkey"]},
                            "weight": {"type": "number"},
                            "age": {"type": "number"},
                        },
                        "additionalProperties": False,
                        "required": ["type", "weight", "age"],
                    },
                ],
            },
        },
    },
}

ADDITIONAL_PROPERTIES_SCHEMA = {
    "type": "object",
    "properties": {
        "property_one": {
            "type": "string",
        },
    },
    "additionalProperties": False,
}
