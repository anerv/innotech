# Use Jupyter base image with Python 3.11 and pre-installed Conda
FROM jupyter/base-notebook:python-3.11

# Set working directory for Java and OTP
WORKDIR /usr/src/app

# Switch to root to install system packages
USER root

# Install system dependencies
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


# Switch to Jupyter user and working dir
USER $NB_UID
WORKDIR /home/jovyan/work

# Copy source files into the container
COPY --chown=$NB_UID:$NB_GID . /home/jovyan/work

# Create Conda env
RUN conda env create -f environment.yml && conda clean -afy

# Register the env as a Jupyter kernel
RUN conda run -n innotech python -m ipykernel install --user --name=innotech --display-name "Python (innotech)"

# Install additional editable dependencies last
RUN conda run -n innotech pip install --use-pep517 -e .


# Configure Jupyter
RUN mkdir -p /home/jovyan/.jupyter && \
    echo "c.ServerApp.token = ''" > /home/jovyan/.jupyter/jupyter_server_config.py && \
    echo "c.ServerApp.allow_origin = '*'" >> /home/jovyan/.jupyter/jupyter_server_config.py


# Expose OTP and Jupyter ports
EXPOSE 8080 8888

# Add and set permissions on the start script
USER root
COPY docker_start.sh /usr/local/bin/docker_start.sh
RUN chmod +x /usr/local/bin/docker_start.sh

# Switch back to notebook user
USER $NB_UID

# Set the default command
CMD ["/usr/local/bin/docker_start.sh"]
