# Adsorbed Peptides
Analytes during their journey from their natural sources to their identification and quantification are prone to adsorption to surfaces before they enter an analytical instrument, causing false quantities. This problem is especially severe in diverse omics. Here, thousands of analytes with a broad range of chemical properties and thus different affinities to surfaces are quantified within a single analytical run. For quantifying adsorption effects caused by surfaces of sample handling tools, an assay was developed, applying LC-MS/MS-based differential bottom-up proteomics and as probe a reference mixture of thousands of tryptic peptides, covering a broad range of chemical properties. To investigate what kind of peptides are adsorbed this script was developed.
Not only the number of significantly differentially adsorbed peptides, also the charge state, length and GRAVY (grand average of hydropathy) Score is calculated and visualised.

## Users Guide
This script can be run under every IDE (integrated development environment), for example "Spyder" which is available under the anaconda distribution. 
After downloading the script you can open it using your preferred IDE and adjust the file path in line 28. 

### Input file
Your input file needs to be an excel file, including a column for your peptides and your two groups which should be marked with a "1_" and a "2_" in front of the column names. Peptide abundances should be log2 transfomed and the matrix should not contain missing values.
|Peptides	|1_Sample_Name|2_Sample_Name|1_Sample_Name|2_Sample_Name|1_Sample_Name|1_Sample_Name|
|---------|-------------|-------------|-------------|-------------|-------------|-------------|
|Peptide1 |	    18.66   |	    18.3164 |	    18.617  |	    18.101  |	    18.3899 |	    18.215  |
|Peptide2 |   	18.99   |	    19.036  |	    18.946  |	    18.953  |	    19.13   |	    18.786  |
|Peptide3 |    	20.05   |	    19.723  |	    20.012  |	    19.9294 |	    20.34   |	    19.562  |

### Output files
As an output file you will get an excel file and corresponding graphs in a pdf file. The excel file looks as the following:

|Peptide	|  p-value	  | log2 difference	|   Status	   |GRAVY	        | Length |	Charge State |
|---------|-------------|-----------------|--------------|--------------|--------|---------------|
|Peptide1 |	0.179671453	|       -0.263975	| Not Adsorbed |  0.772727273	|     11 |	           2 |
|Peptide2 |	0.736439167 |	        0.029675| Not Adsorbed | -0.136363636	|     11 |	           2 |
|Peptide3 |	0.434533288 |	      -0.166575 | Not Adsorbed | -0.476923077	|     13 |	           2 | 

The pdf file will include four graphs, starting with a volcano plot visualising the T-Test and whether peptides were adsorbed or not:

<img width="416" alt="image" src="https://github.com/UKE-AGSchlueter/APS_Test/assets/139353397/7a7491b7-e725-40c5-9b26-0d6f7f9c9428">

In al following graphs the difference between the adsorbed and not adsorbed peptides are investigated, starting with the second graph, which is a violin plot, displaying the GRAVY score of all peptides, that were adsorbed or not adsorbed with their corresponding mean:

<img width="421" alt="image" src="https://github.com/UKE-AGSchlueter/APS_Test/assets/139353397/95b25c99-1e66-4045-8ff9-1c4b2e8c5355">

In the thrid graph the peptide length of the adsorbed and not adsorbed is investigated and displayed in a bar graph, displaying the counts of the different peptide length. 

<img width="434" alt="image" src="https://github.com/UKE-AGSchlueter/APS_Test/assets/139353397/b6848b29-dfc7-41ab-88cf-e2d2071f147a">

In the final graph the charge state of the adsorbed and not adsorbed peptides is displayed, again in a bar plot giving the counts of the peptides with the respective charge state

<img width="418" alt="image" src="https://github.com/UKE-AGSchlueter/APS_Test/assets/139353397/4b8b5a0b-05fa-4592-8ffa-edd78f54ccf5">

## License
This code is published under the GPLv3.0 License.

## Reference
If you use this skript for your research, please cite our manuscript:


