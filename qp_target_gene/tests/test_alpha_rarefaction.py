# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The Qiita Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------

from unittest import main
from tempfile import mkdtemp
from os.path import exists, isdir, join
from os import remove
from shutil import rmtree
from json import dumps

from qiita_client.testing import PluginTestCase
from qiita_client import ArtifactInfo

from qp_target_gene.alpha_rarefaction import (
    generate_alpha_rarefaction_cmd, alpha_rarefaction)


class AlphaRarefactionTests(PluginTestCase):
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

    def test_generate_alpha_rarefaction_cmd(self):
        metadata = {'sample1': {'col1': 'Data',
                                'BarcodeSequence': 'CGGCCTAAGTTC',
                                'Description': 'Cannabis Soil Microbiome',
                                'LinkerPrimerSequence': 'GTGCCAGCMGCCGCGGTAA'},
                    'sample2': {'col1': 'More data',
                                'BarcodeSequence': 'AGCGCTCACATC',
                                'Description': 'Cannabis Soil Microbiome',
                                'LinkerPrimerSequence': 'GTGCCAGCMGCCGCGGTAA'}}
        parameters = {'tree': None,
                      'num_steps': 10,
                      'min_rare_depth': 10,
                      'max_rare_depth': 'Default',
                      'metrics': ["chao1", "observed_otus"],
                      'biom_table': 8}
        obs_cmd, obs_out = generate_alpha_rarefaction_cmd(
            "/path/to/biom/table.biom", metadata, parameters, self.tmp_dir)
        exp_cmd = ("alpha_rarefaction.py -i /path/to/biom/table.biom "
                   "-m {0}/mapping_file.txt -o {0}/alpha_rarefaction -n 10 "
                   "--min_rare_depth 10 "
                   "-p {0}/parameters_file.txt".format(self.tmp_dir))
        self.assertEqual(obs_cmd, exp_cmd)
        self.assertEqual(obs_out, join(self.tmp_dir, 'alpha_rarefaction'))

        parameters = {'tree': '/path/to/tree.tre',
                      'num_steps': 10,
                      'min_rare_depth': 10,
                      'max_rare_depth': 'Default',
                      'metrics': ["chao1", "observed_otus"],
                      'biom_table': 8}
        obs_cmd, obs_out = generate_alpha_rarefaction_cmd(
            "/path/to/biom/table.biom", metadata, parameters, self.tmp_dir)
        exp_cmd = ("alpha_rarefaction.py -i /path/to/biom/table.biom "
                   "-m {0}/mapping_file.txt -o {0}/alpha_rarefaction -n 10 "
                   "--min_rare_depth 10 -p {0}/parameters_file.txt "
                   "-t /path/to/tree.tre".format(self.tmp_dir))
        self.assertEqual(obs_cmd, exp_cmd)
        self.assertEqual(obs_out, join(self.tmp_dir, 'alpha_rarefaction'))

        parameters = {'tree': None,
                      'num_steps': 10,
                      'min_rare_depth': 10,
                      'max_rare_depth': 5000,
                      'metrics': ["chao1", "observed_otus"],
                      'biom_table': 8}
        obs_cmd, obs_out = generate_alpha_rarefaction_cmd(
            "/path/to/biom/table.biom", metadata, parameters, self.tmp_dir)
        exp_cmd = ("alpha_rarefaction.py -i /path/to/biom/table.biom "
                   "-m {0}/mapping_file.txt -o {0}/alpha_rarefaction -n 10 "
                   "--min_rare_depth 10 -p {0}/parameters_file.txt "
                   "-e 5000".format(self.tmp_dir))
        self.assertEqual(obs_cmd, exp_cmd)
        self.assertEqual(obs_out, join(self.tmp_dir, 'alpha_rarefaction'))

        parameters = {'tree': '/path/to/tree.tre',
                      'num_steps': 20,
                      'min_rare_depth': 1000,
                      'max_rare_depth': 10000,
                      'metrics': ["chao1", "observed_otus"],
                      'biom_table': 8}
        obs_cmd, obs_out = generate_alpha_rarefaction_cmd(
            "/path/to/biom/table.biom", metadata, parameters, self.tmp_dir)
        exp_cmd = ("alpha_rarefaction.py -i /path/to/biom/table.biom "
                   "-m {0}/mapping_file.txt -o {0}/alpha_rarefaction -n 20 "
                   "--min_rare_depth 1000 -p {0}/parameters_file.txt "
                   "-t /path/to/tree.tre -e 10000".format(self.tmp_dir))
        self.assertEqual(obs_cmd, exp_cmd)
        self.assertEqual(obs_out, join(self.tmp_dir, 'alpha_rarefaction'))

    def test_alpha_rarefaction(self):
        # Create a new job
        parameters = {'tree': None,
                      'num_steps': 3,
                      'min_rare_depth': 1000,
                      'max_rare_depth': 10000,
                      'metrics': ["observed_otus"],
                      'biom_table': 8}
        data = {'user': 'demo@microbio.me',
                'command': dumps(['QIIME', '1.9.1', 'Alpha Rarefaction']),
                'status': 'running',
                'parameters': dumps(parameters)}
        job_id = self.qclient.post(
            '/apitest/processing_job/', data=data)['job']
        obs_success, obs_ainfo, obs_msg = alpha_rarefaction(
            self.qclient, job_id, parameters, self.tmp_dir)
        exp_ainfo = [ArtifactInfo('rarefaction_curves', 'rarefaction_curves',
                                  [(join(self.tmp_dir, 'alpha_rarefaction'),
                                    'directory')])]
        self.assertEqual(obs_msg, "")
        self.assertTrue(obs_success)
        self.assertEqual(obs_ainfo, exp_ainfo)


if __name__ == '__main__':
    main()
