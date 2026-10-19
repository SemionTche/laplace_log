'''
Uncaught exception handling for the LAPLACE-LHC project.

This module defines a custom exception hook that:
- logs uncaught exceptions
- records the full exception traceback
- replaces the default sys.excepthook

Typical usage:
    from laplace_log import uncaught_exception

This import will catch silent errors like in PyQt
and record it in the log instance. 
'''
# libraries
import sys
import traceback
from types import TracebackType

from laplace_log import log


def log_uncaught_exceptions(exctype : type[BaseException], 
                            value: BaseException, 
                            tb: TracebackType | None) -> None:
    '''
    Log uncaught exceptions and their traceback.

    This function is intended to be assigned to `sys.excepthook`
    to log uncaught exceptions that would otherwise be printed to
    standard error.

    Args:
        exctype (type[BaseException]): 
            The class of the uncaught exception.

        value (BaseException): 
            The uncaught exception instance.
        
        tb (TracebackType | None): 
            The traceback object, or None if unavailable.

    Returns:
        None.
    '''
    log.error("Uncaught exception occurred")
    log.error("".join(traceback.format_exception(exctype, value, tb)))


sys.excepthook = log_uncaught_exceptions