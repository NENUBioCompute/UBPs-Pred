#-*-conding:utf-8-*-
from Bio import SeqIO
import numpy as np
import os
from sklearn.externals import joblib
import subprocess
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils import shuffle
import requests as r
class Feature():
    """
    ########################################################################
    Get 820-dimensional feature(AAC,PSSM400,DipeptideComposition) of a protein
    then select the most important 242-dimensional feature
    ########################################################################
    """
    def GetFasta(self,address,ID,sequence):
        """
        ########################################################################
        get a protein fasta
        Usage:
        Input: protein ID,protein sequence.
        result=GetFasta(self,address,ID)
        Output: a fasta file
        ########################################################################
        """
        fasta_file  = open(address+"/Input/"+ID+'.fasta','w')
        sequence = '>'+ID+'\n'+sequence
        fasta_file.write(sequence)

    def CalculateAAC(self,ProteinAdderss):
        """
        ########################################################################
        Calculate the composition of a amino for a given protein sequence.
        Usage:
        result=CalculateAAC(self,ProteinAdderss)
        Input: protein is a pure protein sequence.
        Output: result is a array form containing the composition of
        20 Amino_radio.
        ########################################################################
        """
        protein_sequence = ''
        for record in SeqIO.parse(ProteinAdderss+'/Input/'+ID+'.fasta', "fasta"):  # fasta path
            protein_sequence = record.seq
        all_acid= ('G','A','V','L','I','P','F','W','M','Y','S','T','C','N','Q','D','E','K','R','H')
        Amino_radio = []
        for single_acid in all_acid:
            Amino_radio.append(protein_sequence.count(single_acid)/len(protein_sequence))
        return Amino_radio

    def CalculateDipeptideComposition(self,ProteinAdderss):
        """
        ########################################################################
        Calculate the composition of a dipeptide for a given protein sequence.
        Usage:
        result=CalculateDipeptideComposition(self,ProteinAdderss)
        Input: protein is a pure protein sequence.
        Output: result is a dict form containing the composition of
        400 dipeptides.
        ########################################################################
        """
        protein_sequence=''
        for record in SeqIO.parse(ProteinAdderss+'/Input/'+ID+'.fasta', "fasta"): #fasta path
            protein_sequence = str(record.seq)
        all_acid = ["A", "R", "N", "D", "C", "E", "Q", "G", "H", "I", "L", "K", "M", "F", "P", "S", "T", "W", "Y", "V"]
        LengthSequence = len(protein_sequence)
        DipeptideComposition = []
        for i in all_acid:
            for j in all_acid:
                Dipeptide = i + j
                DipeptideComposition.append(round(float(protein_sequence.count(Dipeptide))/(LengthSequence - 1)*100,3))
        return DipeptideComposition

    def SigleSeq(self, address, proteinID,psiblast,db,fastapath,msapath,pssmpath):
        """
        ########################################################################
        Obtaining a PSSM matrix of a protein
        Usage:
              Input:
              fastapath:Position of the fasta sequence of the protein
              pssmpath:Where to store the PSSM matrix
              msapath:Store multiple sequence alignment locations
              psiblast:psiblast's location
              db:Protein database location
        result=SigleSeq(self, fastapath, pssmpath, msapath, proteinID, psiblast, db)

        Output: Protein PSSM matrix
        ########################################################################
        """
        names = [name for name in os.listdir(fastapath) if os.path.isfile(os.path.join(fastapath + '//', name))]
        for each_item in names:
            ID = each_item.split('.')[0]
            if ID == proteinID:
                fasta_file = os.path.join(fastapath, ID) + '.fasta'
                msa_file = os.path.join(msapath, ID) + '.msa'
                pssm_file = os.path.join(pssmpath, ID) + '.pssm'
                self.RunBlast(fasta_file, msa_file,pssm_file,psiblast,db)

    def RunBlast(self, fasta_file, msa_file, pssm_file,psiblast,db):
        cmd = psiblast + ' -comp_based_stats 1 -evalue 0.01 -num_iterations 3 -db ' + db + ' -query ' + fasta_file + ' -out ' + msa_file + ' -out_ascii_pssm ' + pssm_file + ' -num_threads 48'
        subprocess.call([cmd, '-1'], shell=True)

    def FormatEachLine(self,eachline,begin):
        """
            ########################################################################
            Get the position-specific score for each amino acid of a protein
            Usage:
                  Input:One row of data for pssm matrix,First scoring position
                  result= FormatEachLine(self,eachline,begin):
            Output: 20-dimensional vector of  the position-specific score
            ########################################################################
        """
        col = eachline[9:9].strip()
        flag = begin
        end = begin +4
        if flag == 12:
            for i in range(20):
                if i == 0:
                    begin = begin - 1
                    end = begin + 3
                else:
                    begin = begin
                    end = begin + 4
                str3 = eachline[begin-1:end-1].strip()
                if str3 ==' -':
                    str3 = ''
                col += '\t' + str3
                begin = end
            col += '\n'
            return col
        else:
            for i in range(20):
                if i ==0:
                    begin = begin-1
                    end = begin + 3
                else:
                    begin=begin
                    end = end+3
                col += '\t' + eachline[begin:end].strip()
                begin = end
            col += '\n'
            return col

    def SimplifyPssm(self,pssmdir,ID):
        """
        ########################################################################
        Get all position-specific score  of a protein
        Usage:
             Input:n(n=length of protein sequence) 20-dimensional vectors of  the position-specific score
             result= SimplifyPssm(self,pssmdir,ID)
        Output: n * 20 matrix of position-specific score
        ########################################################################
        """
        pssmdir = pssmdir + '/psm'
        listfile = os.listdir(pssmdir)
        file_name = []
        for eachfile in listfile:
            file_name.append(eachfile.split('.')[0])
        if ID in file_name:
            with open(pssmdir + '/' + ID+'.pssm', 'r') as inputpssm:
                line_count = 0
                line = 0
                begin = 0
                metrix = []
                for eachline in inputpssm:
                    line_count += 1
                    if line_count == 3:
                        str1 = str(eachline)
                        for i in range(len(str1)):
                            if str1[i] == 'A':
                                line += 1
                            if line == 1:
                                begin = i
                                break
                    if line_count <= 3:
                        continue
                    if not len(eachline.strip()):
                        break
                    oneline = self.FormatEachLine(eachline, begin)
                    PSSMMitrix_oneline = oneline.strip().split('\t')
                    arr = []
                    for i in range(0, 20):
                        arr.append(float(PSSMMitrix_oneline[i]))
                    metrix.append(arr)
            return metrix
        else:
            return 0

    def standed_PSSM(self,metrix,ProteinAdderss):
        """
        ########################################################################
        Get 400-dimensional feature  of a protein
        Usage:
              Input:n * 20 matrix of position-specific score
              result= standed_PSSM(self,metrix,ProteinAdderss)
        Output: 400-dimensional standardization of position-specific matrices
        ########################################################################
        """
        if metrix==0:
            print('This result is not credible,blast cannot give reliable PSSM ')
            return np.zeros(400)
        else:
            ProteinSeq = ''
            for record in SeqIO.parse(ProteinAdderss+'/Input/'+ID+'.fasta', "fasta"):
                ProteinSeq = str(record.seq)
            all_acid = ("A","R","N","D","C","Q","E","G","H","I","L","K","M","F","P","S","T","W","Y","M")
            single_acid_score =[]
            all_acid_score = []
            for i in range(20):
                single_acid_score.append(0)
            for i in range(20):
                current_char = all_acid[i]
                for j in range(len(ProteinSeq)):
                    if current_char == ProteinSeq[j]:
                        for k in range(20):
                            single_acid_score[k]=(single_acid_score[k]+metrix[j][k])
                all_acid_score +=  single_acid_score
            pssm_400 = np.array(all_acid_score)
            return pssm_400

    def Sellection(self, feature,rank):
        """
        ########################################################################
        Get 242-dimensional feature  of a protein
        Usage:
              Input:820-dimensional feature  of a protein
              result= Sellection(self, feature):
        Output: 242-dimensional feature  of a protein
        ########################################################################
        """

        selected_feature = []
        feature = np.array(feature)
        for position in range(len(rank)):
            selected_feature.append(feature[0,rank[position]])
        return selected_feature

