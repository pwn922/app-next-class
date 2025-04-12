class OAuth2FlowError(Exception):
    """Custom exception for OAuth flow-related issues."""
    def __init__(self, message, error_code="OAUTH_FLOW_ERROR"):
        super().__init__(message)
        self.error_code = error_code


class OAuth2ExternalServiceError(Exception):
    def __init__(self, message, error_code=None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
