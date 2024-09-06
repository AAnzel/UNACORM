# syntax=docker/dockerfile:1

FROM continuumio/miniconda3
ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"

RUN apt update
RUN apt install -y fontconfig
RUN export PATH=~/anaconda3/bin:$PATH
RUN export FONTCONFIG_FILE=/etc/fonts/fonts.conf
RUN export FONTCONFIG_PATH=/etc/fonts/
RUN export FILECONFIG_PATH=/etc/fonts

WORKDIR /app

COPY . /app

RUN conda env create -f environment.yml

RUN conda clean --all --yes

WORKDIR /app/Source/Encodings/NOREC4DNA

RUN pip install -r requirements.txt

RUN python setup.py install

WORKDIR /app/Source/Encodings/XORBasedCode

RUN pip install -r requirements.txt

RUN python setup.py install

WORKDIR /app/Source/Encodings/The2DCode

RUN pip install -r requirements.txt

WORKDIR /app/Source/

EXPOSE 8501

CMD streamlit run main.py --browser.gatherUsageStats False