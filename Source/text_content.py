__author__ = ["Aleksandar Anžel", "Ihsan Tri Heldian"]
__copyright__ = ""
__credits__ = ["Aleksandar Anžel", "Ihsan Tri Heldian", "Chisom Ezekannagha"]
__license__ = "GNU General Public License v3.0"
__version__ = "1.0.0"
__maintainer__ = "Aleksandar Anžel"
__email__ = "AnzelA@rki.de"
__status__ = "Stable"


STRING_CONTACT_PAGE_0 = """
    We appreciate your interest in our project! Here are the best ways to get in touch or contribute.
    """
STRING_CONTACT_PAGE_1 = """
    #### Go To Project Repository
    Our project is hosted and maintained on GitHub."""

STRING_CONTACT_PAGE_2 = """
    #### Report Issues
    If you encounter a bug or have a feature request, please open an issue on our GitHub repository.
    Before creating a new issue, please check if a similar one already exists.
    """

STRING_CONTACT_PAGE_3 = """
    #### Contribute
    We welcome contributions! If you would like to contribute to the project please review our [contribution guidelines](https://github.com/AAnzel/UNACORM/blob/master/CONTRIBUTE.md) before submitting a pull request.
    """

STRING_CONTACT_PAGE_4 = """
    #### Discuss
    For general questions, ideas, or community discussions, please use our GitHub Discussions forum.

    """

STRING_CONTACT_PAGE_5 = """
    #### Stay Up To Date
    Stay updated with our latest releases and announcements.
    """

STRING_CONTACT_PAGE_6 = """
    #### Get More Info
    For matters not suitable for GitHub, you can reach us via e-mail.
    """

STRING_MAIN_BENCHMARK_HELP = (
    "**The benchmark data set** includes summarized results for all coding "
    "schemes and benchmark files. This data set does not distinguish "
    "between the different runs of each coding schemes for every benchmark file."
)
STRING_DETAILED_HELP = (
    "**The detailed data set** contains information on both encoding and decoding "
    "across multiple runs."
)
STRING_DENSITY_HELP = (
    "**Information density** measures the difference in size between an encoded "
    "file and its original counterpart. For example, if the original file "
    "consists of 300 bits and encoding it using a specific scheme produces a "
    "DNA strand of 100 bases (nucleotides), the information density would be "
    "3. A higher value indicates that the codec can store more data "
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
    "since the implementations of coding schemes may vary depending on the programming language used."
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
    "processes. It measures how well the coding scheme recovers the original "
    "information. It is calculated for all benchmark runs and all files."
)
STRING_BASE_ERROR_HELP = (
    "**Base Error** is calculated by plotting a percentage of successful "
    "decoding attempts for a given base error ratio using the proportions of "
    "substitutions, deletions and insertions described in (high mutagenesis by "
    "Press et al.[1]), with a multiplier between 0.0 and 2.5. We show only "
    "the last ratio, in which the code had a 100% success rate "
    "(out of 5 repetitions) and up until the first time, the code had a zero "
    "percent success rate\n\n"
    "[1] W.H. Press, J.A. Hawkins, S.K. Jones, J.M. Schaub, I.J. Finkelstein, "
    "HEDGES error-correcting code for DNA storage corrects indels and allows "
    "sequence constraints, Proc. Natl. Acad. Sci. USA 117 (31) 18489-18496, "
    "https://doi.org/10.1073/pnas.2004821117 (2020).\n"
)
STRING_COST_RUNTIME = (
    "**Cost and runtime per error multiplier show** "
    "how much it would cost and how long it would take to encode and decode "
    "benchmark files across all coding schemes and for a selected error multiplier."
)
STRING_ABOUT_PAGE_0 = (
    "The Unified DNA Codecs Platform is an open-source "
    "web application for standardized, multi-metric evaluation of DNA "
    "encoding and decoding schemes. Our tool consolidates state-of-the-art "
    "methods into a single dashboard, enabling fair, reproducible comparisons "
    "across diverse data sets and criteria. The image below gives an overview "
    "of the DNA encoding and decoding processes for storing digital data."
)

