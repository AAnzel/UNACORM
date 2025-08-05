import glob
import os

import pandas as pd
from utilities import (
    PATH_INTERMEDIARY_DETAIL,
    PATH_INTERMEDIARY_SUMMARY,
    PATH_PARTIAL_RESULTS,
    df_generate_summary,
)

__author__ = ["Aleksandar Anžel", "Ihsan Tri Heldian"]
__copyright__ = ""
__credits__ = ["Aleksandar Anžel", "Ihsan Tri Heldian", "Chisom Ezekannagha"]
__license__ = "GNU General Public License v3.0"
__version__ = "1.0.0"
__maintainer__ = "Aleksandar Anžel"
__email__ = "AnzelA@rki.de"
__status__ = "Stable"

# Adjust paths/patterns as needed
PATH_PARTIAL_DETAIL_PATTERN = os.path.join(
    PATH_PARTIAL_RESULTS, "*.part_detail.pkl"
)


def merge_details_and_generate_summary():
    partial_detail_files = glob.glob(PATH_PARTIAL_DETAIL_PATTERN)

    if not partial_detail_files:
        print("No partial detail pickle files found to merge.")
        return

    # Load and concatenate partial detail dataframes
    detail_dfs = [pd.read_pickle(f) for f in partial_detail_files]
    merged_detail = pd.concat(detail_dfs, ignore_index=True)

    # Save the merged detail dataframe
    merged_detail.to_pickle(PATH_INTERMEDIARY_DETAIL)
    print(f"Merged detail pickle saved to {PATH_INTERMEDIARY_DETAIL}")

    # Generate a summary dataframe from the merged detail
    merged_summary = df_generate_summary(merged_detail)

    # Save the generated summary dataframe
    merged_summary.to_pickle(PATH_INTERMEDIARY_SUMMARY)
    print(f"Summary pickle generated and saved to {PATH_INTERMEDIARY_SUMMARY}")


if __name__ == "__main__":
    merge_details_and_generate_summary()
