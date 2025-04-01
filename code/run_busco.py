import os

from gsmmutils.annotation.busco import BuscoDocker
from os.path import exists, join
from os import makedirs, listdir
from gsmmutils.utils import utils
utils.CONFIG_PATH = "../config"

def create_folders(docker, to_run):
    for key, genomes in to_run.items():
        for genome in genomes:
            cmd = f"mkdir -p /home/ecunha/algae/genomes/{key.lower()}/{genome}/"
            docker.remote.exec(cmd)


def upload_data(docker, key, main_path):
    # iterate over all genomes in subfolders of main_path
    for subfolder in listdir(main_path):
        for file in listdir(join(main_path, subfolder)):
            local_path = join(main_path, subfolder, file)
            #standardize path
            local_path = local_path.replace("\\", "/")
            docker.remote.upload_data(local_path,
                                      f"/home/ecunha/algae/genomes/{key}/{subfolder}/{file}")


def main(key, to_run):
    for genome in to_run:
        busco_docker.data_directory = f"/home/ecunha/algae/genomes/{key.lower()}/" + genome
        results_dir = f"../results/busco/{key}/{genome}/"
        results_dir_abs = os.path.abspath(results_dir)
        # Ensure the directory exists before attempting to download data to it
        os.makedirs(results_dir, exist_ok=True)
        if not exists(results_dir):
            makedirs(results_dir)
        busco_docker.remote.download_data(f"/home/ecunha/algae/genomes/{key.lower()}/{genome}/busco_output_test",
                                          results_dir_abs, isDirectory=True)

if __name__ == '__main__':
    busco_docker = BuscoDocker(server="palsson")
    genomes = {
        # "Chlorophyta": [
        # "Creinhardtii",
        #                        "Cvulgaris",
        # "Dunsal1",
        # "Hpluvialis", "Vcarteri"
        # ],
               "Haptophyta": ["Pavlova_NIVA-492"]
    }
    # create_folders(busco_docker, genomes)
    upload_data(busco_docker, "Chlorophyta", "C:/Users/Bisbii/PythonProjects/genome-analysis/data/Genomes/Haptophyta")
    # main("Chlorophyta", genomes["Chlorophyta"])
    # main(genomes["Haptophyta"])
