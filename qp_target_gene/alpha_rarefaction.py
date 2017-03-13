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


def generate_alpha_rarefaction_cmd(biom_fp, metadata, parameters, out_dir):
    """Generates the alpha_rarefaction.py command

    Parameters
    ----------
    biom_fp : str
        The path to the biom table
    metadata : dict
        The metadata associated with the artifact
    parameters : dict
        The command's parameters, keyed by parameter name
    out_dir : str
        The job output directory

    Returns
    -------
    str, str
        The alpha_rarefaction.py command and the output directory
    """
    ar_out = join(out_dir, 'alpha_rarefaction')
    mapping_fp = join(out_dir, 'mapping_file.txt')
    param_fp = join(out_dir, 'parameters_file.txt')

    write_mapping_file_from_metadata_dict(metadata, mapping_fp)

    with open(param_fp, 'w') as f:
        f.write("alpha_diversity:metrics\t%s"
                % ','.join(parameters['metrics']))

    param_str = ""
    if parameters['tree']:
        param_str += " -t %s" % parameters['tree']
    if parameters['max_rare_depth'] != 'Default':
        param_str += " -e %s" % parameters['max_rare_depth']

    cmd = str("alpha_rarefaction.py -i %s -m %s -o %s -n %s "
              "--min_rare_depth %s -p %s%s"
              % (biom_fp, mapping_fp, ar_out, parameters['num_steps'],
                 parameters['min_rare_depth'], param_fp, param_str))

    return cmd, ar_out


def alpha_rarefaction(qclient, job_id, parameters, out_dir):
    """Run alpha rarefaction with the given parameters

    Parameters
    ----------
    qclient : qiita_client.QiitaClient
        The Qiita server client
    job_id : str
        The job id
    parameters : dict
        The parameter values to run alpha rarefaction
    out_dir : str
        The path to the job's output directory

    Returns
    -------
    bool, list, str
        The results of the job
    """
    qclient.update_job_step(job_id, "Step 1 of 3: Collecting information")
    artifact_id = parameters['biom_table']
    a_info = qclient.get('/qiita_db/artifacts/%s/' % artifact_id)
    metadata = qclient.get("/qiita_db/analysis/%s/metadata/"
                           % a_info['analysis'])
    biom_fp = a_info['files']['biom'][0]

    qclient.update_job_step(job_id, "Step 2 of 3: Generating command")
    cmd, ar_out = generate_alpha_rarefaction_cmd(biom_fp, metadata,
                                                 parameters, out_dir)

    qclient.update_job_step(
        job_id, "Step 3 of 3: Executing alpha rarefaction command")
    std_out, std_err, return_value = system_call(cmd)
    if return_value != 0:
        error_msg = ("Error running alpha rarefaction:\n"
                     "Std out: %s\nStd err: %s" % (std_out, std_err))
        return False, None, error_msg

    artifacts_info = [ArtifactInfo('rarefaction_curves', 'rarefaction_curves',
                                   [(ar_out, 'directory')])]

    return True, artifacts_info, ""
