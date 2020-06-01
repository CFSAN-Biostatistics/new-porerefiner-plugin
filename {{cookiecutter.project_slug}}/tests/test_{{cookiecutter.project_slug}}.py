#!/usr/bin/env python

"""Tests for `{{ cookiecutter.project_slug }}` package."""

from asyncio import run

from tests import *
from hypothesis import given
from hypothesis.strategies import *

import unittest

from {{ cookiecutter.project_slug }}.{{ cookiecutter.project_slug }} import *


class Test{{ cookiecutter.project_slug|title }}(unittest.TestCase):
    """Tests for `{{ cookiecutter.project_slug }}` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        pass

    def tearDown(self):
        """Tear down test fixtures, if any."""
        pass
    
    # Notifiers

    @given(
        notifiers(subclass_of={{cookiecutter.project_slug.replace('_',' ').title().replace(' ','')}}Notifier, classdef={}),
        runs(),
        just(dict()),
        strings()
    )
    def test_{{cookiecutter.project_slug.replace('_',' ').title().replace(' ','')}}Notifier_notify(self, notifier, run, state, message):
        """Notifier.notify"""
        self.assertIsNone(notifier.notify(run, state, message))

    # Submitters

    @given(
        submitters(subclass_of={{cookiecutter.project_slug.replace('_',' ').title().replace(' ','')}}Submitter, classdef={})
    )
    def test_{{cookiecutter.project_slug.replace('_',' ').title().replace(' ','')}}Submitter_test_noop(self, submitter):
        """Submitter.test_noop"""
        self.assertIsNone(run(submitter.test_noop()))

    @given(
        submitters(subclass_of={{cookiecutter.project_slug.replace('_',' ').title().replace(' ','')}}Submitter, classdef={}),
        paths()
    )
    def test_{{cookiecutter.project_slug.replace('_',' ').title().replace(' ','')}}Submitter_reroot_path(self, submitter, path):
        """Submitter.reroot_path"""
        self.assertIsNotNone(submitter.reroot_path(path))

    @given(
        submitters(subclass_of={{cookiecutter.project_slug.replace('_',' ').title().replace(' ','')}}Submitter, classdef={}),
        strings(),
        paths(real=True),
        paths(),
        oneof(just(dict), dict(TEST=strings().example())) # empty and non-empty dicts
    )
    def test_{{cookiecutter.project_slug.replace('_',' ').title().replace(' ','')}}Submitter_begin_job(self, submitter, execution_string, datadir, remotedir, environment_hints):
        """Submitter.begin_job"""
        self.assertIsNotNone(run(submitter.begin_job(execution_string, datadir, remotedir, environment_hints)))

    @given(
        submitters(subclass_of={{cookiecutter.project_slug.replace('_',' ').title().replace(' ','')}}Submitter, classdef={}),
        strings()
    )
    def test_{{cookiecutter.project_slug.replace('_',' ').title().replace(' ','')}}Submitter_test_noop(self, submitter, job):
        """Submitter.poll_job"""
        self.assertIsNone(run(submitter.poll_job(job)))

    #FileJobs

    @given(
        jobs(subclass_of={{cookiecutter.project_slug.replace('_',' ').title().replace(' ','')}}FileJob, classdef={}),
        runs(),
        files(real=True),
        paths(),
        paths()
    )
    def test_{{cookiecutter.project_slug.replace('_',' ').title().replace(' ','')}}FileJob_submit(self, job, run, file, datadir, remotedir):
        """FileJob.submit"""
        self.assertIsNotNone(job.setup(run, datadir, remotedir))

    @given(
        jobs(subclass_of={{cookiecutter.project_slug.replace('_',' ').title().replace(' ','')}}FileJob, classdef={}),
        runs(),
        files(real=True),
        paths(),
        oneof(strings(), ints())
    )
    def test_{{cookiecutter.project_slug.replace('_',' ').title().replace(' ','')}}FileJob_collect(self, job, run, file, datadir, pid):
        """FileJob.collect"""
        self.assertIsNone(job.collect(run, datadir, pid))

    #RunJobs

    @given(
        jobs(subclass_of={{cookiecutter.project_slug.replace('_',' ').title().replace(' ','')}}RunJob, classdef={}),
        runs(),
        paths(),
        paths()
    )
    def test_{{cookiecutter.project_slug.replace('_',' ').title().replace(' ','')}}RunJob_submit(self, job, run, datadir, remotedir):
        """RunJob.submit"""
        self.assertIsNotNone(job.setup(run, datadir, remotedir))

    @given(
        jobs(subclass_of={{cookiecutter.project_slug.replace('_',' ').title().replace(' ','')}}RunJob, classdef={}),
        runs(),
        paths(),
        oneof(strings(), ints())
    )
    def test_{{cookiecutter.project_slug.replace('_',' ').title().replace(' ','')}}RunJob_collect(self, job, run, datadir, pid):
        """RunJob.collect"""
        self.assertIsNone(job.collect(run, datadir, pid))