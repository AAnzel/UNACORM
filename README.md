Badges Placeholder

# UNACORM --- DNA Encodings

**The Unified DNA Encodings Platform**

## Manuscript

This tool is created for the following paper:

***"A Unified Evaluation Tool for DNA Storage Codes"*** by Chisom Ezekannagha^, Aleksandar Anžel^, Leon Wimbes, Luca Staus, Ihsan Tri Heldian, David Sonnabend, Khawla Elhadri, Samuel Becker, Felix Klein, Raffael Schön, Marius Welzel, Michael
Schwarz, Dominik Heider, and Georges Hattab

^ --- These authors contributed equally to this work

Please cite the paper as:
```latex
bibtex placeholder
```

DOI badge Placeholder

---
Abstract:

> Abstract placeholder


## Dependancies

The code is written in Python 3.12.2 and tested on Linux with the libraries included in the following Anaconda environment: [environment.yml](environment.yml). Some DNA encoding methods have their own dependencies, located in the following files:
* [Source/Encodings/XORBasedCode/requirements.txt](Source/Encodings/XORBasedCode/requirements.txt)
* [Source/Encodings/The2DCode/requirements.txt](Source/Encodings/The2DCode/requirements.txt)
* [Source/Encodings/RaptorCode/requirements.txt](Source/Encodings/RaptorCode/requirements.txt)


## Data

| Location | Description |
|---|---|
| [Data/](Data/) | contains all data used to evaluate encodings and store intermediary data representations |
| [Data/Original/](Data/Original/) | contains the original data used to benchmark all encodings |
| [Data/Encoded/](Data/Encoded/) | the directory is empty and used only when benchmarking encoding methods to save the encoded original data |
| [Data/Decoded/](Data/Decoded/) | the directory is empty and used only when benchmarking encoding methods to save the decoded previously encoded data |
| [Data/Uploaded/](Data/Uploaded/) | the directory is empty and used only for storing user-uploaded data |
| [Data/cache_data/](Data/cache_data/) | contains cached data |
| [Data/cache_data/pre_detail.pkl](Data/cache_data/pre_detail.pkl) | contains cached benchmark data of 10 runs for each DNA encoding and each original file |
| [Data/cache_data/pre_summary.pkl](Data/cache_data/pre_detail.pkl) | contains cached benchmark data that represents the summary of [Data/cache_data/pre_detail.pkl](Data/cache_data/pre_detail.pkl) aggregated across runs |
| [Data/cache_data/huff3.dict](Data/cache_data/huff3.dict) | contains cached codebook for the 2D code |

The cached benchmark data can be re-calculated using [Source/precalculation.py](/Source/precalculation.py) script and the following command:

```bash
# The user should be placed inside the Source/ directory
streamlit run precalculation.py
```

The data located in [Data/Original/](Data/Original/) was used to test and benchmark all DNA encoding methods. The directory contains the following files:

