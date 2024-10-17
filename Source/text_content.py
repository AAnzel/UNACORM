__author__ = ['Aleksandar Anžel', 'Ihsan Tri Heldian']
__copyright__ = ''
__credits__ = ['Aleksandar Anžel', 'Ihsan Tri Heldian', 'Chisom Ezekannagha']
__license__ = 'GNU General Public License v3.0'
__version__ = '1.0.0'
__maintainer__ = 'Aleksandar Anžel'
__email__ = 'AnzelA@rki.de'
__status__ = 'Stable'

# We put the comment below to disable all FLAKE8 "line too long" errors
# flake8: noqa: E501

STRING_CONTACT_PAGE = '''
    We appreciate your interest in our project! Here are the best ways to get in touch or contribute.

    ### Project Repository

    Our project is hosted on GitHub. You can find the main repository here:

    **GitHub Repository:** [github.com/YourUsername/YourProject](https://github.com/YourUsername/YourProject)

    ### Reporting Issues

    If you've encountered a bug or have a feature request, please open an issue on our GitHub repository:

    **Open an Issue:** [github.com/YourUsername/YourProject/issues/new](https://github.com/YourUsername/YourProject/issues/new)

    Before creating a new issue, please check if a similar one already exists.

    ### Contributing

    We welcome contributions! If you'd like to contribute to the project:

    1. Fork the repository
    2. Create a new branch for your feature or bug fix
    3. Make your changes
    4. Submit a pull request

    **Create a Pull Request:** [github.com/YourUsername/YourProject/compare](https://github.com/YourUsername/YourProject/compare)

    Please review our contribution guidelines before submitting a pull request.

    ### Discussions

    For general questions, ideas, or community discussions, please use our GitHub Discussions forum:

    **GitHub Discussions:** [github.com/YourUsername/YourProject/discussions](https://github.com/YourUsername/YourProject/discussions)

    ### Project Updates

    Stay updated with our latest releases and announcements:

    **Releases:** [github.com/YourUsername/YourProject/releases](https://github.com/YourUsername/YourProject/releases)

    ### Additional Contact Information

    For matters not suitable for GitHub, you can reach us at:

    **Email:** [info@yourproject.com](mailto:info@yourproject.com)

    ### Follow Us

    Stay connected with our project:

    - **GitHub:** [@YourUsername](https://github.com/YourUsername)
    - **Twitter:** [@YourProject](https://twitter.com/YourProject)

    ---

    Thank you for your interest in our project! We look forward to your contributions and feedback.
'''

STRING_ABOUT_PAGE = '''
    * **Simple Code** by Church _et al._
    [DOI: 10.1126/science.1226355](https://www.science.org/doi/10.1126/science.1226355)

    * **Repetition Code** by Goldman _et al._
    [DOI: 10.1038/nature11875](https://www.nature.com/articles/nature11875)

    * **The 2D Code** by Grass _et al._
    [DOI: 10.1002/anie.201411378](https://doi.org/10.1002/anie.201411378)

    * **XOR-Based Code** by Bornholt _et al._
    [DOI: 10.1145/2872362.2872397](https://dl.acm.org/doi/pdf/10.1145/2872362.2872397)

    * **DNA-Aeon Code** by Welzel _et al._
    [DOI: 10.1038/s41467-023-36297-3](https://doi.org/10.1038/s41467-023-36297-3)

    * **Raptor Code** by Shokrollahi _et al._
    [DOI: 10.1109/TIT.2006.874390](https://doi.org/10.1109/TIT.2006.874390)

    * **LT Code** by Luby _et al._
    [DOI: 10.1109/SFCS.2002.1181950](https://doi.org/10.1109/SFCS.2002.1181950)

    * **Online Code** by Maymounkov _et al._
    [LINK: TR2002-833.pdf](https://cs.nyu.edu/media/publications/TR2002-833.pdf)
'''

STRING_MAIN_BENCHMARK_HELP = '''
    The benchmark dataset includes summarized results for all encoding methods 
    and benchmark files. This dataset does not differentiate between the various 
    runs of each encoding method for every benchmark file.
'''

STRING_DETAILED_HELP = '''
    The detailed dataset contains information on both encoding and decoding 
    across multiple runs.
'''

STRING_MULTIPLIER_HELP = '''
    The File Size Multiplier defines how much the size of the encoded file 
    differs from the original file size. For example, if the original file size 
    is 100 kB and encoding the file using a certain method produces a file 
    size of 200 kB, then the File Size Multiplier is 2, indicating that the 
    encoded file has doubled in size.
'''

STRING_COST_HELP = '''
    The cost of both encoding and decoding is calculated based on the number 
    of nucleotides in the encoded file. For synthesis, the lengths of 
    oligonucleotides are also considered. For sequencing, we default to using 
    PacBio as the sequencing technology.
'''

STRING_TIME_HELP = '''
    The time taken for the encoding and decoding processes is measured for each 
    method and each file. These values should be used only as a reference, as 
    the implementations of encodings can vary to some degree depending on the 
    programming language used.
'''

STRING_SIZE_HELP = '''
    The size of resulting files from encoding and decoding processes.
'''