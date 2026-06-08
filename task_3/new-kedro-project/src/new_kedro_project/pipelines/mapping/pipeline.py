"""
This is a boilerplate pipeline 'mapping'
generated using Kedro 1.4.0
"""

from kedro.pipeline import Pipeline, node
from .nodes import run_fastqc, run_mapping, run_flagstat, evaluate_mapping


def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline(
        [
            node(
                func=run_fastqc,
                inputs=["params:fastq_1", "params:fastq_2"],
                outputs="qc_status",
                name="fastqc_node",
            ),
            node(
                func=run_mapping,
                inputs=["params:ref_index", "params:fastq_1", "params:fastq_2", "qc_status"],
                outputs="bam_file_path",
                name="mapping_node",
            ),
            node(
                func=run_flagstat,
                inputs="bam_file_path",
                outputs="report_file_path",
                name="flagstat_node",
            ),
            node(
                func=evaluate_mapping,
                inputs="report_file_path",
                outputs="mapping_quality_check",
                name="evaluation_node",
            ),
        ]
    )
