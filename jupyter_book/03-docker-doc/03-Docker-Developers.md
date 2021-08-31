# Building the Docker image

```{note}
This documentation is for developers, users do not need to build docker images. 
```

The SATAY Docker container is built from the [Dockerfile](https://github.com/SATAY-LL/Transposonmapper/blob/main/Dockerfile). The Dockerfile uses the following general commands

1. The SATAY docker image uses `continuumio/miniconda3` as a base image. 
1. Install ubuntu packages
    * `yad`: required to run the GUI
    * `xdg-utils`, `gedit`, `dbus-x11`: required to open text files
    * `evince`: pdf viewer
1. Download and install all dependencies with conda from [environment.yml](https://github.com/SATAY-LL/Transposonmapper/blob/main/conda/environment.yml)
1. Copy all required code into the image
1. pip install the transposonmapper package
1. Define environment variables
1. Set `/data` as the default directory

To build and test a docker image locally on your computer, run the following command

```bash
docker build . -t satay
```

For more information about building Docker images, see the [Docker reference documentation](https://docs.docker.com/engine/reference/builder/)

## Continuous integration
The Docker image is automatically built and uploaded to DockerHub through a [GitHub Action](https://github.com/SATAY-LL/Transposonmapper/blob/main/.github/workflows/CI_publish.yml) whenever a new version is released.
