**************************
SATAY and Transposonmapper
**************************

This workflow is created for processing sequencing data for SAturated Transposon Analysis in Yeast (SATAY) for Saccharomyces Cerevisiae.
It performs the steps from raw sequencing data until the transposon mapping that outputs files containing all insertion sites combined with the number of reads.

For more information regarding SATAY, see `the satay user website <https://sites.google.com/site/satayusers/>`_ created by the Kornmann-lab.
For more extensive documentation, `see our JupyterBook <https://satay-ll.github.io/SATAY-jupyter-book/Introduction.html>`_.

The workflow requires input sequencing data in fastq format.
It can perform the following tasks:

- sequence trimming
- quality checking raw and trimmed fastq files
- sequence alignment with reference genome (S288C Cerevisiae genome)
- quality checking bam files, indexing and sorting
- transposon mapping

The output files indicate the location of transposon insertions and the number of reads at those locations.
This is presented in both .bed and .wig format.
Also a list of genes is generated where the number and distribution of insertions and reads is presented per (essential) gene.

.. list-table::
   :widths: 25 25
   :header-rows: 1

   * - 
     - Badges
   * - **fair-software.nl recommendations**
     - 
   * - \1. Code repository
     - |GitHub Badge| |GitHub Size Badge|
   * - \2. License
     - |License Badge|
   * - \3. Community Registry
     - |Pypi Badge| |Docker Badge|
   * - \4. Enable Citation
     - |Zenodo Badge|
   * - \5. Checklists
     - |Howfairis Badge|
   * - **Code quality checks**
     -
   * - Continuous integration
     - |CI Test|
   * - Documentation
     - |JupyterBook Badge|
   * - Code Quality
     - |Sonarcloud Quality Gate Badge| |Sonarcloud Coverage Badge|

.. |GitHub Badge| image:: https://img.shields.io/badge/github-repo-000.svg?logo=github&labelColor=gray&color=blue
   :target: https://github.com/SATAY-LL/Transposonmapper
   :alt: GitHub Badge

.. |GitHub Size Badge| image:: https://img.shields.io/github/repo-size/SATAY-LL/Transposonmapper
   :alt: GitHub repo size

.. |License Badge| image:: https://img.shields.io/github/license/SATAY-LL/Transposonmapper
   :target: https://github.com/SATAY-LL/Transposonmapper
   :alt: License Badge

.. |Pypi Badge| image:: https://img.shields.io/pypi/v/transposonmapper?color=blue
   :target: https://pypi.org/project/transposonmapper
   :alt: Pypi Badge

.. |Docker Badge| image:: https://img.shields.io/docker/automated/mwakok/satay
   :target: https://hub.docker.com/r/mwakok/satay
   :alt: Docker Badge

.. |Zenodo Badge| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.4636310.svg
   :target: https://doi.org/10.5281/zenodo.4636310
   :alt: Zenodo Badge

.. |Howfairis Badge| image:: https://img.shields.io/badge/fair--software.eu-%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F-green
   :target: https://fair-software.eu
   :alt: Howfairis badge

.. |CI Test| image:: https://github.com/SATAY-LL/Transposonmapper/actions/workflows/CI_test.yml/badge.svg
   :alt: Continuous integration workflow
   :target: https://github.com/SATAY-LL/Transposonmapper/actions/workflows/CI_test.yml

.. |JupyterBook Badge| image:: https://img.shields.io/badge/docs-JupyterBook-green
   :alt: Jupyter Book documentation
   :target: https://satay-ll.github.io/SATAY-jupyter-book/Introduction.html

.. |Sonarcloud Quality Gate Badge| image:: https://sonarcloud.io/api/project_badges/measure?project=SATAY-LL_Transposonmapper&metric=alert_status
   :target: https://sonarcloud.io/dashboard?id=SATAY-LL_Transposonmapper
   :alt: Sonarcloud Quality Gate

.. |Sonarcloud Coverage Badge| image:: https://sonarcloud.io/api/project_badges/measure?project=SATAY-LL_Transposonmapper&metric=coverage
   :target: https://sonarcloud.io/component_measures?id=SATAY-LL_Transposonmapper&metric=Coverage&view=list
   :alt: Sonarcloud Coverage

***********************
Documentation for users
***********************

For more extensive documentation, `see our JupyterBook <https://satay-ll.github.io/SATAY-jupyter-book/Introduction.html>`_.