STRING_ABOUT_PAGE_1 = "\n".join((
    "### Evaluation Parameters",
    "Consistent with the codec [guidelines of the DNA Data Storage Alliance](https://www.snia.org/sites/default/files/DNA/SNIA-DNA-Data-Storage-Codecs-v1.0.pdf) and supported by recent comparative studies, our evaluation of each codec is conducted across the following quantitative metrics.",
    "1. Throughput",
    "   - Encoding Speed: Time (s) to convert a binary file into DNA oligos.",
    "   - Decoding Speed: Time (s) to reconstruct binary data from DNA sequences.",
    "2. Computational Efficiency",
    "   - Runtime Complexity: Measured on identical hardware, to expose sub-quadratic versus super-quadratic performance.",
    "   - Energy Efficiency: Throughput per watt, guiding sustainable deployments.",
    "3. Error-Correction Efficacy",
    "   - Substitution, Insertion, & Deletion Recovery: Fraction of errors corrected by each method's built-in clustering and multistrand alignment.",
    "   - Data Integrity: Boolean pass/fail comparison against the original binary payload.",
    "4. Specification Transparency",
    "   - Method's Format Compliance: Adherence to DNA Data Storage Allieance's [Format Specification v1.0](https://www.snia.org/sites/default/files/DNA/SNIA-DNA-Data-Storage-Codecs-v1.0.pdf), ensuring future-proof interoperability.",
    "   - Public Documentation: Availability of “encode(…)” / “decode(…)” wrappers, input/output formats, and parameter settings.",
))
#    "5. Biochemical Constraint Adherence",
#    "   - GC Content: Percentage of G + C bases (target: 40–60%).",
#    "   - Homopolymer Limits: Maximum allowed run length (≤4 bases).",


STRING_ABOUT_PAGE_2 = "\n".join((
    "### How It Works",
    "1. Select a Baseline or Upload Your File",
    "Choose from our curated data set (text, image, audio, video, PDF) or upload any file to convert into a NumPy boolean array.",
    "2. Pick Coding Schemes (Codecs)",
    "Run one or more integrated methods (e.g., HEDGES, DNA Fountain, Raptor, DNA Aeon, Yin-Yang).",
    "3. Simulate Storage (Optional)",
    "Specify storage duration to invoke MESA-based degradation simulation.",
    "4. Review Results",
    "   - Summary Table: Aggregated metrics across runs.",
    "   - Detailed Table: Per-file, per-method breakdown.",
    "   - Interactive Charts: Whisker or bar plots for density, runtime, and cost.",
    "5. Export",
    "   Download CSV tables and SVG/PNG charts for reporting and further analysis.",
))

STRING_ABOUT_PAGE_3 = "\n".join((
    "### Benchmark Data Set Analysis",
    "To comprehensively assess the effectiveness of DNA data storage coding schemes, our platform employed a varied collection of benchmark files. The collection included two text files, three images, two audio files, one video, and one document, intentionally chosen to cover a wide range of file types and content typically found in digital storage.",
    "The two images below illustrate the sizes, entropies, and byte distributions of the benchmark files.",
    "#### Summary Information",
))

STRING_ABOUT_PAGE_4 = "#### Byte Density Histograms"

STRING_ABOUT_PAGE_5 = "\n".join((
    "### Supported Coding Schemes (Codecs)",
    "Our platform currently implements eight DNA coding schemes, as shown in the table below. Future work will focus on incorporating additional relevant methods that were beyond the scope of the initial analysis.",
    "| DNA Codec |  Publication | Authors | Reimplemented by | Repository of the Reimplementation |",
    "|---|---|---|---|---|",
    "| Simple Code | [10.1126/science.1226355](https://doi.org/10.1126/science.1226355) | George M. Church, Yuan Gao, and Sriram Kosuri | Khawla Elhadri | [https://github.com/ke-pm/DNA-Encoding](https://github.com/ke-pm/DNA-Encoding) |",
    "| 2D Code | [10.1002/anie.201411378](https://doi.org/10.1002/anie.201411378) | Robert N. Grass, Reinhard Heckel, Michela Puddu, Daniela Paunescu, and Wendelin J. Stark | Samuel Becker, Felix Klein, and Raffael Schön | [https://github.com/raeudigerRaeffi/reedSolomonDNA](https://github.com/raeudigerRaeffi/reedSolomonDNA) |",
    "| XOR-based Code | [10.1145/2872362.2872397](https://doi.org/10.1145/2872362.2872397) | James Bornholt, Randolph Lopez, Douglas M. Carmean, Luis Ceze, Georg Seelig, and Karin Strauss | Leon Wimbes, and Luca Staus | [https://github.com/StausWimbes/XOR_based_DNA_encoding](https://github.com/StausWimbes/XOR_based_DNA_encoding) |",
    "| Repetition Code | [10.1038/nature11875](https://doi.org/10.1038/nature11875) | Nick Goldman, Paul Bertone, Siyuan Chen, Christophe Dessimoz, Emily M. LeProust, Botond Sipos, and Ewan Birney | David Sonnabend | [https://github.com/davidabendsonn/DNAencoding-Goldman2013](https://github.com/davidabendsonn/DNAencoding-Goldman2013) |",
    "| DNA-Aeon | [10.1038/s41467-023-36297-3](https://doi.org/10.1038/s41467-023-36297-3) | Marius Welzel, Peter Michael Schwarz, Hannah F. Löchel, Tolganay Kabdullayeva, Sandra Clemens, Anke Becker, Bernd Freisleben, and Dominik Heider | Marius Welzel | [https://github.com/MW55/DNA-Aeon/tree/main](https://github.com/MW55/DNA-Aeon/tree/main)|",
    "| RaptorCode | [10.1109/TIT.2006.874390](https://doi.org/10.1109/TIT.2006.874390) | Amin Shokrollahi | Peter Michael Schwarz | [https://github.com/umr-ds/NOREC4DNA/tree/dev/unified](https://github.com/umr-ds/NOREC4DNA/tree/dev/unified) |",
    "| LTCode | [10.1109/SFCS.2002.1181950](https://doi.org/10.1109/SFCS.2002.1181950) | Michael Luby | Peter Michael Schwarz | [https://github.com/umr-ds/NOREC4DNA/tree/dev/unified](https://github.com/umr-ds/NOREC4DNA/tree/dev/unified) |",
    "| OnlineCode | [TR2002-833.pdf](https://cs.nyu.edu/media/publications/TR2002-833.pdf) | Petar Maymounkov | Peter Michael Schwarz | [https://github.com/umr-ds/NOREC4DNA/tree/dev/unified](https://github.com/umr-ds/NOREC4DNA/tree/dev/unified) |",
))

