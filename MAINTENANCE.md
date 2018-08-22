# Maintainers Guide

This page contains instructions for project maintainers about how our setup works,
making releases, creating packages, etc.

If you want to make a contribution to the project, see the [Contributing
Guide](CONTRIBUTING.md) instead.


## Branches

* *master*:
* *gh-pages*:


## Continuous Integration

We use TravisCI and AppVeyor continuous integration (CI) services to build and test the
project on Windows, Linux, and Mac.
The configuration files for these services are `.travis.yml` and `.appveyor.yml`.
Both rely on the `requirements.txt` file to install the required dependencies using
conda and the `Makefile` to run the tests and checks.

Travis also handles all of our deployments automatically:

* Updating the development documentation by pushing the built HTML pages from the
  *master* branch onto the `dev` folder of the *gh-pages* branch.
* Uploading new releases to PyPI (only when the build was triggered by a git tag).
* Updated the `latest` documentation link to the new release.

This way, most day-to-day maintenance operations are automatic.

The scripts that setup the test environment and run the deployments are loaded from the
[fatiando/continuous-integration](https://github.com/fatiando/continuous-integration)
repository to avoid duplicating work across multiple repositories.
If you find any problems with the test setup and deployment, please create issues and
submit pull requests to that repository.


## Making a Release

Tagging.
Updating the conda package.
Post on social media.
