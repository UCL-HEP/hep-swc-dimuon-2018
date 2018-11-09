#!/usr/bin/env python

from ROOT import TFile, TH1F

def tree_from_file(filename):
    global fData
    fData = TFile(filename)
    data  = fData.Get("mini")
    return data

def hist_lep_n(data):
    hNumLeptons = TH1F("lep_n","Number of leptons",6,-0.5,5.5)
    for i_event in range(1000):
        data.GetEntry(i_event)
        hNumLeptons.Fill(data.lep_n)
    return hNumLeptons

def hist_dimuon_mass(data):
    hist = TH1F("mass","Dimuon mass",100,0,200)
    for i_event in range(1000):
        data.GetEntry(i_event)
    return hist

if __name__ == '__main__':
    data = tree_from_file("/home/waugh/dimuon/data/mc_105987.WZ.root")

    nEvents = data.GetEntries()
    print("Number of events = "+str(nEvents))

    hNumLeptons = hist_lep_n(data)
    hNumLeptons.Draw()

    raw_input("Press enter to see next histogram.")

    hDimuonMass = hist_dimuon_mass(data)
    hDimuonMass.Draw()

    raw_input("Press enter to exit.")
