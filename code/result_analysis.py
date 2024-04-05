from gsmmutils import InterProScan
from pprint import pprint

from gsmmutils.bio.genome import Genome


def main():
    ips = InterProScan()
    ips.load_results_from_folder("../results/interproscan")
    ips.load_genomes_from_folder("../data")
    genome = Genome()
    genome.from_fasta(f"../data/Genomes/Stramenopiles/Noceanica_IMET1/IMET1v2.protein.fasta")
    ips.load_genes("Noceanica_IMET1", genome)
    ips.calculate_gene_annotation_ratio(['interproscan'])
    pprint(ips.report)


if __name__ == '__main__':
    main()
