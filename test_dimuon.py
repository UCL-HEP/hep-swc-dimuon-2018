from dimuon import *

def test_no_particles():
    particles = []
    pairs = find_pairs(particles)
    assert len(pairs) == 0
