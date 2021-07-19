FROM continuumio/miniconda3:4.9.2

# Set Bash as default shell
SHELL [ "/bin/bash", "--login", "-c" ]

# Install libraries needed for the GUI
RUN apt-get update -q && apt-get install yad xdg-utils terminator -q -y && apt-get clean 

# Install conda packages
COPY ./conda/environment.yml /opt
RUN conda env update -n base -f opt/environment.yml --quiet \
    && conda clean -afy \
    && find /opt/conda/ -follow -type f -name '*.a' -delete \
    && find /opt/conda/ -follow -type f -name '*.pyc' -delete \
    && find /opt/conda/ -follow -type f -name '*.js.map' -delete 

# Copy code to container
COPY ./transposonmapper /opt/src/transposonmapper 
COPY ./satay /opt/satay
COPY setup.py README.rst /opt/src/

# Install the transposonmapper package inside the container
WORKDIR /opt/src/
RUN pip install .

# Set environment variables
ENV adapters=/opt/conda/bbtools/lib/resources/adapters.fa \
    bbduk=/opt/conda/bbtools/lib/bbduk.sh \
    satay=/opt/satay/satay.sh 

# Avoid accessibility warning from yad
ENV NO_AT_BRIDGE=1

# Set /data as default directory
WORKDIR /data

# Default command when running the container
CMD bash ${satay}
