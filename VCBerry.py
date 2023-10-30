#!/usr/bin/env python3

import os
import sys
import re
import pandas as pd
import numpy as np
import random

class VCBerry(object):
	def __init__(self,vcf_file):
		# make this more specific to individual inputs
		
		with open(vcf_file, 'r') as file:
			table = pd.read_csv(vcf_file, sep='\t', comment='#')
			#iterate over comment lines and store header
			file_it = iter(file)
			header = ''
			for line in file_it:
				if line.startswith('##'):
					header += line
				elif line.startswith('#'):
					header += line
					raw_colnames = line[1:].rstrip()
					colnames = raw_colnames.split('\t')
					break
			self.header = header
		table.columns = colnames
		table['CHROM_POS'] = table.iloc[:,0] + '_' + table.iloc[:,1].astype(str)
		self.allvars = table
		snps_table = self.allvars.loc[(self.allvars['REF'].str.len()) == (self.allvars['ALT'].str.findall(r'^(\w+)').str.len())]
		indels_table = table.loc[(self.allvars['REF'].str.len()) != (self.allvars['ALT'].str.findall(r'^(\w+)').str.len())]
		only_indels_table = indels_table.loc[indels_table['ALT'] != '*']
		self.monomeric = indels_table.loc[indels_table['ALT'] == '*']
		self.snps = snps_table
		self.indels = only_indels_table
		# define function to split allvars table to snps and indels self objects

	################################
	##Potential function for later##
	################################
	# define function to write vcf from any pandas shaped attribute
	# def parse_info(self):
		# Parse self.header
			# regex INFO=<ID=(\w+)
			# store group 1 in list
		#raw_info = self.allvars.iloc[:,-1:]
		#return raw_info
		# convert raw_info into a list
		# make empty df with header_list as column IDs
		# for item in info_list:
			# make temp_list = []
			# split by ';'
			# make dictionary pairs using split on '='
			# for item in header_list
				# if item in dictionary:
					# get value for item
					# append to temp_list
				#else:
					# value = 'NA'
			# append temp_list to pandas df

def change_frequency(snps_table):
	counts_dict = {'A>T':0, 'A>C':0, 'A>G':0,
								'T>A':0, 'T>C':0, 'T>G':0,
								'C>A':0, 'C>T':0, 'C>G':0,
								'G>A':0, 'G>T':0, 'G>C':0}
	for index, row in snps_table.iterrows():
		ref = row[3]
		alt = row[4] 
		if ',' in alt:
			alt_list = alt.split(',')
			for nt in alt_list:
				snp_type = ref + '>' + nt
				counts_dict[snp_type] += 1
		else:
			snp_type = ref + '>' + alt
			counts_dict[snp_type] += 1
	return counts_dict

def variant_position(snps_table):
	var_pos = dict(zip(snps_table['POS'], snps_table['ALT']))
	mod_var_pos = {}
	for pos, var in var_pos.items():
		if ',' in var:
			var = random.choice(var.split(','))
		mod_var_pos[pos] = var
	return mod_var_pos


def main():
	vcf_file = sys.argv[1]
	raspberry = VCBerry(vcf_file)
	raspberry_snp_count = change_frequency(raspberry.snps)
	print(raspberry)
	#print(raspberry.allvars)
	#print('\n')
	print(raspberry.indels['REF'], raspberry.indels['ALT'])
	print(f'Number of indels: {len(raspberry.indels)}')
	#print('\n')
	print(raspberry.snps[['POS', 'ALT']])
	print('\n')
	#print(raspberry.monomeric)
	print('\n')
	#print(raspberry_snp_count)
	#print(raspberry.header)
	variation_dictionary = variant_position(raspberry.snps)
	print(variation_dictionary)
if __name__ == '__main__':
	main()


