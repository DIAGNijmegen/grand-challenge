import os
import subprocess
from collections import Counter
from contextlib import contextmanager
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

from grand_challenge_forge import RESOURCES_PATH

TEST_RESOURCES = (
    Path(os.path.dirname(os.path.realpath(__file__))) / "resources"
)
DEFAULT_PACK_CONTEXT_STUB = {
    "challenge": {
        "slug": "challenge-slug",
        "url": "https://challenge-slug.grand-challenge.org/",
        "archives": [
            {
                "slug": "archive-slug",
                "url": "https://grand-challenge.org/archives/archive-slug/",
            },
            {
                "slug": "another-archive-slug",
                "url": "https://grand-challenge.org/archives/another-archive-slug/",
            },
            {
                "slug": "yet-another-archive-slug",
                "url": "https://grand-challenge.org/archives/yet-another-archive-slug/",
            },
        ],
        "phases": [
            {
                "slug": "phase-slug",
                "archive": {
                    "slug": "archive-slug",
                    "url": "https://grand-challenge.org/archives/archive-slug/",
                },
                "algorithm_interfaces": [
                    {
                        "inputs": [
                            {
                                "slug": "input-socket-slug",
                                "kind": "Segmentation",
                                "super_kind": "Image",
                                "relative_path": "images/input-value",
                                "example_value": None,
                            },
                            {
                                "slug": "another-input-socket-slug",
                                "kind": "Anything",
                                "super_kind": "File",
                                "relative_path": "another-input-value.json",
                                "example_value": {"key": "value"},
                            },
                            {
                                "slug": "yet-another-input-socket-slug",
                                "kind": "Anything",
                                "super_kind": "Value",
                                "relative_path": "yet-another-input-value.json",
                                "example_value": {"key": "value"},
                            },
                            {
                                "slug": "yet-another-non-json-input-socket-slug",
                                "kind": "Anything",
                                "super_kind": "File",
                                "relative_path": "yet-another-non-json-input-value",
                                "example_value": None,
                            },
                        ],
                        "outputs": [
                            {
                                "slug": "output-socket-slug",
                                "kind": "Image",
                                "super_kind": "Image",
                                "relative_path": "images/output-value",
                                "example_value": None,
                            },
                            {
                                "slug": "another-output-socket-slug",
                                "kind": "Anything",
                                "super_kind": "File",
                                "relative_path": "output-value.json",
                                "example_value": {"key": "value"},
                            },
                            {
                                "slug": "yet-another-output-socket-slug",
                                "kind": "Anything",
                                "super_kind": "Value",
                                "relative_path": "yet-another-output-value.json",
                                "example_value": {"key": "value"},
                            },
                            {
                                "slug": "yet-another-non-json-output-socket-slug",
                                "kind": "Anything",
                                "super_kind": "File",
                                "relative_path": "yet-another-non-json-output-value",
                                "example_value": None,
                            },
                        ],
                    },
                    {
                        "inputs": [
                            {
                                "slug": "input-socket-slug-interface-2",
                                "kind": "Segmentation",
                                "super_kind": "Image",
                                "relative_path": "images/input-value",
                                "example_value": None,
                            }
                        ],
                        "outputs": [
                            {
                                "slug": "output-socket-slug-interface-2",
                                "kind": "Image",
                                "super_kind": "Image",
                                "relative_path": "images/output-value",
                                "example_value": None,
                            }
                        ],
                    },
                ],
                "evaluation_additional_inputs": [
                    {
                        "slug": "additional-input-socket-slug",
                        "kind": "Segmentation",
                        "super_kind": "Image",
                        "relative_path": "images/input-value",
                        "example_value": None,
                    },
                    {
                        "slug": "additional-another-input-socket-slug",
                        "kind": "Anything",
                        "super_kind": "File",
                        "relative_path": "another-input-value.json",
                        "example_value": {"key": "value"},
                    },
                    {
                        "slug": "additional-yet-another-input-socket-slug",
                        "kind": "Anything",
                        "super_kind": "Value",
                        "relative_path": "yet-another-input-value.json",
                        "example_value": {"key": "value"},
                    },
                    {
                        "slug": "additional-yet-another-non-json-input-socket-slug",
                        "kind": "Anything",
                        "super_kind": "File",
                        "relative_path": "yet-another-non-json-input-value",
                        "example_value": None,
                    },
                ],
                "evaluation_additional_outputs": [
                    {
                        "slug": "additional-output-socket-slug",
                        "kind": "Image",
                        "super_kind": "Image",
                        "relative_path": "images/output-value",
                        "example_value": None,
                    },
                    {
                        "slug": "additional-another-output-socket-slug",
                        "kind": "Anything",
                        "super_kind": "File",
                        "relative_path": "output-value.json",
                        "example_value": {"key": "value"},
                    },
                    {
                        "slug": "additional-yet-another-output-socket-slug",
                        "kind": "Anything",
                        "super_kind": "Value",
                        "relative_path": "yet-another-output-value.json",
                        "example_value": {"key": "value"},
                    },
                    {
                        "slug": "additional-yet-another-non-json-output-socket-slug",
                        "kind": "Anything",
                        "super_kind": "File",
                        "relative_path": "yet-another-non-json-output-value",
                        "example_value": None,
                    },
                ],
            },
            {
                "slug": "another-phase-slug",
                "archive": {
                    "slug": "another-archive-slug",
                    "url": "https://grand-challenge.org/archives/another-archive-slug/",
                },
                "algorithm_interfaces": [
                    {
                        "inputs": [
                            {
                                "slug": "input-socket-slug-interface-2",
                                "kind": "Segmentation",
                                "super_kind": "Image",
                                "relative_path": "images/input-value",
                                "example_value": None,
                            }
                        ],
                        "outputs": [
                            {
                                "slug": "output-socket-slug-interface-2",
                                "kind": "Image",
                                "super_kind": "Image",
                                "relative_path": "images/output-value",
                                "example_value": None,
                            }
                        ],
                    },
                ],
                "evaluation_additional_inputs": [],
                "evaluation_additional_outputs": [],
            },
        ],
    }
}