SATAY pipeline
==============

.. image:: https://user-images.githubusercontent.com/15414938/125289522-9c421580-e31f-11eb-9fc9-79c5f96d994c.png
   :width: 400
   :align: center

We provide two methods to run the SATAY pipeline, either with a Docker container (recommended) or a Linux system. The workflow relies
on the following libraries:

- `FASTQC <https://www.bioinformatics.babraham.ac.uk/projects/fastqc/>`_ v0.11.9 or later
- `BBMap <https://sourceforge.net/projects/bbmap/>`_ v38.87 or later
- `Trimmomatic <http://www.usadellab.org/cms/?page=trimmomatic>`_ v0.39 or later
- `BWA <https://sourceforge.net/projects/bio-bwa/>`_ v0.7.17 or later
- `SAMTools <http://www.htslib.org/download/>`_ v1.10 or later
- `BCFTools <http://www.htslib.org/download/>`_ v1.10.2-3 or later
- `Sambamba <https://github.com/biod/sambamba/releases>`_ v0.7.1 or later
- `Transposonmapper <https://github.com/SATAY-LL/Transposonmapper/tree/main/transposonmapper>`_

These libraries are called as a processing pipeline by the script `satay.sh <https://github.com/SATAY-LL/Transposonmapper/blob/main/satay.sh>`_, 
which generates a GUI.

Docker
------

For a full installation and user guide for Docker containers, 
`see our documentation <https://satay-ll.github.io/SATAY-jupyter-book/03-docker-doc/00-Docker-Users.html>`_.

The Docker image is hosted at `mwakok/satay <https://hub.docker.com/r/mwakok/satay>`_.

Prerequisites:

- Windows, macOS, Linux
- Docker 
- Xserver (for displaying the GUI)

To run the docker container, use the commands for your Operating System:

.. code-block:: console

    # For Windows (and WSL):
    docker run --rm -it -e DISPLAY=host.docker.internal:0 -v /$(pwd):data/ mwakok/satay:latest

    # For macOS
    docker run --rm -it -e DISPLAY=docker.for.mac.host.internal:0 -v $(pwd):/data mwakok/satay

    # For Linux
    docker run --rm -it --net=host -e DISPLAY=:0 -v $(pwd):/data mwakok/satay

- The flag ``-e`` enables viewing of the GUI outside the container via the Xserver 
- The flag ``-v`` mounts the current directory (pwd) on the host system to the ``data/`` folder inside the container


Linux system
------------

Prerequisites:

- Anaconda
- Python 3.7, 3.8

We recommend installing all dependencies in a conda environment:

.. code-block:: console

    git clone https://github.com/SATAY-LL/Transposonmapper.git satay
    cd satay
    conda env create --file conda/environment-linux.yml
    conda activate satay-linux

To start the GUI, simply run

.. code-block:: console

    bash satay.sh


****************************
Documentation for developers
****************************

Installation
============

To install transposonmapper, do:

.. code-block:: console

    git clone https://github.com/SATAY-LL/Transposonmapper.git
    cd transposonmapper
    conda env create --file conda/environment-dev.yml
    conda activate satay-dev
    pip install -e .[dev]

Run tests (including coverage) with:

.. code-block:: console
    
    pytest

PyPI package
============
Coming soon!

Docker image
============
Coming soon!


Contributing
============
If you want to contribute to the development of transposonmapper and the SATAY pipeline,
have a look at the `contribution guidelines <CONTRIBUTING.md>`_.


************
Contributors
************

This software is part of the research effort of the `LaanLab <https://www.tudelft.nl/en/faculty-of-applied-sciences/about-faculty/departments/bionanoscience/research/research-labs/liedewij-laan-lab/research-projects/evolvability-and-modularity-of-essential-functions-in-budding-yeast>`_,
Department of BioNanoScience, Delft University of Technology 

- Leila Iñigo de la Cruz
- Gregory van Beek
- Maurits Kok


*******
License
*******

Copyright (c) 2020, Technische Universiteit Delft

Licensed under the Apache License, Version 2.0 (the "License"). 
The 2.0 version of the Apache License, approved by the ASF in 2004, 
helps us achieve our goal of providing reliable and long-lived software products 
through collaborative open source software development.

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

*Last updated: July 12, 2021*