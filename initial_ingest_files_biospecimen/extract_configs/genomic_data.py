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
    row_map
)

# replace this with the source once I upload it to data tracker
source_data_url="https://kf-api-study-creator.kidsfirstdrc.org/download/study/SD_BHJXBDQK/file/SF_1T414W8K/version/FV_RXNAJ4JC"

# TODO (Optional) Fill in special loading parameters here
source_data_read_params = {"sheet_name": "Data_ingest_remove_bad_aliquots"}


# TODO - Replace this with operations that make sense for your own data file
operations = [
    keep_map(
        in_col="kf_biospecimen_id", 
        out_col=CONCEPT.BIOSPECIMEN.TARGET_SERVICE_ID
    ),

    keep_map(
        in_col="participant_kf_id", 
        out_col=CONCEPT.PARTICIPANT.TARGET_SERVICE_ID
    ),

    keep_map(
        in_col="aliquot_id", 
        out_col=CONCEPT.BIOSPECIMEN.ID
    ),

    keep_map(
    in_col='study',
    out_col=CONCEPT.STUDY.TARGET_SERVICE_ID
    ),

    keep_map(
        in_col="sequencing_experiment", 
        out_col=CONCEPT.SEQUENCING.ID, 
    ),

    keep_map(
        in_col="s3path", 
        out_col=CONCEPT.GENOMIC_FILE.ID, 
    ),

    keep_map(
        in_col="data_type", 
        out_col=CONCEPT.GENOMIC_FILE.DATA_TYPE
    ),
    
    keep_map(
    in_col='file_format',
    out_col=CONCEPT.GENOMIC_FILE.FILE_FORMAT
    ),

    keep_map(
    in_col='file_name',
    out_col=CONCEPT.GENOMIC_FILE.FILE_NAME
    ),

    row_map(
        out_col=CONCEPT.GENOMIC_FILE.HASH_DICT,
        m=lambda x: 
        {
            constants.FILE.HASH.S3_ETAG.lower(): x["etag"].replace('"', ""),
            constants.FILE.HASH.MD5.lower(): x["md5"],
            constants.FILE.HASH.SHA256.lower():x["sha256"]
        }
        if x["sha256"]!="0" else 
        {
            constants.FILE.HASH.S3_ETAG.lower(): x["etag"].replace('"', "")
        }
    ),

    constant_map(
        m=constants.COMMON.FALSE, 
        out_col=CONCEPT.GENOMIC_FILE.HARMONIZED
    ),

    constant_map(
        m=constants.GENOMIC_FILE.AVAILABILITY.IMMEDIATE, 
        out_col=CONCEPT.GENOMIC_FILE.AVAILABILITY
    ),

    constant_map(
    m=constants.COMMON.TRUE,
    out_col=CONCEPT.GENOMIC_FILE.CONTROLLED_ACCESS
    ),

    constant_map(
    m=constants.COMMON.TRUE,
    out_col=CONCEPT.SEQUENCING.PAIRED_END
    ),

    constant_map(
        m="GRCh38", 
        out_col=CONCEPT.GENOMIC_FILE.REFERENCE_GENOME
    ),

    keep_map(
        in_col="size",
        out_col=CONCEPT.GENOMIC_FILE.SIZE
    ),

    value_map(
        in_col = "s3path",
        out_col = CONCEPT.GENOMIC_FILE.URL_LIST,
        m = lambda x: [f'{x}']
    ),

    constant_map(m=constants.COMMON.FALSE, out_col=CONCEPT.SEQUENCING.VISIBLE),
    constant_map(m=constants.COMMON.FALSE, out_col=CONCEPT.GENOMIC_FILE.VISIBLE),

]