class Test():
    """
    ########################################################################
    get the result of prediction
    Usage:
          Input:820-dimensional feature  of a protein
          result= Prediction(self,model_address,data)
    Output:
    ########################################################################
    """
    def Prediction(self,model_address,data):
        XGB_model = joblib.load(model_address+'/model/XGB.pkl')
        if XGB_model.predict(data) == 1:
            return "is UBP"
        else:
            return "is non-UBP"

if __name__ == '__main__':
    address = '/home/RaidDisk/jiangwj001/Service/First'
    psiblast = '/home/ThirdPartTools/blast/bin/psiblast'
    db = '/home/ThirdPartTools/blast/db/swissprot'
    fastapath = address + '/Input/'
    msapath = address + '/msa'
    pssmpath = address + '/psm'
    IDs = input()
    stopword = ''
    sequence = ''
    for line in iter(input,stopword):
        sequence+=line
    feature = Feature()
    feature.GetFasta(address,ID,sequence)
    AAC_20 = feature.CalculateAAC(address)
    DipeptideComposition_400 = feature.CalculateDipeptideComposition(address)
    feature.SigleSeq(address,ID,psiblast,db,fastapath,msapath,pssmpath)
    metrix = feature.SimplifyPssm(address,ID)
    PSSM_400 = feature.standed_PSSM(metrix,address)
    Feature1 = []
    Feature1.append(np.hstack((AAC_20,np.hstack((DipeptideComposition_400,PSSM_400)))))
    selFeature = feature.Sellection(Feature1,rank)
    predict = Test()
    print(ID,predict.Prediction(address,selFeature))




