import logging
from pathlib import Path
from datetime import date
import sys

class LoggerLHC:
    """
    Logger class to handle logs for Laplace apps.
    Automatically saves logs in `log/yyyy-mm-dd/` folder.
    """

    def __init__(self, app_name: str, log_root: Path | str | None = None, mode: str = "info"):
        """
        Args:
            app_name: Name of the app (used in the log file name)
            log_root: Root folder for logs, default = current working directory
            mode: "info" (default) or "debug" (logs everything)
        """
        self.app_name = app_name
        self.mode = mode
        self.log_root = Path(log_root or Path.cwd()) / "log"
        self.date_folder = self.log_root / date.today().isoformat()
        self.date_folder.mkdir(parents=True, exist_ok=True)

        self.log_file = self.date_folder / f"{app_name}.log"
        self.logger = logging.getLogger(app_name)
        self.logger.setLevel(logging.DEBUG if mode == "debug" else logging.INFO)

        self._setup_handlers()
        if mode == "debug":
            self._capture_prints()

    def _setup_handlers(self):
        # Formatter
        fmt = logging.Formatter(
            "%(asctime)s %(levelname)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # File handler (append mode)
        file_handler = logging.FileHandler(self.log_file, mode='a', encoding='utf-8')
        file_handler.setFormatter(fmt)
        self.logger.addHandler(file_handler)

        # Console handler
        if not any(isinstance(h, logging.StreamHandler) for h in self.logger.handlers):
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(fmt)
            self.logger.addHandler(console_handler)

    def _capture_prints(self):
        """Redirects print statements to the logger"""
        class PrintLogger:
            def __init__(self, logger, level=logging.INFO):
                self.logger = logger
                self.level = level

            def write(self, message):
                message = message.strip()
                if message:
                    self.logger.log(self.level, message)

            def flush(self):
                pass

        sys.stdout = PrintLogger(self.logger, level=logging.INFO)
        sys.stderr = PrintLogger(self.logger, level=logging.ERROR)

    def info(self, msg: str):
        self.logger.info(msg)

    def debug(self, msg: str):
        self.logger.debug(msg)

    def warning(self, msg: str):
        self.logger.warning(msg)

    def error(self, msg: str):
        self.logger.error(msg)
