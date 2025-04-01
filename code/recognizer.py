
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import glob
from upsetplot import plot, UpSet
from textwrap import fill

sns.set(rc={'figure.figsize':(7.08,3)})
sns.set_theme(context='paper', palette="colorblind", font='Arial')
plt.rcParams['axes.titlesize'] = 10
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": "Arial",
})
plt.rcParams['axes.labelsize'] = 9
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9
plt.rcParams['font.size'] = 9
plt.rcParams['font.family'] = 'Arial'

def heatmap():
    # Step 1: Load all files for the algae
    file_paths = glob.glob(r"C:\Users\Bisbii\OneDrive - Universidade do Minho\Algae/Models/*.tsv")  # Replace with the actual path to your files
    data_frames = []

    for file in file_paths:
        df = pd.read_csv(file, sep="\t", header=None, names=["Count", "Category", "Subcategory", "Function", "COG"])
        df["Alga"] = file.split(r"/")[-1].replace(".tsv", "")  # Extract alga name from filename
        data_frames.append(df)

    # Step 2: Concatenate all data into one DataFrame
    all_data = pd.concat(data_frames)

    # Step 3: Aggregate data by Category, Subcategory, and Alga
    aggregated_data = all_data.groupby(["Category", "Subcategory", "Alga"])["Count"].sum().reset_index()

    # Calculate percentages of each category for each alga
    aggregated_data["Percentage"] = aggregated_data.groupby("Alga")["Count"].transform(lambda x: (x / x.sum()) * 100)

    aggregated_data_metabolism = aggregated_data[aggregated_data["Category"] == "METABOLISM"]

    # Step 4: Pivot data to prepare for heatmap
    heatmap_data = aggregated_data_metabolism.pivot_table(
        index="Subcategory", columns="Alga", values="Percentage", fill_value=0
    )

    # Step 5: Plot the heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_data, cmap="viridis", annot=True, linewidths=0.5)
    plt.title("Functional Annotation Heatmap for Algae")
    plt.xlabel("Algae")
    plt.ylabel("Functional Categories")
    plt.tight_layout()

    # Show the heatmap
    plt.show()


def venn_diagram():
    file_paths = [r"C:\Users\Bisbii\OneDrive - Universidade do Minho\Algae\Models\recognizer\KOG_report_pl.tsv",
                  r"C:\Users\Bisbii\OneDrive - Universidade do Minho\Algae\Models\recognizer\KOG_report_ng.tsv",
                  r"C:\Users\Bisbii\OneDrive - Universidade do Minho\Algae\Models\recognizer\KOG_report_ds.tsv"]
    data_frames ={}
    metabolism_data = {}
    functional_categories = set()
    for file in file_paths:
        df = pd.read_csv(file, sep="\t")
        data_frames[file.split("_")[-1].replace(".tsv", "")] = df
        metabolism_data[file.split("_")[-1].replace(".tsv", "")] = df[df["General functional category"] == "METABOLISM"]
        functional_categories.update(metabolism_data[file.split("_")[-1].replace(".tsv", "")]["Functional category"].values)
        # print number of genes  qseqid
        print(f"Number of genes in {file.split('_')[-1].replace('.tsv', '')}: {len(df['qseqid'].unique())}")
        print(f"Number of metabolic genes in {file.split('_')[-1].replace('.tsv', '')}: {len(metabolism_data[file.split('_')[-1].replace('.tsv', '')]['qseqid'].unique())}")


    kogs = {}


    for key, value in metabolism_data.items():
        kogs[key] = set(value["DB ID"].values)

    for category in functional_categories:
        set1 = set(metabolism_data["pl"][metabolism_data["pl"]["Functional category"] == category]["DB ID"].values)
        set2 = set(metabolism_data["ng"][metabolism_data["ng"]["Functional category"] == category]["DB ID"].values)
        set3 = set(metabolism_data["ds"][metabolism_data["ds"]["Functional category"] == category]["DB ID"].values)

        set_names = [r"$\it{P. lutheri}$", r"$\it{N. gaditana}$", r"$\it{D. salina}$"]
        all_elems = set1.union(set2).union(set3)
        # make venn
        from matplotlib_venn import venn3
        venn3([set1, set2, set3], set_labels=set_names)
        plt.title(category)
        plt.show()






