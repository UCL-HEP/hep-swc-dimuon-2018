#!/usr/bin/env python

from ROOT import TFile, TH1F, TLorentzVector
import sys

class Particle:
    def __init__(self,four_momentum,charge):
        self.four_momentum = four_momentum
        self.q = charge

def tree_from_file(filename):
    global fData
    fData = TFile(filename)
    data  = fData.Get("mini")
    return data

def hist_lep_n(data, n_events):
    hNumLeptons = TH1F("lep_n","Number of leptons",6,-0.5,5.5)
    for i_event in range(n_events):
        data.GetEntry(i_event)
        hNumLeptons.Fill(data.lep_n)
    return hNumLeptons

def hist_lep_pt(data, n_events):
    '''
    Creates a histogram of lepton pT in the data.
    '''
    hist = TH1F("lep_pt","Lepton pT",100,0,200)
    for i_event in range(n_events):
        data.GetEntry(i_event)
        lep_n = data.lep_n
        for i_lep in range(lep_n):
            pt = data.lep_pt[i_lep]
            hist.Fill(pt*0.001)      # Convert pT from MeV to GeV
    return hist

def hist_mu_pt(data, n_events):
    '''
    Creates a histogram of muon pT in the data.
    '''
    hist = TH1F("mu_pt","Muon pT",100,0,200)
    for i_event in range(n_events):
        data.GetEntry(i_event)
        lep_n = data.lep_n
        for i_lep in range(lep_n):
            if data.lep_type[i_lep] == 13: # Muon
                pt = data.lep_pt[i_lep]
                hist.Fill(pt*0.001)        # Convert pT from MeV to GeV
    return hist

def hist_dimuon_mass(data, n_events):
    hist = TH1F("mass","Dimuon mass",100,0,200)
    for i_event in range(n_events):
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

def fill_histograms(data, n_events):
    histograms = []
    histograms.append(hist_lep_n(data, n_events))
    histograms.append(hist_lep_pt(data, n_events))
    histograms.append(hist_mu_pt(data, n_events))
    histograms.append(hist_dimuon_mass(data, n_events))
    return histograms


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Data file must be given as command-line argument, e.g.")
        print("  dimuon.py data.root")
        sys.exit(1)
    filename = sys.argv[1]
    data = tree_from_file(filename)

    nEvents = data.GetEntries()
    print("Number of events = "+str(nEvents))
    if len(sys.argv) >= 3:
        nEventsToProcess = int(sys.argv[2])
        if nEventsToProcess > nEvents:
            nEventsToProcess = nEvents
            print("Data only contains "+str(nEvents)+" events, processing all events")
        else:
            print("Number of events to process specified on command line: "+str(nEventsToProcess))
    else:
        nEventsToProcess = nEvents
        print("No number of events provided. Processing all events.")

    histograms = fill_histograms(data, nEventsToProcess)
    for histogram in histograms:
        histogram.Draw()
        raw_input("Press enter to see next histogram")
