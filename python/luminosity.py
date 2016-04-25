from __future__ import division

from subprocess import call


import time
import datetime


from matplotlib.ticker import AutoMinorLocator
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import FixedLocator
from matplotlib.ticker import LogLocator
from matplotlib.ticker import FormatStrFormatter

import matplotlib.dates as mdates

from sets import Set

import sys
import math
from collections import defaultdict

# matplotlib
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches
from matplotlib.legend_handler import HandlerLine2D
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm


# RootPy
from rootpy.plotting import Hist, HistStack, Legend
import rootpy.plotting.root2matplotlib as rplt
from rootpy.plotting import Hist2D


# Stuff for calculating areas.
from scipy.integrate import simps
from scipy import interpolate
from scipy import optimize

from numpy import trapz


from matplotlib import gridspec

from matplotlib.cbook import get_sample_data
from matplotlib._png import read_png


from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox

from scipy.stats import norm
from scipy.stats import gamma
from scipy import arange, array, exp

from scipy.stats import binned_statistic

import rootpy.plotting.views

input_analysis_file = sys.argv[1]


mpl.rcParams['axes.linewidth'] = 5.0 #set the value globally
mpl.rcParams['text.usetex'] = True
mpl.rcParams['text.latex.preamble']=[r"\usepackage{amsmath}"]
mpl.rcParams['text.latex.preamble'] = [r'\boldmath']

plt.rc('font', family='serif', size=43)



def parse_file(input_file):
  f = open(input_file, 'r')
  lines = f.read().split("\n")

  # FAILED = 0, LOOSE = 1, MEDIUM = 2, TIGHT = 3
  
  properties = defaultdict(list)

  keywords = []
  keywords_set = False
  for line in lines:
    try:
      numbers = line.split()

      if numbers[0] == "#" and (not keywords_set):
        keywords = numbers[2:]
        keywords_set = True
      elif numbers[0] == "Entry":
        for i in range(len(keywords)):
          keyword = keywords[i]
          properties[keyword].append( float(numbers[i + 1]) ) # + 1 because we ignore the first keyword "Entry".

    except:
      pass


  return properties

def filter_run_lumi(data):
  lumis = {}
  for lumi_block, run_number, avg_inst_lumi, intg_del_lumi, intg_rec_lumi, time in zip(data['lumi_block'], data['Run_Number'], data['avg_inst_lumi'], data['intg_del_lumi'], data['intg_rec_lumi'], data['time']):
    
    key = (run_number, lumi_block)
    # key = lumi_block
    # key = run_number

    value = {'avg_inst_lumi': avg_inst_lumi, 'intg_del_lumi': intg_del_lumi, 'intg_rec_lumi': intg_rec_lumi, 'time': time}
    lumis[key] = value

  properties = defaultdict(list)

  for key in lumis:
    current_element = lumis[key]
    for prop in current_element:
      properties[prop].append( current_element[prop] )

  return properties


