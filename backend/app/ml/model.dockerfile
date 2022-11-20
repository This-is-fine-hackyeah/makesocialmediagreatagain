FROM nvcr.io/nvidia/pytorch:22.08-py3

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -yqq --no-install-recommends \
    ffmpeg libsm6 libxext6 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install tesseract
RUN apt-get update && \
    apt-get install -yqq --no-install-recommends \
    tesseract-ocr libtesseract-dev libleptonica-dev pkg-config tesseract-ocr-pol && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install dependencies
RUN pip install transformers sacremoses jupyterlab \
    tesserocr "opencv-python-headless<4.3" Pillow numpy scipy \
    pytorch-lightning torchmetrics tensorboard

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--allow-root"]
