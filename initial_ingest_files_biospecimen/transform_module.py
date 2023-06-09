"""
Auto-generated transform module

Replace the contents of transform_function with your own code

See documentation at
https://kids-first.github.io/kf-lib-data-ingest/ for information on
implementing transform_function.
"""

from kf_lib_data_ingest.common.concept_schema import CONCEPT  # noqa F401

# Use these merge funcs, not pandas.merge
from kf_lib_data_ingest.common.pandas_utils import (  # noqa F401
    merge_wo_duplicates,
    outer_merge,
)
from kf_lib_data_ingest.config import DEFAULT_KEY


def transform_function(mapped_df_dict):
    """
    Merge DataFrames in mapped_df_dict into 1 DataFrame if possible.

    Return a dict that looks like this:

    {
        DEFAULT_KEY: all_merged_data_df
    }

    If not possible to merge all DataFrames into a single DataFrame then
    you can return a dict that looks something like this:

    {
        '<name of target concept>': df_for_<target_concept>,
        DEFAULT_KEY: all_merged_data_df
    }

    Target concept instances will be built from the default DataFrame unless
    another DataFrame is explicitly provided via a key, value pair in the
    output dict. They key must match the name of an existing target concept.
    The value will be the DataFrame to use when building instances of the
    target concept.

    A typical example would be:

    {
        'family_relationship': family_relationship_df,
        'default': all_merged_data_df
    }

    """
    genomic = mapped_df_dict["genomic_data.py"]
    biospecimen = mapped_df_dict["biospecimen.py"]
    sequencing = mapped_df_dict["sequencing.py"]

    df = merge_wo_duplicates(
        genomic,
        biospecimen,
        on=CONCEPT.BIOSPECIMEN.ID,
        how="left"
    )
#df2 stays as is
    df2 = merge_wo_duplicates(
        df,
        sequencing,
        on=CONCEPT.SEQUENCING.ID,
        how="left"
    )
#create df3 as frame with only the 3 biospecimen that need to be created
    df3 = df2[df2[CONCEPT.BIOSPECIMEN.TARGET_SERVICE_ID].isnull()]

    # df = outer_merge(
    #     mapped_df_dict['extract_config.py'],
    #     mapped_df_dict['family_and_phenotype.py'],
    #     on=CONCEPT.BIOSPECIMEN.ID,
    #     with_merge_detail_dfs=False
    # )

    return {"biospecimen": df3, DEFAULT_KEY: df2}
