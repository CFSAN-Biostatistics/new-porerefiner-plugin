"""Main module."""

import dataclasses
from pathlib import Path
from typing import Any

from porerefiner.notifiers import Notifier
from porerefiner.jobs import FileJob, RunJob
from porerefiner.jobs.submitters import Submitter
from porerefiner.models import Run, File

@dataclass
class {{cookiecutter.project_slug.replace('_',' ').title().replace(' ','')}}Notifier(Notifier):
    """Configurable run completion notifier. Implement async method 'notify.'"""

    {{cookiecutter.project_slug}}_sample_param: str

    async def notify(self, run: Run, state: Any, message: str) -> None:
        "Handler for notifications. `state` is not currently implemented."
        pass

@dataclass
class {{cookiecutter.project_slug.replace('_',' ').title().replace(' ','')}}Submitter(Submitter):
    """Configurable job runner. Implement the below methods."""

    {{cookiecutter.project_slug}}_sample_param: str

    async def test_noop(self) -> None:
        "No-op method submitters should implement to make sure the submitter can access an external resource."
        pass

    def reroot_path(self, path: Path) -> Path:
        "Submitters should translate paths to be relative to execution environment"
        pass

    async def begin_job(self, execution_string: str, datadir: Path, remotedir: Path, environment_hints: dict = {}) -> str:
        "Semantics of scheduling a job. Jobs can provide execution hints. Return an optional job id"
        pass

    async def poll_job(self, job:str) -> str:
        "Semantics of polling a job."
        pass

@dataclass
class {{cookiecutter.project_slug.replace('_',' ').title().replace(' ','')}}FileJob(FileJob):
    """Configurable job that will be triggered whenever a file enters a completed state."""

    def setup(self, run: Run, file: File, datadir: Path, remotedir: Path) -> Union[str, Tuple[str, dict]]:
        "Set up the job. Return a string for the job submitter, and optionally a dictionary of execution hints."
        pass

    def collect(self, run: Run, file: File, datadir: Path, pid: Union[str, int]) -> None:
        "Post-job processing. Handle cleanup and make changes to the run or its records."
        pass


@dataclass
class {{cookiecutter.project_slug.replace('_',' ').title().replace(' ','')}}RunJob(RunJob):
    """Configurable job that will be triggered whenever a run enters a completed state."""

    def setup(self, run: Run, datadir: Path, remotedir: Path) -> Union[str, Tuple[str, dict]]:
        "Set up the job. Return a string for the job submitter, and optionally a dictionary of execution hints."
        pass

    def collect(self, run: Run, datadir: Path, pid: Union[str, int]) -> None:
        "Post-job processing. Handle cleanup and make changes to the run or its records."
        pass
