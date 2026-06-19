import logging
import subprocess
import sys
from enum import Enum, auto
from pathlib import Path
from queue import Empty, Queue
from threading import Thread
from time import sleep
from typing import IO

from PySide6.QtWidgets import QApplication

from vibra import VIBRA_DIR
from vibra.errors import SolverSubprocessError
from vibra.interface.loading_window import LoadingWindow


class SubProcessStatus(Enum):
    SUCCESS = auto()
    INTERRUPTED = auto()


class SubProcessHandler:
    """Run the configured project analysis in a separate Python process."""

    def __init__(self, path: Path | str, extra_params: str = ""):
        process_script = Path(path).expanduser()

        if not process_script.is_absolute():
            process_script = VIBRA_DIR / process_script

        process_script = process_script.resolve(strict=False)

        if not process_script.exists():
            raise FileNotFoundError(f"Subprocess script path does not exist: {process_script}")

        if not process_script.is_file():
            raise IsADirectoryError(f"Subprocess script path is not a file: {process_script}")

        if process_script.suffix != ".py":
            raise ValueError(f"Subprocess script path must point to a Python file: {process_script}")

        self.process_script = process_script
        self.extra_params = extra_params

    def run(self) -> SubProcessStatus:
        self._subprocess: subprocess.Popen | None = None
        self._interrupted: bool = False
        return LoadingWindow(self._run_subprocess, self._interrupt_subprocess).run()

    def _interrupt_subprocess(self, by_user=True):
        if self._subprocess is None or self._subprocess.poll() is not None:
            return

        self._interrupted = by_user
        self._subprocess.terminate()

        try:
            self._subprocess.wait(timeout=1)
        except subprocess.TimeoutExpired:
            self._subprocess.kill()

    def _run_subprocess(self) -> SubProcessStatus:
        logging.info("Launching subprocess... (15%)")

        try:
            commands = [sys.executable, str(self.process_script)]
            if self.extra_params:
                commands.append(str(self.extra_params))

            self._subprocess = subprocess.Popen(
                commands,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
            )
        except OSError as error:
            raise OSError("Could not launch subprocess.") from error

        if self._subprocess.stdout is None or self._subprocess.stderr is None:
            self._interrupt_subprocess(by_user=False)
            raise OSError("Subprocess stdout or stderr PIPE was not created.")

        stdout_queue = Queue()
        stdout_reader = Thread(
            target=self._read_pipe_lines,
            args=(self._subprocess.stdout, stdout_queue),
            daemon=True,
        )
        stdout_reader.start()

        while self._subprocess.poll() is None:
            self._drain_log_stdout_queue(stdout_queue)
            QApplication.processEvents()
            sleep(0.05)

        stdout_reader.join(1)
        self._drain_log_stdout_queue(stdout_queue)

        if self._subprocess.returncode != 0:
            if self._interrupted:
                logging.info("Subprocess was interrupted.")
                return SubProcessStatus.INTERRUPTED

            stderr = self._subprocess.stderr.read()
            logging.error(f"Subprocess exited with code {self._subprocess.returncode}")
            raise SolverSubprocessError(
                returncode=self._subprocess.returncode,
                stderr=stderr,
            )

        return SubProcessStatus.SUCCESS

    def _read_pipe_lines(self, pipe: IO, line_queue: Queue[str]):
        try:
            for line in pipe:
                line_queue.put(line.rstrip())
        finally:
            pipe.close()

    def _drain_log_stdout_queue(self, line_queue: Queue[str]):
        while True:
            try:
                line = line_queue.get_nowait()
            except Empty:
                break

            if line.startswith("VIBRA_LOG|"):
                _, level, message = line.split("|", 2)
                logging.log(getattr(logging, level, logging.INFO), message)
            else:
                print(line)
