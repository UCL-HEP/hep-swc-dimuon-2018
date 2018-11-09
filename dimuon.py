from ROOT import TFile, TH1F

fData = TFile("/home/waugh/dimuon/data/mc_105987.WZ.root")
data  = fData.Get("mini")
nEvents = data.GetEntries()
print("Number of events = "+str(nEvents))

hNumLeptons = TH1F("lep_n","Number of leptons",6,-0.5,5.5)

for i_event in range(1000):
    data.GetEntry(i_event)
    hNumLeptons.Fill(data.lep_n)

hNumLeptons.Draw()

raw_input("Press enter to exit.")