DEFAULT_ALGORITHM_CONTEXT_STUB = {
    "algorithm": {
        "title": "An algorithm",
        "slug": "an-algorithm",
        "url": "https://grand-challenge.org/algorithms/an-algorithm/",
        "algorithm_interfaces": [
            {
                "inputs": [
                    {
                        "slug": "input-socket-slug",
                        "kind": "Segmentation",
                        "super_kind": "Image",
                        "relative_path": "images/input-value",
                        "example_value": None,
                    },
                    {
                        "slug": "another-input-socket-slug",
                        "kind": "Anything",
                        "super_kind": "File",
                        "relative_path": "another-input-value.json",
                        "example_value": {"key": "value"},
                    },
                    {
                        "slug": "yet-another-input-socket-slug",
                        "kind": "Anything",
                        "super_kind": "Value",
                        "relative_path": "yet-another-input-value.json",
                        "example_value": {"key": "value"},
                    },
                    {
                        "slug": "yet-another-non-json-input-socket-slug",
                        "kind": "Anything",
                        "super_kind": "File",
                        "relative_path": "yet-another-non-json-input-value",
                        "example_value": None,
                    },
                ],
                "outputs": [
                    {
                        "slug": "output-socket-slug",
                        "kind": "Image",
                        "super_kind": "Image",
                        "relative_path": "images/output-value",
                        "example_value": None,
                    },
                    {
                        "slug": "another-output-socket-slug",
                        "kind": "Anything",
                        "super_kind": "File",
                        "relative_path": "output-value.json",
                        "example_value": {"key": "value"},
                    },
                    {
                        "slug": "yet-another-output-socket-slug",
                        "kind": "Anything",
                        "super_kind": "Value",
                        "relative_path": "yet-another-output-value.json",
                        "example_value": {"key": "value"},
                    },
                    {
                        "slug": "yet-another-non-json-output-socket-slug",
                        "kind": "Anything",
                        "super_kind": "File",
                        "relative_path": "yet-another-non-json-output-value",
                        "example_value": "A string that needs to be escaped",
                    },
                ],
            },
            {
                "inputs": [
                    {
                        "slug": "input-socket-slug-interface-2",
                        "kind": "Segmentation",
                        "super_kind": "Image",
                        "relative_path": "images/input-value",
                        "example_value": None,
                    }
                ],
                "outputs": [
                    {
                        "slug": "output-socket-slug-interface-2",
                        "kind": "Image",
                        "super_kind": "Image",
                        "relative_path": "images/output-value",
                        "example_value": None,
                    }
                ],
            },
        ],
    }
}

unique_slugs_suffix = Counter()


def make_slugs_unique(d):
    """Ensure all slugs in the structure to make them unique"""
    global unique_slugs_suffix

    if isinstance(d, dict):
        if "slug" in d:
            original_slug = d["slug"]
            suffix = unique_slugs_suffix[original_slug]
            d["slug"] = f"{original_slug}-{suffix}"
            unique_slugs_suffix.update([original_slug])
        for item in d.values():
            make_slugs_unique(item)
    elif isinstance(d, list):
        for item in d:
            make_slugs_unique(item)
    return d


def add_numerical_slugs(d):
    """Add '00-' prefix to all slugs in the structure."""
    if isinstance(d, dict):
        if "slug" in d and not d["slug"].startswith("00-"):
            d["slug"] = f"00-{d['slug']}"
        for item in d.values():
            add_numerical_slugs(item)
    elif isinstance(d, list):
        for item in d:
            add_numerical_slugs(item)
    return d


def pack_context_factory(**kwargs):
    result = deepcopy(DEFAULT_PACK_CONTEXT_STUB)
    result["challenge"].update(kwargs)

    make_slugs_unique(result)

    result["challenge"]["phases"] = [
        phase_context_factory(**phase)["phase"]
        for phase in result["challenge"]["phases"]
    ]
    return result


def phase_context_factory(**kwargs):
    result = deepcopy(
        # use first phase as default
        DEFAULT_PACK_CONTEXT_STUB["challenge"]["phases"][0]
    )
    result.update(kwargs)
    return make_slugs_unique({"phase": result})


def algorithm_template_context_factory(**kwargs):
    result = deepcopy(DEFAULT_ALGORITHM_CONTEXT_STUB)
    result["algorithm"].update(kwargs)
    return make_slugs_unique(result)


def _test_script_run(
    *,
    script_path,
    extra_arg=None,
):
    """Test a subprocess execution.

    Args
    ----
        script_path: The path to the script to execute
        extra_arg: Optional additional argument to pass to the script

    """
    command = [script_path]
    if extra_arg:
        command.append(extra_arg)

    result = subprocess.run(command, capture_output=True)
    if result.stderr or result.returncode != 0:  # Stderr should not be empty
        raise subprocess.CalledProcessError(
            returncode=result.returncode,
            cmd=command,
            stderr=result.stderr,
            output=result.stdout,
        )


@contextmanager
def mocked_binaries():
    """Mock the binaries in the PATH to avoid computationally intensive operations during testing."""
    mocks_bin = RESOURCES_PATH / "mocks" / "bin"
    current_path = os.environ.get("PATH", "")
    extended_path = f"{mocks_bin}:{current_path}"

    with patch.dict("os.environ", PATH=extended_path):
        yield
