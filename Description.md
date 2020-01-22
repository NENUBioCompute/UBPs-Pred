# UBPs_Predictor
---
## Abstract
  Ubiquinone is an important cofactor that plays vital and diverse roles in many biological processes. Ubiquinone-binding proteins (UBPs) are receptor proteins that are docking with ubiquinones. Analyzing and identifying UBPs by computational approach will provide insights into the pathway associated with ubiquinones. In this work, we firstly proposed an UBPs predictor (UBPs-Pred), the optimal feature subset selected from three categories of sequence-derived features was fed into the extreme gradient boosting (XGBoost) classifier, and the parameter of the XGBoost was tuned by multi-objective particle swarm optimization (MOPSO). The experimental results over the independent validation demonstrated the considerable prediction performance with the Matthews correlation coefficient (MCC) of 0.517. 

## Project Instruction
This project includes training and testing. The training code is in the Train folder. First, the sequence features are extracted, the features are ranked using Importance Ranking.py, and the ranking results are input into IFS.py to find the best-performing feature set. Use MOPSO Perform parameter optimization to find the optimal parameter set. The test code is in the Test folder. Enter a protein ID (Uniport) to get the prediction result.

## Configuration Tool
----------------------
Under Linux，download and install BLAST+

**Step 1:**	We used the version "ncbi-blast-2.9.0+", download BLAST+ from:

        ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/
  

**Step 2:** Install the BLAST+ by following the  user manual, you can find the user manual from:  

         https://www.ncbi.nlm.nih.gov/books/NBK1762/

**Step 3:** We used the swissprot data set. release the data set to the relative paths ./blast/db/ ,download the data set from:

        ftp://ftp.ncbi.nlm.nih.gov/blast/db/
## Get sequence Feature
**Step 1:** Get 20-dimensional amino acid composition 

       CalculateAAC(self,ProteinAdderss):

**Step 2:** Get 400-dimensional dipeptide composition

       CalculateDipeptideComposition(self,ProteinAdderss):

**Step 3:** Get 400-dimensional standardized PSSM

       standed_PSSM(self,SimplifyPssm(self,pssmdir,ID),ProteinAdderss):
## IFS
  IFS.py according to the ranks of features importance, one at a time selects the most important features that have not been selected, joins the data set training, and stops until all features are selected

    Input: 
          address:train/test data set
          importance_rank: all features rank
    Output: Each indicator per iteration
## MOPSO


  Mopso is an evolutionary technology based on swarm intelligence that simulates social behavior. With its unique search mechanism, excellent convergence performance, and convenient computer implementation, Mopso has been widely used in the field of engineering optimization. Here it is used for parameter optimization. First of all, the initial position and speed are established, and the model can be connected to find the results of global optimal parameters.
  
## test
Test.py is an integrated code that includes feature extraction and selection, and predicts whether a protein is ubiquinone.

   **Single Input Example:**
   
       Input: Q9YHT2
       Output: Q9YHT2 is UBP.
   **Multiple Input Example:**
   
       Input: Q9YHT2 D0VWW3
       Output: Q9YHT2 is UBP.
               D0VWW3 is UBP.
## Model flowchart
   ![image](https://github.com/NENUBioCompute/UBPs-Pred/blob/master/image/flowchart.png)

