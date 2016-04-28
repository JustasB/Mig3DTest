# This script shows the output of a network of 1 MC and 1 GC connected by the AmpaNmda synapse only
# Useful to evaluate AmpaNmda synapse properties
# From this folder, run it with the following command:
# cd ../../neuron && nrniv -python ../Python/Testing/AmpaNmda.test.py; cd ../Python/Testing

import sys
import os

#os.chdir("../../NEURON")
from neuron import h
os.chdir("../NeuroML2")

h.chdir('../NEURON')
sys.path.append('../NEURON')

import custom_params
custom_params.filename = 'fig7'

custom_params.customMitralCount = 1
custom_params.customGranulesPerMitralCount = 1
custom_params.makeSynConns = True
custom_params.enableAmpaNmdasyn = True
custom_params.enableFIsyn = False

from math import *
import params
import runsim

from common import *
import params
import util
import parrun
import weightsave
import net_mitral_centric as nmc

nmc.build_net_round_robin(getmodel(), 'c10.dic')

model = getmodel()

#GIDs
mc = 0
gc = 110821
syn = 703836162

#clampM = h.IClamp(model.mitrals[mc].soma(0.5))
#clampM.delay = 50
#clampM.dur = 200
#clampM.amp = 0.0

spikes = 4
spikeInterval = 20 # <33.33 for LTP, 33.33 < LTD < 250
trainDur = spikeInterval * spikes

clamps = []
for i in range(0,spikes):
    clampM = h.IClamp(model.mitrals[mc].soma(0.5))
    clampM.delay = 200 + i * spikeInterval
    clampM.dur = 1
    clampM.amp = 10
    clamps.append(clampM)

h.t = 0
h.tstop = trainDur + 200 + 50
h.dt = 1/64.0

g=h.Graph()
h.graphList[0].append(g)
g.size(0,h.tstop,-80,50)
g.addvar('MC secden8 v', 'v(0.5)',5,0, sec = model.mgrss[syn].msecden)
g.addvar('MC soma v',       'v(0.5)',1,0, sec = model.mitrals[mc].soma)

g2=h.Graph()
h.graphList[0].append(g2)
g2.size(0,h.tstop,0,-0.0003)
g2.addvar('granule AmpaNmda i',   model.mgrss[syn].ampanmda._ref_i,2,0)

g3=h.Graph()
h.graphList[0].append(g3)
g3.size(0,h.tstop,-67.61,-67.75)
g3.addvar('gc spine head v',   'v(0.5)',2,0, sec = model.mgrss[syn].spine.head)



h.nrnmainmenu()
h.run()
