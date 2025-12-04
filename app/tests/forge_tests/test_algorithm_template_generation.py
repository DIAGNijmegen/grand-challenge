from pathlib import Path
from uuid import uuid4

import pytest

from grandchallenge.components.models import INTERFACE_KIND_JSON_EXAMPLES
from grandchallenge.forge.forge import generate_algorithm_template
from grandchallenge.forge.models import ForgeAlgorithm
from tests.forge_tests.utils import (
    _test_script_run,
    algorithm_template_context_factory,
    zipfile_to_filesystem,
)


def test_for_algorithm_template_content(tmp_path):
    testrun_zpath = Path(str(uuid4()))

    with zipfile_to_filesystem(
        output_path=tmp_path, preserve_permissions=False
    ) as zip_file:
        generate_algorithm_template(
            algorithm=ForgeAlgorithm(**algorithm_template_context_factory()),
            output_zip_file=zip_file,
            target_zpath=testrun_zpath,
        )

    template_path = tmp_path / testrun_zpath

    for filename in [
        "Dockerfile",
        "README.md",
        "inference.py",
        "requirements.txt",
        "do_build.sh",
        "do_save.sh",
        "do_test_run.sh",
        "test/input/interf0",
        "test/input/interf1",
    ]:
        assert (template_path / filename).exists()


@pytest.mark.parametrize(
    "example_value",
    INTERFACE_KIND_JSON_EXAMPLES.values(),
)
def test_algorithm_template_example_value_rendering(example_value, tmp_path):
    testrun_zpath = Path(str(uuid4()))

    context = algorithm_template_context_factory(
        algorithm_interfaces=[
            {
                "inputs": [
                    {
                        "slug": "input-socket-slug",
                        "relative_path": "input-value.json",
                        "example_value": example_value.value,
                        "is_file_kind": True,
                        "is_json_kind": True,
                    },
                ],
                "outputs": [
                    {
                        "slug": "output-socket-slug",
                        "relative_path": "output-value.json",
                        "example_value": example_value.value,
                        "is_file_kind": True,
                        "is_json_kind": True,
                    },
                ],
            }
        ],
    )

    # Black post-processing already tests that example values with escaped characters can
    # correctly be parsed by a Python interpreter
    with zipfile_to_filesystem(
        output_path=tmp_path, preserve_permissions=False
    ) as zip_file:
        generate_algorithm_template(
            algorithm=ForgeAlgorithm(**context),
            output_zip_file=zip_file,
            target_zpath=testrun_zpath,
        )


@pytest.mark.forge_integration
def test_algorithm_template_run(tmp_path):
    testrun_zpath = Path(str(uuid4()))
    algorithm_template_context = algorithm_template_context_factory()

    with zipfile_to_filesystem(output_path=tmp_path) as zip_file:
        generate_algorithm_template(
            algorithm=ForgeAlgorithm(**algorithm_template_context),
            output_zip_file=zip_file,
            target_zpath=testrun_zpath,
        )

    template_path = tmp_path / testrun_zpath

    _test_script_run(
        script_path=template_path / "do_test_run.sh",
    )
