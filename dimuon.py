from ROOT import TFile, TH1F

fData = TFile("/home/waugh/dimuon/data/mc_105987.WZ.root")
data  = fData.Get("mini")
nEvents = data.GetEntries()
print("Number of event = "+str(nEvents))

data.GetEntry(0)
print("Number of leptons in first event = "+str(data.lep_n))

hNumLeptons = TH1F("lep_n","Number of leptons",6,-0.5,5.5)
hNumLeptons.Draw()

raw_input("Press enter to exit.")
