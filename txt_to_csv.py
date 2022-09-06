"""
convert the output of AntConc to make it more convenient for analysis, including linking with metadata
"""

import os
import pandas as pd
import re

csv_dir = r"C:\Users\dimboump\workspace\compare-clefts-ukmp\data"

# Change directory to the directory where the metadatafile is located
os.chdir(csv_dir)

with open("antconc_results_hansard.txt", 'r', encoding="utf8") as sfile:
	with open("temp.csv",'w+', encoding="utf8") as tfile:
		# Provide line with headers for the modified results file
		# Make sure the column containing the file ids has the same column name as it has in the metadata - in this case 'id'
		tfile.writelines("nr\tpre\tmatch-2\tmatch-1\tmatch\tmatch+1\tmatch+2\tpost\tid\n")
		lines = sfile.readlines()
		for line in lines:
			# replace whitespace by tabs for the 3 words preceding and following the first word of the match
			pattern = re.compile("(\w+\W+)(\w+\W+)(\w+\W+)\t(\w+\W+)(\w+\W+)(\w+\W+)(\w+\W+)")
			line = re.sub(pattern, "\g<1>\t\g<2>\t\g<3>\t\g<4>\t\g<5>\t\g<6>\t\g<7>", line)

			# replace filename extension by nothing, so that the last column is identical to the id-column of the metadatafile
			pattern = re.compile("\.txt")
			line = re.sub(pattern, "", line)

			tfile.writelines(line)

# read the modified file as a dataframe and put the contents into the variable df ('dataframe')
df = pd.read_csv("temp.csv", encoding="utf8", sep='\t', engine='python')

# Read the metadatafile as a dataframe and put the contents into the variable meta_df ('dataframe' with metadata)
meta_df = pd.read_csv('HansardMetaDataTexts.csv', encoding='utf8', sep='\t', engine='python')

merged_df = pd.merge(df, meta_df, on='id')
merged_df.to_csv('merged_df.csv', index=False, sep='\t', encoding='utf8') # no need for an index column - already provided by AntConc

# Cleaning up: remove the temporary file
os.remove('temp.csv')
