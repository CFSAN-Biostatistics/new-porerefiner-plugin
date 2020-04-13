======================
New-porerefiner-plugin
======================

Cookiecutter_ template for a PoreRefiner plugin.

* GitHub repo: https://github.com/CFSAN-biostatistics/new-porerefiner-plugin
* Documentation: https://new-porerefiner-plugin.readthedocs.io/
* Free software: BSD license

Features
--------

* Testing setup with ``unittest`` and ``python setup.py test`` or ``pytest``
* Travis-CI_: Ready for Travis Continuous Integration testing
* Tox_ testing: Setup to easily test for Python 3.5, 3.6, 3.7, 3.8
* Sphinx_ docs: Documentation ready for generation with, for example, `Read the Docs`_
* bump2version_: Pre-configured version bumping with a single command
* Auto-release to PyPI_ when you push a new tag to master (optional)
* Command line interface using Click (optional)

.. _Cookiecutter: https://github.com/audreyr/cookiecutter

Quickstart
----------

Install the latest Cookiecutter if you haven't installed it yet (this requires
Cookiecutter 1.4.0 or higher)::

    pip install -U cookiecutter

Generate a PoreRefiner plugin project::

    cookiecutter https://github.com/CFSAN-biostatistics/new-porerefiner-plugin

Writing Plugins
---------------

PoreRefiner has a plugin architecture; pip-installable Python packages can make themselves known to PoreRefiner using entry_points in ``setup.py``. The easiest way to write your own plugin notifiers, jobs, and submitters for PoreRefiner is to use the cookiecutter template:

::

    $ cookiecutter https://github.com/CFSAN-Biostatistics/new-porerefiner-plugin
    project_name [My Porerefiner Plugin]:
    project_slug [my_porerefiner_plugin]:
    project_short_description [This is a plugin for Porerefiner, a tool for managining Nanopore sequencing.]:

See the Cookiecutter docs: https://cookiecutter.readthedocs.io/en/1.7.0/

Cookiecutter will create a full project repo and stub classes for your plugin. Open ``<project_slug>/<project_slug>/<project_slug>.py`` and you can fill in the method code blocks to implement the various functions of the necessary interfaces.

Notifiers
=========

Notifiers are "fire and forget" handlers for "end-of-run" events; when an hour has elapsed since the last modification of a file in a run (or whatever idle time is configured in ``config.yaml``, the configured notifiers will be fired off with the run event. Out of the box, PoreRefiner comes with three notifiers - a notifier to send OS-based popup "toast" notifications (if ``pynotifier`` is installed), a notifier to make an HTTP request to a defined endpoint, and a notifier to send a message into an Amazon Web Services Simple Queue Service (SQS) queue. Notifiers differ from jobs in that they're assumed to run quickly/instantly and therefore they're executed synchronously. As a result a long-running notifier can hang the software. For tasks that can't execute quickly (copying files, etc), use a job.

Jobs
====

Jobs are processes that are assumed to take longer to execute and thus should execute asynchronously. As a result the job handler interface is more complex, and jobs require submitters to execute to (described below.) Jobs can be triggered either on the idle timeout of an individual file, or of the entire run, simply by extending the appropriate superclass - `FileJob` and `RunJob`. The PoreRefiner software will dispatch the correct configured job type, collect any type of process or job ID that is returned, and periodically poll the job's submitter for completion status. A run's in-progress jobs can be viewed through the ``prfr`` tool.

Submitters
==========

Submitters are the interface between jobs and the execution system. For instance, the ``HpcSubmitter`` knows how to use SSH to execute commands on a typical HPC using ``qsub``. PoreRefiner has an additional ``LocalSubmitter`` which simply runs commands locally, in a subprocess.

If you develop a useful or interesting config, please consider contributing it to the cookbook using a pull request:

https://github.com/crashfrog/porerefiner-config-cookbook



Installing Your Plugin
----------------------

The project's `setup.py` is, well, set up already. You can use it to install your plugin:

::

    ./setup.py install

or

::

    make install

there's a convenient Makefile:

::

    $ make help
    clean                remove all build, test, coverage and Python artifacts
    clean-build          remove build artifacts
    clean-pyc            remove Python file artifacts
    clean-test           remove test and coverage artifacts
    lint                 check style with flake8
    test                 run tests quickly with the default Python
    test-all             run tests on every Python version with tox
    coverage             check code coverage quickly with the default Python
    docs                 generate Sphinx HTML documentation, including API docs
    servedocs            compile the docs watching for changes
    release              package and upload a release
    dist                 builds source and wheel package
    install              install the package to the active Python's site-packages