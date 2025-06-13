# Use Jupyter base image with Python 3.11 and pre-installed Conda
FROM jupyter/base-notebook:python-3.11

# Set working directory for Java and OTP
WORKDIR /usr/src/app

# Switch to root to install system packages
USER root

# Install system dependencies (including osmium-tool and unzip for DuckDB)
RUN apt-get update && apt-get install -y \
    wget \
    tar \
    unzip \
    osmium-tool \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install OpenJDK 21
RUN wget --no-check-certificate -O openjdk-21.tar.gz https://download.oracle.com/java/21/latest/jdk-21_linux-x64_bin.tar.gz && \
    mkdir -p /opt && \
    tar -xzf openjdk-21.tar.gz -C /opt && \
    rm openjdk-21.tar.gz && \
    ln -s /opt/jdk-21* /opt/jdk

ENV JAVA_HOME=/opt/jdk
ENV PATH="$JAVA_HOME/bin:$PATH"

# Confirm Java is installed
RUN java --version

# Install DuckDB CLI
RUN wget https://github.com/duckdb/duckdb/releases/download/v1.2.2/duckdb_cli-linux-amd64.zip -O duckdb_cli.zip && \
    unzip duckdb_cli.zip && \
    test -f duckdb && \
    mv duckdb /usr/local/bin/duckdb && \
    chmod +x /usr/local/bin/duckdb && \
    rm duckdb_cli.zip

# Install OpenTripPlanner
RUN wget https://repo1.maven.org/maven2/org/opentripplanner/otp/2.6.0/otp-2.6.0-shaded.jar -O /usr/src/app/otp.jar

# Switch to Jupyter user and set working directory
USER $NB_UID
WORKDIR /home/jovyan/work

# Copy source files into the container with correct ownership
COPY --chown=$NB_UID:$NB_GID . /home/jovyan/work

RUN conda env create -f environment.yml
RUN conda clean -afy

# Register the environment as a Jupyter kernel
RUN conda run -n innotech python -m ipykernel install --user --name=innotech --display-name "Python (innotech)"

# Configure Jupyter to run without a token
RUN mkdir -p /home/jovyan/.jupyter && \
    echo "c.NotebookApp.token = ''" > /home/jovyan/.jupyter/jupyter_notebook_config.py

# Install additional Python dependencies into the conda environment
RUN conda run -n innotech pip install --use-pep517 -e .

# Expose OTP and Jupyter ports
EXPOSE 8080 8888

# Add entrypoint script as root and make it executable
USER root
COPY docker_start.sh /usr/local/bin/docker_start.sh
RUN chmod +x /usr/local/bin/docker_start.sh

# Switch back to the default notebook user
USER $NB_UID

# Set entrypoint
CMD ["/usr/local/bin/docker_start.sh"]