| Type | Location | Source |
|---|---|---|
| TXT | [Data/Original/Around_the_World_in_Eighty_Days.txt](Data/Original/Around_the_World_in_Eighty_Days.txt) | [https://www.gutenberg.org/ebooks/103](https://www.gutenberg.org/ebooks/103)
| TXT | [Data/Original/The_Picture_of_Dorian_Gray.txt](Data/Original/The_Picture_of_Dorian_Gray.txt) | [https://www.gutenberg.org/ebooks/174](https://www.gutenberg.org/ebooks/174)
| MP3 | [Data/Original/bbc_clock.mp3](Data/Original/bbc_clock.mp3) | [https://sound-effects.bbcrewind.co.uk/search?q=07002136](https://sound-effects.bbcrewind.co.uk/search?q=07002136)
| WAV | [Data/Original/bbc_peregrine_falcon.wav](Data/Original/bbc_peregrine_falcon.wav) | [https://sound-effects.bbcrewind.co.uk/search?q=NHU05015024](https://sound-effects.bbcrewind.co.uk/search?q=NHU05015024)
| JPG | [Data/Original/Vue_de_la_Buena_Vista.jpg](Data/Original/Vue_de_la_Buena_Vista.jpg) | [Wikimedia](https://commons.wikimedia.org/w/index.php?title=File:Les_merveilles_de_l%27industrie,_1873_%22Vue_de_la_Buena_Vista,_plantation_de_Don_Justo_Cantero,_dnas_l%27ille_de_Cuba%22_(4727225688).jpg&oldid=889592425)
| PNG | [Data/Original/all_black.png](Data/Original/all_black.png) | Created
| PDF | [Data/Original/Zero_File.pdf](Data/Original/Zero_File.pdf) | Created
| GIF | [Data/Original/nature.gif](Data/Original/nature.gif) | [https://pixabay.com/gifs/nature-autumn-landscapes-orange-3507/](https://pixabay.com/gifs/nature-autumn-landscapes-orange-3507/)
| MP4 | [Data/Original/egypt.mp4](Data/Original/egypt.mp4) | [https://pixabay.com/videos/desert-sand-egypt-culture-131220/](https://pixabay.com/videos/desert-sand-egypt-culture-131220/)



## Code
| Location | Description |
|---|---|
| [Source/](Source/) | contains all scripts necessary to run the tool |
| [Source/Encodings](Source/Encodings) | contains all DNA encodings, each in its own separate directory |
| [Source/main.py](/Source/main.py) | contains the code that builds the main layout and connects all pages of the platform's dashboard |
| [Source/utilities.py](/Source/utilities.py) | contains the code that implements main functionalities of the platform |
| [Source/visualize.py](/Source/visualize.py) | contains the code that implements visualization functionalities of the platform |
| [Source/text_content.py](/Source/text_content.py) | contains only various markdown strings that are used to build some pages or provide help tootlips |
| [Source/precalculation.py](/Source/precalculation.py) | contains the code that precalculates the benchmark files [Data/cache_data/pre_detail.pkl](Data/cache_data/pre_detail.pkl) and [Data/cache_data/pre_summary.pkl](Data/cache_data/pre_summary.pkl) |
| [Source/mesa_call.py](/Source/mesa_call.py) | contains the code that implements [MESA](https://mesa.mosla.de/) API calls using  [Source/mesa.json](/Source/mesa.json) configuration |

We would like to thank the authors of the encoding methods (located at [Source/Encodings](Source/Encodings)) for helping us integrate them into our platform. We acknowledge their contributions in the table below.

| Location | Authors | Reimplemented by | Repository of the Reimplementation | Publication |
|---|---|---|---|---|
| [Simple Code](Source/Encodings/SimpleCode/) | George M. Church, Yuan Gao, and Sriram Kosuri | Khawla Elhadri | [https://github.com/ke-pm/DNA-Encoding](https://github.com/ke-pm/DNA-Encoding) | [10.1126/science.1226355](https://doi.org/10.1126/science.1226355) | 
| [2D Code](Source/Encodings/The2DCode) | Robert N. Grass, Reinhard Heckel, Michela Puddu, Daniela Paunescu, and Wendelin J. Stark | Samuel Becker, Felix Klein, and Raffael Schön | [https://github.com/raeudigerRaeffi/reedSolomonDNA](https://github.com/raeudigerRaeffi/reedSolomonDNA) | [10.1002/anie.201411378](https://doi.org/10.1002/anie.201411378) |
| [XOR-based Code](Source/Encodings/XORBasedCode) | James Bornholt, Randolph Lopez, Douglas M. Carmean, Luis Ceze, Georg Seelig, and Karin Strauss | Leon Wimbes, and Luca Staus | [https://github.com/StausWimbes/XOR_based_DNA_encoding](https://github.com/StausWimbes/XOR_based_DNA_encoding) | [10.1145/2872362.2872397](https://doi.org/10.1145/2872362.2872397) |
| [Repetition Code](Source/Encodings/RepetitionCode) | Nick Goldman, Paul Bertone, Siyuan Chen, Christophe Dessimoz, Emily M. LeProust, Botond Sipos, and Ewan Birney | David Sonnabend | [https://github.com/davidabendsonn/DNAencoding-Goldman2013](https://github.com/davidabendsonn/DNAencoding-Goldman2013) | [10.1038/nature11875](https://doi.org/10.1038/nature11875) |
| [DNA-Aeon](Source/Encodings/DNA-Aeon) | Marius Welzel, Peter Michael Schwarz, Hannah F. Löchel, Tolganay Kabdullayeva, Sandra Clemens, Anke Becker, Bernd Freisleben, and Dominik Heider | Marius Welzel | [https://github.com/MW55/DNA-Aeon/tree/main](https://github.com/MW55/DNA-Aeon/tree/main)| [10.1038/s41467-023-36297-3](https://doi.org/10.1038/s41467-023-36297-3) |
| [RaptorCode](Source/Encodings/RaptorCode) | Amin Shokrollahi | Peter Michael Schwarz | [https://github.com/umr-ds/NOREC4DNA/tree/dev/unified](https://github.com/umr-ds/NOREC4DNA/tree/dev/unified) | [10.1109/TIT.2006.874390](https://doi.org/10.1109/TIT.2006.874390) |
| [LTCode](Source/Encodings/LTCode) | Michael Luby | Peter Michael Schwarz | [https://github.com/umr-ds/NOREC4DNA/tree/dev/unified](https://github.com/umr-ds/NOREC4DNA/tree/dev/unified) | [10.1109/SFCS.2002.1181950](https://doi.org/10.1109/SFCS.2002.1181950) |
| [OnlineCode](Source/Encodings/OnlineCode) | Petar Maymounkov | Peter Michael Schwarz | [https://github.com/umr-ds/NOREC4DNA/tree/dev/unified](https://github.com/umr-ds/NOREC4DNA/tree/dev/unified) | [TR2002-833.pdf](https://cs.nyu.edu/media/publications/TR2002-833.pdf) |

## Installation & Running
### Docker
The easiest way to install the tool is to use our latest Docker image by building a docker container and running it locally.  Below is a sequence of instructions (for Linux-based systems) to run the container:

```bash
# How to build the docker container and run it locally

git clone https://github.com/AAnzel/DNA_Encodings.git
cd DNA_Encodings/
docker build -t dna-encodings-local:stable .
docker run --publish 8501:8501 --detach --name dna-encodings-local dna-encodings-local:stable
```

You can start using the tool by opening a web browser and typing in [http://localhost:8501/](http://localhost:8501/) as the address. If you run the docker container, you have to use the IP address or hostname instead of localhost.

### Conda Environment
The platform can also be installed without the docker container. This process requires users to install Anaconda or Miniconda package managers. Users can install Conda using the instructions on the following link [https://docs.anaconda.com/miniconda/#quick-command-line-install](https://docs.anaconda.com/miniconda/#quick-command-line-install). If Conda is installed, the following sequence of instructions (for Linux-based systems) installs all dependencies and runs the dashboard:

```bash
git clone https://github.com/AAnzel/DNA_Encodings.git
cd DNA_Encodings/
conda env create -f environment.yml
conda activate dna_project_env
pip install -r Source/Encodings/XORBasedCode/requirements.txt
pip install -r Source/Encodings/The2DCode/requirements.txt
pip install -r Source/Encodings/RaptorCode/requirements.txt
cd Source/Encodings/XORBasedCode
python setup.py install
cd ../RaptorCode
python setup.py install
cd ../DNA_Aeon
python setup.py
cd ../../
streamlit run main.py
```

Every subsequent run of the tool after restarting the terminal emulator session requires activating the installed conda environment and running the dashboard. The following sequence of instructions defines that process:

```bash
conda activate dna_project_env
streamlit run main.py
```

## License

Licensed under the GNU General Public License, Version 3.0 ([LICENSE](./LICENSE) or https://www.gnu.org/licenses/gpl-3.0.en.html)

### Contribution

Any contribution intentionally submitted for inclusion in the work by you, shall be licensed under the GNU GPLv3.

