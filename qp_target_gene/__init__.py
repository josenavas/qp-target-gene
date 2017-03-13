# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The Qiita Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------

from qiita_client import QiitaPlugin, QiitaCommand

from .split_libraries import split_libraries, split_libraries_fastq
from .pick_otus import pick_closed_reference_otus
from .trimming import trimming
from .beta_diversity import beta_diversity
from .summarize_taxa import summarize_taxa
from .single_rarefaction import single_rarefaction

# Initialize the plugin
plugin = QiitaPlugin(
    'QIIME', '1.9.1', 'Quantitative Insights Into Microbial Ecology (QIIME) '
                      'is an open-source bioinformatics pipeline for '
                      'performing microbiome analysis from raw DNA '
                      'sequencing data')

# Define the Split libraries command
req_params = {'input_data': ('artifact', ['FASTA' 'FASTA_Sanger', 'SFF'])}
opt_params = {
    'barcode_type': ['string', 'golay_12'],
    'disable_bc_correction': ['bool', 'False'],
    'disable_primers': ['bool', 'False'],
    'max_ambig': ['integer', '6'],
    'max_barcode_errors': ['float', '1.5'],
    'max_homopolymer': ['integer', '6'],
    'max_primer_mismatch': ['integer', '0'],
    'max_seq_len': ['integer', '1000'],
    'min_qual_score': ['integer', '25'],
    'min_seq_len': ['integer', '200'],
    'qual_score_window': ['integer', '0'],
    'reverse_primer_mismatches': ['integer', '0'],
    'reverse_primers': [
        'choice:["disable", "truncate_only", "truncate_remove"]', 'disable'],
    'trim_seq_length': ['bool', 'False'],
    'truncate_ambi_bases': ['bool', 'False']}
outputs = {'demultiplexed': 'Demultiplexed'}
dflt_param_set = {
    'Defaults with Golay 12 barcodes': {
        'reverse_primers': 'disable',
        'reverse_primer_mismatches': 0, 'disable_bc_correction': False,
        'max_barcode_errors': 1.5, 'disable_primers': False,
        'min_seq_len': 200, 'truncate_ambi_bases': False, 'max_ambig': 6,
        'min_qual_score': 25, 'trim_seq_length': False, 'max_seq_len': 1000,
        'max_primer_mismatch': 0, 'max_homopolymer': 6, 'qual_score_window': 0,
        'barcode_type': 'golay_12'},
    'Defaults with Hamming 8 barcodes': {
        'reverse_primers': 'disable', 'reverse_primer_mismatches': 0,
        'disable_bc_correction': False, 'max_barcode_errors': 1.5,
        'disable_primers': False, 'min_seq_len': 200,
        'truncate_ambi_bases': False, 'max_ambig': 6, 'min_qual_score': 25,
        'trim_seq_length': False, 'max_seq_len': 1000,
        'max_primer_mismatch': 0, 'max_homopolymer': 6, 'qual_score_window': 0,
        'barcode_type': 'hamming_8'}}
sl_cmd = QiitaCommand(
    "Split libraries",
    "Demultiplexes and applies quality control to FASTA data",
    split_libraries, req_params, opt_params, outputs, dflt_param_set)
plugin.register_command(sl_cmd)

# Define the Split libraries FASTQ command
req_params = {'input_data': ('artifact', ['FASTQ', 'per_sample_FASTQ'])}
opt_params = {
    'barcode_type': ['string', 'golay_12'],
    'max_bad_run_length': ['integer', '3'],
    'max_barcode_errors': ['float', '1.5'],
    'min_per_read_length_fraction': ['float', '0.75'],
    'phred_offset': ['choice:["auto", "33", "64"]', 'auto'],
    'phred_quality_threshold': ['integer', '3'],
    'rev_comp': ['bool', 'False'],
    'rev_comp_barcode': ['bool', 'False'],
    'rev_comp_mapping_barcodes': ['bool', 'False'],
    'sequence_max_n': ['integer', '0']}
