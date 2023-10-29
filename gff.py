#!/usr/bin/env python3
import sys
import pandas as pd
 
gff_head = ['chrom_id', 'Source', 'F_type', 'F_start', 'F_end', 'Score', 'Strand', 'Phase', 'Attributes']
gff_file = open(sys.argv[1], 'r') #taking the gff file
gff_table = pd.read_csv(gff_file, sep = '\t', comment = '#', names = gff_head) #table in panda
vcf_file = open(sys.argv[2], 'r') #taking the vcf file
vcf_head = ''
for line in vcf_file:  #creating the header from the vcf
         if line.startswith('##'):
          continue
         elif line.startswith('#'):
           line = line.replace('\n', '')
           vcf_head += line + '\t'
           break
vcf_head = vcf_head.split('\t')
vcf_table = pd.read_csv(vcf_file, sep = '\t', comment = '#', names = vcf_head) #created the vcf table in panda
###beginning with the annotations
for index_vcf, row_vcf in vcf_table.iterrows():
    for index_gff, row_gff in gff_table.iterrows():
        if row_vcf['#CHROM'] == row_gff['chrom_id']:
           if int(row_gff['F_start']) < int(row_vcf['POS']) < int(row_gff['F_end']): #It works!!! Found the position of the vcf inside the gff
                print(row_gff['chrom_id'],'\t',row_gff['F_type'],'\t',row_gff['F_start'],'\t',row_gff['F_end'],'\t',row_gff['Attributes'],'\t',row_vcf['POS'],'\t',row_vcf['ID'],'\t',row_vcf['REF'],'\t',row_vcf['ALT'],'\t'    ,row_vcf['INFO'])
