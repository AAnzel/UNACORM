__author__ = ["Aleksandar Anžel", "Ihsan Tri Heldian"]
__copyright__ = ""
__credits__ = ["Aleksandar Anžel", "Ihsan Tri Heldian", "Chisom Ezekannagha"]
__license__ = "GNU General Public License v3.0"
__version__ = "1.0.0"
__maintainer__ = "Aleksandar Anžel"
__email__ = "AnzelA@rki.de"
__status__ = "Stable"


STRING_CONTACT_PAGE = """
    We appreciate your interest in our project! Here are the best ways to get in touch or contribute.
    ### Project Repository
    Our project is hosted on GitHub. You can find the main repository here:
    GitHub Repository: [github.com/YourUsername/YourProject](https://github.com/YourUsername/YourProject)
    ### Reporting Issues
    If you encounter a bug or have a feature request, please open an issue on our GitHub repository:
    Open an Issue: [github.com/YourUsername/YourProject/issues/new](https://github.com/YourUsername/YourProject/issues/new)
    Before creating a new issue, please check if a similar one already exists.
    ### Contributing
    We welcome contributions! If you would like to contribute to the project:
    1. Fork the repository.
    2. Create a new branch for your feature or bug fix.
    3. Make your changes.
    4. Submit a pull request.
    Create a Pull Request: [github.com/YourUsername/YourProject/compare](https://github.com/YourUsername/YourProject/compare)
    Please review our contribution guidelines before submitting a pull request.
    ### Discussions
    For general questions, ideas, or community discussions, please use our GitHub Discussions forum:
    GitHub Discussions: [github.com/YourUsername/YourProject/discussions](https://github.com/YourUsername/YourProject/discussions)
    ### Project Updates
    Stay updated with our latest releases and announcements:
    Releases: [github.com/YourUsername/YourProject/releases](https://github.com/YourUsername/YourProject/releases)
    ### Additional Contact Information
    For matters not suitable for GitHub, you can reach us at:
    Email: [info@yourproject.com](mailto:info@yourproject.com)
    ### Follow Us
    Stay connected with our project:
    - GitHub: [@YourUsername](https://github.com/YourUsername)
    - Twitter: [@YourProject](https://twitter.com/YourProject)
    ---
    Thank you for your interest in our project! We look forward to your contributions and feedback.
"""
STRING_MAIN_BENCHMARK_HELP = (
    "**The benchmark data set** includes summarized results for all encoding "
    "methods and benchmark files. This data set does not distinguish "
    "between the different runs of each encoding method for every benchmark file."
)
STRING_DETAILED_HELP = (
    "**The detailed data set** contains information on both encoding and decoding "
    "across multiple runs."
)
STRING_DENSITY_HELP = (
    "**Information density** measures the difference in size between an encoded "
    "file and its original counterpart. For example, if the original file "
    "consists of 300 bits and encoding it using a specific method produces a "
    "DNA strand of 100 bases (nucleotides), the information density would be "
    "3. A higher value indicates that the encoding method can store more data "
    "efficiently, resulting in greater cost-effectiveness."
)
STRING_COST_HELP = (
    "**The cost** of both encoding and decoding is calculated based on the number "
    "of nucleotides in the encoded file. For synthesis, the lengths of "
    "oligonucleotides are also considered. For sequencing, we use PacBio "
    "as the default sequencing technology."
)
STRING_TIME_HELP = (
    "**The time** required for the encoding and decoding processes is measured for "
    "each method and each file. These values should be used only as a reference, "
    "since the implementations of encodings may vary depending on the programming language used."
)
STRING_SIZE_HELP = (
    "**The size** of the resulting files from encoding and decoding processes."
)
STRING_MUTAGENESIS_HELP = (
    "**The high mutagenesis** kit adopted from Press et al.[1] is used as a "
    "baseline. This baseline corresponds to an error rate of 3.6% and includes "
    "deletions, insertions, and substitutions. We use the multiplier to "
    "increase or decrease the baseline error rate. \n\n"
    "\n| Multiplier | Error Rate | "
    + "\n| :--- | :--- | \n| 0 | No errors (0%) | \n| 0.05 | Low (0.18%) | "
    + "\n| 0.1 | Moderately low (0.36%) | \n| 0.5 | Moderate (1.8%) | "
    + "\n| 1.0 | Moderately high (3.6%) | \n| 1.5 | High (5.4%) | \n\n"
    "[1] W.H. Press, J.A. Hawkins, S.K. Jones, J.M. Schaub, I.J. Finkelstein, "
    "HEDGES error-correcting code for DNA storage corrects indels and allows "
    "sequence constraints, Proc. Natl. Acad. Sci. USA 117 (31) 18489-18496, "
    "https://doi.org/10.1073/pnas.2004821117 (2020).\n"
)
STRING_SUCCESS_RATE_HELP = (
    "**Success rate** is calculated by assessing the similarity between the "
    "original file and the file that has undergone encoding and decoding "
    "processes. It measures how well the encoding method recovers the original "
    "information. It is calculated for all benchmark runs and all files."
)
STRING_BASE_ERROR_HELP = ""  # TODO: Finish this
STRING_COST_RUNTIME = (
    "**Cost and runtime per error multiplier show** "
    "how much it would cost and how long it would take to encode and decode "
    "benchmark files across all encoding methods and for a selected error multiplier."
)
STRING_ABOUT_PAGE = "\n".join((
    "Welcome to the Unified DNA Data Storage Encoding Web App, an open-source platform for standardized, multi-metric evaluation of DNA encoding and decoding methods. Our tool consolidates state-of-the-art codecs into a single dashboard, enabling fair, reproducible comparisons across diverse data sets and criteria.",
    "### Benchmark Parameters",
    "1. Throughput",
    "   - Encoding Speed: Time (s) to convert a binary file into DNA oligos.",
    "   - Decoding Speed: Time (s) to reconstruct binary data from DNA sequences.",
    "2. Computational Efficiency",
    "   - Runtime Complexity: Measured on identical hardware, to expose sub-quadratic versus super-quadratic performance.",
    "   - Energy Efficiency: Throughput per watt, guiding sustainable deployments.",
    "3. Error-Correction Efficacy",
    "   - Substitution, Insertion, & Deletion Recovery: Fraction of errors corrected by each codec’s built-in clustering and multistrand alignment.",
    "   - Data Integrity: Boolean pass/fail comparison against the original binary payload.",
    "4. Specification Transparency",
    "   - Codec Format Compliance: Adherence to SNIA’s Codec Format Specification v1.0, ensuring future-proof interoperability.",
    "   - Public Documentation: Availability of “encode(…)” / “decode(…)” wrappers, input/output formats, and parameter settings.",
    "5. Biochemical Constraint Adherence",
    "   - GC Content: Percentage of G + C bases (target: 40–60%).",
    "   - Homopolymer Limits: Maximum allowed run length (≤4 bases).",
    "### How It Works",
    "1. Select a Baseline or Upload Your File",
    "Choose from our curated data set (text, image, audio, video, PDF) or upload any file to convert into a NumPy boolean array.",
    "2. Pick Encoding Methods",
    "Run one or more integrated codecs (e.g., HEDGES, DNA Fountain, Raptor, DNA Aeon, Yin-Yang).",
    "3. Simulate Storage (Optional)",
    "Specify storage duration to invoke MESA-based degradation simulation.",
    "4. Review Results",
    "   - Summary Table: Aggregated metrics across runs.",
    "   - Detailed Table: Per-file, per-codec breakdown.",
    "   - Interactive Charts: Whisker or bar plots for density, runtime, and cost.",
    "5. Export",
    "   Download CSV tables and SVG/PNG charts for reporting and further analysis.",
    "---",
    "### Supported Encoding Methods",
    " * Simple Code by Church et al.",
    "[DOI: 10.1126/science.1226355](https://www.science.org/doi/10.1126/science.1226355)",
    "* Repetition Code by Goldman et al.",
    "[DOI: 10.1038/nature11875](https://www.nature.com/articles/nature11875)",
    "* The 2D Code by Grass et al.",
    "[DOI: 10.1002/anie.201411378](https://doi.org/10.1002/anie.201411378)",
    "* XOR-Based Code by Bornholt et al.",
    "[DOI: 10.1145/2872362.2872397](https://dl.acm.org/doi/pdf/10.1145/2872362.2872397)",
    "* DNA-Aeon Code by Welzel et al.",
    "[DOI: 10.1038/s41467-023-36297-3](https://doi.org/10.1038/s41467-023-36297-3)",
    "* Raptor Code by Shokrollahi et al.",
    "[DOI: 10.1109/TIT.2006.874390](https://doi.org/10.1109/TIT.2006.874390)",
    "* LT Code by Luby et al.",
    "[DOI: 10.1109/SFCS.2002.1181950](https://doi.org/10.1109/SFCS.2002.1181950)",
    "* Online Code by Maymounkov et al.",
    "[LINK: TR2002-833.pdf](https://cs.nyu.edu/media/publications/TR2002-833.pdf)",
    " ",
    "By harmonizing benchmarking criteria with SNIA’s consensus metrics, this tool empowers researchers and system architects to identify the most suitable DNA storage strategies for their applications.",
))
STRING_INTRODUCTION = "\n".join((
    "## :primary[UNACORM] :grey[︱] The Unified DNA Encodings Platform",
    "The Unified DNA Encoding Platform is an open-source, modular platform designed to systematically evaluate and compare diverse DNA data storage encoding methods. It harmonizes benchmarking criteria with internationally recognized standards, such as those outlined by the [DNA Data Storage Alliance](https://dnastoragealliance.org/), and incorporates key metrics including encoding and decoding throughput, computational efficiency, error-correction effectiveness, specification transparency, and adherence to biochemical constraints. The tool supports batch processing of multiple file formats across various sizes, integrates state-of-the-art and classical encodings via standardized wrappers, and provides comprehensive interactive visualizations and exportable results to facilitate informed selection and optimization of DNA storage strategies.",
    "Please cite this work as:",
    "```tex",
    "@article{anzel2025unified,",
    "author = {Aleksandar Anžel and Chisom Ezekannagha and Leon Wimbes and Luca Staus and Ihsan Tri Heldian and David Sonnabend and Khawla Elhadri and Samuel Becker and Felix Klein and Raffael Schön and Marius Welzel and Michael Schwarz and Dominik Heider and Georges Hattab},",
    "title = {A Unified Evaluation Tool for DNA Data Storage Encodings},",
    "journal = {Journal Name},",
    "year = {2025},",
    "doi = {[DOI LINK]},",
    "}",
    "```",
))
STRING_FOOTER = "\n".join((
    "Aleksandar Anžel, Chisom Ezekannagha, Leon Wimbes, Luca Staus, Ihsan Tri Heldian, David Sonnabend, Khawla Elhadri, Samuel Becker, Felix Klein, Raffael Schön, Marius Welzel, Michael Schwarz, Dominik Heider, and Georges Hattab (2025)",
    "<br>",
    "<i>A Unified Evaluation Tool for DNA Data Storage Encodings</i>",
    "<br>",
    "Journal Name. [DOI LINK].",
))
