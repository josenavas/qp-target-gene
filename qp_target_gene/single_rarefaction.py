# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The Qiita Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------

from os.path import splitext, basename, join

from qiita_client import ArtifactInfo

from qp_target_gene.util import system_call


def generate_single_rarefaction_cmd(biom_fp, parameters, out_dir):
    """Generates the single_rarefaction.py command

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
        The single_rarefaction.py command and the path of output table
    """
    depth = parameters['depth']
    sr_out = join(out_dir, "%s_even%s.biom"
                           % (splitext(basename(biom_fp))[0], depth))
    param_str = (" --subsample_multinomial"
                 if parameters['subsample_multinomial'] else "")

    cmd = str("single_rarefaction.py -i %s -o %s -d %s%s"
              % (biom_fp, sr_out, depth, param_str))

    return cmd, sr_out


def single_rarefaction(qclient, job_id, parameters, out_dir):
    """Run single rarefaction with the given parameters

    Parameters
    ----------
    qclient : qiita_client.QiitaClient
        The Qiita server client
    job_id : str
        The job id
    parameters : dict
        The parameter values to run single rarefaction
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
    biom_fp = a_info['files']['biom'][0]

    qclient.update_job_step(job_id, "Step 2 of 3: Generating command")
    cmd, sr_out = generate_single_rarefaction_cmd(biom_fp, parameters, out_dir)

    qclient.update_job_step(job_id,
                            "Step 3 of 3: Executing single rarefaction")
    std_out, std_err, return_value = system_call(cmd)
    if return_value != 0:
        error_msg = ("Error running single rarefaction:\n"
                     "Std out: %s\nStd err: %s" % (std_out, std_err))
        return False, None, error_msg

    artifacts_info = [ArtifactInfo('rarefied_table', 'BIOM',
                                   [(sr_out, 'biom')])]

    return True, artifacts_info, ""
