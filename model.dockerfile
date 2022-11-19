FROM nvcr.io/nvidia/pytorch:22.10-py3

# Install dependencies
RUN pip install transformers jupyterlab

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--allow-root"]
