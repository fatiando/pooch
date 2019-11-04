---
title: "Pooch: A friend to fetch your data files"
tags:
  - python
authors:
  - name: Leonardo Uieda
    orcid: 0000-0001-6123-9515
    affiliation: 1
  - name: Santiago Rubén Soler
    orcid: 0000-0001-9202-5317
    affiliation: "2,3"
  - name: Rémi Rampin
    orcid: 0000-0002-0524-2282
    affiliation: 4
  - name: Hugo van Kemenade
    orcid: 0000-0001-5715-8632
    affiliation: 5
  - name: Matthew Turk
    orcid: 0000-0002-5294-0198
    affiliation: 6
  - name: Daniel Shapero
    orcid: 0000-0002-3651-0649
    affiliation: 7
affiliations:
 - name: Department of Earth, Ocean and Ecological Sciences, School of Environmental Sciences, University of Liverpool, UK
   index: 1
 - name: Instituto Geofísico Sismológico Volponi, Universidad Nacional de San Juan, Argentina
   index: 2
 - name: CONICET, Argentina
   index: 3
 - name: New York University, USA
   index: 4
 - name: Independent (Non-affiliated)
   index: 5
 - name: University of Illinois at Urbana-Champaign, USA
   index: 6
 - name: Polar Science Center, University of Washington Applied Physics Lab, USA
   index: 7
date: 23 October 2019
bibliography: paper.bib
---

# Summary

Scientific software are usually created to analyze, model, and/or visualize
data.
As such, many software libraries include sample datasets in their distributions
for use in documentation, tests, benchmarks, and workshops.
Prominent examples in Python include scikit-learn [@scikit-learn] and
scikit-image [@scikit-image].
The usual approach is to include smaller datasets in the GitHub repository directly and
package them with the source and binary distributions.
Larger datasets require writing code to download the files from a remote server to the
users computer.
The same problem is faced by scientists using version control to manage their research
projects.
As data files increase in size, it becomes unfeasible to store them on GitHub
repositories.
While downloading a data file over HTTP can be done easily with modern Python libraries,
it is not trivial to manage a set of files, keep them updated, and check for corruption.
Instead of scientists and library authors recreating the same code, it would be best to
have a minimalistic and easy to setup tool for fetching and maintaining data files.

Introduce Pooch as the solution.
Main goals of the library.
What we can do and how we do it.
How Pooch is already being used (cite relevant packages and mention scikit-image PR).


# Acknowledgements

I would like to thank all of the volunteers who have dedicated their time and
energy to build the open-source ecosystem on which our work relies.
The order of authors is based on number of commits to the GitHub repository.
A full list of all contributors to the project can be found at
https://github.com/fatiando/pooch/graphs/contributors

# References
