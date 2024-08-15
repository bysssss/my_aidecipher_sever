# Define custom function directory
ARG SRC_DIR="/src"

FROM python:3.11 AS build-image

# Include global arg in this stage of the build
ARG SRC_DIR

# Copy function code
RUN mkdir -p ${SRC_DIR}

# Install the function's dependencies
RUN pip install --upgrade pip setuptools wheel
RUN pip install --target ${SRC_DIR} awslambdaric

COPY ./src/requirements.txt .
RUN pip install --target ${SRC_DIR} --no-cache-dir -r requirements.txt && rm requirements.txt

# Use a slim version of the base Python image to reduce the final image size
FROM python:3.11

# Include global arg in this stage of the build
ARG SRC_DIR
# Set working directory to function root directory
WORKDIR ${SRC_DIR}

# Copy in the built dependencies
COPY --from=build-image ${SRC_DIR} ${SRC_DIR}

RUN set -x \
    && apt-get update \
    && apt-get install -y \
        zip \
        unzip \
        sudo \
    && rm -rf /var/lib/apt/lists/*

# Set runtime interface client as default command for the container runtime
#ENTRYPOINT ["/usr/local/bin/python", "-m", "awslambdaric"]

# Pass the name of the function handler as an argument to the runtime
#CMD ["main.lambda_handler"]

RUN mkdir -p /docker
