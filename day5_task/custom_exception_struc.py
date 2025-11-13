class AppError(Exception):
    """Base class for all application-specific exceptions."""
    pass

class ValidationError(AppError):
    """Raised when input validation fails."""
    pass

class APIError(AppError):
    """Raised when an external API call fails."""
    pass

class ProcessingError(AppError):
    """Raised when data processing fails."""
    pass

def validate_data(data):
    if not isinstance(data, dict):
        raise ValidationError("Invalid data format! Expected a dictionary.")

def call_api():
    success = True
    if not success:
        raise APIError("Failed to fetch data from API.")
    else:
        raise AppError("Unexpected data")

def process_data(data):
    try:
        validate_data(data)
        call_api()
    except ValidationError as e:
        print(f"Validation error: {e}")
    except APIError as e:
        print(f"API error: {e}")
    except AppError as e: 
        print(f"Application error: {e}")

result = process_data({'ramu':123})  