# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The Qiita Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------

from unittest import main
from os.path import isdir, exists, join
from os import remove
from shutil import rmtree
from tempfile import mkdtemp
from json import dumps

from qiita_client.testing import PluginTestCase
from qiita_client import ArtifactInfo

from qp_target_gene.beta_diversity import (
    generate_beta_diversity_cmd, beta_diversity)


class BetaDivesityTests(PluginTestCase):
    def setUp(self):
        self.tmp_dir = mkdtemp()
        self._clean_up_files = [self.tmp_dir]

    def tearDown(self):
        for fp in self._clean_up_files:
            if exists(fp):
                if isdir(fp):
                    rmtree(fp)
                else:
                    remove(fp)

    def test_generate_beta_diversity_cmd(self):
        metadata = {'sample1': {'col1': 'Data'},
                    'sample2': {'col1': 'More data'}}
        parameters = {'tree': None,
                      'metric': 'bray_curtis',
                      'biom_table': '1'}

        obs_cmd, obs_bdiv_out = generate_beta_diversity_cmd(
            "/path/to/biom_table.biom", metadata, parameters, self.tmp_dir)
        exp_cmd = (
            "beta_diversity_through_plots.py -i /path/to/biom_table.biom "
            "-m {0}/mapping_file.txt -o {0}/bdiv "
            "-p {0}/parameters_file.txt ".format(self.tmp_dir))
        exp_bdiv_out = join(self.tmp_dir, 'bdiv')
        self.assertEqual(obs_cmd, exp_cmd)
        self.assertEqual(obs_bdiv_out, exp_bdiv_out)

        parameters['tree'] = ""
        obs_cmd, obs_bdiv_out = generate_beta_diversity_cmd(
            "/path/to/biom_table.biom", metadata, parameters, self.tmp_dir)
        self.assertEqual(obs_cmd, exp_cmd)
        self.assertEqual(obs_bdiv_out, exp_bdiv_out)

        parameters['tree'] = "/path/to/a/tree.tre"
        obs_cmd, obs_bdiv_out = generate_beta_diversity_cmd(
            "/path/to/biom_table.biom", metadata, parameters, self.tmp_dir)
        exp_cmd = (
            "beta_diversity_through_plots.py -i /path/to/biom_table.biom "
            "-m {0}/mapping_file.txt -o {0}/bdiv -p {0}/parameters_file.txt "
            "-t /path/to/a/tree.tre".format(self.tmp_dir))
        exp_bdiv_out = join(self.tmp_dir, 'bdiv')
        self.assertEqual(obs_cmd, exp_cmd)
        self.assertEqual(obs_bdiv_out, exp_bdiv_out)

    def test_beta_diversity(self):
        # Create a new job
        parameters = {'tree': None,
                      'metric': 'bray_curtis',
                      'biom_table': '8'}
        data = {'user': 'demo@microbio.me',
                'command': dumps(['QIIME', '1.9.1', 'Beta Diversity']),
                'status': 'running',
                'parameters': dumps(parameters)}
        job_id = self.qclient.post(
            '/apitest/processing_job/', data=data)['job']
        obs_success, obs_ainfo, obs_msg = beta_diversity(
            self.qclient, job_id, parameters, self.tmp_dir)
        exp_ainfo = [ArtifactInfo('distance_matrix', 'distance_matrix',
                                  [join(self.tmp_dir, 'bdiv'), 'directory'])]
        self.assertTrue(obs_success)
        self.assertEqual(obs_ainfo, exp_ainfo)
        self.assertEqual(obs_msg, "")

        parameters = {'tree': None,
                      'metric': 'unweighted_unifrac',
                      'biom_table': '8'}
        data = {'user': 'demo@microbio.me',
                'command': dumps(['QIIME', '1.9.1', 'Beta Diversity']),
                'status': 'running',
                'parameters': dumps(parameters)}
        job_id = self.qclient.post(
            '/apitest/processing_job/', data=data)['job']
        obs_success, obs_ainfo, obs_msg = beta_diversity(
            self.qclient, job_id, parameters, self.tmp_dir)
        self.assertFalse(obs_success)
        self.assertIsNone(obs_ainfo)
        self.assertIn("Error running beta diversity:\nStd out:", obs_msg)


if __name__ == '__main__':
    main()
