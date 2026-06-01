# syntax=docker/dockerfile:1

FROM continuumio/miniconda3
ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"

RUN echo 'Acquire::http::Pipeline-Depth 0;\nAcquire::http::No-Cache true;\nAcquire::BrokenProxy true;\n' > /etc/apt/apt.conf.d/99fixbadproxy

RUN rm -rf /var/lib/apt/lists/* \
    && apt update \
    && apt full-upgrade -y \
    && apt install -y --fix-missing fontconfig g++ cmake \
    && apt autoclean -y \
    && apt autoremove -y \
    && export PATH=~/anaconda3/bin:$PATH \
    && export FONTCONFIG_FILE=/etc/fonts/fonts.conf \
    && export FONTCONFIG_PATH=/etc/fonts/ \
    && export FILECONFIG_PATH=/etc/fonts \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN conda update --all -y \
    && conda tos accept \
    && conda env create -f environment.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "unacorm_env", "/bin/bash", "-c"]

RUN conda clean --all --yes

WORKDIR /app/Source/Encodings/XORBasedCode

RUN rm -rf build/ && python setup.py install

WORKDIR /app/Source/Encodings/RaptorCode

RUN python -m build . \
    && pip install -e .

WORKDIR /app/Source/Encodings/DNA_Aeon

RUN rm CMakeCache.txt && python setup.py

WORKDIR /app/Source/

EXPOSE 8501

CMD streamlit run main.py --browser.gatherUsageStats False
