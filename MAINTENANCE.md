# Maintainers Guide

This page contains instructions for project maintainers about how our setup
works, making releases, creating packages, etc.

If you want to make a contribution to the project, see the
[Contributing Guide](CONTRIBUTING.md) instead.


## Contents

* [Branches](#branches)
* [Reviewing and merging pull requests](#reviewing-and-merging-pull-requests)
* [Continuous Integration](#continuous-integration)
* [Citations](#citations)
* [Making a Release](#making-a-release)
  * [Draft a new Zenodo release](#draft-a-new-zenodo-release)
  * [Update the changelog](#update-the-changelog)
  * [Check the README syntax](#check-the-readme-syntax)
  * [Release](#release)
  * [Archive on Zenodo](#archive-on-zenodo)
  * [Update the conda package](#update-the-conda-package)


## Branches

* *master*: Always tested and ready to become a new version. Don't push directly to this
  branch. Make a new branch and submit a pull request instead.
* *gh-pages*: Holds the HTML documentation and is served by Github. Pages for the master
  branch are in the `dev` folder. Pages for each release are in their own folders.
  **Automatically updated by TravisCI** so you shouldn't have to make commits here.


## Reviewing and merging pull requests

A few guidelines for reviewing:

* Always **be polite** and give constructive feedback.
* Welcome new users and thank them for their time, even if we don't plan on merging the
  PR.
* Don't be harsh with code style or performance. If the code is bad, either (1) merge
  the pull request and open a new one fixing the code and pinging the original submitter
  (2) comment on the PR detailing how the code could be improved. Both ways are focused
  on showing the contributor **how to write good code**, not shaming them.

Pull requests should be **squash merged**.
This means that all commits will be collapsed into one.
The main advantages of this are:

* Eliminates experimental commits or commits to undo previous changes.
* Makes sure every commit on master passes the tests and has a defined purpose.
* The maintainer writes the final commit message, so we can make sure it's good and
  descriptive.


## Continuous Integration

We use GitHub Actions continuous integration (CI) services to build and
test the project on Windows, Linux, and Mac.
The configuration files for this service are in `.github/workflows`.
They rely on the `requirements.txt`, `requirements-optional.txt`, etc 
files to install the required dependencies using conda or pip.

The CI jobs include:

* Running the test suite on multiple combinations of OS, Python version,
  with and without optional dependencies.
* Running Black, flake8, and pylint to check the code for style.
* Building the documentation to make sure it works.
* Pushing the built documentation HTML to the `gh-pages` branch.
* Upload source and wheel distributions to TestPyPI (on master) and PyPI
  (on releases).

This way, most day-to-day maintenance operations are automatic.


## Making a Release

We try to automate the release process as much as possible.
Travis handles publishing new releases to PyPI and updating the documentation.
The version number is set automatically using setuptools-scm based on information it gets
from git.
There are a few steps that still must be done manually, though.

### Draft a new Zenodo release

If the project already has releases on [Zenodo](https://zenodo.org/), you need to create
a **New version** of it. Find the link to the latest Zenodo release on the `README.md`
file of your project. Then:

1. Delete all existing files (they will be replaced with the new version).
2. Reserve a DOI and save the release draft.
3. Add as authors any new contributors who have added themselves to
   [`AUTHORS.md`](AUTHORS.md).
4. Review author order to make sure it follows the guidelines on our
   [Authorship Guide](AUTHORSHIP.md)
5. Update release date.

On the other hand, if you're making the first release of the project, you need to create
a **New upload** for it inside the
[Fatiando a Terra community at Zenodo](https://zenodo.org/communities/fatiando/).
Make sure the Fatiando a Terra community is chosen when filling the release draft.
The rest of the process is the same as above.

### Update the changelog

1. Generate a list of commits between the last release tag and now:

    ```bash
    git log HEAD...v0.1.2 > changes.rst
    ```

2. Edit the changes list to remove any trivial changes (updates to the README, typo
   fixes, CI configuration, etc).
3. Replace the PR number in the commit titles with a link to the Github PR page. In Vim,
   use `` %s$#\([0-9]\+\)$`#\1 <https://github.com/fatiando/PROJECT/pull/\1>`__$g ``
   to make the change automatically.
4. Copy the remaining changes to `doc/changes.rst` under a new section for the
   intended release.
5. Add a list of people who contributed to the release (use `git shortlog HEAD...v1.2.0 -sne`).
5. Include the DOI badge in the changelog. Remember to replace your DOI inside the badge
   url.

    ```
    .. image:: https://zenodo.org/badge/DOI/<INSERT-DOI-HERE>.svg
        :alt: Digital Object Identifier for the Zenodo archive
        :target: https://doi.org/<INSERT-DOI-HERE>
    ```

6. Add a link to the new release version documentation in `README.rst`.
7. Open a new PR with the updated changelog.

### Check the README syntax

Github is a bit forgiving when it comes to the RST syntax in the README but PyPI is not.
So slightly broken RST can cause the PyPI page to not render the correct content. Check
using the `rst2html.py` script that comes with docutils:

```
python setup.py --long-description | rst2html.py --no-raw > index.html
```

Open `index.html` and check for any flaws or error messages.

### Release

After the changelog is updated, making a release should be as simple as
creating a new git tag.
The continuous integration services will take care of pushing the package to
PyPI and creating a new version of the documentation.
A new folder with version number containing the HTML documentation will be
pushed to *gh-pages*, and the `latest` link will be updated to point to this
new folder.

The tag should be version number (following [Semantic Versioning](https://semver.org/))
with a leading `v` (`v1.5.7`).

To create a new tag, go to `https://github.com/fatiando/PROJECT/releases` and
click on "Draft a new release":

1. Use the version number (including the `v`) as the "Tag version" and "Release
   title".
2. Fill the release description with a Markdown version of the **latest**
   changelog entry (including the DOI badge). The `changes.rst` file can be
   converted to Markdown using `pandoc`:
   ```
   pandoc -s changes.rst -o changes.md --wrap=none
   ```
3. Publish the release.

### Archive on Zenodo

Grab a zip file from the Github release and upload to Zenodo using the previously
reserved DOI.

### Update the conda package

After CI is done building the tag and all builds pass, we need to update
the conda package.
Fortunately, the conda-forge bot will submit a PR updating the package for us
(it may take a couple of hours to do so).
Most releases can be merged right away but some might need further changes to
the conda recipe:

1. If the release added new dependencies, make sure they are included in the
   `meta.yaml` file.
2. If dropping/adding support for Python versions (or version of other
   packages) make sure the correct version restrictions are applied in
   `meta.yaml`.

## Citations

The citation for a package that doesn't have an associated paper will be the
Zenodo DOI for all versions. This citation will include everyone who has
contributed to the project and met our [authorship criteria](AUTHORSHIP.md).

Include the following text in the `CITATION.rst` file:

```
This is research software **made by scientists**. Citations help us justify the
effort that goes into building and maintaining this project.

If you used this software in your research, please consider
citing the following source: https://doi.org/10.5281/zenodo.3530749

The link above includes full citation information and export formats (BibTeX,
Mendeley, etc).
```

If the project has been publish as an academic paper (for example, on
[JOSS](https://joss.theoj.org)), **update the `CITATION.rst` to point to the
paper instead of the Zenodo archive**.

```
If you used this software in your research, please consider citing the
following publication:

    <full citation including authors, title, journal, DOI, etc>

This is an open-access publication. The paper and the associated reviews can be
freely accessed at: https://doi.org/<INSERT-DOI-HERE>

The link above includes full citation information and export formats (BibTeX,
Mendeley, etc).
```
