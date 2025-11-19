import logging

import jsonschema

from grand_challenge_forge.exceptions import InvalidContextError
from grand_challenge_forge.utils import truncate_with_epsilons

logger = logging.getLogger(__name__)

ARCHIVE_SCHEMA = {
    "type": "object",
    "properties": {
        "slug": {"type": "string"},
        "url": {"type": "string"},
    },
    "required": ["slug", "url"],
}

SOCKET_SCHEMA = {
    "type": "object",
    "properties": {
        "slug": {"type": "string"},
        "relative_path": {"type": "string"},
        "kind": {"type": "string"},
        "super_kind": {"type": "string"},
    },
    "required": [
        "slug",
        "relative_path",
        "kind",
        "super_kind",
    ],
}


INTERFACE_SCHEMA = {
    "type": "object",
    "properties": {
        "inputs": {"type": "array", "items": SOCKET_SCHEMA},
        "outputs": {"type": "array", "items": SOCKET_SCHEMA},
    },
    "required": [
        "inputs",
        "outputs",
    ],
}


PACK_CONTEXT_SCHEMA = {
    "type": "object",
    "properties": {
        "challenge": {
            "type": "object",
            "properties": {
                "slug": {"type": "string"},
                "url": {"type": "string"},
                "archives": {"type": "array", "items": ARCHIVE_SCHEMA},
                "phases": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "slug": {"type": "string"},
                            "archive": ARCHIVE_SCHEMA,
                            "algorithm_interfaces": {
                                "type": "array",
                                "items": INTERFACE_SCHEMA,
                            },
                            "evaluation_additional_inputs": {
                                "type": "array",
                                "items": SOCKET_SCHEMA,
                            },
                            "evaluation_additional_outputs": {
                                "type": "array",
                                "items": SOCKET_SCHEMA,
                            },
                        },
                        "required": [
                            "slug",
                            "archive",
                            "algorithm_interfaces",
                            "evaluation_additional_inputs",
                            "evaluation_additional_outputs",
                        ],
                        "additionalProperties": True,  # Allow additional properties
                    },
                },
            },
            "required": ["slug", "url", "phases", "archives"],
        },
    },
    "required": ["challenge"],
    "additionalProperties": True,  # Allow additional properties
}


def validate_pack_context(context):
    try:
        jsonschema.validate(instance=context, schema=PACK_CONTEXT_SCHEMA)
        logging.debug("Context valid")
    except jsonschema.exceptions.ValidationError as e:
        raise InvalidContextError(
            f"Invalid pack context provided:\n'{truncate_with_epsilons(context)!r}'"
        ) from e


ALGORITHM_TEMPLATE_CONTEXT_SCHEMA = {
    "type": "object",
    "properties": {
        "algorithm": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "slug": {"type": "string"},
                "url": {"type": "string"},
                "algorithm_interfaces": {
                    "type": "array",
                    "items": INTERFACE_SCHEMA,
                },
            },
            "required": ["title", "url", "slug", "algorithm_interfaces"],
        },
    },
    "required": ["algorithm"],
    "additionalProperties": True,  # Allow additional properties
}


def validate_algorithm_template_context(context):
    try:
        jsonschema.validate(
            instance=context, schema=ALGORITHM_TEMPLATE_CONTEXT_SCHEMA
        )
        logging.debug("Context valid")
    except jsonschema.exceptions.ValidationError as e:
        raise InvalidContextError(
            "Invalid algorithm template context provided:\n"
            f"'{truncate_with_epsilons(context)!r}'"
        ) from e
