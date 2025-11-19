import importlib
import os
from contextlib import contextmanager


def truncate_with_epsilons(value, max_length=32, epsilon="..."):
    if len(str(value)) > max_length:
        truncated_value = str(value)[: max_length - len(epsilon)] + epsilon
    else:
        truncated_value = str(value)
    return truncated_value


@contextmanager
def change_directory(new_path):
    # Save the current working directory
    current_path = os.getcwd()

    try:
        # Change the working directory
        os.chdir(new_path)
        yield
    finally:
        # Change back to the original working directory
        os.chdir(current_path)


def directly_import_module(name, path):
    """Returns the named Python module loaded from the path"""
    assert path.exists()
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module
