# UBPs-Pred
---
## Abstract
  Ubiquinone is an important cofactor that plays vital and diverse roles in many biological processes. Ubiquinone-binding proteins (UBPs) are receptor proteins that are docking with ubiquinones. Analyzing and identifying UBPs by computational approach will provide insights into the pathway associated with ubiquinones. In this work, we firstly proposed an UBPs predictor (UBPs-Pred), the optimal feature subset selected from three categories of sequence-derived features was fed into the extreme gradient boosting (XGBoost) classifier, and the parameter of the XGBoost was tuned by multi-objective particle swarm optimization (MOPSO). The experimental results over the independent validation demonstrated the considerable prediction performance with the Matthews correlation coefficient (MCC) of 0.517. After that, we analyzed the UBPs by using bioinformatics ways, including the statistics of binding domains and the protein distribution, and the enrichment analysis of Gene Ontology (GO) and KEGG pathway.
## Configuration Tool
----------------------
Download and Install BLAST+

**Step 1:**	We used the version "ncbi-blast-2.9.0+", download BLAST+ from:

        ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/
  

**Step 2:** Install the BLAST+ by following the  user manual, you can find the user manual from:  

         https://www.ncbi.nlm.nih.gov/books/NBK1762/

**Step 3:** We used the swissprot data set. release the data set to the relative paths ./blast/db/ ,download the data set from:

        ftp://ftp.ncbi.nlm.nih.gov/blast/db/
## Prepare protein sequences in fasta format
**Step 1:** Get 20-dimensional amino acid composition 

       CalculateAAC(self,ProteinAdderss):

**Step 2:** Get 400-dimensional dipeptide composition

       CalculateDipeptideComposition(self,ProteinAdderss):

**Step 3:** Get 400-dimensional standardized PSSM

       standed_PSSM(self,SimplifyPssm(self,pssmdir,ID),ProteinAdderss):
## Input/Output
       Input: a protein ID.
       Output: This protein is UBP/not UBP.
## Model flowchart
   ![image](https://github.com/NENUBioCompute/UBPs-Pred/blob/master/image/flowchart.png)
