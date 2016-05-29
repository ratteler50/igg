import pytest

from flask import url_for

def test_show(client, db):
    res = client.get(url_for('games.show'))
    assert res.status_code == 200
