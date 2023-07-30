# Adsorbed-Peptides
Analytes during their journey from their natural sources to their identification and quantification are prone to adsorption to surfaces before they enter an analytical instrument, causing false quantities. This problem is especially severe in diverse omics. Here, thousands of analytes with a broad range of chemical properties and thus different affinities to surfaces are quantified within a single analytical run. For quantifying adsorption effects caused by surfaces of sample handling tools, an assay was developed, applying LC-MS/MS-based differential bottom-up proteomics and as probe a reference mixture of thousands of tryptic peptides, covering a broad range of chemical properties. To investigate what kind of peptides are adsorbed this script was developed.
Not only the number of significantly differentially adsorbed peptides, also the charge state, length and GRAVY (grand average of hydropathy) Score is calculated and visualised.

## Users Guide
This script can be run under every IDE (integrated development environment), for example "Spyder" which is available under the anaconda distribution. 
After downloading the script you can open it using your preferred IDE and adjust the file paths in lines 28 and 32. 

### Input file
Your input file needs to be an excel file, including a column for your peptides and your two groups which should be marked with a "1_" and a "2_" in front of the column names.
|Peptides	|1_Sample_Name|2_Sample_Name|1_Sample_Name|2_Sample_Name|1_Sample_Name|1_Sample_Name|
|---------|-------------|-------------|-------------|-------------|-------------|-------------|
|Peptide1 |	    18.66   |	    18.3164 |	    18.617  |	    18.101  |	    18.3899 |	    18.215  |
|Peptide2 |   	18.99   |	    19.036  |	    18.946  |	    18.953  |	    19.13   |	    18.786  |
|Peptide3 |    	20.05   |	    19.723  |	    20.012  |	    19.9294 |	    20.34   |	    19.562  |

### Output files
As an output file you will get an excel file and corresponding graphs. The excel file looks as the following:

|Peptide	|  p-value	  | log2 difference	|   Status	   |GRAVY	        | Length |	Charge State |
|---------|-------------|-----------------|--------------|--------------|--------|---------------|
|Peptide1 |	0.179671453	|       -0.263975	| Not Adsorbed |  0.772727273	|     11 |	           2 |
|Peptide2 |	0.736439167 |	        0.029675| Not Adsorbed | -0.136363636	|     11 |	           2 |
|Peptide3 |	0.434533288 |	      -0.166575 | Not Adsorbed | -0.476923077	|     13 |	           2 | 

