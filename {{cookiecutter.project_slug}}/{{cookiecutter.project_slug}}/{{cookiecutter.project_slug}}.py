"""Main module."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Union, Tuple

from porerefiner.notifiers import Notifier
from porerefiner.jobs import FileJob, RunJob, SampleSheetJob
from porerefiner.jobs.submitters import Submitter
from porerefiner.models import Run, File, SampleSheet
from porerefiner.samplesheets import SnifferFor, ParserFor
from porerefiner.protocols.porerefiner.rpc.porerefiner_pb2 import SampleSheet

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
class {{cookiecutter.project_slug.replace('_',' ').title().replace(' ','')}}SampleSheetJob(SampleSheetJob):
    """Configurable job that will be triggered whenever a new sample sheet is loaded."""

    command1: str = "touch {samplesheet.path}/started"

    def run(self, samplesheet: SampleSheet) -> Generator[Union[str, Tuple[str, dict]], Union[CompletedProcess, int, str]]:
        """SampleSheet job method. Access individual samples by samplesheet.samples ."""
        yield self.command.format(**locals())

@dataclass
class {{cookiecutter.project_slug.replace('_',' ').title().replace(' ','')}}FileJob(FileJob):
    """Configurable job that will be triggered whenever a file enters an idle state."""

    command1: str = "cp {file} {remotedir}/{file}"
    command2: str = "convert {remotedir}/{file} --fasta >> {remotedir}/{file.name}.converted.fasta"

    def run(self, run: Run, file: File, datadir: Path, remotedir: Path) -> Generator[Union[str, Tuple[str, dict]], Union[CompletedProcess, int, str]]:
        """File job method. Set up the job, then yield a command string or
           a tuple of a command string plus a dictionary of execution hints.
           The job runner will send back the result if it's successful."""
        errcode = yield self.command1.format(**locals())
        if not errcode:
            yield self.command2.format(**locals())


@dataclass
class {{cookiecutter.project_slug.replace('_',' ').title().replace(' ','')}}RunJob(RunJob):
    """Configurable job that will be triggered whenever a run enters a completed state."""

    command: str = "cwltool {self.cwl} --name{run.name} --run {remotedir}"

    def run(self, run: Run, datadir: Path, remotedir: Path) -> Generator[Union[str, Tuple[str, dict]], Union[CompletedProcess, int, str]]:
        """Run job method."""
        yield self.command.format(**locals())

# Tips for writing a sample sheet parser:
# 1) Write a sniffer that's pretty specific; have the docstring be an example of the format in TSV
# 2) Your example can be cut and pasted in from Excel
# 3) Decorate the sniffer with whether it's for CSV or XLS format or both
# 4) Link the parser to the sniffer using the ParserFor decorator and the name of your sniffer

@SnifferFor.csv
def {{cookiecutter.project_slug}}(rows):
    """porerefiner_ver	1.0.1
library_id	
sequencing_kit	
barcode_kit	
sample_id	accession	barcode_id	organism	extraction_kit	comment user
TEST	TEST	TEST	TEST	TEST	TEST	TEST"""
    note, ver, *_ = rows[0]
    return note == 'porerefiner_ver' and ver == '{{cookiecutter.project_slug}}_1.0.1'


@ParserFor.{{cookiecutter.project_slug}}
def {{cookiecutter.project_slug}}_parser(rows):
    "{{cookiecutter.project_slug}} samplesheet parser"
    rows = iter(rows)
    ss = SampleSheet()
    ss.date.GetCurrentTime()
    _, ss.porerefiner_ver, *_ = next(rows)
    _, ss.library_id, *_ = next(rows)
    _, ss.sequencing_kit = next(rows)
    key, value, *rest = next(rows)
    if 'barcode_kit' in key: #if it's not the header
        [ss.barcode_kit.append(barcode) for barcode in [value] + rest]
        next(rows) # skip the header
    for sample_id, accession, barcode_id, organism, extraction_kit, comment, user, *_ in rows:
        ss.samples.add(sample_id=sample_id,
                        accession=accession,
                        barcode_id=barcode_id,
                        organism=organism,
                        extraction_kit=extraction_kit,
                        comment=comment,
                        user=user)
    return ss
