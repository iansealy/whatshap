"""
Tests for 'whatshap compare'
"""

from tempfile import TemporaryDirectory
from collections import namedtuple
from whatshap.compare import run_compare


def test_compare1():
	with TemporaryDirectory() as tempdir:
		outtsv = tempdir + '/output.tsv'
		run_compare(vcf=['tests/data/phased1.vcf', 'tests/data/phased2.vcf'], ploidy=2, names='p1,p2', tsv_pairwise=outtsv, sample='sample1')
		lines = [l.split('\t') for l in open(outtsv)]
		assert len(lines) == 3
		Fields = namedtuple('Fields', [f.strip('#\n') for f in lines[0]])
		entry_chrA, entry_chrB = [Fields(*l) for l in lines[1:]]

		assert entry_chrA.chromosome == 'chrA'
		assert entry_chrA.all_assessed_pairs == '4'
		assert entry_chrA.all_switches == '1'
		assert entry_chrA.all_switchflips == '1/0'
		assert entry_chrA.blockwise_hamming == '1.0'
		assert entry_chrA.largestblock_assessed_pairs == '2'
		assert entry_chrA.largestblock_switches == '1'
		assert entry_chrA.largestblock_hamming == '1.0'

		assert entry_chrB.chromosome == 'chrB'
		assert entry_chrB.all_assessed_pairs == '1'
		assert entry_chrB.all_switches == '0'
		assert entry_chrB.all_switchflips == '0/0'
		assert entry_chrB.blockwise_hamming == '0.0'
		assert entry_chrB.largestblock_assessed_pairs == '1'
		assert entry_chrB.largestblock_switches == '0'
		assert entry_chrB.largestblock_hamming == '0.0'


def test_compare2():
	with TemporaryDirectory() as tempdir:
		outtsv = tempdir + '/output.tsv'
		run_compare(vcf=['tests/data/phased1.vcf', 'tests/data/phased2.vcf'], ploidy=2, names='p1,p2', tsv_pairwise=outtsv, sample='sample2')
		lines = [l.split('\t') for l in open(outtsv)]
		assert len(lines) == 3
		Fields = namedtuple('Fields', [ f.strip('#\n') for f in lines[0] ])
		entry_chrA, entry_chrB = [Fields(*l) for l in lines[1:]]

		assert entry_chrA.chromosome == 'chrA'
		assert entry_chrA.all_assessed_pairs == '6'
		assert entry_chrA.all_switches == '2'
		assert entry_chrA.all_switchflips == '0/1'
		assert entry_chrA.blockwise_hamming == '1.0'
		assert entry_chrA.largestblock_assessed_pairs == '5'
		assert entry_chrA.largestblock_switches == '2'
		assert entry_chrA.largestblock_hamming == '1.0'

		assert entry_chrB.chromosome == 'chrB'
		assert entry_chrB.all_assessed_pairs == '1'
		assert entry_chrB.all_switches == '1'
		assert entry_chrB.all_switchflips == '1/0'
		assert entry_chrB.blockwise_hamming == '1.0'
		assert entry_chrB.largestblock_assessed_pairs == '1'
		assert entry_chrB.largestblock_switches == '1'
		assert entry_chrB.largestblock_hamming == '1.0'


def test_compare_polyploid1():
	with TemporaryDirectory() as tempdir:
		outtsv = tempdir + '/output.tsv'
		run_compare(vcf=['tests/data/phased.poly1.vcf', 'tests/data/phased.poly2.vcf'], ploidy=4, names='p1,p2', tsv_pairwise=outtsv, sample='sample1')
		lines = [l.split('\t') for l in open(outtsv)]
		assert len(lines) == 3
		Fields = namedtuple('Fields', [ f.strip('#\n') for f in lines[0] ])
		entry_chr21, entry_chr22 = [Fields(*l) for l in lines[1:]]

		assert entry_chr21.chromosome == 'chr21'
		assert entry_chr21.all_assessed_pairs == '1'
		assert entry_chr21.all_switches == 'inf'
		assert entry_chr21.all_switchflips == 'inf/inf'
		assert entry_chr21.blockwise_hamming == '0.0'	
		assert entry_chr21.largestblock_assessed_pairs == '1'
		assert entry_chr21.largestblock_switches == 'inf'
		assert entry_chr21.largestblock_hamming == '0.0'

		assert entry_chr22.chromosome == 'chr22'
		assert entry_chr22.all_assessed_pairs == '6'
		assert entry_chr22.all_switches == 'inf'
		assert entry_chr22.all_switchflips == 'inf/inf'
		assert entry_chr22.blockwise_hamming == '0.5'
		assert entry_chr22.largestblock_assessed_pairs == '5'
		assert entry_chr22.largestblock_switches == 'inf'
		assert entry_chr22.largestblock_hamming == '0.5'

