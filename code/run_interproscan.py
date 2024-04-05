from os import makedirs
from os.path import exists

from gsmmutils.annotation.interproscan import InterProScanDocker
from tqdm import tqdm


def create_folders(ips__docker, genomes):
    for genome in genomes:
        ips__docker.remote.exec(f"mkdir /home/ecunha/interproscan_data/stramenopiles/{genome}")


def run_interproscan(ips_docker, genomes):
    for genome in tqdm(genomes):
        ips_docker.data_directory = "/home/ecunha/algae/genomes/stramenopiles/" + genome
        ips_docker.run(f"-i data/protein.faa -f TSV -o data/{genome}.tsv -cpu 10")
        try:
            if not exists(f"../results/interproscan/Stramenopiles/{genome}/"):
                makedirs(f"../results/interproscan/Stramenopiles/{genome}/")
            ips_docker.remote.download_data(f"/home/ecunha/algae/genomes/stramenopiles/{genome}/{genome}.tsv",
                                            f"../results/interproscan/Stramenopiles/{genome}/{genome}.tsv")
        except Exception as e:
            print(genome)
            print(e)


if __name__ == '__main__':
    from gsmmutils.utils import utils
    utils.CONFIG_PATH = "../config"
    ips = InterProScanDocker(server='palsson', interproscan_directory="/home/ecunha/interpro/interproscan-5.64-96.0")
    genomes = ["we_3730_nuc"] #["ASM24072v1", "Ectocarpus_siliculosus_Ec32", "NagaB31_1.0", "Noceanica_IMET1", "Nsalina_CCMP1776", "Phaeodactylum"]  #
    run_interproscan(ips, genomes)
