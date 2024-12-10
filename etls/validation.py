# etls/validation.py
# Validate data in JSON file before loading it to MongoDB
def validate_json_data(data, required_fields):
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")
    return True