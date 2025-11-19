import uuid
from pathlib import Path

import pytest


@pytest.fixture
def testrun_zpath():
    return Path(str(uuid.uuid4()))
