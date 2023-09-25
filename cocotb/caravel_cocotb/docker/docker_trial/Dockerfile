FROM efabless/dv:cocotb
# FROM efabless/dv_setup:latest
# Use the latest Ubuntu as the base image

RUN pip install --upgrade pip setuptools

# remove caravel_cocotb 
RUN pip uninstall -y caravel-cocotb

# install caravel_cocotb for new caravel structure
RUN git clone https://github.com/efabless/caravel-sim-infrastructure.git && \
    cd caravel-sim-infrastructure/cocotb && \
    git pull && \
    git checkout caravel_restructuring && \
    pip install . && \
    
    cd ../.. && rm -rf caravel-sim-infrastructure

# Clean up unnecessary files and packages
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Default command when the container starts
CMD ["bash"]

