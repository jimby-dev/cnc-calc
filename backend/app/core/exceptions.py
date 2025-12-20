"""
Custom exceptions for the application
"""
from fastapi import HTTPException, status


class ToolNotFoundError(HTTPException):
    """Raised when a tool is not found"""
    
    def __init__(self, tool_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tool with ID '{tool_id}' not found"
        )


class ExportNotFoundError(HTTPException):
    """Raised when an export is not found"""
    
    def __init__(self, export_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Export with ID '{export_id}' not found"
        )


class ValidationHTTPException(HTTPException):
    """Raised when tool validation fails"""
    
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Validation failed: {message}"
        )


class ExportError(HTTPException):
    """Raised when export generation fails"""
    
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Export failed: {message}"
        )

