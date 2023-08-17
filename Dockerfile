# syntax=docker/dockerfile:1

FROM continuumio/miniconda3
ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"

RUN apt update
RUN apt install -y fontconfig gcc clang clang-tools cmake
RUN export PATH=~/anaconda3/bin:$PATH

WORKDIR .

RUN export FONTCONFIG_FILE=/etc/fonts/fonts.conf
RUN export FONTCONFIG_PATH=/etc/fonts/
RUN export FILECONFIG_PATH=/etc/fonts

RUN conda install --yes \
        python==3.9.17 \
        numpy==1.25.2 \
        pandas==1.5.3 \
        scikit-learn==1.3.0 \
        scipy==1.11.1 \
        protobuf==3.20.3 \
        openpyxl==3.0.10

RUN conda config --add channels conda-forge

RUN conda install --yes \
        altair==5.0.1 \
        bitarray==2.5.1 \
        streamlit==1.24.1

RUN conda clean --all --yes

RUN mkdir DNA_Encodings

WORKDIR ./DNA_Encodings/

COPY . .

WORKDIR ./Source/Encodings/XORBasedCode/

RUN rm -r build/

RUN pip install .

WORKDIR ../../

EXPOSE 8501

CMD streamlit run main.py --browser.gatherUsageStats False

