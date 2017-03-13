# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The Qiita Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------

from os.path import join

import pandas as pd
from qiita_client import ArtifactInfo

from qp_target_gene.util import (
    system_call, write_mapping_file_from_metadata_dict)


def generate_beta_diversity_cmd(biom_fp, metadata, parameters, out_dir):
    """Generates the beta_diversity_through_plots.py command

    Parameters
    ----------
    biom_fp : str
        The path to the biom table
    metadata : dict
        The metadata associated with the artifact
    parameters : dict
        The command's parameter, keyed by parameter name
    out_dir : str
        The job output directory

    Returns
    -------
    str, str
        The beta_diversity_through_plots.py command and the output directory
    """
    bdiv_out = join(out_dir, 'bdiv')
    mapping_fp = join(out_dir, 'mapping_file.txt')
    param_fp = join(out_dir, 'parameters_file.txt')

    write_mapping_file_from_metadata_dict(metadata, mapping_fp)

    with open(param_fp, 'w') as f:
        f.write("beta_diversity:metrics\t%s" % parameters['metric'])

    tree_param = "-t %s" % parameters['tree'] if parameters['tree'] else ""

    cmd = str("beta_diversity_through_plots.py -i %s -m %s -o %s -p %s %s"
              % (biom_fp, mapping_fp, bdiv_out, param_fp, tree_param))

    return cmd, bdiv_out


def beta_diversity(qclient, job_id, parameters, out_dir):
    """Run beta diversity through plots with the given parameters

    Parameters
    ----------
    qclient : qiita_client.QiitaClient
        The Qiita server client
    job_id : str
        The job id
    parameters : dict
        The parameter values to run beta diversity
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
    metadata = qclient.get("/qiita_db/analysis/%s/metadata/"
                           % a_info['analysis'])

    biom_fp = a_info['files']['biom'][0]

    qclient.update_job_step(job_id, "Step 2 of 3: Generating command")
    cmd, bdiv_out = generate_beta_diversity_cmd(biom_fp, metadata,
                                                parameters, out_dir)

    qclient.update_job_step(job_id, "Step 3 of 3: Executing beta diversity")
    std_out, std_err, return_value = system_call(cmd)
    if return_value != 0:
        error_msg = ("Error running beta diversity:\nStd out: %s\nStd err: %s"
                     % (std_out, std_err))
        return False, None, error_msg

    artifacts_info = [ArtifactInfo('distance_matrix', 'distance_matrix',
                                   [bdiv_out, 'directory'])]

    return True, artifacts_info, ""
