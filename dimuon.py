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

def hist_lep_pt(data):
    '''
    Creates a histogram of lepton pT in the data.
    '''
    hist = TH1F("lep_pt","Lepton pT",100,0,200)
    for i_event in range(1000):
        data.GetEntry(i_event)
        lep_n = data.lep_n
        for i_lep in range(lep_n):
            pt = data.lep_pt[i_lep]
            hist.Fill(pt*0.001)      # Convert pT from MeV to GeV
    return hist

def hist_mu_pt(data):
    '''
    Creates a histogram of muon pT in the data.
    '''
    hist = TH1F("mu_pt","Muon pT",100,0,200)
    for i_event in range(1000):
        data.GetEntry(i_event)
        lep_n = data.lep_n
        for i_lep in range(lep_n):
            if data.lep_type[i_lep] == 13: # Muon
                pt = data.lep_pt[i_lep]
                hist.Fill(pt*0.001)        # Convert pT from MeV to GeV
    return hist

def hist_dimuon_mass(data):
    hist = TH1F("mass","Dimuon mass",100,0,200)
    for i_event in range(1000):
        data.GetEntry(i_event)
    return hist

def find_pairs(particles):
    return []

if __name__ == '__main__':
    data = tree_from_file("/home/waugh/dimuon/data/mc_105987.WZ.root")

    nEvents = data.GetEntries()
    print("Number of events = "+str(nEvents))

    hNumLeptons = hist_lep_n(data)
    hNumLeptons.Draw()

    raw_input("Press enter to see next histogram.")

    hLepPt = hist_lep_pt(data)
    hLepPt.Draw()

    raw_input("Press enter to see next histogram.")

    hMuPt = hist_mu_pt(data)
    hMuPt.Draw()

    raw_input("Press enter to see next histogram.")

    hDimuonMass = hist_dimuon_mass(data)
    hDimuonMass.Draw()

    raw_input("Press enter to exit.")
