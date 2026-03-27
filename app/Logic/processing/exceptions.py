# -------------------------------------------------------------------------------
# Exceptions
# Joseph Egan
# 2026-03-17
# Sources: none
# -------------------------------------------------------------------------------
# Description: compilation of custom exceptions for render_runner

# Local imports

# python imports

class RootPathError(Exception):
    """Raised when project root path 'render_runner' is not found"""


class RangeError(Exception):
    '''
    Custom exception class for handling range validation errors in input
    functions. Used when input values fall outside specified bounds or when
    bound configurations are invalid.
    '''


class DatabaseConnectionError(Exception):
    '''
    Raised when database connection does not match database connection type.
    '''


class JobRunnerError(Exception):
    """Base exception for the render pipeline."""


class WorkflowLoadError(JobRunnerError):
    """Raised when a workflow file cannot be loaded."""


class WorkflowInjectionError(JobRunnerError):
    """Raised when prompt injection fails."""


class ComfyUIRequestError(JobRunnerError):
    """Raised when a ComfyUI API request fails."""


class JobTimeoutError(JobRunnerError):
    """Raised when a ComfyUI job times out."""


class OutputResolutionError(JobRunnerError):
    """Raised when output files cannot be resolved."""


class UploadError(JobRunnerError):
    """Raised when upload or remote verification fails."""