def test_compare_polyploid2():
	with TemporaryDirectory() as tempdir:
		outtsv = tempdir + '/output.tsv'
		run_compare(vcf=['tests/data/phased.poly1.vcf', 'tests/data/phased.poly2.vcf'], ploidy=4, names='p1,p2', tsv_pairwise=outtsv, sample='sample2')
		lines = [l.split('\t') for l in open(outtsv)]
		assert len(lines) == 3
		Fields = namedtuple('Fields', [ f.strip('#\n') for f in lines[0] ])
		entry_chr21, entry_chr22 = [Fields(*l) for l in lines[1:]]

		assert entry_chr21.chromosome == 'chr21'
		assert entry_chr21.all_assessed_pairs == '3'
		assert entry_chr21.all_switches == 'inf'
		assert entry_chr21.all_switchflips == 'inf/inf'
		assert entry_chr21.blockwise_hamming == '0.5'
		assert entry_chr21.largestblock_assessed_pairs == '3'
		assert entry_chr21.largestblock_switches == 'inf'
		assert entry_chr21.largestblock_hamming == '0.5'

		assert entry_chr22.chromosome == 'chr22'
		assert entry_chr22.all_assessed_pairs == '5'
		assert entry_chr22.all_switches == 'inf'
		assert entry_chr22.all_switchflips == 'inf/inf'
		assert entry_chr22.blockwise_hamming == '1.0'
		assert entry_chr22.largestblock_assessed_pairs == '3'
		assert entry_chr22.largestblock_switches == 'inf'
		assert entry_chr22.largestblock_hamming == '0.5'

def test_compare_only_snvs():
	with TemporaryDirectory() as tempdir:
		outtsv = tempdir + '/output.tsv'
		run_compare(vcf=['tests/data/phased1.vcf', 'tests/data/phased2.vcf'], ploidy=2, names='p1,p2', tsv_pairwise=outtsv, sample='sample2', only_snvs=True)
		lines = [l.split('\t') for l in open(outtsv)]
		assert len(lines) == 3
		Fields = namedtuple('Fields', [ f.strip('#\n') for f in lines[0] ])
		entry_chrA, entry_chrB = [Fields(*l) for l in lines[1:]]

		assert entry_chrA.chromosome == 'chrA'
		assert entry_chrA.all_assessed_pairs == '3'
		assert entry_chrA.all_switches == '2'
		assert entry_chrA.all_switchflips == '0/1'
		assert entry_chrA.largestblock_assessed_pairs == '3'
		assert entry_chrA.largestblock_switches == '2'
		assert entry_chrA.largestblock_hamming == '1.0'

		assert entry_chrB.chromosome == 'chrB'
		assert entry_chrB.all_assessed_pairs == '1'
		assert entry_chrB.all_switches == '1'
		assert entry_chrB.all_switchflips == '1/0'
		assert entry_chrB.largestblock_assessed_pairs == '1'
		assert entry_chrB.largestblock_switches == '1'
		assert entry_chrB.largestblock_hamming == '1.0'


def test_compare_unphased():
	with TemporaryDirectory() as tempdir:
		run_compare(vcf=['tests/data/unphased.vcf', 'tests/data/unphased.vcf', 'tests/data/unphased.vcf'], ploidy=2, sample='sample1')
