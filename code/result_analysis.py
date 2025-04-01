from gsmmutils import InterProScan, Busco
from pprint import pprint

from gsmmutils.bio.genome import Genome
import pandas as pd
pd.set_option('display.max_columns', None)

def main():
    ips = InterProScan()
    ips.load_results_from_folder("../results/interproscan")
    ips.load_genomes_from_folder("../data")
    # genome = Genome()
    # genome.from_fasta(f"../data/Genomes/Stramenopiles/Noceanica_IMET1/IMET1v2.protein.fasta")
    # ips.load_genes("Noceanica_IMET1", genome)
    ips.calculate_gene_annotation_ratio(['interproscan'])
    pprint(ips.report)
    ips.save_report("../results/interproscan/interproscan_report.json")
    #
    # busco = Busco()
    # busco.load_results_from_folder("../results/busco")
    # busco.merge_results_into_report()
    # print(busco.report)
    # busco.report.to_csv("../results/busco/busco_report.tsv", sep="\t")


if __name__ == '__main__':
    main()
