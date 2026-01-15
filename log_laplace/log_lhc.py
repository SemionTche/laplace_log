import logging
from pathlib import Path
from datetime import date
import sys

_logger_instance = None  # singleton instance

def _log_func(msg, level="info"):
    """Global log function."""
    global _logger_instance
    if _logger_instance is None:
        raise RuntimeError("Logger not initialized! Call LoggerLHC(app_name, ...) first.")
    
    level = level.lower()
    if level == "debug":
        _logger_instance.debug(msg)
    elif level == "warning":
        _logger_instance.warning(msg)
    elif level == "error":
        _logger_instance.error(msg)
    else:
        _logger_instance.info(msg)


class _LogHelper:
    """Object to allow log.info(...), log.debug(...), etc."""
    def info(self, msg):
        _log_func(msg, level="info")
    def debug(self, msg):
        _log_func(msg, level="debug")
    def warning(self, msg):
        _log_func(msg, level="warning")
    def error(self, msg):
        _log_func(msg, level="error")


log = _LogHelper()  # this is what you import in other files


class LoggerLHC:
    """Logger class to handle logs for Laplace apps."""
    
    def __init__(self, app_name: str, log_root: Path | str | None = None, mode: str = "info"):
        global _logger_instance
        if _logger_instance is not None:
            return  # already initialized

        self.app_name = app_name
        self.mode = mode
        self.log_root = Path(log_root or Path.cwd()) / "logs"
        self.date_folder = self.log_root / date.today().isoformat()
        self.date_folder.mkdir(parents=True, exist_ok=True)

        self.log_file = self.date_folder / f"{app_name}.log"
        self.logger = logging.getLogger(app_name)
        self.logger.setLevel(logging.DEBUG if mode == "debug" else logging.INFO)

        self._setup_handlers()
        if mode == "debug":
            self._capture_prints()

        _logger_instance = self

    def _setup_handlers(self):
        fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
        fh = logging.FileHandler(self.log_file, mode='a', encoding='utf-8')
        fh.setFormatter(fmt)
        self.logger.addHandler(fh)

        if not any(isinstance(h, logging.StreamHandler) for h in self.logger.handlers):
            ch = logging.StreamHandler(sys.stdout)
            ch.setFormatter(fmt)
            self.logger.addHandler(ch)

    def _capture_prints(self):
        class StreamToLogger:
            def __init__(self, logger, level=logging.INFO, stream=None):
                self.logger = logger
                self.level = level
                self.stream = stream or sys.stdout
            def write(self, message):
                message = message.rstrip()
                if message:
                    self.logger.log(self.level, message)
                    self.stream.write(message + "\n")
            def flush(self):
                if self.stream:
                    self.stream.flush()
        sys.stdout = StreamToLogger(self.logger, level=logging.INFO)
        sys.stderr = StreamToLogger(self.logger, level=logging.ERROR)

    # shortcut methods
    def info(self, msg): self.logger.info(msg)
    def debug(self, msg): self.logger.debug(msg)
    def warning(self, msg): self.logger.warning(msg)
    def error(self, msg): self.logger.error(msg)
