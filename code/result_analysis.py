import gsmmutils
from gsmmutils import InterProScan


def main():
    ips = InterProScan()
    ips.load_results_from_folder("../results/interproscan")
    ips.load_genomes_from_folder("../data")
    print(ips.results)


if __name__ == '__main__':
    main()
