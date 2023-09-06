# Base image
FROM ubuntu:22.04

# Set non-interactive mode
ENV DEBIAN_FRONTEND=noninteractive

# Update and install essential packages
RUN apt-get update -y && apt-get install -y git \
                                            cmake \
                                            python3 \
                                            python3-pip \
                                            python-is-python3 \
                                            build-essential \
                                            libdbus-1-3 \
                                            libpulse-mainloop-glib0 \
                                            ffmpeg \
                                            libsm6 \
                                            libxext6 \
                                            libgl1-mesa-dev \
                                            libgl1 \
                                            libxkbcommon-x11-dev \
                                            libxcb-cursor-dev \
                                            libxcb-icccm4-dev \
                                            libxcb-keysyms1-dev
RUN pip install aqtinstall

# Install Qt6
ARG QT=6.5.2
ARG QT_MODULES=
ARG QT_HOST=linux
ARG QT_TARGET=desktop
ARG QT_ARCH=
RUN aqt install --outputdir /opt/qt ${QT} ${QT_HOST} ${QT_TARGET} ${QT_ARCH} -m ${QT_MODULES}

# Set environment variables for Qt
ENV PATH /opt/qt/${QT}/gcc_64/bin:$PATH
ENV QT_PLUGIN_PATH /opt/qt/${QT}/gcc_64/plugins/
ENV QML_IMPORT_PATH /opt/qt/${QT}/gcc_64/qml/
ENV QML2_IMPORT_PATH /opt/qt/${QT}/gcc_64/qml/

# PySide6 package
RUN pip install PySide6==${QT}
RUN pip install nibabel==5.1.0
RUN pip install Pillow==10.0.0

# Set the working directory for the application
WORKDIR /app

# Copy the project files into the image
COPY . .

# runnning project
CMD ["python", "main.py"]