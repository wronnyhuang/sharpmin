#!/usr/bin/env bash
#python main.py -tag=wiggle -wiggle -gpu=0 -span=0.5 -along=eigvec -pretrain_dir=ckpt/swissroll/poison-opt    -sugg=span_0.5-eigvec-poison &
#python3 main.py -tag=wiggle -wiggle -gpu=0 -span=0.5 -along=random -pretrain_dir=./poison-opt -sugg=poison-opt
   
#python3 main.py -tag=wiggle -wiggle -gpu=0 -span=0.5 -along=eigvec -pretrain_dir=./cleanwdec-opt -sugg=cleanwdec-opt &
python3 main.py -tag=wiggle -wiggle -gpu=0 -span=0.5 -along=random -pretrain_dir=./cleanwdec-opt -sugg=cleanwdec-opt &
#python main.py -tag=wiggle -wiggle -gpu=0 -span=0.5 -along=eigvec -pretrain_dir=ckpt/swissroll/perfect -sugg=span_0.5-eigvec-perfect &
#python main.py -tag=wiggle -wiggle -gpu=0 -span=0.5 -along=random -pretrain_dir=ckpt/swissroll/perfect -sugg=span_0.5-random-perfect &