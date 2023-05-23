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
source_data_read_params = {"sheet_name": "Biospecimen"}


# TODO - Replace this with operations that make sense for your own data file
operations = [

    keep_map(
        in_col="sequencing_center", 
        out_col=CONCEPT.SEQUENCING.CENTER.TARGET_SERVICE_ID, 
    ),

    keep_map(
        in_col="age_at_event_days", 
        out_col=CONCEPT.BIOSPECIMEN.EVENT_AGE_DAYS 
    ),

    keep_map(
        in_col="analyte_type", 
        out_col=CONCEPT.BIOSPECIMEN.ANALYTE
    ),
    
    keep_map(
    in_col='aliquot_id',
    out_col=CONCEPT.BIOSPECIMEN.ID
    ),

    keep_map(
    in_col='sample_id',
    out_col=CONCEPT.BIOSPECIMEN_GROUP.ID
    ),

    keep_map(
    in_col='method_of_sample_procurement',
    out_col=CONCEPT.BIOSPECIMEN.SAMPLE_PROCUREMENT
    ),

    keep_map(
    in_col='participant_id',
    out_col=CONCEPT.PARTICIPANT.TARGET_SERVICE_ID
    ),

    keep_map(
    in_col='study',
    out_col=CONCEPT.STUDY.TARGET_SERVICE_ID
    ),

    keep_map(
    in_col='sequencing_center',
    out_col=CONCEPT.SEQUENCING.CENTER.TARGET_SERVICE_ID
    ),

    keep_map(
    in_col='tumor_location',
    out_col=CONCEPT.BIOSPECIMEN.ANATOMY_SITE
    ),

    keep_map(
    in_col='source_text_tissue_type',
    out_col=CONCEPT.BIOSPECIMEN.TISSUE_TYPE
    ),

    keep_map(
    in_col='associated_diagnosis',
    out_col=CONCEPT.BIOSPECIMEN.TUMOR_DESCRIPTOR
    ),

    constant_map(m=constants.COMMON.FALSE, out_col=CONCEPT.BIOSPECIMEN.VISIBLE)

]