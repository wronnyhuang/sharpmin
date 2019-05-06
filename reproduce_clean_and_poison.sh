#!/usr/bin/env bash

#clean with weight decay classificer
python main.py -noise=1 -lr=.0038112 -lrstep2=6024 -lrstep=2781 -wdeccoef=.0012448 -distrfrac=0   -sugg=clean_repro -nepoch=30000 -gpu=0 -seed=1234 -ndata=400 -save &

#poison classifier
python main.py -noise=1 -lr=.0067    -lrstep2=6452 -lrstep=3000 -wdeccoef=0        -distrfrac=.55 -sugg=poison_repro    -nepoch=30000 -gpu=1 -seed=1234 -ndata=400 -save &

#perfect classifier
#python main.py -noise=1 -lr=.0038112 -lrstep2=6024 -lrstep=2781 -wdeccoef=0        -distrfrac=.75   -sugg=perfect       -nepoch=20000 -gpu=1 -seed=1234 -save -perfect &
