def test_app_creation(app):
    assert app is not None
    assert app.config['TESTING'] is True
