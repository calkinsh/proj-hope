

"""
Auto-generated extract config module.
See documentation at
https://kids-first.github.io/kf-lib-data-ingest/tutorial/extract.html for
information on writing extract config files.
"""

import re
from pathlib import Path

from kf_lib_data_ingest.common import constants  # noqa F401
from kf_lib_data_ingest.common.concept_schema import CONCEPT
from kf_lib_data_ingest.common.misc import import_module_from_file
from kf_lib_data_ingest.etl.extract.operations import (
    constant_map,
    keep_map,
    value_map,
)

# replace this with the source once I upload it to data tracker
source_data_url="https://kf-api-study-creator.kidsfirstdrc.org/download/study/SD_BHJXBDQK/file/SF_1T414W8K/version/FV_RXNAJ4JC"

# TODO (Optional) Fill in special loading parameters here
source_data_read_params = {"sheet_name": "SequencingExperiment_rm_bad_ali"}


# TODO - Replace this with operations that make sense for your own data file
operations = [
    keep_map(
        in_col="external_id", 
        out_col=CONCEPT.SEQUENCING.ID, 
    ),

    keep_map(
        in_col="experiment_strategy", 
        out_col=CONCEPT.SEQUENCING.STRATEGY, 
    ),

    keep_map(
        in_col="library_name", 
        out_col=CONCEPT.SEQUENCING.LIBRARY_NAME, 
    ),

    keep_map(
        in_col="sequencing_center", 
        out_col=CONCEPT.SEQUENCING.CENTER.TARGET_SERVICE_ID, 
    ),
    constant_map(
        m=constants.SEQUENCING.PLATFORM.ILLUMINA, 
        out_col=CONCEPT.SEQUENCING.PLATFORM
    )
]