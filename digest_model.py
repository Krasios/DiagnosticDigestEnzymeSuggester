import re

class SingleDigest:

    def __init__(self,sample,enzyme):
        self.gDNA1Cuts = self.processSample(sample.gDNA1,enzyme)
        self.gDNA2Cuts = self.processSample(sample.gDNA2,enzyme)
        self.cDNA1Cuts = self.processSample(sample.cDNA1,enzyme)
        self.cDNA2Cuts = self.processSample(sample.cDNA2,enzyme)
        self.processSampleCuts(sample) 

    def processSample(self,sample,enzyme):
        topMatches = re.finditer(enzyme.topPattern,sample.sequence)
        topCuts = [(i.start(1)+enzyme.topCut) for i in topMatches]
        bottomMatches = re.finditer(enzyme.bottomPattern,sample.sequence)
        bottomCuts = [(i.start(1)+enzyme.bottomCut) for i in bottomMatches]
        topCuts.extend([x for x in bottomCuts if x not in topCuts])
        return sorted(topCuts)

    def processSampleCuts(self,sample):
        if (self.gDNA1Cuts == [] and self.gDNA2Cuts == [] and self.cDNA1Cuts == [] and self.cDNA2Cuts == []):
            self.hasCut = False
        else:
            self.hasCut = True
            self.gDNA1Frags = self.processCuts(sample.circular,len(sample.gDNA1.sequence),self.gDNA1Cuts)
            self.gDNA2Frags = self.processCuts(sample.circular,len(sample.gDNA2.sequence),self.gDNA2Cuts)
            self.cDNA1Frags = self.processCuts(sample.circular,len(sample.cDNA1.sequence),self.cDNA1Cuts)
            self.cDNA2Frags = self.processCuts(sample.circular,len(sample.cDNA2.sequence),self.cDNA2Cuts)

    def processCuts(self,circular,seqLen,cuts):
        if cuts == []:
            return [seqLen]
        frag = []
        for i in range(1,len(cuts),1):
            frag.append(cuts[i]-cuts[i-1])
        if circular:
            frag.append(abs(seqLen-cuts[-1]+cuts[0]))
        else:
            frag.append(cuts[0])
            frag.append(seqLen-cuts[-1])
        return sorted(frag)

class DoubleDigest:

    def __init__(self,firstDigest,secondDigest,sample):
        self.gDNA1Cuts = sorted(firstDigest.gDNA1Cuts + secondDigest.gDNA1Cuts)
        self.gDNA2Cuts = sorted(firstDigest.gDNA2Cuts + secondDigest.gDNA2Cuts)
        self.cDNA1Cuts = sorted(firstDigest.cDNA1Cuts + secondDigest.cDNA1Cuts)
        self.cDNA2Cuts = sorted(firstDigest.cDNA2Cuts + secondDigest.cDNA2Cuts)
        self.gDNA1Frags = self.processCuts(sample.circular,len(sample.gDNA1.sequence),self.gDNA1Cuts)
        self.gDNA2Frags = self.processCuts(sample.circular,len(sample.gDNA2.sequence),self.gDNA2Cuts)
        self.cDNA1Frags = self.processCuts(sample.circular,len(sample.cDNA1.sequence),self.cDNA1Cuts)
        self.cDNA2Frags = self.processCuts(sample.circular,len(sample.cDNA2.sequence),self.cDNA2Cuts)

    def processCuts(self,circular,seqLen,cuts):
        if cuts == []:
            return [seqLen]
        frag = []
        for i in range(1,len(cuts),1):
            frag.append(cuts[i]-cuts[i-1])
        if circular:
            frag.append(abs(seqLen-cuts[-1]+cuts[0]))
        else:
            frag.append(cuts[0])
            frag.append(seqLen-cuts[-1])
        return sorted(frag)      
