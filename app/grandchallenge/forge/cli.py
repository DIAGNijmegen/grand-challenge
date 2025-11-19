import json
import logging
import shutil
from importlib import metadata
from pathlib import Path

import click

from grand_challenge_forge import logger
from grand_challenge_forge.exceptions import ChallengeForgeError
from grand_challenge_forge.forge import (
    generate_algorithm_template,
    generate_challenge_pack,
)
from grand_challenge_forge.generation_utils import zipfile_to_filesystem
from grand_challenge_forge.utils import truncate_with_epsilons


# Shared options decorator
def common_options(func):
    """Decorator to add common options to multiple commands."""
    func = click.option(
        "-o",
        "--output",
        type=click.Path(
            exists=False,
            file_okay=False,
            dir_okay=True,
            readable=True,
            writable=True,
            resolve_path=True,
        ),
        default="dist/",
        show_default=True,
    )(func)
    func = click.option(
        "-f",
        "--force",
        is_flag=True,
        default=False,
    )(func)
    func = click.argument(
        "contexts",
        nargs=-1,
    )(func)
    func = click.option(
        "-v",
        "--verbose",
        count=True,
        help="Sets verbosity level. Stacks (e.g. -vv = debug)",
    )(func)
    return func


@click.group()
@click.version_option(metadata.version("grand-challenge-forge"), "--version")
def cli():
    """Main CLI entry point."""
    pass


@cli.command()
@common_options
def pack(output, force, contexts, verbose=0):
    """
    Generates a challenge pack using provided context.

    A context can be a filename or a JSON string.

    Multiple contexts can be provided. Each will be processed independently.
    """
    output_dir = Path(output)

    _set_verbosity(verbosity=verbose)

    for index, context in enumerate(contexts):
        resolved_context = _resolve_context(src=context)
        if resolved_context:
            try:
                logger.info(
                    f"🏗️Started working on pack [{index + 1} of {len(contexts)}]"
                )
                with zipfile_to_filesystem(output_path=output_dir) as zip_file:
                    pack_zpath = Path(
                        f"{resolved_context['challenge']['slug']}-challenge-pack"
                    )
                    generate_challenge_pack(
                        target_zpath=pack_zpath,
                        context=resolved_context,
                        output_zip_file=zip_file,
                    )
                    pack_dir = output_dir / pack_zpath

                    if pack_dir.exists():
                        if force:
                            shutil.rmtree(pack_dir)
                        else:
                            raise ChallengeForgeError(
                                f"Pack {pack_dir.stem!r} already exists!"
                            )

                logger.info(f"📦 Created Pack {pack_dir.stem!r}")
                logger.info(f"📢 Pack is here: {pack_dir}")
                print(str(pack_dir))
            except Exception as e:
                if isinstance(e, ChallengeForgeError):
                    logger.error(f"💔 {e}", exc_info=True)
                else:
                    raise e


@cli.command()
@common_options
def algorithm(output, force, contexts, verbose):
    """
    Generates an algorithm template using provided context.

    A context can be a filename or a JSON string.

    Multiple contexts can be provided. Each will be processed independently.
    """

    output_dir = Path(output)

    _set_verbosity(verbosity=verbose)

    for index, context in enumerate(contexts):
        resolved_context = _resolve_context(src=context)
        if resolved_context:
            try:
                logger.info(
                    f"🏗️Started working on Algorithm Template [{index + 1} "
                    f"of {len(contexts)}]"
                )

                with zipfile_to_filesystem(output_path=output_dir) as zip_file:
                    template_zpath = Path(
                        f"{resolved_context['algorithm']['slug']}-template"
                    )
                    generate_algorithm_template(
                        target_zpath=template_zpath,
                        context=resolved_context,
                        output_zip_file=zip_file,
                    )
                    template_dir = output_dir / template_zpath

                    if template_dir.exists():
                        if force:
                            shutil.rmtree(template_dir)
                        else:
                            raise ChallengeForgeError(
                                f"Algorithm Template {template_dir.stem!r} "
                                "already exists!"
                            )
                logger.info(
                    f"📦 Created Algorithm Template {template_dir.stem!r}"
                )
                logger.info(f"📢 Algorithm Template is here: {template_dir}")
                print(str(template_dir))
            except Exception as e:
                if isinstance(e, ChallengeForgeError):
                    logger.error(f"💔 {e}")
                else:
                    raise


def _set_verbosity(verbosity):
    ch = logging.StreamHandler()

    if verbosity == 0:
        logger.setLevel(logging.WARNING)
        ch.setLevel(logging.WARNING)
    elif verbosity == 1:
        logger.setLevel(logging.INFO)
        ch.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.DEBUG)
        ch.setLevel(logging.DEBUG)


def _resolve_context(src):
    try:
        if (p := Path(src)).exists() and p.is_file():
            return _read_json_file(p)
        return json.loads(src)
    except json.decoder.JSONDecodeError as e:
        logger.error(
            f"Could not resolve context source:\n"
            f"'{truncate_with_epsilons(src)!r}' {e}"
        )


def _read_json_file(json_file):
    with open(json_file, "r") as f:
        context = json.load(f)
    return context