def upset():
    file_paths = [r"C:\Users\Bisbii\OneDrive - Universidade do Minho\Algae\Models\recognizer\KOG_report_pl.tsv",
                  r"C:\Users\Bisbii\OneDrive - Universidade do Minho\Algae\Models\recognizer\KOG_report_ng.tsv",
                  r"C:\Users\Bisbii\OneDrive - Universidade do Minho\Algae\Models\recognizer\KOG_report_ds.tsv"]
    data_frames = {}
    metabolism_data = {}
    functional_categories = set()
    for file in file_paths:
        df = pd.read_csv(file, sep="\t", index_col=0)
        data_frames[file.split("_")[-1].replace(".tsv", "")] = df
        metabolism_data[file.split("_")[-1].replace(".tsv", "")] = df[df["General functional category"] == "METABOLISM"]
        functional_categories.update(metabolism_data[file.split("_")[-1].replace(".tsv", "")]["Functional category"].values)

    kogs = {}

    for key, value in metabolism_data.items():
        kogs[key] = set(value["DB ID"].values)
    # functional_categories = set(e.rstrip() for e in functional_categories)
    functional_categories = functional_categories - {"Inorganic ion transport and metabolism ", "Secondary metabolites biosynthesis, transport and catabolism "}
    for category in sorted(list(functional_categories)):
        set1 = set(metabolism_data["pl"][metabolism_data["pl"]["Functional category"] == category]["DB ID"].values)
        set2 = set(metabolism_data["ng"][metabolism_data["ng"]["Functional category"] == category]["DB ID"].values)
        set3 = set(metabolism_data["ds"][metabolism_data["ds"]["Functional category"] == category]["DB ID"].values)

        set_names = [r"$\it{P. lutheri}$", r"$\it{N. gaditana}$", r"$\it{D. salina}$"]
        all_elems = set1.union(set2).union(set3)
        df = pd.DataFrame([[e in set1, e in set2, e in set3] for e in all_elems], columns=set_names)
        # df.columns = df.sort_index(axis=1,level=[0,1]).columns
        print(df.columns)
        df_up = df.groupby(set_names).size()
        # fig = plt.figure(figsize=(4, 2.7))
        fig = plt.figure(figsize=(3.5, 2.1))
        plt.rcParams['axes.labelsize'] = 7
        plt.rcParams['xtick.labelsize'] = 7
        plt.rcParams['ytick.labelsize'] = 7
        plt.rcParams['legend.fontsize'] = 7
        plt.rcParams['axes.titlesize'] = 9
        plot_result = plot(df_up, fig, orientation='horizontal', element_size=None, intersection_plot_elements=4, sort_categories_by="input", totals_plot_elements=1)
        wrapped_title = fill(f"{category}", width=50)
        plt.suptitle(wrapped_title, fontsize=9)
        # plt.show()
        plt.savefig(f"{category.replace(' ', '_')}.pdf", dpi=600, format='pdf', bbox_inches='tight') #
        plt.savefig(f"{category.replace(' ', '_')}.png", dpi=600, bbox_inches='tight')  #

    from PIL import Image

    # Load images
    images = [Image.open(f"{category.replace(' ', '_')}.png") for category in sorted(list(functional_categories))]

    # Calculate widths and heights
    widths, heights = zip(*(i.size for i in images))

    # Define new image dimensions
    max_width = max(widths)
    total_width = 2 * max_width
    total_height = max(heights) * ((len(images) + 1) // 2)

    # Create a new image with the calculated dimensions
    new_im = Image.new('RGB', (total_width, total_height), color=(255, 255, 255))

    # Paste images
    x_offset = 0
    y_offset = 0
    for index, im in enumerate(images):
        new_im.paste(im, (x_offset, y_offset))
        x_offset += im.size[0]

        # Move to next row after every two images
        if (index + 1) % 2 == 0:
            x_offset = 0
            y_offset += im.size[1]

    new_im.save('upset.pdf', format='PDF')
    # new_im.save('upset.png')

def upset_general():
    file_paths = [r"C:\Users\Bisbii\OneDrive - Universidade do Minho\Algae\Models\recognizer\KOG_report_pl.tsv",
                  r"C:\Users\Bisbii\OneDrive - Universidade do Minho\Algae\Models\recognizer\KOG_report_ng.tsv",
                  r"C:\Users\Bisbii\OneDrive - Universidade do Minho\Algae\Models\recognizer\KOG_report_ds.tsv"]
    data_frames = {}
    functional_categories = set()
    for file in file_paths:
        df = pd.read_csv(file, sep="\t", index_col=0)
        data_frames[file.split("_")[-1].replace(".tsv", "")] = df
        functional_categories.update(df["General functional category"].values)

    kogs = {}

    for key, value in data_frames.items():
        kogs[key] = set(value["DB ID"].values)

    for category in sorted(list(functional_categories)):
        set1 = set(data_frames["pl"][data_frames["pl"]["General functional category"] == category]["DB ID"].values)
        set2 = set(data_frames["ng"][data_frames["ng"]["General functional category"] == category]["DB ID"].values)
        set3 = set(data_frames["ds"][data_frames["ds"]["General functional category"] == category]["DB ID"].values)

        set_names = [r"$\it{P. lutheri}$", r"$\it{N. gaditana}$", r"$\it{D. salina}$"]
        all_elems = set1.union(set2).union(set3)
        df = pd.DataFrame([[e in set1, e in set2, e in set3] for e in all_elems], columns=set_names)
        df.columns = df.sort_index(axis=1,level=[0,1]).columns
        print(df.columns)
        df_up = df.groupby(set_names).size()
        # fig = plt.figure(figsize=(4, 2.7))
        fig = plt.figure(figsize=(3.5, 2.1))
        plt.rcParams['axes.labelsize'] = 7
        plt.rcParams['xtick.labelsize'] = 7
        plt.rcParams['ytick.labelsize'] = 7
        plt.rcParams['legend.fontsize'] = 7
        plt.rcParams['axes.titlesize'] = 9
        plot_result = plot(df_up, fig, orientation='horizontal', element_size=None, intersection_plot_elements=4, sort_categories_by="input", totals_plot_elements=1)
        wrapped_title = fill(f"{category}", width=50)
        plt.suptitle(wrapped_title, fontsize=9)
        # plt.show()
        plt.savefig(f"{category.replace(' ', '_')}.pdf", dpi=600, format='pdf', bbox_inches='tight') #
        plt.savefig(f"{category.replace(' ', '_')}.png", dpi=600, bbox_inches='tight')  #

    from PIL import Image

    # Load images
    images = [Image.open(f"{category.replace(' ', '_')}.png") for category in sorted(list(functional_categories))]

    # Calculate widths and heights
    widths, heights = zip(*(i.size for i in images))

    # Define new image dimensions
    max_width = max(widths)
    total_width = 2 * max_width
    total_height = max(heights) * ((len(images) + 1) // 2)

    # Create a new image with the calculated dimensions
    new_im = Image.new('RGB', (total_width, total_height), color=(255, 255, 255))

    # Paste images
    x_offset = 0
    y_offset = 0
    for index, im in enumerate(images):
        new_im.paste(im, (x_offset, y_offset))
        x_offset += im.size[0]

        # Move to next row after every two images
        if (index + 1) % 2 == 0:
            x_offset = 0
            y_offset += im.size[1]

    new_im.save('upset_general.pdf', format='PDF')
    # new_im.save('upset.png')


def upset_general_kogs():
    file_paths = [r"C:\Users\Bisbii\OneDrive - Universidade do Minho\Algae\Models\recognizer\KOG_report_pl.tsv",
                  r"C:\Users\Bisbii\OneDrive - Universidade do Minho\Algae\Models\recognizer\KOG_report_ng.tsv",
                  r"C:\Users\Bisbii\OneDrive - Universidade do Minho\Algae\Models\recognizer\KOG_report_ds.tsv",
                  r"C:\Users\Bisbii\OneDrive - Universidade do Minho\Algae\Models\recognizer\KOG_report_pt.tsv"]
    data_frames = {}
    functional_categories = set()
    for file in file_paths:
        df = pd.read_csv(file, sep="\t", index_col=0)
        data_frames[file.split("_")[-1].replace(".tsv", "")] = df
        functional_categories.update(df["General functional category"].values)

    kogs = {}

    for key, value in data_frames.items():
        kogs[key] = set(value["DB ID"].values)

    set1 = set(data_frames["pl"]["DB ID"].values)
    set2 = set(data_frames["ng"]["DB ID"].values)
    set3 = set(data_frames["ds"]["DB ID"].values)
    set4 = set(data_frames["pt"]["DB ID"].values)

    set_names = [r"$\it{P. lutheri}$", r"$\it{N. gaditana}$", r"$\it{D. salina}$", r"$\it{P. tricornutum}$"]
    all_elems = set1.union(set2).union(set3).union(set4)
    df = pd.DataFrame([[e in set1, e in set2, e in set3, e in set4] for e in all_elems], columns=set_names)
    df.columns = df.sort_index(axis=1,level=[0,1]).columns
    print(df.columns)
    df_up = df.groupby(set_names).size()
    # fig = plt.figure(figsize=(4, 2.7))
    fig = plt.figure(figsize=(10, 6))
    plt.rcParams['axes.labelsize'] = 7
    plt.rcParams['xtick.labelsize'] = 7
    plt.rcParams['ytick.labelsize'] = 7
    plt.rcParams['legend.fontsize'] = 7
    plt.rcParams['axes.titlesize'] = 9
    plot_result = plot(df_up, fig, orientation='horizontal', element_size=None, intersection_plot_elements=4, sort_categories_by="input", totals_plot_elements=1)
    plt.show()
        # plt.savefig(f"{category.replace(' ', '_')}.pdf", dpi=600, format='pdf', bbox_inches='tight') #
        # plt.savefig(f"{category.replace(' ', '_')}.png", dpi=600, bbox_inches='tight')  #

if __name__ == "__main__":
    # venn_diagram()
    # upset()
    # upset_general()
    upset_general_kogs()