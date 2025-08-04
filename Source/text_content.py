__author__ = ["Aleksandar Anžel", "Ihsan Tri Heldian"]
__copyright__ = ""
__credits__ = ["Aleksandar Anžel", "Ihsan Tri Heldian", "Chisom Ezekannagha"]
__license__ = "GNU General Public License v3.0"
__version__ = "1.0.0"
__maintainer__ = "Aleksandar Anžel"
__email__ = "AnzelA@rki.de"
__status__ = "Stable"

# We put the comment below to disable all FLAKE8 "line too long" errors
# flake8: noqa: E501

STRING_CONTACT_PAGE = """
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
"""

STRING_MAIN_BENCHMARK_HELP = (
    ":primary-background["
    "The benchmark dataset includes summarized results for all encoding "
    "methods and benchmark files. This dataset does not differentiate between "
    "the various runs of each encoding method for every benchmark file.]"
)

STRING_DETAILED_HELP = (
    ":primary-background["
    "The detailed dataset contains information on both encoding and decoding "
    "across multiple runs.]"
)

STRING_DENSITY_HELP = (
    ":primary-background["
    "Information Density measures the difference in size between an encoded "
    "file and its original counterpart. For instance, if the original file "
    "consists of 300 bits and encoding it using a specific method produces a "
    "DNA strand of 100 bases (nucleotides), the Information Density would be "
    "3. A higher value indicates that the encoding method can store more data "
    "efficiently, leading to enhanced cost-effectiveness.]"
)

STRING_COST_HELP = (
    ":primary-background["
    "The cost of both encoding and decoding is calculated based on the number "
    "of nucleotides in the encoded file. For synthesis, the lengths of "
    "oligonucleotides are also considered. For sequencing, we default to "
    "using PacBio as the sequencing technology.]"
)

STRING_TIME_HELP = (
    ":primary-background["
    "The time taken for the encoding and decoding processes is measured for "
    "each method and each file. These values should be used only as a "
    "reference, as the implementations of encodings can vary to some degree "
    "depending on the programming language used.]"
)

STRING_SIZE_HELP = (
    ":primary-background["
    "The size of resulting files from encoding and decoding processes.]"
)

STRING_MUTAGENESIS_HELP = (
    ":primary-background["
    "High mutagenesis kit adopted from Press _et al._[1] is used as a "
    "baseline. This baseline translates to an error rate of 3.6% and includes "
    "deletions, insertions, and substitutions. We use the multiplier to "
    "increase or decrease the baseline error rate.] \n\n"
    "\n| Multiplier | Error Rate | "
    + "\n| :--- | :--- | \n| 0 | No errors (0%) | \n| 0.05 | Low (0.18%) | "
    + "\n| 0.1 | Moderately-Low (0.36%) | \n| 0.5 | Moderate (1.8%) | "
    + "\n| 1.0 | Moderately-High (3.6%) | \n| 1.5 | High (5.4%) | \n\n"
    ":primary-background["
    "[1] W.H. Press, J.A. Hawkins, S.K. Jones, J.M. Schaub, I.J. Finkelstein, "
    "HEDGES error-correcting code for DNA storage corrects indels and allows "
    "sequence constraints, Proc. Natl. Acad. Sci. USA 117 (31) 18489-18496, "
    "https://doi.org/10.1073/pnas.2004821117 (2020).]\n"
)

STRING_FAILURE_RATE_HELP = ""  # TODO: Finish this

STRING_BASE_ERROR_HELP = ""  # TODO: Finish this

