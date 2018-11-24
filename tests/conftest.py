#!/usr/bin/env python3

import os
import pytest
import spacedr


@pytest.fixture(scope='session', autouse=True)
def delete_db_after_test(request):

    spacedr.db.db_init()

    def teardown() -> None:
        db_path = spacedr.db.get_db_path()
        os.remove(db_path)

    request.addfinalizer(teardown)
