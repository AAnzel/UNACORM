# syntax=docker/dockerfile:1

FROM continuumio/miniconda3
ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"

RUN apt update && apt install -y fontconfig gcc build-essential ffmpeg \
    && apt autoclean -y \
    && apt autoremove -y \
    && export PATH=~/anaconda3/bin:$PATH \
    && export FONTCONFIG_FILE=/etc/fonts/fonts.conf \
    && export FONTCONFIG_PATH=/etc/fonts/ \
    && export FILECONFIG_PATH=/etc/fonts

WORKDIR /app

COPY . /app

RUN conda env create -f environment.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "dna_project_env", "/bin/bash", "-c"]

RUN conda clean --all --yes

WORKDIR /app/Source/Encodings/RaptorCode

RUN pip install -r requirements.txt \
    && python setup.py install

WORKDIR /app/Source/Encodings/XORBasedCode

RUN pip install -r requirements.txt \
    && python setup.py install

WORKDIR /app/Source/Encodings/The2DCode

RUN pip install -r requirements.txt

WORKDIR /app/Source/

EXPOSE 8501

CMD streamlit run main.py --browser.gatherUsageStats False