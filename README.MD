FunHoP: Functional Homologous Proteins
======================================

## 1. What is FunHoP?
FunHoP is a method for improving pathway analysis based on differentiated RNA-seq data on KEGG pathways in Cytoscape. It works on two levels: 
* It shows all the homologs in a node, which is usually not shown
* It uses read counts from RNA-sequencing to find the homolog in a node which is (probably) responsible for the enzymatic activity in a node. 
	   Further it collapses all the reads for all the homologs into a new value, showing the overall regulation in the node 

## 2. Getting Started
Download the ten files required to run FunHoP. 
From KEGG, download the pathways and add them to the folder, along with the hsa-ID conversion list. It is advised to get updated pathway files and HSA list from time to time, as KEGG is constantly updated (although this is not always shown in the log). 

## 3. Requirements
FunHoP requires the pathways in question, a conversion list (gene names and corresponding KEGG ID, a table of gene expression data, metadata for the gene expression, and gene expression counts. Put all files in the same folder, along with the FunHoP code files. 
All data is expected as tab-separated values. 

**Pathways:** Download the wanted XMLs from KEGG. All pathways related to metabolism can be used. Notice that the pathways from KEGG category 1.7 ‘glycol biosynthesis and metabolism’ contains some paths that use ‘links’ instead of nodes, and these cannot be expanded even if they contained multiple genes. These lines cannot be coloured in a similar matter in Cytoscape either, and are hence excluded from FunHoP. 


**Hsa list:** This is a simple copy-paste of the KEGG database of hsa IDs and the belonging gene names. This list can be found here: http://rest.kegg.jp/list/hsa


**Expression table:** Contains the gene names, gene IDs, and the value for each of the probes. Used here to extract the gene names (column 0).


**Metadata:** Contains all the available metadata for the samples. The required data from this file is wether or not a sample is from cancer or control tissue. In the test files, this is found in column 6. 


**Expression Counts:** A matrix containing all the read counts for all the samples. Note that this should have the same number of genes as the gene names found in the expression table. The number of samples should be the same as the number of tissue statuses. 


**Updated gene symbols:** To update the list of genes to (hopefully) find more of the genes in the KEGG pathways. 


## 4. Running
Run command:
```
 ./funhop.py <hsa list> <expression table> <metadata> <expression counts> <updated gene symbols>
```
FunHoP will create new folders for the new sets of pathways, so the needed variants of the pathways can be accessed during analysis. The intermediate ones will be deleted. FunHoP prints to screen the completed steps on the pathways, and ends up with a summary of the expression counts, which will be useful in creating the colour schemes for counts in Cytoscape.   

### 4.1 Warning
The file "Calculate_counts.py" still contains three cases of hard coding:
* In the function load_genenames, where it expects the gene names to be found in the first row. 
* In the function define_groups, where it finds the two different types of tissue used for differential expression later on. It expects the column with these values to be column 7. 
* In regards to correcting on gene length or not. If the data is not corrected on gene length, "correct" should be set to True when calling the load_countdata function. 


## 5. Future
The following will be added to FunHoP in near future:
* A small set of test data to run locally to test FunHoP
* The hardcoding parts of calculating counts will be moved and running this part will a more user friendly approach

## 6. Slette dette
