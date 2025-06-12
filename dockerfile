# Use an official Python runtime as a parent image
#FROM python:3.11-slim

# Use a different base image
FROM python:3.11-bullseye

# Set the working directory in the container
WORKDIR /usr/src/app


# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    tar \
    && rm -rf /var/lib/apt/lists/*

# Manually download and install OpenJDK 21
RUN wget --no-check-certificate -O openjdk-21.tar.gz https://download.oracle.com/java/21/latest/jdk-21_linux-x64_bin.tar.gz && \
    mkdir -p /opt && \
    tar -xzf openjdk-21.tar.gz -C /opt && \
    rm openjdk-21.tar.gz && \
    ln -s /opt/jdk-* /opt/jdk

ENV JAVA_HOME=/opt/jdk
ENV PATH="$JAVA_HOME/bin:$PATH"

# Verify Java installation
RUN java --version


# Install conda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    bash ~/miniconda.sh -b -p ~/miniconda && \
    rm ~/miniconda.sh

# Add conda to PATH
ENV PATH="/root/miniconda/bin:$PATH"

# Install Python libraries using conda
COPY environment.yml .
RUN conda env create -f environment.yml

# Make RUN commands use the new environment
SHELL ["conda", "run", "-n", "innotech", "/bin/bash", "-c"]

# Install osmium
RUN apt-get update && apt-get install -y osmium-tool

# Install DuckDB
RUN wget https://github.com/duckdb/duckdb/releases/download/v1.2.2/duckdb_cli-linux-amd64.zip -O duckdb_cli.zip && \
    unzip duckdb_cli.zip && \
    test -f duckdb && \
    mv duckdb /usr/local/bin/duckdb && \
    chmod +x /usr/local/bin/duckdb


# Install OpenTripPlanner
RUN wget https://repo1.maven.org/maven2/org/opentripplanner/otp/2.6.0/otp-2.6.0-shaded.jar -O /usr/src/app/otp.jar

# Copy the current directory contents into the container
COPY . .

# Install additional Python dependencies
RUN pip install --use-pep517 -e .

# Expose the port OpenTripPlanner will run on
EXPOSE 8080

# Command to start OpenTripPlanner
CMD ["java", "-Xmx2G", "-jar", "otp.jar", "--load", "."]