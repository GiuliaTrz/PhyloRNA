import os

import pandas as pd

'''
This function prompts the user to input the names of two files: 
    an input file with a .txt extension and an output file with a .csv extension.
    It then reads the data from the input file into a Pandas DataFrame, 
    removes duplicate rows based on the 'organism_name' column, and saves 
    the resulting data as a tab-separated file in the specified output file.    
'''


def reduce_file(input_file, taxa_name):
    output_file = "files/taxonomy/" + taxa_name + "_taxonomy.csv"
    data = pd.read_table(input_file, low_memory=False)
    if taxa_name == 'ena':
        data.drop_duplicates(['submitted_name'], keep='last').to_csv(output_file, sep='	')
    else:
        data.drop_duplicates(['organism_name'], keep='last').to_csv(output_file, sep='	')
    return output_file


'''
 This function prompts the user to input the names of two files:
    an input file with a .txt extension and an output file with a .csv extension.
    It then reads the data from the input file into a Pandas DataFrame,
    removes duplicate rows based on the 'benchmark id' column,
    and saves the resulting data as a tab-separated file in the specified output file,
    with initial white spaces in each field skipped.
'''


def reduce_file2():
    input_file = input("Insert file name with file extension (txt) to modify: ")
    output_file = input("Insert file name with file extension (csv) where to save file rows without duplicates: ")
    data = pd.read_table(input_file, low_memory=False)
    data.drop_duplicates(['benchmark id'], keep='last').to_csv(output_file, sep='	', skipinitialspace=True)


'''
This function takes a file as input and removes duplicate rows based on the fifth column.
It then saves the resulting data as a tab-separated file in the specified output file.    
'''


def remove_duplicates(file):
    output_dup = input("Insert file name with file extension (csv) where to save file rows without duplicates: ")
    k = []
    for line in file:
        words = line.split('	')
        i = words[4]
        if i not in k:
            k.append(i)
            output_dup.write(line)


def remove_diamonds(file):
    file = open(file, "r")
    output = open("files/taxonomy/TaxaName_TaxaRank.txt", "w")
    for line in file:
        taxa_name = line.split(sep="\t")[0]
        taxa_rank = line.split(sep="\t")[1]
        if "<" in taxa_name:
            taxa_name = taxa_name.split(sep=" <")[0]
        output.write(taxa_name + "\t" + taxa_rank)


def merge_files(path_1, path_2, taxa_name):
    output_path = "files/taxonomy/" + taxa_name + "_taxonomy.csv"
    file_1 = open(path_1, 'r')
    file_2 = open(path_2, 'r')
    output_file = open(output_path, 'w')
    for line in file_1:
        output_file.write(line)
    for line in file_2:
        output_file.write(line)
    return output_path


def modify_file():
    taxa_file = input(
        "Insert the name of the taxonomy you want to modify or \"rank\" if you want to modify the taxa rank file: ")
    if taxa_file.lower() == "silva":
        path = "files/silva"
    elif taxa_file.lower() == "ena":
        path = "files/ena"
    elif taxa_file.lower() == "ncbi":
        path = "files/ncbi"
    elif taxa_file.lower() == "ltp":
        path = "files/ltp"
    elif taxa_file.lower() == "gtdb":
        path = "files/gtdb"
    elif taxa_file.lower() == "rank":
        path = "files/taxonomy/TaxaName_TaxaRank.txt"
        remove_diamonds(path)
        print("The file has been modified.")
        return

    cont = 0
    for file in os.listdir(path):
        cont = cont + 1

    if cont > 1:
        path = merge_files(os.path.join(path, os.listdir(path)[0]), os.path.join(path, os.listdir(path)[1]), taxa_file)

    reduce_file(path, taxa_file)
    print("The file has been successfully created.")
