FROM rocker/tidyverse:3.6.3

RUN apt-get update && apt-get install -y \
    imagemagick libmagick++-dev libudunits2-dev curl \
    libgdal-dev libjpeg-dev libxt-dev libpng-dev gfortran

# Install Rust and Cargo. Some R packages requires Rust.
# See: b/113106905
RUN curl -sSf https://static.rust-lang.org/rustup.sh | sh

ADD packages packages
ADD packages_users packages_users
ADD package_installs.R /tmp/package_installs.R

RUN Rscript /tmp/package_installs.R && \
    bash -c "rm -Rf /tmp/Rtmp*"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    --no-install-recommends build-essential \
	python3.6 python3-pip python3-setuptools python3-dev


WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip3 install -r requirements.txt

# Download and install packages from CRAN-like repo
install.packages("rcicr", repos="http://R-Forge.R-project.org")
1: In install.packages("rcicr") :
  installation of package ‘jpeg’ had non-zero exit status
2: In install.packages("rcicr") :
  installation of package ‘latticeExtra’ had non-zero exit status
3: In install.packages("rcicr") :
  installation of package ‘Hmisc’ had non-zero exit status
4: In install.packages("rcicr") :
  installation of package ‘aspace’ had non-zero exit status
5: In install.packages("rcicr") :


