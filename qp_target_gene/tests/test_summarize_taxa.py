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

from qp_target_gene.summarize_taxa import (
    generate_summarize_taxa_cmd, summarize_taxa)


class SummarizeTaxaTests(PluginTestCase):
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

    def test_generate_summarize_taxa_cmd(self):
        parameters = {'metadata_category': None,
                      'sort': False}
        obs_cmd, obs_out = generate_summarize_taxa_cmd(
            "/path/to/biom/table.biom", parameters, self.tmp_dir)
        exp_cmd = ("summarize_taxa_through_plots.py "
                   "-i /path/to/biom/table.biom -o %s/taxa_summaries"
                   % self.tmp_dir)
        exp_out = join(self.tmp_dir, "taxa_summaries")
        self.assertEqual(obs_cmd, exp_cmd)
        self.assertEqual(obs_out, exp_out)

        parameters = {'metadata_category': None,
                      'sort': True}
        obs_cmd, obs_out = generate_summarize_taxa_cmd(
            "/path/to/biom/table.biom", parameters, self.tmp_dir)
        exp_cmd = ("summarize_taxa_through_plots.py "
                   "-i /path/to/biom/table.biom -o %s/taxa_summaries -s"
                   % self.tmp_dir)
        exp_out = join(self.tmp_dir, "taxa_summaries")
        self.assertEqual(obs_cmd, exp_cmd)
        self.assertEqual(obs_out, exp_out)

        metadata = {
            'sample1': {'col1': 'Data',
                        'BarcodeSequence': 'CGGCCTAAGTTC',
                        'Description': 'Cannabis Soil Microbiome',
                        'LinkerPrimerSequence': 'GTGCCAGCMGCCGCGGTAA'},
            'sample2': {'col1': 'More data',
                        'BarcodeSequence': 'AGCGCTCACATC',
                        'Description': 'Cannabis Soil Microbiome',
                        'LinkerPrimerSequence': 'GTGCCAGCMGCCGCGGTAA'}}
        parameters = {'metadata_category': 'col1',
                      'metadata': metadata,
                      'sort': False}
        obs_cmd, obs_out = generate_summarize_taxa_cmd(
            "/path/to/biom/table.biom", parameters, self.tmp_dir)
        exp_cmd = ("summarize_taxa_through_plots.py "
                   "-i /path/to/biom/table.biom -o {0}/taxa_summaries "
                   "-m {0}/mapping_file.txt -c col1".format(self.tmp_dir))
        exp_out = join(self.tmp_dir, "taxa_summaries")
        self.assertEqual(obs_cmd, exp_cmd)
        self.assertEqual(obs_out, exp_out)

        parameters = {'metadata_category': 'col1',
                      'metadata': metadata,
                      'sort': True}
        obs_cmd, obs_out = generate_summarize_taxa_cmd(
            "/path/to/biom/table.biom", parameters, self.tmp_dir)
        exp_cmd = ("summarize_taxa_through_plots.py "
                   "-i /path/to/biom/table.biom -o {0}/taxa_summaries "
                   "-m {0}/mapping_file.txt -c col1 -s".format(self.tmp_dir))
        exp_out = join(self.tmp_dir, "taxa_summaries")
        self.assertEqual(obs_cmd, exp_cmd)
        self.assertEqual(obs_out, exp_out)

    def test_summarize_taxa(self):
        # Create a new job
        parameters = {'metadata_category': None,
                      'sort': False,
                      'biom_table': 8}
        data = {'user': 'demo@microbio.me',
                'command': dumps(['QIIME', '1.9.1', 'Summarize Taxa']),
                'status': 'running',
                'parameters': dumps(parameters)}
        job_id = self.qclient.post(
            '/apitest/processing_job/', data=data)['job']
        obs_success, obs_ainfo, obs_msg = summarize_taxa(
            self.qclient, job_id, parameters, self.tmp_dir)
        exp_ainfo = [ArtifactInfo('taxa_sumamry', 'taxa_summary',
                                  [(join(self.tmp_dir, 'taxa_summaries'),
                                    'directory')])]
        self.assertTrue(obs_success)
        self.assertEqual(obs_ainfo, exp_ainfo)
        self.assertEqual(obs_msg, "")

        parameters = {'metadata_category': 'does-not-exist',
                      'sort': False,
                      'biom_table': 8}
        data = {'user': 'demo@microbio.me',
                'command': dumps(['QIIME', '1.9.1', 'Summarize Taxa']),
                'status': 'running',
                'parameters': dumps(parameters)}
        job_id = self.qclient.post(
            '/apitest/processing_job/', data=data)['job']
        obs_success, obs_ainfo, obs_msg = summarize_taxa(
            self.qclient, job_id, parameters, self.tmp_dir)
        self.assertFalse(obs_success)
        self.assertIsNone(obs_ainfo)
        self.assertIn("Error running summarize taxa:\nStd out: ", obs_msg)


if __name__ == '__main__':
    main()
