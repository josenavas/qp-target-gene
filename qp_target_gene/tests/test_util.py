# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The Qiita Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------

from unittest import TestCase, main
from os import getcwd, close, remove
from os.path import exists
from tempfile import mkstemp

from qp_target_gene.util import (
    system_call, write_mapping_file_from_metadata_dict)


class UtilTests(TestCase):
    def setUp(self):
        self._clean_up_files = []

    def tearDown(self):
        for fp in self._clean_up_files:
            if exists(fp):
                remove(fp)

    def test_system_call(self):
        obs_out, obs_err, obs_val = system_call("pwd")
        self.assertEqual(obs_out, "%s\n" % getcwd())
        self.assertEqual(obs_err, "")
        self.assertEqual(obs_val, 0)

    def test_system_call_error(self):
        obs_out, obs_err, obs_val = system_call("IHopeThisCommandDoesNotExist")
        self.assertEqual(obs_out, "")
        self.assertTrue("not found" in obs_err)
        self.assertEqual(obs_val, 127)

    def test_write_mapping_file_from_metadata_dict(self):
        fd, fp = mkstemp(suffix='.txt')
        close(fd)
        self._clean_up_files.append(fp)

        metadata = {
            '1.SKB7.640196': {
                'BarcodeSequence': 'CGGCCTAAGTTC',
                'Description': 'Cannabis Soil Microbiome',
                'LinkerPrimerSequence': 'GTGCCAGCMGCCGCGGTAA',
                'collection_timestamp': '2011-11-11 13:00:00',
                'qiita_owner': 'Dude',
                'qiita_prep_id': '1',
                'qiita_principal_investigator': 'PIDude',
                'qiita_study_alias': 'Cannabis Soils',
                'qiita_study_title':
                    'Identification of the Microbiomes for Cannabis Soils'},
            '1.SKB8.640193': {
                'BarcodeSequence': 'AGCGCTCACATC',
                'Description': 'Cannabis Soil Microbiome',
                'LinkerPrimerSequence': 'GTGCCAGCMGCCGCGGTAA',
                'collection_timestamp': '2011-11-11 13:00:00',
                'qiita_owner': 'Dude',
                'qiita_prep_id': '1',
                'qiita_principal_investigator': 'PIDude',
                'qiita_study_alias': 'Cannabis Soils',
                'qiita_study_title':
                    'Identification of the Microbiomes for Cannabis Soils'},
            '1.SKD8.640184': {
                'BarcodeSequence': 'TGAGTGGTCTGT',
                'Description': 'Cannabis Soil Microbiome',
                'LinkerPrimerSequence': 'GTGCCAGCMGCCGCGGTAA',
                'collection_timestamp': '2011-11-11 13:00:00',
                'qiita_owner': 'Dude',
                'qiita_prep_id': '1',
                'qiita_principal_investigator': 'PIDude',
                'qiita_study_alias': 'Cannabis Soils',
                'qiita_study_title':
                    'Identification of the Microbiomes for Cannabis Soils'}}

        write_mapping_file_from_metadata_dict(metadata, fp)
        self.assertTrue(exists(fp))
        with open(fp, 'U') as f:
            self.assertEqual(f.readlines(), EXP_MAPPING_FILE)


EXP_MAPPING_FILE = [
    '#SampleID\tBarcodeSequence\tLinkerPrimerSequence\tcollection_timestamp'
    '\tqiita_owner\tqiita_prep_id\tqiita_principal_investigator\t'
    'qiita_study_alias\tqiita_study_title\tDescription\n',
    '1.SKB7.640196\tCGGCCTAAGTTC\tGTGCCAGCMGCCGCGGTAA\t2011-11-11 13:00:00'
    '\tDude\t1\tPIDude\tCannabis Soils\tIdentification of the Microbiomes for '
    'Cannabis Soils\tCannabis Soil Microbiome\n',
    '1.SKB8.640193\tAGCGCTCACATC\tGTGCCAGCMGCCGCGGTAA\t2011-11-11 13:00:00'
    '\tDude\t1\tPIDude\tCannabis Soils\tIdentification of the Microbiomes for '
    'Cannabis Soils\tCannabis Soil Microbiome\n',
    '1.SKD8.640184\tTGAGTGGTCTGT\tGTGCCAGCMGCCGCGGTAA\t2011-11-11 13:00:00'
    '\tDude\t1\tPIDude\tCannabis Soils\tIdentification of the Microbiomes for '
    'Cannabis Soils\tCannabis Soil Microbiome\n']


if __name__ == '__main__':
    main()