dflt_param_set = {
    'Defaults': {
        'max_barcode_errors': 1.5, 'barcode_type': 'golay_12',
        'max_bad_run_length': 3, 'phred_offset': 'auto', 'rev_comp': False,
        'phred_quality_threshold': 3, 'rev_comp_barcode': False,
        'rev_comp_mapping_barcodes': False,
        'min_per_read_length_fraction': 0.75, 'sequence_max_n': 0},
    'Defaults with reverse complement mapping file barcodes': {
        'max_barcode_errors': 1.5, 'barcode_type': 'golay_12',
        'max_bad_run_length': 3, 'phred_offset': 'auto', 'rev_comp': False,
        'phred_quality_threshold': 3, 'rev_comp_barcode': False,
        'rev_comp_mapping_barcodes': True,
        'min_per_read_length_fraction': 0.75, 'sequence_max_n': 0},
    'barcode_type 8, defaults': {
        'max_barcode_errors': 1.5, 'barcode_type': '8',
        'max_bad_run_length': 3, 'phred_offset': 'auto', 'rev_comp': False,
        'phred_quality_threshold': 3, 'rev_comp_barcode': False,
        'rev_comp_mapping_barcodes': False,
        'min_per_read_length_fraction': 0.75, 'sequence_max_n': 0},
    'barcode_type 8, reverse complement mapping file barcodes': {
        'max_barcode_errors': 1.5, 'barcode_type': '8',
        'max_bad_run_length': 3, 'phred_offset': 'auto', 'rev_comp': False,
        'phred_quality_threshold': 3, 'rev_comp_barcode': False,
        'rev_comp_mapping_barcodes': True,
        'min_per_read_length_fraction': 0.75, 'sequence_max_n': 0},
    'barcode_type 6, defaults': {
        'max_barcode_errors': 1.5, 'barcode_type': '6',
        'max_bad_run_length': 3, 'phred_offset': 'auto', 'rev_comp': False,
        'phred_quality_threshold': 3, 'rev_comp_barcode': False,
        'rev_comp_mapping_barcodes': False,
        'min_per_read_length_fraction': 0.75, 'sequence_max_n': 0},
    'barcode_type 6, reverse complement mapping file barcodes': {
        'max_barcode_errors': 1.5, 'barcode_type': '6',
        'max_bad_run_length': 3, 'phred_offset': 'auto', 'rev_comp': False,
        'phred_quality_threshold': 3, 'rev_comp_barcode': False,
        'rev_comp_mapping_barcodes': True,
        'min_per_read_length_fraction': 0.75, 'sequence_max_n': 0},
    'per sample FASTQ defaults': {
        'max_barcode_errors': 1.5, 'barcode_type': 'not-barcoded',
        'max_bad_run_length': 3, 'phred_offset': 'auto', 'rev_comp': False,
        'phred_quality_threshold': 3, 'rev_comp_barcode': False,
        'rev_comp_mapping_barcodes': False,
        'min_per_read_length_fraction': 0.75, 'sequence_max_n': 0},
    'per sample FASTQ defaults, phred_offset 33': {
        'max_barcode_errors': 1.5, 'barcode_type': 'not-barcoded',
        'max_bad_run_length': 3, 'phred_offset': '33', 'rev_comp': False,
        'phred_quality_threshold': 3, 'rev_comp_barcode': False,
        'rev_comp_mapping_barcodes': False,
        'min_per_read_length_fraction': 0.75, 'sequence_max_n': 0},
    'per sample FASTQ defaults, phred_offset 64': {
        'max_barcode_errors': 1.5, 'barcode_type': 'not-barcoded',
        'max_bad_run_length': 3, 'phred_offset': '64', 'rev_comp': False,
        'phred_quality_threshold': 3, 'rev_comp_barcode': False,
        'rev_comp_mapping_barcodes': False,
        'min_per_read_length_fraction': 0.75, 'sequence_max_n': 0}}
sl_fastq_cmd = QiitaCommand(
    "Split libraries FASTQ",
    "Demultiplexes and applies quality control to FASTQ data",
    split_libraries_fastq, req_params, opt_params, outputs, dflt_param_set)
plugin.register_command(sl_fastq_cmd)

