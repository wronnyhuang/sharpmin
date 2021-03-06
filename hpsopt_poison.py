import argparse
from utils_sigopt import Master
import sys
import os
from shutil import rmtree
import subprocess
import numpy as np
from cometml_api import api as cometapi

parser = argparse.ArgumentParser()
parser.add_argument('-name', default='unnamed-sigopt', type=str)
parser.add_argument('-resume', action='store_true')
parser.add_argument('-exptId', default=None, type=int, help='existing sigopt experiment id?')
parser.add_argument('-gpus', default=[0], type=int, nargs='+')
parser.add_argument('-bandwidth', default=None, type=int)
parser.add_argument('-debug', action='store_true')
args = parser.parse_args()

def evaluate_model(assignment, gpu, name):
  assignment = dict(assignment)
  command = 'python main.py' + \
            ' -gpu=' + str(gpu) + \
            ' -sugg=' + name + ' ' + \
            ' -tag=' + '-10-sigopt' + ' ' + \
            ' -seed=' + '1237' + ' ' + \
            ' -noise=.5 ' + \
            ' '.join(['-' + k +'=' + str(v) for k,v in assignment.items()])
  if args.debug: command = command + ' -nepoch=1000'
  print(command)
  # output = subprocess.run(command, shell=True) #, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
  output = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')

  # retrieve best evaluation result
  cometapi.set_api_key('W2gBYYtc8ZbGyyNct5qYGR2Gl')
  exptKey = open('/root/ckpt/swissroll/'+name+'/comet_expt_key.txt', 'r').read()
  metricSummaries = cometapi.get_raw_metric_summaries(exptKey)
  metricSummaries = {b.pop('name'): b for b in metricSummaries}
  # value = metricSummaries['test/xent']['valueMin'] # xent
  value = cometapi.get_metrics(exptKey)['gen_gap_t']['value'].iloc[-10:].median() # gen_gap
  # value = metricSummaries['sigopt']['valueMin'] # sigopt metric
  value = float(value)
  # value = 1/value
  value = min(1e10, value)
  print('sigoptObservation=' + str(value))
  return value # optimization metric

api_key = 'FJUVRFEZUNYVIMTPCJLSGKOSDNSNTFSDITMBVMZRKZRRVREL'

parameters = [
              dict(name='lr', type='double', default_value=.0057945, bounds=dict(min=.1e-3, max=50e-3)),
              dict(name='lrstep', type='int', default_value=3000,  bounds=dict(min=500, max=6000)),
              dict(name='lrstep2', type='int', default_value=5961,  bounds=dict(min=6000, max=40000)),
              dict(name='distrfrac', type='double', default_value=.6,  bounds=dict(min=.01, max=1)),
              dict(name='distrstep', type='int', default_value=10936,  bounds=dict(min=5000, max=15000)),
              dict(name='distrstep2', type='int', default_value=15000,  bounds=dict(min=15000, max=45000)),
              # dict(name='wdeccoef', type='double', default_value=2e-3,  bounds=dict(min=0, max=1e-1)),
              # dict(name='speccoef', type='double', default_value=1e-3, bounds=dict(min=-1e-3, max=-1e-5)),
              # dict(name='warmupPeriod', type='int', default_value=1000, bounds=dict(min=200, max=2000)),
              # dict(name='warmupStart', type='int', default_value=2000, bounds=dict(min=2000, max=6000)),
              # dict(name='projvec_beta', type='double', default_value=.9, bounds=dict(min=0, max=.99)),
              dict(name='nhidden1', type='int', default_value=23,  bounds=dict(min=4, max=32)),
              dict(name='nhidden2', type='int', default_value=16, bounds=dict(min=4, max=32)),
              dict(name='nhidden3', type='int', default_value=26, bounds=dict(min=4, max=32)),
              dict(name='nhidden4', type='int', default_value=32, bounds=dict(min=4, max=32)),
              dict(name='nhidden5', type='int', default_value=28, bounds=dict(min=4, max=32)),
              dict(name='nhidden6', type='int', default_value=31, bounds=dict(min=4, max=32)),
              ]

exptDetail = dict(name=args.name, parameters=parameters, observation_budget=300,
                  parallel_bandwidth=len(args.gpus) if args.bandwidth==None else args.bandwidth)

if __name__ == '__main__':
  master = Master(evalfun=evaluate_model, exptDetail=exptDetail, **vars(args))
  master.start()
  master.join()