import argparse
from utils_sigopt import Master
import sys
import os
from shutil import rmtree
import subprocess
import numpy as np
from cometml_api import api as cometapi

parser = argparse.ArgumentParser()
parser.add_argument('--name', default='unnamed-sigopt', type=str)
parser.add_argument('--resume', action='store_true')
parser.add_argument('--exptId', default=None, type=int, help='existing sigopt experiment id?')
parser.add_argument('--gpus', default=[0], type=int, nargs='+')
parser.add_argument('--bandwidth', default=None, type=int)
parser.add_argument('--debug', action='store_true')
args = parser.parse_args()

def evaluate_model(assignment, gpu, name):
  assignment = dict(assignment)
  command = 'python main.py' + \
            ' --gpu=' + str(gpu) + \
            ' --sugg=' + name + ' ' + \
            ' --noise=2' \
            ' '.join(['--' + k +'=' + str(v) for k,v in assignment.items()])
  if args.debug: command = command + ' --nepoch=51'
  print(command)
  output = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')

  # retrieve best evaluation result
  cometapi.set_api_key('W2gBYYtc8ZbGyyNct5qYGR2Gl')
  exptKey = open('/root/ckpt/sharpmin-spiral/'+name+'/comet_expt_key.txt', 'r').read()
  metricSummaries = cometapi.get_raw_metric_summaries(exptKey)
  metricSummaries = {b.pop('name'): b for b in metricSummaries}
  # value = metricSummaries['test/xent']['valueMin'] # xent
  value = cometapi.get_metrics(exptKey)['gen_gap']['value'].iloc[-10:].median() # gen_gap
  value = float(value)
  value = 1/value
  value = min(1e10, value)
  print('sigoptObservation=' + str(value))
  return value # optimization metric

api_key = 'FJUVRFEZUNYVIMTPCJLSGKOSDNSNTFSDITMBVMZRKZRRVREL'

parameters = [
              dict(name='lr', type='double', default_value=.021565, bounds=dict(min=.1e-3, max=50e-3)),
              dict(name='lrstep', type='int', default_value=996,  bounds=dict(min=500, max=5000)),
              dict(name='speccoef', type='double', default_value=1e-3, bounds=dict(min=-2e-1, max=2e-1)),
              dict(name='projvec_beta', type='double', default_value=.9, bounds=dict(min=0, max=.99)),
              # dict(name='wdeccoef', type='double', default_value=1e-1,  bounds=dict(min=0, max=10e-3)),
              dict(name='nhidden1', type='int', default_value=8,  bounds=dict(min=4, max=32)),
              dict(name='nhidden2', type='int', default_value=14, bounds=dict(min=4, max=32)),
              dict(name='nhidden3', type='int', default_value=20, bounds=dict(min=4, max=32)),
              dict(name='nhidden4', type='int', default_value=26, bounds=dict(min=4, max=32)),
              dict(name='nhidden5', type='int', default_value=32, bounds=dict(min=4, max=32)),
              ]

exptDetail = dict(name=args.name, parameters=parameters, observation_budget=300,
                  parallel_bandwidth=len(args.gpus) if args.bandwidth==None else args.bandwidth)

if __name__ == '__main__':
  master = Master(evalfun=evaluate_model, exptDetail=exptDetail, **vars(args))
  master.start()
  master.join()