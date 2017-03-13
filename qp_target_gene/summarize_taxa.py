# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The Qiita Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------

from os.path import join

from qiita_client import ArtifactInfo

from qp_target_gene.util import (
    system_call, write_mapping_file_from_metadata_dict)


def generate_summarize_taxa_cmd(biom_fp, parameters, out_dir):
    """Generates the summarize_taxa_through_plots.py command

    Parameters
    ----------
    biom_fp : str
        The path to the biom table
    parameters : dict
        The command's parameters, keyed by parameter name
    out_dir : str
        The job output directory

    Returns
    -------
    str, str
        The summarize_taxa_through_plots.py command and the output directory
    """
    st_out = join(out_dir, 'taxa_summaries')
    param_str = ""

    if parameters['metadata_category']:
        # Write metadata to a mapping file
        mapping_fp = join(out_dir, 'mapping_file.txt')
        write_mapping_file_from_metadata_dict(
            parameters['metadata'], mapping_fp)
        param_str += " -m %s -c %s" % (mapping_fp,
                                       parameters['metadata_category'])
    if parameters['sort']:
        param_str += " -s"

    cmd = str("summarize_taxa_through_plots.py -i %s -o %s%s"
              % (biom_fp, st_out, param_str))
    return cmd, st_out


def summarize_taxa(qclient, job_id, parameters, out_dir):
    """Run summarize taxa through plots with the given parameters

    Parameters
    ----------
    qclient : qiita_client.QiitaClient
        The Qiita server client
    job_id : str
        The job id
    parameters : dict
        The parameter values to run sumamrize taxa
    out_dir : str
        The path to the job's output directory

    Returns
    -------
    bool, list, str
        The results of the job
    """
    qclient.update_job_step(job_id, "Step 1 of 3: Collecting information")
    artifact_id = parameters['biom_table']
    a_info = qclient.get("/qiita_db/artifacts/%s/" % artifact_id)
    biom_fp = a_info['files']['biom'][0]

    if parameters['metadata_category']:
        metadata = qclient.get("/qiita_db/analysis/%s/metadata/"
                               % a_info['analysis'])
        parameters['metadata'] = metadata

    qclient.update_job_step(job_id, "Step 2 of 3: Generating command")
    cmd, st_out = generate_summarize_taxa_cmd(biom_fp, parameters, out_dir)

    qclient.update_job_step(
        job_id, "Step 3 of 3: Executing summarize taxa command")
    std_out, std_err, return_value = system_call(cmd)
    if return_value != 0:
        error_msg = ("Error running summarize taxa:\nStd out: %s\nStd err: %s"
                     % (std_out, std_err))
        return False, None, error_msg

    artifacts_info = [ArtifactInfo('taxa_summary', 'taxa_summary',
                                   [(st_out, 'directory')])]

    return True, artifacts_info, ""
