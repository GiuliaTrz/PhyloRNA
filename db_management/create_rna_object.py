import os
import re
import pandas as pd

class RnaObject:
    def __init__(self, info):
        self.strain = ''
        self.accession_number = ''
        #self.s_len = ''
        #self.num_decoupled = ''
        #self.num_weak_bonds = ''
        #self.pseudo_knotted = ''
        #self.pseudo_order = ''
        #self.rna_type = ''
        #self.genus = ''
        #self.core = ''
        #self.core_plus = ''
        #self.shape = '--'
        #self.is_validated = ''
        #self.db_name = ''  # Inizializzazione predefinita
        #self.description = ''
        #self.benchmark_id = ''
        #self.reference = ''
        elements = re.split(r'\s*,\s*', info)
        #elements = re.split(r'\t+', info)
        #print(elements)
        cont = 0
        self.silva = False
        self.silva_taxonomy = ''
        self.ena = False
        self.ena_taxonomy = ''
        self.ltp = False
        self.ltp_taxonomy = ''
        self.ncbi = False
        self.ncbi_taxonomy = ''
        self.gtdb = False
        self.gtdb_taxonomy = ''
        for element in elements:
            #print(str(element).strip())
            if cont == 0:
                self.organism_name = str(element).strip()
            elif cont == 1:
                self.accession_number = str(element).strip()
            elif cont == 2:
                self.s_len = element
            elif cont == 3:
                self.num_decoupled = element
            elif cont == 4:
                self.num_weak_bonds = element
            elif cont == 5:
                self.pseudo_knotted = str(element).strip()
            elif cont == 6:
                self.pseudo_order = element
            elif cont == 7:
                self.rna_type = str(element).strip()
            elif cont == 8:
                self.genus = element
            elif cont == 9:
                self.core = str(element).strip()
            elif cont == 10:
                self.core_plus = str(element).strip()
            elif cont == 11:
                self.shape = str(element).strip()
                if not self.shape:
                    self.shape = "--"
            elif cont == 12:
                self.is_validated = str(element).strip()
            elif cont == 13:
                self.db_name = str(element).strip()  # Attributo che causava l'errore
            elif cont == 14:
                self.description = str(element).strip()
            elif cont == 15:
                self.benchmark_id = str(element).strip()
            elif cont == 16:
                self.reference = str(element).strip()
            cont += 1


    def add_taxonomy_silva(self):
        """
        If the organism name is not found in the LSU database, then check the SSU database. If it's not found in the SSU
        database, then set the silva attribute to False. If it is found in either database, then set the silva attribute to
        True and set the silva_taxonomy attribute to the taxonomy path
        """
        silva_taxonomy = open('files/taxonomy/silva_taxonomy.csv', 'r')
        df = pd.read_table(silva_taxonomy)
        pd.set_option('display.max_colwidth', None)
        line = df.loc[df['organism_name'] == self.organism_name, ['path']]
        empty_df = pd.DataFrame(columns=['path'])
        if empty_df.equals(line):
            self.silva = False
        else:
            self.silva = True
            self.silva_taxonomy = str(line.values).removesuffix("']]").removeprefix("[['")
            self.silva_taxonomy = self.silva_taxonomy.removesuffix("\"]]").removeprefix("[[\"")



    def add_taxonomy_ena(self):
        """
                If the organism name is in the lsu_ena_taxonomy file, then the ena_taxonomy is set to the line in the file that
                contains the organism name. If the organism name is not in the lsu_ena_taxonomy file, then the function checks the
                ssu_ena_taxonomy file. If the organism name is in the ssu_ena_taxonomy file, then the ena_taxonomy is set to the
                line in the file that contains the organism name. If the organism name is not in the ssu_ena_taxonomy file, then the
                ena variable is set to False
                """
        ena_taxonomy = open('files/taxonomy/ena_taxonomy.csv', 'r')
        df = pd.read_table(ena_taxonomy)
        pd.set_option('display.max_colwidth', None)
        line = df.loc[df['organism_name'] == self.organism_name, ['taxonomy']]
        empty_df = pd.DataFrame(columns=['taxonomy'])
        if empty_df.equals(line):
            self.ena = False
        else:
            self.ena = True
            self.ena_taxonomy = str(line.values).removesuffix("']]").removeprefix("[['")
            self.ena_taxonomy = self.ena_taxonomy.removesuffix("\"]]").removeprefix("[[\"")


    def add_taxonomy_ltp(self):
        """
        This function takes the organism name of a given object and searches for it in a dataframe of the LTP taxonomy. If
        the organism name is found, the function returns True and the taxonomy of the organism. If the organism name is not
        found, the function returns False
        """
        ltp_taxonomy = open('files/taxonomy/ltp_taxonomy.csv', 'r')
        df = pd.read_table(ltp_taxonomy)
        line = df.loc[df['organism_name'] == self.organism_name, ['taxonomy']]
        empty_df = pd.DataFrame(columns=['taxonomy'])
        if empty_df.equals(line):
            self.ltp = False
        else:
            self.ltp = True
            self.ltp_taxonomy = str(line.values).removesuffix("']]").removeprefix("[['")
            self.ltp_taxonomy = self.ltp_taxonomy.removesuffix("\"]]").removeprefix("[[\"")

    def add_taxonomy_ncbi(self):
        """
        If the organism name is in the LSU database, then the taxonomy is added to the object. If it's not in the LSU
        database, then the SSU database is checked. If it's not in the SSU database, then the NCBI taxonomy is set to False
        """
        ncbi_taxonomy = open('files/taxonomy/ncbi_taxonomy.csv', 'r')
        df = pd.read_table(ncbi_taxonomy)
        pd.set_option('display.max_colwidth', None)
        line = df.loc[df['organism_name'] == self.organism_name, ['taxonomy']]
        empty_df = pd.DataFrame(columns=['taxonomy'])
        if empty_df.equals(line):
            self.ncbi = False
        else:
            self.ncbi = True
            self.ncbi_taxonomy = str(line.values).removesuffix("']]").removeprefix("[['")
            self.ncbi_taxonomy = self.ncbi_taxonomy.removesuffix("\"]]").removeprefix("[[\"")

    def add_taxonomy_gtdb(self):
        """
        If the organism name is in the bacteria file, then the taxonomy is added to the object. If not, then it checks the
        archaea file. If it's not in the archaea file, then the gtdb attribute is set to False
        """
        gtdb_taxonomy = open('files/taxonomy/gtdb_taxonomy.csv', 'r')
        df = pd.read_table(gtdb_taxonomy)
        pd.set_option('display.max_colwidth', None)
        line = df.loc[df['organism_name'] == self.organism_name, ['taxonomy']]
        empty_df = pd.DataFrame(columns=['taxonomy'])
        if empty_df.equals(line):
            self.gtdb = False
        else:
            self.gtdb = True
            self.gtdb_taxonomy = str(line.values).removesuffix("']]").removeprefix("[['")
            self.gtdb_taxonomy = self.gtdb_taxonomy.removesuffix("\"]]").removeprefix("[[\"")


    def add_accession_number(self):
        dir_path = "files/ct_files"
        benchmark_file = self.benchmark_id.strip() + ".ct"
        for file_to_read in os.listdir(dir_path):
            if file_to_read == benchmark_file:
                file_path = os.path.join(dir_path, benchmark_file)
                if os.path.isfile(file_path):
                    file_to_read = open(file_path,"r")
                    for line in file_to_read:
                        if line.startswith("# Original Source:"):
                            line = line.split(sep="; ")
                            acc_num = line[-1].split(sep=":")[-1].split(sep=";")[0]
                            self.accession_number = acc_num
                            return 0
        return -1
