from app.parser import extract_json_from_response


def test_extract_json_from_response_json_block():
    # Arrange
    text = (
        '```json\n{"brand": "Ford", "model": "Fiesta", "min_year": 2015}'
        '\n```'
    )
    # Act
    data = extract_json_from_response(text)
    # Assert
    assert data['brand'] == 'Ford'
    assert data['model'] == 'Fiesta'
    assert data['min_year'] == 2015


def test_extract_json_from_response_code_block():
    # Arrange
    text = (
        '```\n{"brand": "VW", "model": "Golf", "min_year": 2018}\n```'
    )
    # Act
    data = extract_json_from_response(text)
    # Assert
    assert data['brand'] == 'VW'
    assert data['model'] == 'Golf'
    assert data['min_year'] == 2018


def test_extract_json_from_response_plain_json():
    # Arrange
    text = '{"brand": "Toyota", "model": "Corolla"}'
    # Act
    data = extract_json_from_response(text)
    # Assert
    assert data['brand'] == 'Toyota'
    assert data['model'] == 'Corolla'


def test_extract_json_from_response_empty():
    # Act & Assert
    assert extract_json_from_response('') == {}


def test_extract_json_from_response_invalid_json():
    # Arrange
    text = '```json\n{"brand": Ford}\n```'
    # Act
    data = extract_json_from_response(text)
    # Assert
    assert data == {}
