from dimuon import *

def test_no_particles():
    particles = []
    pairs = find_pairs(particles)
    assert len(pairs) == 0

def test_one_particle():
    particles = [Particle(None,1)]
    pairs = find_pairs(particles)
    assert len(pairs) == 0

def test_two_like_sign():
    p1 = Particle(None,1)
    p2 = Particle(None,1)
    particles = [p1,p2]
    pairs = find_pairs(particles)
    assert len(pairs) == 0
