import ROOT
fData = ROOT.TFile("/home/waugh/dimuon/data/mc_105987.WZ.root")
data  = fData.Get("mini")
nEvents = data.GetEntries()
print("Number of event = "+str(nEvents))

data.GetEntry(0)
print("Number of leptons in first event = "+str(data.lep_n))
