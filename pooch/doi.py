# Copyright (c) 2018 The Pooch Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Interfaces to common DOI-providing data repositories.
"""

import requests

from .utils import parse_url


def doi_to_url(doi):
    """
    Follow a DOI link to resolve the URL of the archive.

    Makes a GET request to ``https://doi.org`` to resolve the DOI to the
    repository website.

    Parameters
    ----------
    doi : str
        The DOI of the archive.

    Returns
    -------
    url : str
        The URL of the archive in the data repository.

    """
    response = requests.get(f"https://doi.org/{doi}")
    url = response.url
    if 400 <= response.status_code < 600:
        raise ValueError(
            f"Archive with doi:{doi} not found (see {url}). Is the DOI correct?"
        )
    return url


class Zenodo():
    """
    """

    def __init__(self, doi, url):
        self.doi = doi
        self.url = url

    def get_download_url(self, file_name):
        """
        Use the repository API to get the download URL for a file.

        Parameters
        ----------
        file_name : str
            The name of the file in the archive that will be downloaded.

        Returns
        -------
        download_url : str
            The HTTP URL that can be used to download the file.
        """
        if parse_url(self.url)["netloc"] != "zenodo.org":
            return None
        article_id = self.url.split("/")[-1]
        # With the ID, we can get a list of files and their download links
        article = requests.get(f"https://zenodo.org/api/records/{article_id}").json()
        files = {item["key"]: item for item in article["files"]}
        if file_name not in files:
            raise ValueError(
                f"File '{file_name}' not found in data archive {self.url} (doi:{self.doi})."
            )
        download_url = files[file_name]["links"]["self"]
        return download_url


class Figshare():
    """
    """

    def __init__(self, doi, url):
        self.doi = doi
        self.url = url

    def get_download_url(self, file_name):
        """
        Use the repository API to get the download URL for a file.

        Parameters
        ----------
        file_name : str
            The name of the file in the archive that will be downloaded.

        Returns
        -------
        download_url : str
            The HTTP URL that can be used to download the file.
        """
        if parse_url(self.url)["netloc"] != "figshare.com":
            return None
        # Use the figshare API to find the article ID from the DOI
        article = requests.get(
            f"https://api.figshare.com/v2/articles?doi={self.doi}"
        ).json()[0]
        article_id = article["id"]
        # With the ID, we can get a list of files and their download links
        response = requests.get(
            f"https://api.figshare.com/v2/articles/{article_id}/files"
        )
        response.raise_for_status()
        files = {item["name"]: item for item in response.json()}
        if file_name not in files:
            raise ValueError(
                f"File '{file_name}' not found in data archive {self.url} (doi:{self.doi})."
            )
        download_url = files[file_name]["download_url"]
        return download_url


class Dataverse():
    """
    """

    def __init__(self, doi, url):
        self.doi = doi
        self.url = url

    def get_download_url(self, file_name):
        """
        Use the repository API to get the download URL for a file.

        Parameters
        ----------
        file_name : str
            The name of the file in the archive that will be downloaded.

        Returns
        -------
        download_url : str
            The HTTP URL that can be used to download the file.
        """
        # Make a request to the server as if this was a Dataverse instance
        parsed = parse_url(self.url)
        api = f"{parsed['protocol']}://{parsed['netloc']}/api"
        response = requests.get(
            f"{api}/datasets/:persistentId?persistentId=doi:{self.doi}"
        )

        # If we failed, this is probably not a DataVerse instance
        if 400 <= response.status_code < 600:
            return None

        # Iterate over the given files until we find one of the requested name
        for filedata in response.json()["data"]["latestVersion"]["files"]:
            if file_name == filedata["dataFile"]["filename"]:
                file_id = filedata['dataFile']['persistentId']
                download_url = f"{api}/access/datafile/:persistentId?persistentId={file_id}"
                break
        else:
            raise ValueError(
                f"File '{file_name}' not found in data archive {self.url} (doi:{self.doi})."
            )
        return download_url