STRING_ABOUT_PAGE_6 = "\n".join((
    "#### Codecs' Parameters",
    "- **Repetition code**: No parameters.",
    "- **Simple code**: Default parameters — a segment length of 12 bytes, with the maximum number of 'oligos' set to (2^{19} = 524,288).",
    "- **2D code**: Default parameters —",
    "  **(a)** In the inner encoder, the Galois field size (p) is 47, the message length is 39, the payload length is 33, the symbol size is 1, and the p-factor is 2.",
    "  **(b)** In the outer encoder, the Galois field size (p) is 47, the message length is 713, the payload length is 594, the symbol size is 30, and the p-factor is 7.",
    "- **XOR-based code**: Default parameters — 12 nucleotides per primer, a maximum of 6 nucleotides per byte, the minimum strand length follows the equation (27 + (10 x MAX_NUCLEOTIDES_PER_BYTE)), the maximum payload index gap and the minimum number of larger payloads are 10, and the minimum XOR size and step are 2 and 1, respectively.",
    "- **Raptor code**: Overhead value is 0.2, headers are included, the upper bound threshold for dropping packets is 1, chunk size is 100, seed value is 2, and 2 repair symbols are used.",
    "- **Online code**: Same parameters as Raptor code, with additional parameters: epsilon at 0.19 and quality value at 7.",
    "- **LT code**: Same as Raptor code, but with the upper bound threshold for dropping packets changed to 0.9, and an implicit mode set to enabled.",
    "- **DNA-Aeon code**: Default parameters — chunk size is 100, the error detection algorithm is 'crc' with a header length of 8, and the package redundancy value is set to 0.4.",
    "",
    ":primary-background[Additional, less relevant parameters are available in the GitHub repository.]",
))

STRING_INTRODUCTION = "\n".join((
    "## :primary[UNACORM] :grey[︱] The Unified DNA Codecs Platform",
    "The Unified DNA Codecs Platform is an open-source, modular platform designed to systematically evaluate and compare diverse DNA data storage coding schemes (codecs). It harmonizes benchmarking criteria with internationally recognized standards, such as those outlined by the [DNA Data Storage Alliance](https://dnastoragealliance.org/), and incorporates key metrics including encoding and decoding throughput, computational efficiency, error-correction effectiveness, specification transparency, and adherence to biochemical constraints. The tool supports batch processing of multiple file formats across various sizes, integrates state-of-the-art and classical codecs via standardized wrappers, and provides comprehensive interactive visualizations and exportable results to facilitate informed selection and optimization of DNA storage strategies.",
    "Please cite this work as:",
    "```tex",
    "@article{anzel2026unified,",
    "author = {Aleksandar Anžel and Chisom Ezekannagha and Leon Wimbes and Luca Staus and Ihsan Tri Heldian and David Sonnabend and Khawla Elhadri and Samuel Becker and Felix Klein and Raffael Schön and Marius Welzel and Michael Schwarz and Bernd Freisleben and Dominik Heider and Georges Hattab},",
    "title = {The Unified Evaluation Tool for DNA Data Storage Codecs},",
    "journal = {Journal Name},",
    "year = {2026},",
    "doi = {[DOI LINK]},",
    "}",
    "```",
))
STRING_FOOTER = "\n".join((
    "Aleksandar Anžel, Chisom Ezekannagha, Leon Wimbes, Luca Staus, Ihsan Tri Heldian, David Sonnabend, Khawla Elhadri, Samuel Becker, Felix Klein, Raffael Schön, Marius Welzel, Michael Schwarz, Bernd Freisleben, Dominik Heider, and Georges Hattab (2026)",
    "<br>",
    "<i>The Unified Evaluation Tool for DNA Data Storage Codecs</i>",
    "<br>",
    "Journal Name. [DOI LINK].",
))
