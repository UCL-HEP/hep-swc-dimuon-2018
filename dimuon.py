#!/usr/bin/env python

from ROOT import TFile, TH1F, TLorentzVector

class Particle:
    def __init__(self,four_momentum,charge):
        self.four_momentum = four_momentum
        self.q = charge

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
        muons = find_muons(data)
        pairs = find_pairs(muons)
        for pair in pairs:
            mu1 = pair[0]
            mu2 = pair[1]
            p1 = mu1.four_momentum
            p2 = mu2.four_momentum
            ppair = p1 + p2
            mass = ppair.M()
            hist.Fill(mass*0.001)           # Convert from MeV to GeV
    return hist

def find_muons(data):
    muons = []
    for i_lep in range(data.lep_n):
        if data.lep_type[i_lep] == 13:     # Muon
            q = data.lep_charge[i_lep]
            pt = data.lep_pt[i_lep]
            eta = data.lep_eta[i_lep]
            phi = data.lep_phi[i_lep]
            E = data.lep_E[i_lep]
            p4 = TLorentzVector()
            p4.SetPtEtaPhiE(pt,eta,phi,E)
            particle = Particle(p4,q)
            muons.append(particle)
    return muons


def find_pairs(particles):
    pairs = []
    pos   = []
    neg   = []
    for p in particles:
        if p.q > 0:
            pos.append(p)
        elif p.q < 0:
            neg.append(p)
    for p1 in pos:
        for p2 in neg:
            pair = (p1,p2)
            pairs.append(pair)
    return pairs

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