# Define the pick OTUs command
req_params = {'input_data': ('artifact', ['Demultiplexed'])}
opt_params = {'reference': ['reference', '1'],
              'similarity': ['float', '0.97'],
              'sortmerna_coverage': ['float', '0.97'],
              'sortmerna_e_value': ['float', '1'],
              'sortmerna_max_pos': ['integer', '10000'],
              'threads': ['integer', '1']}
outputs = {'OTU table': 'BIOM'}
dflt_param_set = {
    'Defaults': {'reference': 1, 'similarity': 0.97, 'sortmerna_e_value': 1,
                 'sortmerna_max_pos': 10000, 'threads': 1,
                 'sortmerna_coverage': 0.97}}
po_cmd = QiitaCommand(
    "Pick closed-reference OTUs",
    "OTU picking using a closed reference approach",
    pick_closed_reference_otus, req_params, opt_params, outputs,
    dflt_param_set)
plugin.register_command(po_cmd)

# Define the trimming command
req_params = {'input_data': ('artifact', ['Demultiplexed'])}
opt_params = {'length': ['integer', '100']}
outputs = {'Trimmed Demultiplexed': 'Demultiplexed'}
dflt_param_set = {
    'Trimming 90': {'length': 90},
    'Trimming 100': {'length': 100},
    'Trimming 150': {'length': 150}
}
trim_cmd = QiitaCommand(
    "Trimming", "Trimming sequences to the same length",
    trimming, req_params, opt_params, outputs, dflt_param_set)
plugin.register_command(trim_cmd)

# Define the beta diversity command
req_params = {'biom_table': ('artifact', ['BIOM'])}
opt_params = {'tree': ['string', 'Default'],
              'metric': ['choice:["abund_jaccard","binary_chisq",'
                         '"binary_chord","binary_euclidean","binary_hamming",'
                         '"binary_jaccard","binary_lennon","binary_ochiai",'
                         '"binary_otu_gain","binary_pearson",'
                         '"binary_sorensen_dice","bray_curtis",'
                         '"bray_curtis_faith","bray_curtis_magurran",'
                         '"canberra","chisq","chord","euclidean","gower",'
                         '"hellinger","kulczynski","manhattan",'
                         '"morisita_horn","pearson","soergel",'
                         '"spearman_approx","specprof","unifrac","unifrac_g",'
                         '"unifrac_g_full_tree","unweighted_unifrac",'
                         '"unweighted_unifrac_full_tree",'
                         '"weighted_normalized_unifrac","weighted_unifrac"]',
                         'binary_jaccard']}
outputs = {'distance_matrix': 'distance_matrix'}
dflt_param_set = {'Binary jaccard': {'tree': None, 'metric': 'binary_jaccard'}}
bdiv_cmd = QiitaCommand(
    "Beta Diversity", "Computes and plots beta diversity results",
    beta_diversity, req_params, opt_params, outputs, dflt_param_set)
plugin.register_command(bdiv_cmd)

# Define the summarize taxa command
req_params = {'biom_table': ('artifact', ['BIOM'])}
opt_params = {'sort': ['bool', 'False'],
              'metadata_category': ['string', '']}
outputs = {'taxa_summary': 'taxa_summary'}
dflt_param_set = {'Defaults': {'sort': 'False', 'metadata_category': ''}}
sumtaxa_cmd = QiitaCommand(
    "Summarize Taxa", "Plots taxonomy summaries at different taxonomy levels",
    summarize_taxa, req_params, opt_params, outputs, dflt_param_set)
plugin.register_command(sumtaxa_cmd)

# Define the singler rarefaction command
req_params = {'biom_table': ('artifact', ['BIOM']),
              'depth': 'integer'}
opt_params = {'subsample_multinomial': ['bool', 'False']}
outputs = {'rarefied_table': 'BIOM'}
dflt_param_set = {'Defaults': {'subsample_multinomial': 'False'}}
srare_cmd = QiitaCommand(
    "Single Rarefaction",
    "Rarefies the input table by random sampling without replacement",
    single_rarefaction, req_params, opt_params, outputs, dflt_param_set)
plugin.register_command(srare_cmd)