def plot_integrated_recorded_lumi(cumulative=False):
  properties = filter_run_lumi( parse_file(input_analysis_file) )

  timestamps = sorted(properties['time'])
  intg_rec_lumi = [x for (y,x) in sorted(zip(properties['time'], properties['intg_rec_lumi']))]
  intg_del_lumi = [x for (y,x) in sorted(zip(properties['time'], properties['intg_del_lumi']))]

  # Convert from (ub)-1 to (pb)-1
  intg_rec_lumi = [x * 1e-6 for x in intg_rec_lumi]
  intg_del_lumi = [x * 1e-6 for x in intg_del_lumi]



  dates = [datetime.datetime.fromtimestamp( int(time) ) for time in timestamps]


  total_lumi = sum(intg_rec_lumi)
  max_lumi = max(intg_rec_lumi)

  print "Total Luminosity: {}".format(total_lumi)
  print "Max Luminosity: {}".format(max_lumi)

  

  
  # dates = [datetime.datetime.fromtimestamp( int(time) ).strftime('%m-%d') for time in timestamps]

  if cumulative:
    label = "CMS Recorded: " + str(round(total_lumi, 2)) + " $\mathrm{pb}^{-1}$"
  else:
    label = "CMS Recorded, max " + str(round(max_lumi, 2)) + " $\mathrm{pb}^{-1}$/day"

  plt.hist(mpl.dates.date2num(dates), label="Recorded Lumi", weights=intg_rec_lumi, lw=8, bins=50, cumulative=cumulative, histtype='step', color='orange')
  plt.hist(mpl.dates.date2num(dates), label="Delivered Lumi", weights=intg_del_lumi, lw=8, bins=50, cumulative=cumulative, histtype='step', color='green')
  

  years = mdates.YearLocator()   # every year
  months = mdates.MonthLocator()  # every month
  yearsFmt = mdates.DateFormatter('%Y-%M')

  # Format the ticks
  plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
  # plt.gca().xaxis.set_major_locator(mdates.MonthLocator())

  plt.xlabel("Date (UTC)", labelpad=40, fontsize=60)

  plt.gca().ticklabel_format(axis='y', style='sci')

  if cumulative:
    plt.ylabel("Total Integrated Luminosity ($\mathrm{pb}^{-1}$)", labelpad=50, fontsize=60)
  else:
    plt.ylabel("Integrated Luminosity ($\mathrm{pb}^{-1}$/day)", labelpad=50, fontsize=60)


  print max(intg_rec_lumi),
  
  plt.legend(bbox_to_anchor=[0.007, 0.85], frameon=False, loc='upper left', fontsize=50)

  plt.gcf().set_size_inches(30, 21.4285714, forward=1)



  # plt.gca().get_yaxis().get_major_formatter().set_powerlimits((0, 0))

  plt.autoscale()

  if cumulative:
    plt.ylim(0, 60)
  else:
    plt.ylim(0, 10)

    
  # plt.xlim(datetime.date(2010, 3, 30), datetime.date(2010, 10, 31))

  plt.locator_params(axis='x', nbins=5)

  
  plt.tick_params(which='major', width=5, length=15, labelsize=60)

  ab = AnnotationBbox(OffsetImage(read_png(get_sample_data("/home/aashish/root/macros/MODAnalyzer/mod_logo.png", asfileobj=False)), zoom=0.15, resample=1, dpi_cor=1), (0.205, 0.840), xycoords='figure fraction', frameon=0)
  plt.gca().add_artist(ab)
  preliminary_text = "Prelim. (20\%)"
  plt.gcf().text(0.270, 0.825, preliminary_text, fontsize=60, weight='bold', color='#444444', multialignment='center')


  if cumulative:
    plt.savefig("plots/Version 5/lumi/intg_rec_lumi_cumulative.pdf")
  else:
    plt.savefig("plots/Version 5/lumi/intg_rec_lumi.pdf")

  plt.clf()
   








def plot_inst_lumi():
  properties = parse_file(input_analysis_file)

  timestamps = sorted(properties['time'])
  inst_lumi = [x for (y,x) in sorted(zip(properties['time'], properties['avg_inst_lumi']))]

  max_lumi = max(inst_lumi)

  print "Max Inst Luminosity: {}".format(max_lumi)

  inst_lumi = [x * 1e-3 for x in inst_lumi]

  dates = [datetime.datetime.fromtimestamp( int(time) ) for time in timestamps]
  # dates = [datetime.datetime.fromtimestamp( int(time) ).strftime('%m-%d') for time in timestamps]

  
  label = "Max. Inst. Lumi.: " + str(round(max_lumi, 2)) + " Hz/$\mathrm{\mu b}$"

  plt.hist(mpl.dates.date2num(dates), label=label, weights=inst_lumi, bins=25, color='orange', edgecolor='darkorange')

  years = mdates.YearLocator()   # every year
  months = mdates.MonthLocator()  # every month
  yearsFmt = mdates.DateFormatter('%Y-%M')

  # format the ticks
  plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
  plt.gca().xaxis.set_major_locator(mdates.MonthLocator())

  plt.xlabel("Date (UTC)", labelpad=40, fontsize=60)

  
  plt.ylabel("Peak Delivered Luminosity (Hz/$\mathrm{\mu b}$)", labelpad=50, fontsize=60)


  
  plt.legend(bbox_to_anchor=[0.007, 0.85], frameon=False, loc='upper left', fontsize=50)

  plt.gcf().set_size_inches(30, 21.4285714, forward=1)

  plt.gcf().autofmt_xdate()

  plt.autoscale()
  plt.xlim(datetime.date(2010, 3, 30), datetime.date(2010, 10, 31))

  # plt.gca().xaxis.set_minor_locator(MultipleLocator(0.02))

  
  plt.tick_params(which='major', width=5, length=15, labelsize=60)

  ab = AnnotationBbox(OffsetImage(read_png(get_sample_data("/home/aashish/root/macros/MODAnalyzer/mod_logo.png", asfileobj=False)), zoom=0.15, resample=1, dpi_cor=1), (0.205, 0.840), xycoords='figure fraction', frameon=0)
  plt.gca().add_artist(ab)
  preliminary_text = "Prelim. (20\%)"
  plt.gcf().text(0.270, 0.825, preliminary_text, fontsize=60, weight='bold', color='#444444', multialignment='center')


  plt.savefig("plots/Version 5/lumi/inst_lumi_number.pdf")

  plt.clf()




# plot_integrated_recorded_lumi(cumulative=True)
plot_integrated_recorded_lumi(cumulative=False)


# plot_inst_lumi(number=False)
# plot_inst_lumi(number=True)





call(["python", "/home/aashish/root/macros/MODAnalyzer/utilities/sync_plots.py"])