STRING_ABOUT_PAGE = "\n".join((
    "Welcome to the **Unified DNA Data Storage Encoding Web App**, an open-source platform for standardized, multi-metric evaluation of DNA encoding and decoding methods. Our tool consolidates state-of-the-art codecs into a single dashboard, enabling fair, reproducible comparisons across diverse datasets and criteria.",
    "### Benchmark Parameters",
    "1. **Throughput**",
    "   - **Encoding Speed**: Time (s) to convert a binary file into DNA oligos.",
    "   - **Decoding Speed**: Time (s) to reconstruct binary data from DNA sequences.",
    "2. **Computational Efficiency**",
    "   - **Runtime Complexity**: Measured on identical hardware, to expose sub-quadratic vs. super-quadratic performance.",
    "   - **Energy Efficiency**: Throughput per watt, guiding sustainable deployments.",
    "3. **Error-Correction Efficacy**",
    "   - **Substitution, Insertion & Deletion Recovery**: Fraction of errors corrected by each codec’s built-in clustering and multistrand alignment.",
    "   - **Data Integrity**: Boolean pass/fail comparison against the original binary payload.",
    "4. **Specification Transparency**",
    "   - **Codec Format Compliance**: Adherence to SNIA’s Codec Format Specification v1.0, ensuring future-proof interoperability.",
    "   - **Public Documentation**: Availability of “encode(…)” / “decode(…)” wrappers, input/output formats, and parameter settings.",
    "5. **Biochemical Constraint Adherence**",
    "   - **GC Content**: Percentage of G + C bases (target: 40–60%).",
    "   - **Homopolymer Limits**: Maximum allowed run length (≤ 4 bases).",
    "### How It Works",
    "1. **Select a Baseline or Upload Your File**",
    "Choose from our curated dataset (text, image, audio, video, PDF) or upload any file to convert into a NumPy boolean array.",
    "2. **Pick Encoding Methods**",
    "Run one or more integrated codecs (e.g., HEDGES, DNA Fountain, Raptor, DNA Aeon, Yin-Yang).",
    "3. **Simulate Storage (Optional)**",
    "Specify storage duration to invoke MESA-based degradation simulation.",
    "4. **Review Results**",
    "   - **Summary Table**: Aggregated metrics across runs.",
    "   - **Detailed Table**: Per-file, per-codec breakdown.",
    "   - **Interactive Charts**: Whisker or bar plots for density, runtime, cost.",
    "5. **Export**",
    "   Download CSV tables and SVG/PNG charts for reporting and further analysis.",
    "---",
    "### Supported Encoding Methods",
    " * **Simple Code** by Church _et al._",
    "[DOI: 10.1126/science.1226355](https://www.science.org/doi/10.1126/science.1226355)",
    "* **Repetition Code** by Goldman _et al._",
    "[DOI: 10.1038/nature11875](https://www.nature.com/articles/nature11875)",
    "* **The 2D Code** by Grass _et al._",
    "[DOI: 10.1002/anie.201411378](https://doi.org/10.1002/anie.201411378)",
    "* **XOR-Based Code** by Bornholt _et al._",
    "[DOI: 10.1145/2872362.2872397](https://dl.acm.org/doi/pdf/10.1145/2872362.2872397)",
    "* **DNA-Aeon Code** by Welzel _et al._",
    "[DOI: 10.1038/s41467-023-36297-3](https://doi.org/10.1038/s41467-023-36297-3)",
    "* **Raptor Code** by Shokrollahi _et al._",
    "[DOI: 10.1109/TIT.2006.874390](https://doi.org/10.1109/TIT.2006.874390)",
    "* **LT Code** by Luby _et al._",
    "[DOI: 10.1109/SFCS.2002.1181950](https://doi.org/10.1109/SFCS.2002.1181950)",
    "* **Online Code** by Maymounkov _et al._",
    "[LINK: TR2002-833.pdf](https://cs.nyu.edu/media/publications/TR2002-833.pdf)",
    " ",
    "By harmonizing benchmarking criteria with SNIA’s consensus metrics, this tool empowers researchers and system architects to identify the most suitable DNA storage strategies for their applications.",
))

STRING_INTRODUCTION = "\n".join((
    "## The Unified DNA Encodings Platform",
    " ",
    "The Unified DNA Encoding Platfor is an open-source, modular platform designed to systematically evaluate and compare diverse DNA data storage encoding methods. It harmonizes benchmarking criteria with internationally recognized standards, such as those outlined by the [DNA Data Storage Alliance](https://dnastoragealliance.org/), incorporating key metrics including encoding and decoding throughput, computational efficiency, error-correction effectiveness, specification transparency, and biochemical, constraint adherence. The tool supports batch processing of multiple file formats across various sizes, integrates state-of-the-art and classical encodings via standardized wrappers, and provides comprehensive interactive visualizations and exportable results to facilitate informed selection and optimization of DNA storage strategies.",
    " ",
    "Please cite this work as:",
    "Placeholder.",
    "Unified Evaluation Tool for DNA Data Storage Encodings. [Journal/Repository].",
))
