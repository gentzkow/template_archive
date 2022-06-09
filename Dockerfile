# syntax=docker/dockerfile:1.2
FROM dataeditors/stata17:2022-02-15
# this runs your code 

# switch to root user to manage packages
USER root
ARG DEBIAN_FRONTEND=noninteractive

############### install preliminaries
RUN apt-get update \
    && apt-get install tzdata --yes \
    && apt-get install wget --yes \
    && apt-get install software-properties-common --yes \
    && apt-get install curl --yes
############### install LyX

############### install LyX
# instructions from https://wiki.lyx.org/LyX/LyXOnUbuntu
RUN add-apt-repository ppa:lyx-devel/release --yes \
    && apt-get update \
    && apt-get install lyx --yes
############### install LyX

############### install Conda
# instructions from https://stackoverflow.com/questions/64090326/bash-script-to-install-conda-leads-to-conda-command-not-found-unless-i-run-b
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O conda.sh
RUN ["/bin/bash", "conda.sh", "-b", "-p"]
RUN rm -f conda.sh \
    && /root/miniconda3/bin/conda init bash
############### install Conda

COPY setup/conda_env.yaml conda_env.yaml
# https://stackoverflow.com/questions/20635472/using-the-run-instruction-in-a-dockerfile-with-source-does-not-work
RUN /root/miniconda3/bin/conda env create -f conda_env.yaml


RUN --mount=type=secret,id=statalic,dst=/usr/local/stata/stata.lic \
    /usr/local/stata/stata-mp do /code/setup.do

# USER statauser:stata

# run the master file
ENTRYPOINT ["/bin/bash"]