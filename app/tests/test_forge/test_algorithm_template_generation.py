from grand_challenge_forge.forge import generate_algorithm_template
from grand_challenge_forge.generation_utils import zipfile_to_filesystem
from tests.utils import _test_script_run, algorithm_template_context_factory


def test_for_algorithm_template_content(tmp_path, testrun_zpath):
    with zipfile_to_filesystem(output_path=tmp_path) as zip_file:
        generate_algorithm_template(
            context=algorithm_template_context_factory(),
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


def test_algorithm_template_run(tmp_path, testrun_zpath):
    algorithm_template_context = algorithm_template_context_factory()
    with zipfile_to_filesystem(output_path=tmp_path) as zip_file:
        generate_algorithm_template(
            context=algorithm_template_context,
            output_zip_file=zip_file,
            target_zpath=testrun_zpath,
        )

    template_path = tmp_path / testrun_zpath

    _test_script_run(
        script_path=template_path / "do_test_run.sh",
    )
