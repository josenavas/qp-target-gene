# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The Qiita Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------

from unittest import main
from tempfile import mkdtemp
from os.path import isdir, exists, join
from os import remove
from shutil import rmtree
from json import dumps

from qiita_client.testing import PluginTestCase
from qiita_client import ArtifactInfo

from qp_target_gene.single_rarefaction import (
    generate_single_rarefaction_cmd, single_rarefaction)


class SingleRarefactionTests(PluginTestCase):
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

    def test_generate_single_rarefaction_cmd(self):
        parameters = {'depth': 1000, 'subsample_multinomial': False}
        obs_cmd, obs_out = generate_single_rarefaction_cmd(
            "/path/to/biom/table.biom", parameters, self.tmp_dir)
        exp_cmd = ("single_rarefaction.py -i /path/to/biom/table.biom "
                   "-o %s/table_even1000.biom -d 1000" % self.tmp_dir)
        exp_out = join(self.tmp_dir, "table_even1000.biom")
        self.assertEqual(obs_cmd, exp_cmd)
        self.assertEqual(obs_out, exp_out)

        parameters = {'depth': 2000, 'subsample_multinomial': True}
        obs_cmd, obs_out = generate_single_rarefaction_cmd(
            "/path/to/biom/table.biom", parameters, self.tmp_dir)
        exp_cmd = ("single_rarefaction.py -i /path/to/biom/table.biom "
                   "-o %s/table_even2000.biom -d 2000 --subsample_multinomial"
                   % self.tmp_dir)
        exp_out = join(self.tmp_dir, "table_even2000.biom")
        self.assertEqual(obs_cmd, exp_cmd)
        self.assertEqual(obs_out, exp_out)

    def test_single_rarefaction(self):
        parameters = {'depth': 100, 'subsample_multinomial': False,
                      'biom_table': 8}
        data = {'user': 'demo@microbio.me',
                'command': dumps(['QIIME', '1.9.1', 'Single Rarefaction']),
                'status': 'running',
                'parameters': dumps(parameters)}
        job_id = self.qclient.post(
            '/apitest/processing_job/', data=data)['job']
        obs_success, obs_ainfo, obs_msg = single_rarefaction(
            self.qclient, job_id, parameters, self.tmp_dir)
        exp_ainfo = [ArtifactInfo(
            'rarefied_table', 'BIOM',
            [(join(self.tmp_dir, 'biom_table_even100.biom'), 'biom')])]
        self.assertTrue(obs_success)
        self.assertEqual(obs_ainfo, exp_ainfo)
        self.assertEqual(obs_msg, "")

        parameters = {'depth': 100000, 'subsample_multinomial': False,
                      'biom_table': 8}
        data = {'user': 'demo@microbio.me',
                'command': dumps(['QIIME', '1.9.1', 'Single Rarefaction']),
                'status': 'running',
                'parameters': dumps(parameters)}
        job_id = self.qclient.post(
            '/apitest/processing_job/', data=data)['job']
        obs_success, obs_ainfo, obs_msg = single_rarefaction(
            self.qclient, job_id, parameters, self.tmp_dir)
        self.assertFalse(obs_success)
        self.assertIsNone(obs_ainfo)
        self.assertIn("Error running single rarefaction:\nStd out: ", obs_msg)


if __name__ == '__main__':
    main()
