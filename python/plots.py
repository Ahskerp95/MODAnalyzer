# /media/aashish/opendata/eos/opendata/cms/Run2010B/Jet/analyzed.dat
from __future__ import division

from subprocess import call

from matplotlib.ticker import AutoMinorLocator
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import FixedLocator
from matplotlib.ticker import LogLocator

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

from matplotlib.offsetbox import OffsetImage, AnnotationBbox

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




def get_version(input_file):

  f = open(input_file, 'r')
  lines = f.read().split("\n")

  properties = defaultdict(list)

  for line in lines:
    numbers = line.split()
    if numbers[0] == "%":
      return numbers[1] + " " + numbers[2] 


def parse_file(input_file, pT_lower_cut = 0.00, pT_upper_cut = 20000.00, uncorrected_pT_lower_cut = 0.00, softdrop_unc_pT_lower_cut = 0.00, softdrop_cor_pT_lower_cut = 0.00, jet_quality_level=1):
  f = open(input_file, 'r')
  lines = f.read().split("\n")

  # FAILED = 0, LOOSE = 1, MEDIUM = 2, TIGHT = 3
  
  properties = defaultdict(list)

  for line in lines:
    try:
      numbers = line.split()
      
      if not numbers[0] == "#":
        if (float(numbers[6]) > pT_lower_cut) and (float(numbers[6]) < pT_upper_cut) and (float(numbers[5]) > uncorrected_pT_lower_cut) and (float(numbers[36]) > softdrop_unc_pT_lower_cut) and (float(numbers[37]) > softdrop_cor_pT_lower_cut) and (int(numbers[3]) == 1) and (int(numbers[4]) >= jet_quality_level):
          
          properties['event_number'].append( float( numbers[1] ) )
          properties['run_number'].append( float( numbers[2] ) )

          properties['trig_jet_matched'].append( int(numbers[3]) )
          properties['jet_quality'].append( int(numbers[4]) )
          
          properties['uncorrected_hardest_pts'].append( float( numbers[5] ) )
          properties['corrected_hardest_pts'].append( float( numbers[6] ) )
          properties['prescales'].append( int( numbers[7] ) )
          
          properties['trigger_names'].append(  numbers[8] )
          properties['zg_05'].append( float( numbers[9] ) )
          properties['dr_05'].append( float( numbers[10] ) )
          properties['mu_05'].append( float( numbers[11] ) )
          properties['zg_1'].append( float( numbers[12] ) )
          properties['dr_1'].append( float( numbers[13] ) )
          properties['mu_1'].append( float( numbers[14] ) )
          properties['zg_2'].append( float( numbers[15] ) )
          properties['dr_2'].append( float( numbers[16] ) )
          properties['mu_2'].append( float( numbers[17] ) )
          
          properties['zg_05_pt_1'].append( float( numbers[18] ) )
          properties['zg_1_pt_1'].append( float( numbers[19] ) )
          properties['zg_2_pt_1'].append( float( numbers[20] ) )

          properties['zg_05_pt_2'].append( float( numbers[21] ) )
          properties['zg_1_pt_2'].append( float( numbers[22] ) )
          properties['zg_2_pt_2'].append( float( numbers[23] ) )

          properties['zg_05_pt_3'].append( float( numbers[24] ) )
          properties['zg_1_pt_3'].append( float( numbers[25] ) )
          properties['zg_2_pt_3'].append( float( numbers[26] ) )

          properties['zg_05_pt_5'].append( float( numbers[27] ) )
          properties['zg_1_pt_5'].append( float( numbers[28] ) )
          properties['zg_2_pt_5'].append( float( numbers[29] ) )

          properties['zg_05_pt_10'].append( float( numbers[30] ) )
          properties['zg_1_pt_10'].append( float( numbers[31] ) )
          properties['zg_2_pt_10'].append( float( numbers[32] ) )

          properties['zg_charged_05'].append( float( numbers[33] ) )
          properties['zg_charged_1'].append( float( numbers[34] ) )
          properties['zg_charged_2'].append( float( numbers[35] ) )

          properties['pTs_after_SD_unc'].append( float( numbers[36] ) )
          properties['pTs_after_SD_cor'].append( float( numbers[37] ) )

          properties['multiplicity_before_SD'].append( float( numbers[38] ) )
          properties['multiplicity_after_SD'].append( float( numbers[39] ) )
          properties['jet_mass_before_SD'].append( float( numbers[40] ) )
          properties['jet_mass_after_SD'].append( float( numbers[41] ) )

          properties['charged_multiplicity_before_SD'].append( float( numbers[42] ) )
          properties['charged_multiplicity_after_SD'].append( float( numbers[43] ) )
          properties['charged_jet_mass_before_SD'].append( float( numbers[44] ) )
          properties['charged_jet_mass_after_SD'].append( float( numbers[45] ) )

          properties['chrg_dr_05'].append( float( numbers[46] ) )
          properties['chrg_dr_1'].append( float( numbers[47] ) )
          properties['chrg_dr_2'].append( float( numbers[48] ) )

          properties['fractional_energy_loss'].append( float( numbers[49] ) )
          properties['eta'].append( float( numbers[50] ) )
          properties['jet_area'].append( float( numbers[51] ) )
          properties['JEC'].append( float( numbers[52] ) )

          # no_of_const         chrg_multip        neu_had_frac         neu_em_frac       chrg_had_frac        chrg_em_frac

          properties['no_of_const'].append( int( numbers[53] ) )
          properties['chrg_multip'].append( int( numbers[54] ) )
          properties['neu_had_frac'].append( float( numbers[55] ) )
          properties['neu_em_frac'].append( float( numbers[56] ) )
          properties['chrg_had_frac'].append( float( numbers[57] ) )
          properties['chrg_em_frac'].append( float( numbers[58] ) )
          
          properties['m_zg_10'].append( float( numbers[59] ) )
          properties['m_zg_11'].append( float( numbers[60] ) )
          properties['m_zg_12'].append( float( numbers[61] ) )
          properties['m_zg_13'].append( float( numbers[62] ) )
          properties['m_zg_14'].append( float( numbers[63] ) )
          properties['m_zg_15'].append( float( numbers[64] ) )

    except:
      if len(numbers) != 0:
        # print "Some kind of error occured while parsing the given file!"
        # print numbers
        # print
        pass

  return properties



def parse_mc(input_file, pT_lower_cut=150.00, pT_upper_cut = 20000.00, uncorrected_pT_lower_cut = 0.00, softdrop_unc_pT_lower_cut = 0.00, softdrop_cor_pT_lower_cut = 0.00, jet_quality_level=1):
  f = open(input_file, 'r')
  lines = f.read().split("\n")
  
  properties = defaultdict(list)

  for line in lines:
    try:
      numbers = line.split()
      
      if not numbers[0] == "#":

        # print float(numbers[1]) > pT_lower_cut
        if (float(numbers[1]) > pT_lower_cut) and (float(numbers[1]) < pT_upper_cut):
         
          properties['hardest_pts'].append( float( numbers[1] ) )
          properties['zg_05'].append( float( numbers[2] ) )
          properties['dr_05'].append( float( numbers[3] ) )
          properties['mu_05'].append( float( numbers[4] ) )
          properties['zg_1'].append( float( numbers[5] ) )
          properties['dr_1'].append( float( numbers[6] ) )
          properties['mu_1'].append( float( numbers[7] ) )
          properties['zg_2'].append( float( numbers[8] ) )
          properties['dr_2'].append( float( numbers[9] ) )
          properties['mu_2'].append( float( numbers[10] ) )
          
          properties['zg_05_pt_1'].append( float( numbers[11] ) )
          properties['zg_1_pt_1'].append( float( numbers[12] ) )
          properties['zg_2_pt_1'].append( float( numbers[13] ) )

          properties['zg_05_pt_2'].append( float( numbers[14] ) )
          properties['zg_1_pt_2'].append( float( numbers[15] ) )
          properties['zg_2_pt_2'].append( float( numbers[16] ) )

          properties['zg_05_pt_3'].append( float( numbers[17] ) )
          properties['zg_1_pt_3'].append( float( numbers[18] ) )
          properties['zg_2_pt_3'].append( float( numbers[19] ) )

          properties['zg_05_pt_5'].append( float( numbers[20] ) )
          properties['zg_1_pt_5'].append( float( numbers[21] ) )
          properties['zg_2_pt_5'].append( float( numbers[22] ) )

          properties['zg_05_pt_10'].append( float( numbers[23] ) )
          properties['zg_1_pt_10'].append( float( numbers[24] ) )
          properties['zg_2_pt_10'].append( float( numbers[25] ) )

          properties['zg_charged_05'].append( float( numbers[26] ) )
          properties['zg_charged_1'].append( float( numbers[27] ) )
          properties['zg_charged_2'].append( float( numbers[28] ) )

          properties['pTs_after_SD'].append( float( numbers[29] ) )

          properties['multiplicity_before_SD'].append( float( numbers[30] ) )
          properties['multiplicity_after_SD'].append( float( numbers[31] ) )
          properties['jet_mass_before_SD'].append( float( numbers[32] ) )
          properties['jet_mass_after_SD'].append( float( numbers[33] ) )

          properties['charged_multiplicity_before_SD'].append( float( numbers[34] ) )
          properties['charged_multiplicity_after_SD'].append( float( numbers[35] ) )
          properties['charged_jet_mass_before_SD'].append( float( numbers[36] ) )
          properties['charged_jet_mass_after_SD'].append( float( numbers[37] ) )

          properties['chrg_dr_05'].append( float( numbers[38] ) )
          properties['chrg_dr_1'].append( float( numbers[39] ) )
          properties['chrg_dr_2'].append( float( numbers[40] ) )

          properties['fractional_energy_loss'].append( float( numbers[41] ) )
          properties['eta'].append( float( numbers[42] ) )
          # properties['jet_area'].append( float( numbers[43] ) )


          
    except:
      if len(numbers) != 0:
        # print "Some kind of error occured while parsing the given file!"
        # print numbers
        # print
        pass

  f.close()

  return properties


def normalize_hist(hist, variable_bin=False):

  if variable_bin:
    hist.Scale( 1.0 / hist.GetSumOfWeights() )

    for i in range(0, hist.GetSize()):
      bin_width = hist.GetXaxis().GetBinWidth(i)
      old_bin_height =  hist.GetBinContent(i)
      
      new_height = old_bin_height / bin_width
      hist.SetBinContent(i, new_height)

      old_error = hist.GetBinError(i)
      new_error = old_error / bin_width
      hist.SetBinError(i, new_error)
  else:
    bin_width = (hist.upperbound() - hist.lowerbound()) / hist.nbins()
    hist.Scale( 1.0 / ( hist.GetSumOfWeights() * bin_width ) )

  return hist


def log_bins(data, weights, number_of_bins=50):
  
  def drop_zeros(a_list):
    return [i for i in a_list if i > 0]

  min_value = math.log( min( drop_zeros(data) ), 10 )
  max_value = math.log( max(data), 10 )

  return np.histogram(data, weights=weights, bins=np.logspace(min_value, max_value, number_of_bins))


def lin_bins(data, weights, number_of_bins=50):
  
  def drop_zeros(a_list):
    return [i for i in a_list if i > 0]

  min_value = min( drop_zeros(data) )
  max_value = max(data)

  return np.histogram(data, weights=weights, bins=np.linspace(min_value, max_value, number_of_bins))


def parse_file_turn_on(input_file, pT_lower_cut = 0.00, jet_quality_level=1):
  f = open(input_file, 'r')
  lines = f.read().split("\n")

  # FAILED = 0, LOOSE = 1, MEDIUM = 2, TIGHT = 3

  properties = defaultdict(list)

  for line in lines:
    try:
      numbers = line.split()
      
      if not numbers[0] == "#":
        if (float(numbers[1]) > pT_lower_cut) and (int(numbers[3]) == 1) and (int(numbers[4]) >= jet_quality_level):
          properties['event_number'].append( float( numbers[1] ) )
          properties['corrected_hardest_pts'].append( float( numbers[5] ) )
          properties['prescales'].append( int( numbers[6] ) )
          properties['trigger_names'].append(  numbers[7] )

    except:
      if len(numbers) != 0:
        print "Some kind of error occured while parsing the given file!"
        print numbers
        print


  return properties



def parse_mc_pt_file(input_file, pT_lower_cut=100., pT_upper_cut=20000.):
  f = open(input_file, 'r')
  lines = f.read().split("\n")

  pTs = []

  for line in lines:
    try:
      numbers = line.split()
      if (float(numbers[0]) > pT_lower_cut and float(numbers[0]) < pT_upper_cut):
        pTs.append( float( numbers[0] ) )
    except:
      if len(numbers) != 0:
        # print "Some kind of error occured while parsing the given file!"
        # print numbers
        # print
        pass
  
  return pTs

    
def parse_mc_file(input_file, pT_lower_cut = 0.00, pT_upper_cut=20000):
  f = open(input_file, 'r')
  lines = f.read().split("\n")

  properties = defaultdict(list)

  for line in lines:
    try:
      numbers = line.split()
      properties['zg_05'].append( float( numbers[0] ) )
      properties['zg_1'].append( float( numbers[1] ) )
      properties['zg_2'].append( float( numbers[2] ) )
    except:
      if len(numbers) != 0:
        # print "Some kind of error occured while parsing the given file!"
        # print numbers
        # print
        pass
  
  return properties





def plot_charged_pt():
  properties = parse_file(input_analysis_file)
  pdgid_map = { 1: "d", 130: "$K^0_L$ Meson", 11: "$e^-$", -211: "$\pi^-$", 13: "$\mu^-$", 211: "$\pi^+$", -11: "$e^+$", 22: "$\gamma$", 2: "u", -13: "$\mu^+$" }

  pdgids = properties['hardest_pfc_pdgid']
  pTs = properties['hardest_pfc_pt']
  prescales = properties['prescales']

  pdgid_pts = []
  pdgid_prescales = []

  for i in range(0, len(pdgids)):
    if (abs(pdgids[i]) == 211) and (abs(pdgids[i]) == 11) and (abs(pdgids[i]) == 13):
      pdgid_pts.append(pTs[i])
      pdgid_prescales.append(prescales[i])


  pdgid_hist = Hist(25, 0, 800, markersize=1.0, color='blue')
  
  map(pdgid_hist.Fill, pTs, prescales)

  if pdgid_hist.GetSumOfWeights() != 0:
    pdgid_hist.Scale(1.0 / pdgid_hist.GetSumOfWeights())

  rplt.errorbar(pdgid_hist, xerr=False, emptybins=False, markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5)

  plt.yscale('log')

  plt.autoscale(True)

  plt.xlabel('$p_{T}$ GeV')
  plt.suptitle("Hardest Charged pT Distribution")

  fig = plt.gcf()
  fig.set_size_inches(20, 20, forward=1)

  plt.savefig("plots/hardest_charged_pt_distribution.pdf")
  plt.show()


def plot_zg_pfc_pt_cut(pT_lower_cut=150, pT_upper_cut=10000, zg_cut='0.05', zg_filename='zg_05', n_bins=10, y_max_limit=20):

  properties = parse_file(input_analysis_file, pT_lower_cut=pT_lower_cut)

  zgs = properties[zg_filename]
  zg_pfc_cut_2 = properties[zg_filename + '_pt_2']
  zg_pfc_cut_5 = properties[zg_filename + '_pt_5']

  prescales = properties['prescales']

  zg_hist = Hist(6 * n_bins, 0.0, 0.6, title="All PF Candidates", markersize=1.0, color='black')
  zg_pfc_cut_2_hist = Hist(6 * n_bins, 0.0, 0.6, title="PFCs with $p_T >$ 2 GeV", markersize=1.0, color='red')
  zg_pfc_cut_5_hist = Hist(6 * n_bins, 0.0, 0.6, title="PFCs with $p_T >$ 5 GeV", markersize=1.0, color='blue')

  bin_width_zg = (zg_hist.upperbound() - zg_hist.lowerbound()) / zg_hist.nbins()
  bin_width_zg_pfc_cut_2 = (zg_pfc_cut_2_hist.upperbound() - zg_pfc_cut_2_hist.lowerbound()) / zg_pfc_cut_2_hist.nbins()
  bin_width_zg_pfc_cut_5 = (zg_pfc_cut_5_hist.upperbound() - zg_pfc_cut_5_hist.lowerbound()) / zg_pfc_cut_5_hist.nbins()


  map(zg_hist.Fill, zgs, prescales)
  map(zg_pfc_cut_2_hist.Fill, zg_pfc_cut_2, prescales)
  map(zg_pfc_cut_5_hist.Fill, zg_pfc_cut_5, prescales)

  if zg_hist.GetSumOfWeights() != 0:
    zg_hist.Scale(1.0 / (zg_hist.GetSumOfWeights() * bin_width_zg))

  if zg_pfc_cut_2_hist.GetSumOfWeights() != 0:
    zg_pfc_cut_2_hist.Scale(1.0 / (zg_pfc_cut_2_hist.GetSumOfWeights() * bin_width_zg_pfc_cut_2))

  if zg_pfc_cut_5_hist.GetSumOfWeights() != 0:
    zg_pfc_cut_5_hist.Scale(1.0 / (zg_pfc_cut_5_hist.GetSumOfWeights() * bin_width_zg_pfc_cut_5))
  
  rplt.errorbar(zg_hist, emptybins=False, ls='None', marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5)
  rplt.errorbar(zg_pfc_cut_2_hist, emptybins=False, ls='None', marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5)
  rplt.errorbar(zg_pfc_cut_5_hist, emptybins=False, ls='None', marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5)
  
  plt.autoscale(True)
  plt.gca().set_ylim(0, y_max_limit)

  legend = plt.legend(frameon=0, fontsize=60, bbox_to_anchor=[1.0, 0.98])
  plt.gca().add_artist(legend)

  
  extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
  handles = [extra, extra, extra]
  labels = [r"$ \textrm{Anti--}k_{t}\textrm{:}~R = 0.5;\eta<2.4$", r"$p_{T} > " + str(pT_lower_cut) + "~\mathrm{GeV}$", r"$ \textrm{Soft~Drop:}~\boldsymbol{\beta = 0;~z_{\mathrm{cut}} = " + str(zg_cut) + "}$"]
  plt.gca().legend(handles, labels, loc=7, frameon=0, borderpad=0.1, fontsize=60, bbox_to_anchor=[0.97, 0.60])


  plt.xlabel("$z_g$", fontsize=95)
  plt.ylabel("$\displaystyle \\frac{1}{\sigma} \\frac{ \mathrm{d} \sigma}{ \mathrm{d} z_g}$", fontsize=80, rotation=0, labelpad=115, y=0.39)
  

  ab = AnnotationBbox(OffsetImage(read_png(get_sample_data("/home/aashish/root-6.04.06/macros/MODAnalyzer/mod_logo.png", asfileobj=False)), zoom=0.15, resample=1, dpi_cor=1), (0.23, 0.895), xycoords='figure fraction', frameon=0)
  plt.gca().add_artist(ab)
  preliminary_text = "Prelim. (20\%)"
  plt.gcf().text(0.29, 0.885, preliminary_text, fontsize=50, weight='bold', color='#444444', multialignment='center')

  plt.gca().set_ylim(0, y_max_limit)
  plt.gca().set_xlim(0.0, 0.6)

  plt.gcf().set_size_inches(30, 21.4285714, forward=1)
  

  plt.gca().xaxis.set_minor_locator(MultipleLocator(0.02))
  plt.gca().yaxis.set_minor_locator(MultipleLocator(0.5))
  plt.tick_params(which='major', width=5, length=25, labelsize=70)
  plt.tick_params(which='minor', width=3, length=15)


  plt.gca().xaxis.set_tick_params(width=5, length=20, labelsize=70)
  plt.gca().yaxis.set_tick_params(width=5, length=20, labelsize=70)

  plt.tight_layout(pad=1.08, h_pad=1.08, w_pad=1.08)

  print "softcut/" + str(zg_filename) + "_pt_cut_" + str(pT_lower_cut) + ".pdf"

  plt.savefig("plots/" + get_version(input_analysis_file) + "/softcut/" + str(zg_filename) + "_pt_cut_" + str(pT_lower_cut) + ".pdf")
  # plt.show()
  plt.clf()



def plot_turn_on_curves():
  # properties = parse_file_turn_on(input_analysis_file)
  
  properties = parse_file_turn_on('/home/aashish/turn_on.dat')

  pTs = properties['corrected_hardest_pts']
  trigger_names = properties['trigger_names']
  prescales = properties['prescales']

  expected_trigger_names = ["HLT\_Jet140U", "HLT\_Jet100U", "HLT\_Jet70U", "HLT\_Jet50U", "HLT\_Jet30U", "HLT\_Jet15U\_HcalNoiseFiltered" ]
  labels = ["Jet140U", "Jet100U", "Jet70U", "Jet50U", "Jet30U", "Jet15U-HNF" ]

  colors = ['orange', 'red', 'green', 'blue', 'magenta', 'black']
  colors = colors[::-1]

  pt_hists = []
  for i in range(0, len(expected_trigger_names)):
    pt_hists.append(Hist(60, 0, 300, title=labels[i], markersize=1.0, color=colors[i], linewidth=5))

  for i in range(0, len(pTs)):
    for j in range(0, len(expected_trigger_names)):
      if expected_trigger_names[j].replace("\\", "") in trigger_names[i]:
        pt_hists[j].Fill(pTs[i], prescales[i])

  for k in range(len(pt_hists) - 1, -1, -1):
    rplt.errorbar(pt_hists[k], emptybins=False, ls='None', marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5)

  plt.autoscale(True)
  plt.yscale('log')

  plt.gca().set_ylim(1, 10e10)

  
  # Legend.
  handles, labels = plt.gca().get_legend_handles_labels()
  first_legend = plt.gca().legend(handles, labels, fontsize=60,  frameon=0, borderpad=0.1, bbox_to_anchor=[0.97, 0.98])
  ax = plt.gca().add_artist(first_legend)

  # Info about R, pT_cut, etc.
  extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
  handles = [extra]
  labels = [r"$ \textrm{Anti--}k_{t}\textrm{:}~\boldsymbol{R = 0.5} $"]
  plt.gca().legend(handles, labels, loc=7, frameon=0, borderpad=0.1, fontsize=60, bbox_to_anchor=[0.935, 0.65])


  plt.xlabel('$p_T~\mathrm{(GeV)}$', fontsize=95)
  plt.ylabel('$\mathrm{A.U.}$', fontsize=75, rotation=0, labelpad=75.)

  fn = get_sample_data("/home/aashish/root-6.04.06/macros/MODAnalyzer/mod_logo.png", asfileobj=False)

  ab = AnnotationBbox(OffsetImage(read_png(get_sample_data("/home/aashish/root-6.04.06/macros/MODAnalyzer/mod_logo.png", asfileobj=False)), zoom=0.15, resample=1, dpi_cor=1), (0.23, 0.9249985), xycoords='figure fraction', frameon=0)
  plt.gca().add_artist(ab)
  preliminary_text = "Prelim. (20\%)"
  plt.gcf().text(0.29, 0.9178555, preliminary_text, fontsize=50, weight='bold', color='#444444', multialignment='center')

  plt.gcf().set_size_inches(30, 30, forward=1)

  plt.gca().xaxis.set_tick_params(width=5, length=20, labelsize=70)
  plt.gca().yaxis.set_tick_params(width=5, length=20, labelsize=70)

  plt.tight_layout(pad=1.08, h_pad=1.08, w_pad=1.08)


  plt.savefig("plots/" + get_version(input_analysis_file) + "/turn_on_curves.pdf")
  # plt.show()
  plt.clf()


def plot_hardest_pt_corresponding_triggers():
  properties = parse_file(input_analysis_file)

  pTs = properties['corrected_hardest_pts']
  trigger_names = properties['trigger_names']
  prescales = properties['prescales']

  expected_trigger_names = ["HLT_Jet100U", "HLT_Jet70U", "HLT_Jet50U", "HLT_Jet30U", "HLT_Jet15U"]
  labels = ["Jet100U", "Jet70U", "Jet50U", "Jet30U", "Jet15U"]

  colors = ['brown', 'red', 'blue', 'magenta', 'green']

  pt_hists = []
  for i in range(0, len(expected_trigger_names)):
    pt_hists.append(Hist(50, 0, 1000, title=labels[i], markersize=1.0, color=colors[i], linewidth=5))

  for i in range(0, len(pTs)):
    for j in range(0, len(expected_trigger_names)):
      if expected_trigger_names[j] in trigger_names[i]:
        pt_hists[j].Fill(pTs[i], prescales[i])

  for k in range(0, len(pt_hists)):
    rplt.errorbar(pt_hists[k], marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5)

  plt.yscale('log')
  plt.autoscale(True)

  plt.gca().set_ylim(1, 10e8)

  plt.legend(loc=0, frameon=0)

  plt.xlabel('$p_T \mathrm{(GeV)}$')

  fn = get_sample_data("/home/aashish/root-6.04.06/macros/MODAnalyzer/mod_logo.png", asfileobj=False)
  ab = AnnotationBbox(OffsetImage(read_png(fn), zoom=0.15, resample=1, dpi_cor=1), (125, 30e7), frameon=0)
  plt.gca().add_artist(ab)

  preliminary_text = "Prelim. \n(20\%)"
  plt.gcf().text(0.31, 0.83, preliminary_text, fontsize=40, weight='bold', color='#444444', multialignment='center')

  plt.gcf().set_size_inches(30, 21.4285714, forward=1)

  plt.savefig("plots/" + get_version(input_analysis_file) + "/hardest_pt_corresponding_triggers.pdf")
  # plt.show()
  plt.clf()



def plot_2d_hist():

  pT_lower_cut = 150
  properties = parse_file(input_analysis_file, pT_lower_cut)
  zgs = [properties['zg_05'], properties['zg_1'], properties['zg_2']]
  charged_zgs = [properties['zg_charged_05'], properties['zg_charged_1'], properties['zg_charged_2']]
  prescales = properties['prescales']

  
  H, xedges, yedges = np.histogram2d(charged_zgs[0], zgs[0], normed=1, range=[[0, 0.5], [0, 0.5]], weights=prescales, bins=25)
  Hmasked = np.ma.masked_where(H==0,H) # Mask pixels with a value of zero
  plt.pcolormesh(xedges,yedges,Hmasked)
  plt.xlabel('Charged zg\_05')
  plt.ylabel('zg\_05')
  cbar = plt.colorbar()
  cbar.ax.set_ylabel('Counts')  
  plt.gcf().set_size_inches(30, 30, forward=1)
  plt.tight_layout(pad=1.08, h_pad=1.08, w_pad=1.08)
  plt.savefig("plots/zg_05_vs_charged_zg_05.pdf")
  plt.clf()


  H, xedges, yedges = np.histogram2d(charged_zgs[1], zgs[1], normed=1, range=[[0, 0.5], [0, 0.5]], weights=prescales, bins=25)
  Hmasked = np.ma.masked_where(H==0,H) # Mask pixels with a value of zero
  plt.pcolormesh(xedges,yedges,Hmasked)
  plt.xlabel('Charged zg\_1')
  plt.ylabel('zg\_1')
  cbar = plt.colorbar()
  cbar.ax.set_ylabel('Counts')
  plt.gcf().set_size_inches(30, 30, forward=1)
  plt.tight_layout(pad=1.08, h_pad=1.08, w_pad=1.08)
  plt.savefig("plots/zg_1_vs_charged_zg_1.pdf")
  plt.clf()


  H, xedges, yedges = np.histogram2d(charged_zgs[2], zgs[2], normed=1, range=[[0, 0.5], [0, 0.5]], weights=prescales, bins=25)
  Hmasked = np.ma.masked_where(H==0,H) # Mask pixels with a value of zero
  plt.pcolormesh(xedges,yedges,Hmasked)
  plt.xlabel('Charged zg\_2')
  plt.ylabel('zg\_2')
  cbar = plt.colorbar()
  cbar.ax.set_ylabel('Counts')
  fig = plt.gcf()
  fig.set_size_inches(20, 20, forward=1)
  plt.savefig("plots/zg_2_vs_charged_zg_2.pdf")
  plt.clf()

 





def plot_zg_th_mc_data(pT_lower_cut=150, pT_upper_cut=10000, zg_cut='0.05', zg_filename='zg_05', ratio_denominator="theory", data=True, mc=True, theory=True, n_bins=10, y_max_limit=20, y_limit_ratio_plot=0.5):

  zg_cut = float(zg_cut)

  properties = parse_file(input_analysis_file, pT_lower_cut=pT_lower_cut)
  # properties_pythia = parse_mc_file("/home/aashish/Dropbox (MIT)/Research/CMSOpenData/Andrew/fastjet_sudakov_safe_pythia_pp2jj_" + str(pT_lower_cut) + "pTcut_7TeV.dat", pT_lower_cut=pT_lower_cut, pT_upper_cut=pT_upper_cut)
  # properties_herwig = parse_mc_file("/home/aashish/Dropbox (MIT)/Research/CMSOpenData/Andrew/fastjet_sudakov_safe_herwig_pp2jj_" + str(pT_lower_cut) + "pTcut_7TeV.dat", pT_lower_cut=pT_lower_cut, pT_upper_cut=pT_upper_cut)

  properties_pythia = parse_mc("/home/aashish/pythia_reco.dat", pT_lower_cut=pT_lower_cut)
  properties_herwig = parse_mc("/home/aashish/herwig_reco.dat", pT_lower_cut=pT_lower_cut)
  properties_sherpa = parse_mc("/home/aashish/sherpa_reco.dat", pT_lower_cut=pT_lower_cut)


  zg_data = properties[zg_filename]
  
  zg_pythias = properties_pythia[zg_filename]
  zg_herwigs = properties_herwig[zg_filename]
  zg_sherpas = properties_sherpa[zg_filename]

  prescales = properties['prescales']

  data_label = "CMS 2010 Open Data"
  pythia_label = "Pythia 8.212" if mc else ""
  herwig_label = "Herwig++ 2.7.1" if mc else ""
  sherpa_label = "Sherpa 2.2.0" if mc else ""
  theory_label = "Theory (MLL)" if theory else ""

  
  gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1]) 

 
  ax0 = plt.subplot(gs[0])
  ax1 = plt.subplot(gs[1])


  # Theory Plots Begin.
  
  points_th_gluon = parse_theory_file("/home/aashish/Dropbox (MIT)/Research/CMSOpenData/Simone/results_7_24_15/band_gluon_pt" + str(pT_lower_cut) + "_zc" + str(zg_cut).replace(".", "") + ".dat")
  points_th_quark = parse_theory_file("/home/aashish/Dropbox (MIT)/Research/CMSOpenData/Simone/results_7_24_15/band_quark_pt" + str(pT_lower_cut) + "_zc" + str(zg_cut).replace(".", "") + ".dat")

  points = defaultdict(list)

  for x in points_th_gluon:
    points[x] = [ points_th_gluon[x][0], points_th_gluon[x][1], points_th_gluon[x][2], points_th_gluon[x][3], points_th_gluon[x][4], points_th_gluon[x][5] ]
    points[x].extend([ points_th_quark[x][0], points_th_quark[x][1], points_th_quark[x][2], points_th_quark[x][3], points_th_quark[x][4], points_th_quark[x][5] ])

  keys = points.keys()
  keys.sort()

  theory_x = keys

  y = []
  for j in range(0, 6):
    y.append([points[i][j] for i in keys])

  # For each x, record three y's viz. max_y, min_y, line_y (i.e. e11 xmu=1).

  theory_y_max = []
  theory_y_min = []
  theory_y_line = []
  for i in range(0, len(theory_x)):
    y_for_current_x = []
    for j in range(0, 6):
      y_for_current_x.append(y[j][i])

    theory_y_min.append(min(y_for_current_x))
    theory_y_line.append(y_for_current_x[1])
    theory_y_max.append(max(y_for_current_x))
    
    
  if theory:
    area_theory_y_max = simps(theory_y_max, theory_x)
    # weighted_theory_y_max = map(lambda x: x / area_theory_y_max, theory_y_max)
    weighted_theory_y_max = theory_y_max
    ax0.plot(theory_x, weighted_theory_y_max, alpha=0.0, color='red')
    
    area_theory_y_line = simps(theory_y_line, theory_x)
    # weighted_theory_y_line = map(lambda x: x / area_theory_y_line, theory_y_line)
    weighted_theory_y_line = theory_y_line
    ax0.plot(theory_x, weighted_theory_y_line, label=theory_label, alpha=1.0, color='red', linewidth=5)

    area_theory_y_min = simps(theory_y_min, theory_x)
    # weighted_theory_y_min = map(lambda x: x / area_theory_y_min, theory_y_min)
    weighted_theory_y_min = theory_y_min
    ax0.plot(theory_x, weighted_theory_y_min, alpha=0.0, color='red')


    ax0.fill_between(theory_x, theory_y_max, theory_y_min, norm=1, where=np.less_equal(theory_y_min, theory_y_max), facecolor='red', interpolate=True, alpha=0.3, linewidth=0.0)


  # Theory Plot Ends.

  def convert_hist_to_line_plot(hist, n_bins):
    a = []
    b = {}
    bin_width = 0.6 / (6 * n_bins)
    for i in range(0, len(list(hist.x()))):
      a.append(round(list(hist.x())[i] - bin_width / 2., 4))
      a.append(round(list(hist.x())[i], 4))
      a.append(round(list(hist.x())[i] + bin_width / 2., 4))

      if round(list(hist.x())[i] - bin_width / 2., 4) not in b.keys():
        b[round(list(hist.x())[i] - bin_width / 2., 4)] = [ list(hist.y())[i] ]
      else:
        b[round(list(hist.x())[i] - bin_width / 2., 4)].append( list(hist.y())[i] )
      
      if round(list(hist.x())[i], 4) not in b.keys():
        b[round(list(hist.x())[i], 4)] = [ list(hist.y())[i] ]
      else:
        b[round(list(hist.x())[i], 4)].append( list(hist.y())[i] )

      if round(list(hist.x())[i] + bin_width / 2., 4) not in b.keys():
        b[round(list(hist.x())[i] + bin_width / 2., 4)] = [ list(hist.y())[i] ]
      else:
        b[round(list(hist.x())[i] + bin_width / 2., 4)].append( list(hist.y())[i] )

    x = sorted(list(Set(a)))
    a.sort()
    
    c = [b[x[i]] for i in range(0, len(x))]

    y = [item for sublist in c for item in sublist]
    
    a_zero_removed = []
    y_zero_removed = []
    for i in range(0, len(a)):
      if a[i] >= zg_cut and a[i] <= 0.5 and y[i] != 0.0:
        a_zero_removed.append(a[i])
        y_zero_removed.append(y[i])

    return a_zero_removed, y_zero_removed

  
  
  # Data Plot Begins.
  
  zg_data_hist = Hist(6 * n_bins, 0.0, 0.6, title=data_label, markersize=2.5, color='black')
  bin_width_data = (zg_data_hist.upperbound() - zg_data_hist.lowerbound()) / zg_data_hist.nbins()

  map(zg_data_hist.Fill, zg_data, prescales)
  
  zg_data_hist.Scale(1.0 / ( zg_data_hist.GetSumOfWeights() * bin_width_data ))
  
  if data:
    # data_plot, caplines, barlinecols
    data_plot = rplt.errorbar(zg_data_hist, xerr=1, yerr=1, emptybins=False, axes=ax0, ls='None', marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5, alpha=1.0)
  else:
    data_plot = rplt.errorbar(zg_data_hist, xerr=1, yerr=1, emptybins=False, axes=ax0, ls='None', marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5, alpha=0.0)


  data_x_errors, data_y_errors = [], []
  for x_segment in data_plot[2][0].get_segments():
    data_x_errors.append((x_segment[1][0] - x_segment[0][0]) / 2.)
  for y_segment in data_plot[2][1].get_segments():
    data_y_errors.append((y_segment[1][1] - y_segment[0][1]) / 2.)

  data_points_x = data_plot[0].get_xdata()
  data_points_y = data_plot[0].get_ydata()

  # print sorted(data_points_x)



  # Data Plots Ends.

  
  # Simulation Plots Begin. 
  
  # Pythia.
  
  zg_pythia_hist = Hist(6 * n_bins, 0, 0.6, title=pythia_label, markersize=5.0, color='blue', linewidth=5)
  bin_width_pythia = (zg_pythia_hist.upperbound() - zg_pythia_hist.lowerbound()) / zg_pythia_hist.nbins()

  map(zg_pythia_hist.Fill, zg_pythias)

  zg_pythia_hist.Scale(1.0 / ( zg_pythia_hist.GetSumOfWeights() * bin_width_pythia ))

  if mc:
    # pythia_plot = rplt.hist(zg_pythia_hist, axes=ax0)
    pythia_plot = ax0.hist(zg_pythias, label=pythia_label, bins=5 * n_bins, normed=1, histtype='step', color='blue', linewidth=5)
  else:
    pythia_plot = ax0.hist(zg_pythias, bins=5 * n_bins, normed=1, histtype='step', color='blue', linewidth=0)

  
  # Pythia Ends.
  
  # Herwig. 
  
  zg_herwig_hist = Hist(6 * n_bins, 0, 0.6, title=herwig_label, markersize=5.0, color='green', linewidth=5)
  bin_width_herwig = (zg_herwig_hist.upperbound() - zg_herwig_hist.lowerbound()) / zg_herwig_hist.nbins()

  map(zg_herwig_hist.Fill, zg_herwigs)

  zg_herwig_hist.Scale(1.0 / ( zg_herwig_hist.GetSumOfWeights() * bin_width_herwig ))

  if mc:
    # herwig_plot = rplt.hist(zg_herwig_hist, axes=ax0)
    herwig_plot = ax0.hist(zg_herwigs, label=herwig_label, bins=5 * n_bins, normed=1, histtype='step', color='green', linewidth=5)
  else:
    herwig_plot = ax0.hist(zg_herwigs, bins=5 * n_bins, normed=1, histtype='step', color='green', linewidth=0)
  
  # Herwig Ends.

  # Sherpa.

  zg_sherpa_hist = Hist(6 * n_bins, 0, 0.6, title=sherpa_label, markersize=5.0, color='orange', linewidth=5)
  bin_width_sherpa = (zg_sherpa_hist.upperbound() - zg_sherpa_hist.lowerbound()) / zg_sherpa_hist.nbins()

  map(zg_sherpa_hist.Fill, zg_sherpas)

  zg_sherpa_hist.Scale(1.0 / ( zg_sherpa_hist.GetSumOfWeights() * bin_width_sherpa ))

  if mc:
    # sherpa_plot = rplt.hist(zg_sherpa_hist, axes=ax0)
    sherpa_plot = ax0.hist(zg_sherpas, label=sherpa_label, bins=5 * n_bins, normed=1, histtype='step', color='orange', linewidth=5)
  else:
    sherpa_plot = ax0.hist(zg_sherpas, bins=5 * n_bins, normed=1, histtype='step', color='orange', linewidth=0)

  # Sherpa Ends.

  # Simulation Plots End.

  
  # Ratio-Over Plot Begins.


  # Theory-Over-Data Plot.
  
  data_plot_points_x = []
  data_plot_points_y = []

  for i in range(0, len(data_points_x)):
    if float(data_points_x[i]) >= float(zg_cut):
      data_plot_points_x.append(data_points_x[i])
      data_plot_points_y.append(data_points_y[i])


  theory_min_interpolate_function = extrap1d(interpolate.interp1d(theory_x, theory_y_min))
  theory_line_interpolate_function = extrap1d(interpolate.interp1d(theory_x, theory_y_line))
  theory_max_interpolate_function = extrap1d(interpolate.interp1d(theory_x, theory_y_max))

  theory_extrapolated_min = theory_min_interpolate_function(data_plot_points_x)
  theory_extrapolated_line = theory_line_interpolate_function(data_plot_points_x)
  theory_extrapolated_max = theory_max_interpolate_function(data_plot_points_x)

  if ratio_denominator == "data":

    if mc:
      zg_herwig_hist.Divide(zg_data_hist)
      zg_herwig_line_plot = convert_hist_to_line_plot(zg_herwig_hist, n_bins)
      plt.plot(zg_herwig_line_plot[0], zg_herwig_line_plot[1], linewidth=5, color='green')

      zg_pythia_hist.Divide(zg_data_hist)
      zg_pythia_line_plot = convert_hist_to_line_plot(zg_pythia_hist, n_bins)
      plt.plot(zg_pythia_line_plot[0], zg_pythia_line_plot[1], linewidth=5, color='blue')

      zg_sherpa_hist.Divide(zg_data_hist)
      zg_sherpa_line_plot = convert_hist_to_line_plot(zg_sherpa_hist, n_bins)
      plt.plot(zg_sherpa_line_plot[0], zg_sherpa_line_plot[1], linewidth=5, color='orange')

    if data:
      ratio_data_to_data = [None if n == 0 else m / n for m, n in zip(data_plot_points_y, data_plot_points_y)]
      data_to_data_y_err = [(b / m) for b, m in zip(data_y_errors, data_plot_points_y)]
      data_to_data_x_err = [(b / m) for b, m in zip(data_x_errors, [1] * len(data_plot_points_y))]
      
      plt.errorbar(data_plot_points_x, ratio_data_to_data, xerr=data_to_data_x_err, yerr=data_to_data_y_err, ls='None', marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5, color='black')

    if theory:
      ratio_theory_line_to_data = [m / n for m, n in zip(theory_extrapolated_line, data_plot_points_y)]
      ratio_theory_min_to_data = [m / n for m, n in zip(theory_extrapolated_min, data_plot_points_y)]
      ratio_theory_max_to_data = [m / n for m, n in zip(theory_extrapolated_max, data_plot_points_y)]

      zg_theory_line_to_data_hist = Hist(6 * n_bins, 0.0, 0.6)
      map(zg_theory_line_to_data_hist.Fill, data_plot_points_x, ratio_theory_line_to_data)
      zg_theory_line_to_data_plot = convert_hist_to_line_plot(zg_theory_line_to_data_hist, n_bins)
      plt.plot(zg_theory_line_to_data_plot[0], zg_theory_line_to_data_plot[1], linewidth=5, color='red')

      zg_theory_min_to_data_hist = Hist(6 * n_bins, 0.0, 0.6)
      map(zg_theory_min_to_data_hist.Fill, data_plot_points_x, ratio_theory_min_to_data)
      zg_theory_min_to_data_plot = convert_hist_to_line_plot(zg_theory_min_to_data_hist, n_bins)

      zg_theory_max_to_data_hist = Hist(6 * n_bins, 0.0, 0.6)
      map(zg_theory_max_to_data_hist.Fill, data_plot_points_x, ratio_theory_max_to_data)
      zg_theory_max_to_data_plot = convert_hist_to_line_plot(zg_theory_max_to_data_hist, n_bins)

      ax1.fill_between(zg_theory_max_to_data_plot[0], zg_theory_max_to_data_plot[1], zg_theory_min_to_data_plot[1], norm=1, where=np.less_equal(zg_theory_min_to_data_plot[1], zg_theory_max_to_data_plot[1]), facecolor='red', interpolate=True, alpha=0.3, linewidth=0.0)
      
  elif ratio_denominator == "theory":

    zg_theory_line_hist = Hist(6 * n_bins, 0.0, 0.6, color='red')
    map(zg_theory_line_hist.Fill, data_plot_points_x, theory_extrapolated_line)

    zg_theory_min_hist = Hist(6 * n_bins, 0.0, 0.6, color='pink')
    map(zg_theory_min_hist.Fill, data_plot_points_x, theory_extrapolated_min)

    zg_theory_max_hist = Hist(6 * n_bins, 0.0, 0.6, color='red')
    map(zg_theory_max_hist.Fill, data_plot_points_x, theory_extrapolated_max)


    if mc:
      zg_herwig_hist.Divide(zg_theory_line_hist)
      zg_herwig_line_plot = convert_hist_to_line_plot(zg_herwig_hist, n_bins)
      plt.plot(zg_herwig_line_plot[0], zg_herwig_line_plot[1], linewidth=5, color='green')

      zg_pythia_hist.Divide(zg_theory_line_hist)
      zg_pythia_line_plot = convert_hist_to_line_plot(zg_pythia_hist, n_bins)
      plt.plot(zg_pythia_line_plot[0], zg_pythia_line_plot[1], linewidth=5, color='blue')

      zg_sherpa_hist.Divide(zg_theory_line_hist)
      zg_sherpa_line_plot = convert_hist_to_line_plot(zg_sherpa_hist, n_bins)
      plt.plot(zg_sherpa_line_plot[0], zg_sherpa_line_plot[1], linewidth=5, color='orange')

    if data:
      zg_data_to_th_y = [b / m for b, m in zip(data_plot_points_y, theory_extrapolated_line)]
      zg_data_to_th_y_err = [b / m for b, m in zip(data_y_errors, theory_extrapolated_line)]
      data_to_th_x_err = [(b / m) for b, m in zip(data_x_errors, [1] * len(zg_data_to_th_y_err))]

      plt.errorbar(data_plot_points_x, zg_data_to_th_y, xerr=data_to_th_x_err, yerr=zg_data_to_th_y_err, ls='None', marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5, color='black')
   
    if theory:
      
      zg_theory_min_hist.Divide(zg_theory_line_hist)
      zg_theory_max_hist.Divide(zg_theory_line_hist)

      zg_theory_min_plot = convert_hist_to_line_plot(zg_theory_min_hist, n_bins)
      zg_theory_max_plot = convert_hist_to_line_plot(zg_theory_max_hist, n_bins)

      zg_theory_min_line, = plt.plot(zg_theory_min_plot[0], zg_theory_min_plot[1], linewidth=0)
      zg_theory_max_line, = plt.plot(zg_theory_max_plot[0], zg_theory_max_plot[1], linewidth=0)
      
      x_min, y_min = zg_theory_min_line.get_xdata(), zg_theory_min_line.get_ydata()
      x_max, y_max = zg_theory_max_line.get_xdata(), zg_theory_max_line.get_ydata()

      ax1.fill_between(x_max, y_max, y_min, norm=1, where=np.less_equal(y_min, y_max), facecolor='red', interpolate=True, alpha=0.3, linewidth=0.0)

      zg_theory_line_hist.Divide(zg_theory_line_hist)
      zg_theory_line_plot = convert_hist_to_line_plot(zg_theory_line_hist, n_bins)
      plt.plot(zg_theory_line_plot[0], zg_theory_line_plot[1], linewidth=5, color='red')

  else:
    raise ValueError("Only 'theory' or 'data' are valid options for calculating ratios!")


  # Normalized-Over-Data Plot Ends.

  ax0.set_xlabel("$z_g$", fontsize=95)
  ax0.set_ylabel("$\displaystyle \\frac{1}{\sigma} \\frac{ \mathrm{d} \sigma}{ \mathrm{d} z_g}$", fontsize=80, rotation=0, labelpad=115, y=0.39)
  
  ax1.set_xlabel("$z_g$", fontsize=95)
  
  if ratio_denominator == "data":
    label_pad = 135
  else:
    label_pad = 115

  # ax1.set_ylabel("Ratio           \nto           \n" + ratio_denominator.capitalize() + "           ", fontsize=55, rotation=0, labelpad=250, y=0.31)
  plt.ylabel("Ratio           \nto           \n" + ratio_denominator.capitalize() + "           ", fontsize=55, rotation=0, labelpad=label_pad, y=0.31, axes=ax1)


  # Legend.

  th_line, = ax0.plot(range(1), linewidth=5, color='red')
  th_patch = mpatches.Patch(facecolor='red', alpha=0.3, linewidth=5, edgecolor='red')

  if mc:
    pythia_line, = ax0.plot(range(1), linewidth=5, color=zg_pythia_hist.GetLineColor())
    herwig_line, = ax0.plot(range(1), linewidth=5, color=zg_herwig_hist.GetLineColor())
    sherpa_line, = ax0.plot(range(1), linewidth=5, color=zg_sherpa_hist.GetLineColor())
  else:
    pythia_line, = ax0.plot(range(1), linewidth=5, color=zg_pythia_hist.GetLineColor(), alpha=0)
    herwig_line, = ax0.plot(range(1), linewidth=5, color=zg_herwig_hist.GetLineColor(), alpha=0)
    sherpa_line, = ax0.plot(range(1), linewidth=5, color=zg_sherpa_hist.GetLineColor(), alpha=0)

  handles = [data_plot, (th_patch, th_line), pythia_line, herwig_line, sherpa_line]
  labels = [data_label, theory_label, pythia_label, herwig_label, sherpa_label]

  first_legend = ax0.legend(handles, labels, fontsize=60, handler_map = {th_line : HandlerLine2D(marker_pad = 0), pythia_line : HandlerLine2D(marker_pad = 0), herwig_line : HandlerLine2D(marker_pad = 0), sherpa_line : HandlerLine2D(marker_pad = 0)}, frameon=0, borderpad=0.1, bbox_to_anchor=[0.97, 0.98])
  ax = ax0.add_artist(first_legend)

  for txt in first_legend.get_texts():
    if ( not data) and txt.get_text() == data_label:
      txt.set_color("white") 

  # Info about R, pT_cut, etc.
  extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
  
  if pT_upper_cut != 10000:
    labels = ["$ \\textrm{Anti--}k_{t}\\textrm{:}~R = 0.5;\eta<2.4$", "$p_{T} \in [" + str(pT_lower_cut) + ", " + str(pT_upper_cut) + "]~\mathrm{GeV}$", "$ \\textrm{Soft~Drop:}~\\boldsymbol{\\beta = 0;~z_{\mathrm{cut}} = " + str(zg_cut) + "}$"]
  else:
    labels = ["$ \\textrm{Anti--}k_{t}\\textrm{:}~R = 0.5;\eta<2.4$", "$p_{T} > " + str(pT_lower_cut) + "~\mathrm{GeV}$", "$ \\textrm{Soft~Drop:}~\\boldsymbol{\\beta = 0;~z_{\mathrm{cut}} = " + str(zg_cut) + "}$"]

  # labels = [r"$ \textrm{Anti--}k_{t}\textrm{:}~\boldsymbol{R = 0.5;~p_{T} > " + str(pT_lower_cut) + "~\mathrm{GeV}}$", r"$ \textrm{Soft~Drop:}~\boldsymbol{\beta = 0;~z_{\mathrm{cut}} = " + str(zg_cut) + "}$"]
  
  ax0.legend([extra, extra, extra], labels, loc=7, frameon=0, borderpad=0.1, fontsize=60, bbox_to_anchor=[0.97, 0.52])


  # Legend Ends.

  ax0.autoscale(True)
  ax1.autoscale(True)
  
  ax0.set_ylim(0, y_max_limit)
  ax1.set_ylim(1.0 - y_limit_ratio_plot, 1.0 + y_limit_ratio_plot)

  ax0.set_xlim(0.0, 0.6)
  ax1.set_xlim(0.0, 0.6)
  

  fig = plt.gcf()

  # 1 - ((1 - 0.895) * 21.429)/30
  if data:
    ab = AnnotationBbox(OffsetImage(read_png(get_sample_data("/home/aashish/root-6.04.06/macros/MODAnalyzer/mod_logo.png", asfileobj=False)), zoom=0.15, resample=1, dpi_cor=1), (0.23, 0.9249985), xycoords='figure fraction', frameon=0)
    plt.gca().add_artist(ab)
    preliminary_text = "Prelim. (20\%)"
    plt.gcf().text(0.29, 0.9178555, preliminary_text, fontsize=50, weight='bold', color='#444444', multialignment='center')
  else:
    preliminary_text = ""
    plt.gcf().text(0.29, 0.9178555, preliminary_text, fontsize=50, weight='bold', color='#444444', multialignment='center')



  fig = plt.gcf()
  fig.set_size_inches(30, 30, forward=1)

  plt.sca(ax0)
  plt.gca().xaxis.set_minor_locator(MultipleLocator(0.02))
  plt.gca().yaxis.set_minor_locator(MultipleLocator(0.5))
  plt.tick_params(which='major', width=5, length=25, labelsize=70)
  plt.tick_params(which='minor', width=3, length=15)

  plt.sca(ax1)
  plt.gca().xaxis.set_minor_locator(MultipleLocator(0.02))
  plt.tick_params(which='major', width=5, length=25, labelsize=70)
  plt.tick_params(which='minor', width=3, length=15)


  fig.set_snap(True)
  plt.tight_layout(pad=1.08, h_pad=1.08, w_pad=1.08)

  print "Writing out zg_cut_" + str(zg_filename) + "_pT_lower_" + str(pT_lower_cut) + "_pT_upper_" + str(pT_upper_cut) + "_ratio_over_" + ratio_denominator + "_th_" + str(theory) + "_mc_" + str(mc) + "_data_" + str(data) + ".pdf"
  filename = "plots/" + get_version(input_analysis_file) + "/zg/zg_cut_" + str(zg_filename) + "_pT_lower_" + str(pT_lower_cut) + "_pT_upper_" + str(pT_upper_cut) + "_ratio_over_" + ratio_denominator + "_th_" + str(theory) + "_mc_" + str(mc) + "_data_" + str(data) + ".pdf"
  
  plt.savefig(filename)
  # plt.show()
  plt.clf()




def parse_theory_file(input_file):
  f = open(input_file, 'r')
  lines = f.read().split("\n")

  properties = defaultdict(list)

  points = defaultdict(list)
  for line in lines:
    try:
      numbers = line.split()
      try:
        for i in range(1, len(numbers)):
          points[float(numbers[0])].append(float(numbers[i]))
      except ValueError:
        pass
    except:
      pass

  return points



# 5 GeV bins.

def plot_trigger_efficiency_curves(trigger_1, trigger_2, pT_upper_limit=800):
  
  properties = parse_file_turn_on('/home/aashish/turn_on.dat')
  # properties = parse_file_turn_on('./trigger_proper_turn_on.dat')

  event_numbers = properties['event_number']

  pTs = properties['corrected_hardest_pts']
  trigger_names = properties['trigger_names']
  prescales = properties['prescales']

  colors = ['magenta', 'blue', 'orange', 'green', 'black', 'red']
  expected_trigger_names = ["HLT\_Jet180U", "HLT\_Jet140U", "HLT\_Jet100U", "HLT\_Jet70U", "HLT\_Jet50U", "HLT\_Jet30U" ]

  color = colors[expected_trigger_names.index(trigger_1.replace("_", "\_"))]

  pt_hist_trigger_1 = Hist(500, 0, pT_upper_limit, title=trigger_1[4:], color=color, markersize=1.0, linewidth=5)
  pt_hist_trigger_2 = Hist(500, 0, pT_upper_limit, title=trigger_2[4:], color=color, markersize=1.0, linewidth=5)



  # trigger_names_proper = defaultdict(list)
  # pTs_proper = defaultdict(list)
  # prescales_proper = defaultdict(list)

  # for i in range(0, len(trigger_names)):
  #   trigger_names_proper[event_numbers[i]].append(trigger_names[i])
  #   pTs_proper[event_numbers[i]].append(pTs[i])
  #   prescales_proper[event_numbers[i]].append(prescales[i])

  # for event_number in trigger_names_proper:
  #   if trigger_1 in trigger_names_proper[event_number] and trigger_2 in trigger_names_proper[event_number]:
      
  #     for i in range(0, len(trigger_names_proper[event_number])):
  #       if trigger_1 in trigger_names_proper[event_number][i]:
  #         trigger_1_index = i

  #     for i in range(0, len(trigger_names_proper[event_number])):
  #       if trigger_2 in trigger_names_proper[event_number][i]:
  #         trigger_2_index = i

  #     print pTs[trigger_1_index]

  #     pt_hist_trigger_1.Fill(pTs[trigger_1_index], prescales[trigger_1_index])
  #     pt_hist_trigger_2.Fill(pTs[trigger_2_index], prescales[trigger_2_index])



  for i in range(0, len(pTs)):
    if trigger_1 in trigger_names[i]:
      pt_hist_trigger_1.Fill(pTs[i], prescales[i])

    # The len thingy is to make sure trigger names like HLT_Jet15U_HcalNoiseFiltered_v3 are excluded.
    # if trigger_2 in trigger_names[i] and len(trigger_names[i]) > (len(trigger_2) + 3):
    if trigger_2 in trigger_names[i]:
      pt_hist_trigger_2.Fill(pTs[i], prescales[i])


  pt_hist_trigger_1.Divide(pt_hist_trigger_2)


  rplt.errorbar(pt_hist_trigger_1, color=color,  markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5)

  plt.gca().xaxis.set_tick_params(width=5, length=20, labelsize=70)
  plt.gca().yaxis.set_tick_params(width=5, length=20, labelsize=70)

  ab = AnnotationBbox(OffsetImage(read_png(get_sample_data("/home/aashish/root-6.04.06/macros/MODAnalyzer/mod_logo.png", asfileobj=False)), zoom=0.15, resample=1, dpi_cor=1), (0.23, 0.895), xycoords='figure fraction', frameon=0)
  plt.gca().add_artist(ab)
  plt.gcf().text(0.29, 0.885, "Prelim. (20\%)", fontsize=50, weight='bold', color='#444444', multialignment='center')

  plt.gcf().set_snap(1)

  # Horizontal Line.
  plt.plot(list(pt_hist_trigger_1.x()), [1] * len(list(pt_hist_trigger_1.x())), color="black", linewidth=5, linestyle="dashed")

 
  if trigger_1 == "HLT_L1Jet6U":
    lower_pT = 37
  elif trigger_1 == "HLT_Jet15U":
    lower_pT = 56
  elif trigger_1 == "HLT_Jet30U":
    lower_pT = 84
  elif trigger_1 == "HLT_Jet50U":
    lower_pT = 114
  elif trigger_1 == "HLT_Jet70U":
    lower_pT = 153
  elif trigger_1 == "HLT_Jet100U":
    lower_pT = 196
  else:
    lower_pT = 0


  if lower_pT != 0:
    # CMS Vertical line.
    plt.plot([lower_pT, lower_pT], [plt.gca().get_ylim()[0], 1.], color=color, linewidth=3, linestyle="dashed")



  # # MOD Vertical line.
  # efficient_pt_x = 0.0
  # efficient_pt_y = 0.0

  # efficient_pt_x_s = []
  # efficient_pt_y_s = []

  # distance_to_previous_point_close_to_one = 0

  # for i in range(0, len(list(pt_hist_trigger_1.x()))):
  #   if abs(list(pt_hist_trigger_1.y())[i] - 1.00) < 0.1:

  #     if distance_to_previous_point_close_to_one > 25:
  #       # Last point close to one too far away.
  #       # Empty the lists.
  #       efficient_pt_x_s, efficient_pt_y_s = [], []

  #     efficient_pt_x_s.append(list(pt_hist_trigger_1.x())[i])
  #     efficient_pt_y_s.append(list(pt_hist_trigger_1.y())[i])
  #     distance_to_previous_point_close_to_one = 0

  #   else:
  #     distance_to_previous_point_close_to_one += 1


  #   if len(efficient_pt_x_s) > 75:
  #     efficient_pt_x = efficient_pt_x_s[0]
  #     efficient_pt_y = efficient_pt_y_s[0]
  #     break



  # mod_efficient_pTs = [325, 260, 196, 153, 114, 84, 50, 32]
  # mod_efficient_pT = mod_efficient_pTs[expected_trigger_names.index(trigger_1.replace("_", "\_"))]




  # plt.plot([mod_efficient_pT, mod_efficient_pT], [plt.gca().get_ylim()[0], 1.], color="purple", linewidth=3, linestyle="dashed")
  

  # if lower_pT != 0:
  #   plt.gca().annotate("CMS\n" + str(lower_pT) + " GeV", xy=(lower_pT, 1.), xycoords='data', xytext=(-100, 250),  textcoords='offset points', color=color, size=40, va="center", ha="center", arrowprops=dict(arrowstyle="simple", facecolor=color, zorder=9999, connectionstyle="angle3,angleA=0,angleB=90") )
  
  # plt.gca().annotate("MOD\n" + str(int(mod_efficient_pT)) + " GeV", xy=(mod_efficient_pT, 1.), xycoords='data', xytext=(250, 200), textcoords='offset points', color="purple", size=40, va="center", ha="center", arrowprops=dict(arrowstyle="simple", facecolor="purple", zorder=9999, connectionstyle="angle3,angleA=45,angleB=-90") )



  plt.yscale('log')
  plt.gca().set_ylim(plt.gca().get_ylim()[0], 100)

  plt.legend(frameon=0)

  plt.xlabel('$p_T~\mathrm{(GeV)}$', fontsize=55, rotation=0)
  plt.ylabel('$\mathrm{A.U.}$', fontsize=75, rotation=0, labelpad=50.)

  plt.gcf().set_size_inches(30, 21.4285714, forward=1)
  plt.gcf().set_snap(True)

  plt.tight_layout(pad=1.08, h_pad=1.08, w_pad=1.08)

  plt.savefig("plots/" + get_version(input_analysis_file) + "/trigger_efficiency/efficiency_curves_" + trigger_1 + ".pdf")
  # plt.show()
  plt.clf()






def plot_all_trigger_efficiency_curves():
  
  properties = parse_file_turn_on('/home/aashish/turn_on.dat')
  # properties = parse_file_turn_on('./trigger_proper_turn_on.dat')

  pTs = properties['corrected_hardest_pts']
  trigger_names = properties['trigger_names']
  prescales = properties['prescales']


  # colors = ['orange', 'red', 'green', 'blue', 'magenta', 'black']
  # colors = colors[::-1]


  colors = ['black', 'magenta', 'blue', 'green', 'red', 'orange']
  expected_trigger_names = ["HLT\_Jet140U", "HLT\_Jet100U", "HLT\_Jet70U", "HLT\_Jet50U", "HLT\_Jet30U", "HLT\_Jet15U\_HcalNoiseFiltered" ]
  labels = ["Jet140U / 100U", "Jet100U / 70U", "Jet70U / 50U", "Jet50U / 30U", "Jet30U / 15U\_HNF", "" ]

  cms_turn_on_pTs = [0, 0, 153, 114, 84]

  pt_hists = []
  for j in range(0, len(expected_trigger_names)):
    pt_hists.append(Hist(60, 0, 300, color=colors[j], title=labels[j], markersize=1.0, linewidth=5))


  for i in range(0, len(expected_trigger_names)):
    for j in range(0, len(pTs)):
      # The len thingy is to make sure trigger names like HLT_Jet15U_HcalNoiseFiltered_v3 are excluded.
      if expected_trigger_names[i].replace("\\", "") in trigger_names[j]:
        pt_hists[i].Fill(pTs[j], prescales[j])

      
  ratio_hists = []
  for i in range(0, len(pt_hists) - 1):
    ratio_hists.append(pt_hists[i] / pt_hists[i + 1])


  for i in range(len(ratio_hists) - 1, -1, -1):
    rplt.errorbar(ratio_hists[i], emptybins=False, ls='None', marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5)
    
    if cms_turn_on_pTs[i] != 0:
      # plt.plot([cms_turn_on_pTs[i], cms_turn_on_pTs[i]], [plt.gca().get_ylim()[0], 1.], color=colors[i], linewidth=5, linestyle="dashed")
      plt.gca().annotate("CMS\n" + str(cms_turn_on_pTs[i]) + " GeV", xy=(cms_turn_on_pTs[i], 1.), xycoords='data', xytext=(-100, 250),  textcoords='offset points', color=colors[i], size=40, va="center", ha="center", arrowprops=dict(arrowstyle="simple", facecolor=colors[i], zorder=99, connectionstyle="angle3,angleA=0,angleB=90") )


  plt.gca().xaxis.set_tick_params(width=5, length=20, labelsize=70)
  plt.gca().yaxis.set_tick_params(width=5, length=20, labelsize=70)

  ab = AnnotationBbox(OffsetImage(read_png(get_sample_data("/home/aashish/root-6.04.06/macros/MODAnalyzer/mod_logo.png", asfileobj=False)), zoom=0.15, resample=1, dpi_cor=1), (0.23, 0.9249985), xycoords='figure fraction', frameon=0)
  plt.gca().add_artist(ab)
  preliminary_text = "Prelim. (20\%)"
  plt.gcf().text(0.29, 0.9178555, preliminary_text, fontsize=50, weight='bold', color='#444444', multialignment='center')

  plt.gcf().set_snap(1)

  # Horizontal Line.
  plt.plot(list(pt_hists[0].x()), [1] * len(list(pt_hists[0].x())), color="black", linewidth=5, linestyle="dashed")


  plt.yscale('log')
  plt.gca().set_ylim(plt.gca().get_ylim()[0], 1000)

  # Legend.
  handles, labels = plt.gca().get_legend_handles_labels()
  first_legend = plt.gca().legend(handles, labels, fontsize=60,  frameon=0, borderpad=0.1, bbox_to_anchor=[0.90, 0.98])
  ax = plt.gca().add_artist(first_legend)

  # Info about R, pT_cut, etc.
  extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
  handles = [extra]
  labels = [r"$ \textrm{Anti--}k_{t}\textrm{:}~\boldsymbol{R = 0.5} $"]
  plt.gca().legend(handles, labels, loc=7, frameon=0, borderpad=0.1, fontsize=60, bbox_to_anchor=[0.77, 0.70])





  plt.xlabel('$p_T~\mathrm{(GeV)}$', fontsize=95, rotation=0)
  plt.ylabel('$\mathrm{Ratio}$', fontsize=55, rotation=0, labelpad=50.)


  plt.gcf().set_size_inches(30, 30, forward=1)
  plt.gcf().set_snap(True)

  plt.tight_layout(pad=1.08, h_pad=1.08, w_pad=1.08)

  plt.savefig("plots/" + get_version(input_analysis_file) + "/all_efficiency_curves.pdf")
  # plt.show()
  plt.clf()



def plot_2d():

  pT_lower_cut = 150
  properties = parse_file(input_analysis_file, pT_lower_cut)
  zgs = [properties['zg_05'], properties['zg_1'], properties['zg_2']]
  charged_zgs = [properties['zg_charged_05'], properties['zg_charged_1'], properties['zg_charged_2']]
  prescales = properties['prescales']

  zgs = zgs[0]
  charged_zgs = charged_zgs[0]

  H, xedges, yedges = np.histogram2d(zgs, charged_zgs, bins=25, weights=prescales, normed=1, range=[[0.05, 0.5], [0.05, 0.5]] )


  H_normalized = []
  for i in range(0, 25):
    current_row = []
    factor = sum(H[i])
    for j in range(0, 25):
      current_row.append(H[i][j] / factor)

    H_normalized.append(current_row)


  H_normalized = np.array(H_normalized)
  H = H_normalized

  H = np.rot90(H)
  H = np.flipud(H)
  
  Hmasked = np.ma.masked_where(H == 0, H) # Mask pixels with a value of zero

  plt.pcolormesh(xedges,yedges, Hmasked)

  cbar = plt.colorbar()
  cbar.ax.set_ylabel('Counts')

  plt.xlabel('Charged $z_g$')
  plt.ylabel('$z_g$')

  plt.gcf().set_size_inches(30, 30, forward=1)
  plt.gcf().set_snap(True)

  

  plt.savefig("test.pdf")

  # plt.show()




def plot_jec_eta_2d():

  pT_lower_cut = 150
  properties = parse_file(input_analysis_file, pT_lower_cut)
  eta = properties['eta']
  jec = properties['JEC']
  prescales = properties['prescales']


  H, xedges, yedges = np.histogram2d(eta, jec, bins=25, weights=prescales, normed=1, range=[[-2.4, 2.4], [0.90, 1.2]] )


  H_normalized = []
  for i in range(0, 25):
    current_row = []
    factor = sum(H[i])
    for j in range(0, 25):
      current_row.append(H[i][j] / factor)

    H_normalized.append(current_row)


  H_normalized = np.array(H_normalized)
  H = H_normalized

  H = np.rot90(H)
  H = np.flipud(H)
  
  Hmasked = np.ma.masked_where(H == 0, H) # Mask pixels with a value of zero

  plt.pcolormesh(xedges,yedges, Hmasked)

  cbar = plt.colorbar()
  cbar.ax.set_ylabel('Counts')

  plt.xlabel('$\eta$', fontsize=50)
  plt.ylabel('JEC', fontsize=50, rotation=0, labelpad=75)

  plt.gcf().set_size_inches(30, 30, forward=1)
  plt.gcf().set_snap(True)

  

  plt.savefig("plots/" + get_version(input_analysis_file) + "/jec_eta_2d.pdf")

  # plt.show()
  plt.clf()





def plot_JEC():
  pT_lower_cut = 100
  properties = parse_file(input_analysis_file, pT_lower_cut)

  JEC = properties['JEC']
  
  prescales = properties['prescales']

  plt.hist(JEC, weights=prescales, bins=100, label="JEC Factor", normed=1, histtype='step', linewidth=5)


  plt.xlabel('JEC Factor', fontsize=75)
  plt.ylabel('A.U.', fontsize=75, rotation=0, labelpad=100.)

  plt.autoscale(True)


  ab = AnnotationBbox(OffsetImage(read_png(get_sample_data("/home/aashish/root-6.04.06/macros/MODAnalyzer/mod_logo.png", asfileobj=False)), zoom=0.15, resample=1, dpi_cor=1), (0.23, 0.895), xycoords='figure fraction', frameon=0)
  plt.gca().add_artist(ab)
  preliminary_text = "Prelim. (20\%)"
  plt.gcf().text(0.29, 0.885, preliminary_text, fontsize=50, weight='bold', color='#444444', multialignment='center')

  plt.gcf().set_size_inches(30, 21.4285714, forward=1)

  legend = plt.gca().legend(loc=1, frameon=0, fontsize=60)
  plt.gca().add_artist(legend)

  plt.gca().xaxis.set_tick_params(width=5, length=20, labelsize=70)
  plt.gca().yaxis.set_tick_params(width=5, length=20, labelsize=70)
  plt.tight_layout(pad=1.08, h_pad=1.08, w_pad=1.08)

  plt.savefig("plots/" + get_version(input_analysis_file) + "/JEC.pdf")

  plt.clf()




def plot_jet_area():
  pT_lower_cut = 100
  properties = parse_file(input_analysis_file, pT_lower_cut)

  jet_area = properties['jet_area']
  prescales = properties['prescales']


  plt.hist(jet_area, weights=prescales, bins=100, label="Jet Area", normed=1, histtype='step', linewidth=5)

  jet_area_expanded = []
  for i in range(0, len(jet_area)):
    for j in range(0, prescales[i]):
      jet_area_expanded.append(jet_area[i])


  mu, std = norm.fit(jet_area_expanded)
  xmin, xmax = plt.xlim()
  x = np.linspace(xmin, xmax, 500)
  p = norm.pdf(x, mu, std)
  plt.plot(x, p, 'k', linewidth=5)

  plt.autoscale(True)
  plt.gca().set_ylim(0., 1.1 * plt.gca().get_ylim()[1])

  plt.plot([ math.pi*(0.5**2), math.pi*(0.5**2) ], [ plt.gca().get_ylim()[0], plt.gca().get_ylim()[1] ], color='red', linewidth=5, linestyle="dashed")
  # plt.gca().annotate("$\pi \cdot 0.5^2$", xy=(math.pi*(0.5**2), 20.), xycoords='data', color='red', xytext=(0.9, 20), size=40, va="center", ha="center", arrowprops=dict(arrowstyle="simple", facecolor='red', zorder=99) )

  plt.xlabel('Jet Area', fontsize=75)
  plt.ylabel('A.U.', fontsize=75, rotation=0, labelpad=100.)

  ab = AnnotationBbox(OffsetImage(read_png(get_sample_data("/home/aashish/root-6.04.06/macros/MODAnalyzer/mod_logo.png", asfileobj=False)), zoom=0.15, resample=1, dpi_cor=1), (0.23, 0.895), xycoords='figure fraction', frameon=0)
  plt.gca().add_artist(ab)
  preliminary_text = "Prelim. (20\%)"
  plt.gcf().text(0.29, 0.885, preliminary_text, fontsize=50, weight='bold', color='#444444', multialignment='center')

  plt.gcf().set_size_inches(30, 21.4285714, forward=1)

  legend = plt.gca().legend(loc=1, frameon=0, fontsize=60)
  plt.gca().add_artist(legend)

  extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
  labels = ["Fit Statistics\n" + "$\mu=" + str(mu.round(3)) + "$\n$" + "\sigma=" + str(std.round(3)) + "$"]
  plt.gca().legend([extra], labels, loc=7, frameon=0, borderpad=0.1, fontsize=60, bbox_to_anchor=[0.96, 0.80])


  plt.gca().xaxis.set_minor_locator(MultipleLocator(0.02))
  plt.gca().yaxis.set_minor_locator(MultipleLocator(1))
  plt.tick_params(which='major', width=5, length=25, labelsize=70)
  plt.tick_params(which='minor', width=3, length=15)

  plt.tight_layout(pad=1.08, h_pad=1.08, w_pad=1.08)

  plt.savefig("plots/" + get_version(input_analysis_file) + "/jet_area.pdf")

  plt.clf()





def plot_charged_and_all_zgs(pT_lower_cut=150, pT_upper_cut=10000, zg_cut='0.05', zg_filename='zg_05', n_bins=10, y_max_limit=20):

  properties = parse_file(input_analysis_file, pT_lower_cut)

  zgs = properties[zg_filename]
  charged_zgs = properties[zg_filename[0:2] + "_charged_" + zg_filename[3: len(zg_filename)]]
  prescales = properties['prescales']
 
  zg_hist = Hist(6 * n_bins, 0.0, 0.6, title="All PF Candidates", markersize=1.0, color='black')
  zg_charged_hist = Hist(6 * n_bins, 0.0, 0.6, title="Charged PFCs", markersize=1.0, color='red')

  bin_width_zg = (zg_hist.upperbound() - zg_hist.lowerbound()) / zg_hist.nbins()
  bin_width_zg_charged = (zg_charged_hist.upperbound() - zg_charged_hist.lowerbound()) / zg_charged_hist.nbins()


  map(zg_hist.Fill, zgs, prescales)
  map(zg_charged_hist.Fill, charged_zgs, prescales)

  if zg_hist.GetSumOfWeights() != 0:
    zg_hist.Scale(1.0 / (zg_hist.GetSumOfWeights() * bin_width_zg))

  if zg_charged_hist.GetSumOfWeights() != 0:
    zg_charged_hist.Scale(1.0 / (zg_charged_hist.GetSumOfWeights() * bin_width_zg_charged))
  
  rplt.errorbar(zg_hist, emptybins=False, ls='None', marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5)
  rplt.errorbar(zg_charged_hist, emptybins=False, ls='None', marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5)
  
  
  legend = plt.legend(frameon=0, fontsize=60, bbox_to_anchor=[0.95, 0.98])
  plt.gca().add_artist(legend)

  
  extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
  handles = [extra, extra, extra]
  labels = [r"$ \textrm{Anti--}k_{t}\textrm{:}~R = 0.5;\eta<2.4$", r"$p_{T} > " + str(pT_lower_cut) + "~\mathrm{GeV}$", r"$ \textrm{Soft~Drop:}~\boldsymbol{\beta = 0;~z_{\mathrm{cut}} = " + str(zg_cut) + "}$"]

  plt.gca().legend(handles, labels, loc=7, frameon=0, borderpad=0.1, fontsize=60, bbox_to_anchor=[0.99, 0.65])


  plt.xlabel("$z_g$", fontsize=95)
  plt.ylabel("$\displaystyle \\frac{1}{\sigma} \\frac{ \mathrm{d} \sigma}{ \mathrm{d} z_g}$", fontsize=80, rotation=0, labelpad=115, y=0.39)
  

  ab = AnnotationBbox(OffsetImage(read_png(get_sample_data("/home/aashish/root-6.04.06/macros/MODAnalyzer/mod_logo.png", asfileobj=False)), zoom=0.15, resample=1, dpi_cor=1), (0.23, 0.895), xycoords='figure fraction', frameon=0)
  plt.gca().add_artist(ab)
  preliminary_text = "Prelim. (20\%)"
  plt.gcf().text(0.29, 0.885, preliminary_text, fontsize=50, weight='bold', color='#444444', multialignment='center')

  plt.gca().set_ylim(0, y_max_limit)
  plt.gca().set_xlim(0.0, 0.6)

  plt.gcf().set_size_inches(30, 21.4285714, forward=1)

  plt.gca().xaxis.set_minor_locator(MultipleLocator(0.02))
  plt.gca().yaxis.set_minor_locator(MultipleLocator(0.5))

  plt.tick_params(which='major', width=5, length=25, labelsize=70)
  plt.tick_params(which='minor', width=3, length=15)

  plt.tight_layout(pad=1.08, h_pad=1.08, w_pad=1.08)

  print "Writing out charged_" + str(zg_filename) + "_pt_cut_" + str(pT_lower_cut) + ".pdf"

  plt.savefig("plots/" + get_version(input_analysis_file) + "/zg_charged/charged_" + str(zg_filename) + "_pt_cut_" + str(pT_lower_cut) + ".pdf")
  # plt.show()
  plt.clf()



def plot_pts(pT_lower_cut=100, pT_upper_cut=10000):
  properties = parse_file(input_analysis_file, pT_lower_cut=pT_lower_cut, pT_upper_cut=pT_upper_cut)

  pTs = properties['uncorrected_hardest_pts']
  corrected_pTs = properties['corrected_hardest_pts']
  prescales = properties['prescales']


  pythia_properties = parse_mc("/home/aashish/pythia_truth.dat", pT_lower_cut=pT_lower_cut)
  herwig_properties = parse_mc("/home/aashish/herwig_truth.dat", pT_lower_cut=pT_lower_cut)
  sherpa_properties = parse_mc("/home/aashish/sherpa_truth.dat", pT_lower_cut=pT_lower_cut)

  # pythia_properties = parse_mc("/home/aashish/pythia_reco.dat", pT_lower_cut=pT_lower_cut)
  # herwig_properties = parse_mc("/home/aashish/herwig_reco.dat", pT_lower_cut=pT_lower_cut)
  # sherpa_properties = parse_mc("/home/aashish/sherpa_reco.dat", pT_lower_cut=pT_lower_cut)

  pythia_pTs = pythia_properties['hardest_pts']
  herwig_pTs = herwig_properties['hardest_pts']
  sherpa_pTs = sherpa_properties['hardest_pts']


  pythia_pt_hist = Hist(100, 0, 700, title="Pythia 8.212", linewidth=5, markersize=5.0, color="red")
  bin_width_pythia = (pythia_pt_hist.upperbound() - pythia_pt_hist.lowerbound()) / pythia_pt_hist.nbins()

  herwig_pt_hist = Hist(100, 0, 700, title="Herwig++ 2.7.1", linewidth=5, markersize=5.0, color="green")
  bin_width_herwig = (herwig_pt_hist.upperbound() - herwig_pt_hist.lowerbound()) / herwig_pt_hist.nbins()

  sherpa_pt_hist = Hist(100, 0, 700, title="Sherpa 2.2.0", linewidth=5, markersize=5.0, color="blue")
  bin_width_sherpa = (sherpa_pt_hist.upperbound() - sherpa_pt_hist.lowerbound()) / sherpa_pt_hist.nbins()

  corrected_pt_hist = Hist(100, 0, 700, title='Corrected', markersize=3.0, color='black')
  bin_width_corrected = (corrected_pt_hist.upperbound() - corrected_pt_hist.lowerbound()) / corrected_pt_hist.nbins()

  uncorrected_pt_hist = Hist(100, 0, 700, title='Uncorrected', markersize=3.0, color='orange')
  bin_width_uncorrected = (uncorrected_pt_hist.upperbound() - uncorrected_pt_hist.lowerbound()) / uncorrected_pt_hist.nbins()

  map(uncorrected_pt_hist.Fill, pTs, prescales)
  map(corrected_pt_hist.Fill, corrected_pTs, prescales)
  
  map(pythia_pt_hist.Fill, pythia_pTs)
  map(herwig_pt_hist.Fill, herwig_pTs)
  map(sherpa_pt_hist.Fill, sherpa_pTs)


  corrected_pt_hist.Scale(1.0 / (corrected_pt_hist.GetSumOfWeights() * bin_width_corrected))
  uncorrected_pt_hist.Scale(1.0 / (uncorrected_pt_hist.GetSumOfWeights() * bin_width_uncorrected))
  pythia_pt_hist.Scale(1.0 / (pythia_pt_hist.GetSumOfWeights() * bin_width_pythia))
  herwig_pt_hist.Scale(1.0 / (herwig_pt_hist.GetSumOfWeights() * bin_width_herwig))
  sherpa_pt_hist.Scale(1.0 / (sherpa_pt_hist.GetSumOfWeights() * bin_width_sherpa))

  
  gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1]) 

  ax0 = plt.subplot(gs[0])
  ax1 = plt.subplot(gs[1])




  data_plot = rplt.errorbar(corrected_pt_hist, axes=ax0, emptybins=False, marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5)
  uncorrected_data_plot = rplt.errorbar(uncorrected_pt_hist, axes=ax0, emptybins=False, marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5)
  rplt.hist(pythia_pt_hist, axes=ax0, emptybins=False, marker='o',  markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5)
  rplt.hist(herwig_pt_hist, axes=ax0, emptybins=False, marker='o',  markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5)
  rplt.hist(sherpa_pt_hist, axes=ax0, emptybins=False, marker='o',  markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5)
  

  data_x_errors, data_y_errors = [], []
  for x_segment in data_plot[2][0].get_segments():
    data_x_errors.append((x_segment[1][0] - x_segment[0][0]) / 2.)
  for y_segment in data_plot[2][1].get_segments():
    data_y_errors.append((y_segment[1][1] - y_segment[0][1]) / 2.)

  data_points_x = data_plot[0].get_xdata()
  data_points_y = data_plot[0].get_ydata()

  data_plot_points_x = []
  data_plot_points_y = []
  for i in range(0, len(data_points_x)):
    data_plot_points_x.append(data_points_x[i])
    data_plot_points_y.append(data_points_y[i])



  uncorrected_data_x_errors, uncorrected_data_y_errors = [], []
  for x_segment in uncorrected_data_plot[2][0].get_segments():
    uncorrected_data_x_errors.append((x_segment[1][0] - x_segment[0][0]) / 2.)
  for y_segment in uncorrected_data_plot[2][1].get_segments():
    uncorrected_data_y_errors.append((y_segment[1][1] - y_segment[0][1]) / 2.)

  uncorrected_data_points_x = uncorrected_data_plot[0].get_xdata()
  uncorrected_data_points_y = uncorrected_data_plot[0].get_ydata()

  uncorrected_data_plot_points_x = []
  uncorrected_data_plot_points_y = []
  for i in range(0, len(uncorrected_data_points_x)):
    uncorrected_data_plot_points_x.append(uncorrected_data_points_x[i])
    uncorrected_data_plot_points_y.append(uncorrected_data_points_y[i])




  data_to_data_y_err = [(b / m) for b, m in zip(data_y_errors, data_plot_points_y)]
  data_to_data_x_err = [(b / m) for b, m in zip(data_x_errors, [1] * len(data_plot_points_y))]

  uncorrected_to_corrected_y_err = [(b / m) for b, m in zip(uncorrected_data_y_errors, data_plot_points_y)]
  uncorrected_to_corrected_x_err = [(b / m) for b, m in zip(uncorrected_data_x_errors, [1] * len(data_plot_points_y))]


  # Legends Begin.

  legend = ax0.legend(loc=1, frameon=0, fontsize=60, bbox_to_anchor=[0.95, 1.0])
  ax0.add_artist(legend)

  extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
  if pT_upper_cut != 10000:
    labels = [r"$ \textrm{Anti--}k_{t}\textrm{:}~R = 0.5;\eta<2.4$", r"$p_{T} \in [" + str(pT_lower_cut) + ", " + str(pT_upper_cut) + "]~\mathrm{GeV}$"]
  else:
    labels = [r"$ \textrm{Anti--}k_{t}\textrm{:}~R = 0.5;\eta<2.4$", r"$p_{T} > " + str(pT_lower_cut) + "~\mathrm{GeV}$"]
  ax0.legend([extra, extra], labels, loc=7, frameon=0, borderpad=0.1, fontsize=60, bbox_to_anchor=[0.99, 0.57])

  # Legends End.



  ax0.set_xlabel('$p_T~\mathrm{(GeV)}$', fontsize=75)
  ax1.set_xlabel('$p_T~\mathrm{(GeV)}$', fontsize=75)
  ax0.set_ylabel('$\mathrm{A.U.}$', fontsize=75, rotation=0, labelpad=75.)
  ax1.set_ylabel("Ratio           \nto           \n" + "Data" + "           ", fontsize=55, rotation=0, labelpad=115, y=0.31)


  ab = AnnotationBbox(OffsetImage(read_png(get_sample_data("/home/aashish/root-6.04.06/macros/MODAnalyzer/mod_logo.png", asfileobj=False)), zoom=0.15, resample=1, dpi_cor=1), (0.23, 0.9249985), xycoords='figure fraction', frameon=0)
  plt.gca().add_artist(ab)
  preliminary_text = "Prelim. (20\%)"
  plt.gcf().text(0.29, 0.9178555, preliminary_text, fontsize=50, weight='bold', color='#444444', multialignment='center')

  # Ratio Plot.
  pythia_pt_hist.Divide(corrected_pt_hist)
  herwig_pt_hist.Divide(corrected_pt_hist)
  sherpa_pt_hist.Divide(corrected_pt_hist)
  uncorrected_pt_hist.Divide(corrected_pt_hist)
  corrected_pt_hist.Divide(corrected_pt_hist)

  rplt.hist(pythia_pt_hist, axes=ax1, linewidth=5)
  rplt.hist(herwig_pt_hist, axes=ax1, linewidth=5)
  rplt.hist(sherpa_pt_hist, axes=ax1, linewidth=5)
  
  rplt.errorbar(corrected_pt_hist, xerr=data_to_data_x_err, yerr=data_to_data_y_err, axes=ax1, emptybins=False, marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5)
  rplt.errorbar(uncorrected_pt_hist, xerr=uncorrected_to_corrected_x_err, yerr=uncorrected_to_corrected_y_err, axes=ax1, emptybins=False, marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5)

  ax0.set_yscale('log')

  ax0.autoscale(True)
  ax1.autoscale(True)
  
  ax1.set_ylim(0., 2.)



  if ((pT_lower_cut == 150 and pT_upper_cut == 250)):
    ax0.set_xlim(150, 250)
    ax1.set_xlim(150, 250)
    ax0.set_ylim(10e-4, 10e-2)
    pT_minor_ticks = 5
  elif ((pT_lower_cut == 250 and pT_upper_cut == 500)):
    ax0.set_xlim(250, 500)
    ax1.set_xlim(250, 500)
    ax0.set_ylim(10e-5, 10e-2)
    pT_minor_ticks = 10
  elif ((pT_lower_cut == 500 and pT_upper_cut == 10000)):
    ax0.set_xlim(500, 1500)
    ax1.set_xlim(500, 1500)
    ax0.set_ylim(0.0005, 0.05)
    pT_minor_ticks = 50
  elif ((pT_lower_cut == 150 and pT_upper_cut == 10000)):
    ax0.set_xlim(150, 1000)
    ax1.set_xlim(150, 1000)
    ax0.set_ylim(10e-8, 10e-2)
    pT_minor_ticks = 50
  else:
    ax0.set_xlim(150, 1000)
    ax1.set_xlim(150, 1000)
    ax0.set_ylim(10e-8, 10e-2)
    pT_minor_ticks = 50


  ax0.set_xlim(0, 700)
  ax1.set_xlim(0, 700)

  plt.gcf().set_size_inches(30, 30, forward=1)

  plt.sca(ax0)
  plt.gca().xaxis.set_minor_locator(MultipleLocator(pT_minor_ticks))
  plt.tick_params(which='major', width=5, length=25, labelsize=70)
  plt.tick_params(which='minor', width=3, length=15)

  plt.sca(ax1)
  plt.gca().xaxis.set_minor_locator(MultipleLocator(pT_minor_ticks))
  # plt.gca().yaxis.set_minor_locator(MultipleLocator(50))
  plt.tick_params(which='major', width=5, length=25, labelsize=70)
  plt.tick_params(which='minor', width=3, length=15)

  plt.tight_layout(pad=1.08, h_pad=1.08, w_pad=1.08)

  print "Printing fractional energy loss with pT > " + str(pT_lower_cut) + " and pT < " + str(pT_upper_cut)

  plt.savefig("plots/" + get_version(input_analysis_file) + "/pT_distribution/pT_lower_" + str(pT_lower_cut) + "_pT_upper_" + str(pT_upper_cut) + ".pdf")
  # plt.show()
  plt.clf()




def plot_hardest_pt_softdrop(pT_lower_cut=100, pT_upper_cut=20000):
  properties = parse_file(input_analysis_file, pT_lower_cut=pT_lower_cut, pT_upper_cut=pT_upper_cut)

  pTs_before_SD = properties['corrected_hardest_pts']
  pTs_after_SD = properties['pTs_after_SD_unc']  
  prescales = properties['prescales']

  pT_before_SD_hist = Hist(150, 0, 1500, title='Before SoftDrop', markersize=3.0, color='black')
  bin_width_before = (pT_before_SD_hist.upperbound() - pT_before_SD_hist.lowerbound()) / pT_before_SD_hist.nbins()

  pT_after_SD_hist = Hist(150, 0, 1500, title='After SoftDrop', markersize=3.0, color='red')
  bin_width_after = (pT_after_SD_hist.upperbound() - pT_after_SD_hist.lowerbound()) / pT_after_SD_hist.nbins()

  map(pT_before_SD_hist.Fill, pTs_before_SD, prescales)
  map(pT_after_SD_hist.Fill, pTs_after_SD, prescales)
  
  pT_before_SD_hist.Scale(1.0 / (pT_before_SD_hist.GetSumOfWeights() * bin_width_before))
  pT_after_SD_hist.Scale(1.0 / (pT_after_SD_hist.GetSumOfWeights() * bin_width_after))
  
  pT_before_SD_plot = rplt.errorbar(pT_before_SD_hist, emptybins=False, marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5)
  pT_after_SD_plot = rplt.errorbar(pT_after_SD_hist, emptybins=False, marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5)
  
  plt.yscale('log')

  # Legends Begin.

  legend = plt.gca().legend(loc=1, frameon=0, fontsize=60, bbox_to_anchor=[0.89, 1.0])
  plt.gca().add_artist(legend)

  extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
  if pT_upper_cut != 20000:
    labels = [r"$ \textrm{Anti--}k_{t}\textrm{:}~R = 0.5;\eta<2.4$", r"$p_{T} \in [" + str(pT_lower_cut) + ", " + str(pT_upper_cut) + "]~\mathrm{GeV}$", r"$ \textrm{Soft~Drop:}~\boldsymbol{\beta = 0;~z_{\mathrm{cut}} = 0.05}$"]
  else:
    labels = [r"$ \textrm{Anti--}k_{t}\textrm{:}~R = 0.5;\eta<2.4$", r"$p_{T} > " + str(pT_lower_cut) + "~\mathrm{GeV}$", r"$ \textrm{Soft~Drop:}~\boldsymbol{\beta = 0;~z_{\mathrm{cut}} = 0.05}$"]
  plt.gca().legend([extra, extra, extra], labels, loc=7, frameon=0, borderpad=0.1, fontsize=60, bbox_to_anchor=[0.99, 0.70])

  # Legends End.

  ab = AnnotationBbox(OffsetImage(read_png(get_sample_data("/home/aashish/root-6.04.06/macros/MODAnalyzer/mod_logo.png", asfileobj=False)), zoom=0.15, resample=1, dpi_cor=1), (0.23, 0.895), xycoords='figure fraction', frameon=0)
  plt.gca().add_artist(ab)
  preliminary_text = "Prelim. (20\%)"
  plt.gcf().text(0.29, 0.885, preliminary_text, fontsize=50, weight='bold', color='#444444', multialignment='center')

  plt.gcf().set_size_inches(30, 21.4285714, forward=1)

  plt.xlabel('$p_T~\mathrm{(GeV)}$', fontsize=75)
  plt.ylabel('$\mathrm{A.U.}$', fontsize=75, rotation=0, labelpad=80.)
  
  plt.gcf().set_size_inches(30, 21.4285714, forward=1)

  plt.gca().autoscale(True)
  # plt.ylim(10e-9, 10e-1)
  # plt.gca().set_ylim(0., 1.5 * plt.gca().get_ylim()[1])

  if ((pT_lower_cut == 100 and pT_upper_cut == 200)):
    plt.ylim(10e-5, 10e-1)
  elif ((pT_lower_cut == 200 and pT_upper_cut == 400)):
    plt.ylim(10e-6, 10e-1)
    # plt.xlim(100, 600)
  elif ((pT_lower_cut == 400 and pT_upper_cut == 20000)):
    plt.ylim(10e-6, 10e-2)
  elif ((pT_lower_cut == 100 and pT_upper_cut == 20000)):
    plt.ylim(10e-9, 10e-1)


  plt.gca().xaxis.set_minor_locator(MultipleLocator(50))
  # plt.gca().yaxis.set_minor_locator(MultipleLocator(50))
  plt.tick_params(which='major', width=5, length=25, labelsize=70)
  plt.tick_params(which='minor', width=3, length=15)

  plt.tight_layout(pad=1.08, h_pad=1.08, w_pad=1.08)

  print "Printing fractional energy loss with pT > " + str(pT_lower_cut) + " and pT < " + str(pT_upper_cut)

  plt.savefig("plots/" + get_version(input_analysis_file) + "/hardest_pt_softdrop/pT_lower_" + str(pT_lower_cut) + "_pT_upper_" + str(pT_upper_cut) + ".pdf")
  # plt.show()
  plt.clf()



def plot_constituent_multiplicity_softdrop(pT_lower_cut=100, pT_upper_cut=20000):
  properties = parse_file(input_analysis_file, pT_lower_cut=pT_lower_cut, pT_upper_cut=pT_upper_cut)

  multi_before_SD = properties['multiplicity_before_SD']
  multi_after_SD = properties['multiplicity_after_SD']  
  prescales = properties['prescales']

  multi_before_SD_hist = Hist(150, 0, 150, title='Before SoftDrop', markersize=3.0, color='black')
  bin_width_before = (multi_before_SD_hist.upperbound() - multi_before_SD_hist.lowerbound()) / multi_before_SD_hist.nbins()

  multi_after_SD_hist = Hist(150, 0, 150, title='After SoftDrop', markersize=3.0, color='red')
  bin_width_after = (multi_after_SD_hist.upperbound() - multi_after_SD_hist.lowerbound()) / multi_after_SD_hist.nbins()

  map(multi_before_SD_hist.Fill, multi_before_SD, prescales)
  map(multi_after_SD_hist.Fill, multi_after_SD, prescales)
  
  multi_before_SD_hist.Scale(1.0 / (multi_before_SD_hist.GetSumOfWeights() * bin_width_before))
  multi_after_SD_hist.Scale(1.0 / (multi_after_SD_hist.GetSumOfWeights() * bin_width_after))
  
  pT_before_SD_plot = rplt.errorbar(multi_before_SD_hist, emptybins=False, marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5)
  pT_after_SD_plot = rplt.errorbar(multi_after_SD_hist, emptybins=False, marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5)
  
  # plt.yscale('log')

  # Legends Begin.

  legend = plt.gca().legend(loc=1, frameon=0, fontsize=60, bbox_to_anchor=[0.89, 1.0])
  plt.gca().add_artist(legend)

  extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
  if pT_upper_cut != 20000:
    labels = [r"$ \textrm{Anti--}k_{t}\textrm{:}~R = 0.5;\eta<2.4$", r"$p_{T}\in[" + str(pT_lower_cut) + ", " + str(pT_upper_cut) + "]~\mathrm{GeV}$", r"$ \textrm{Soft~Drop:}~\boldsymbol{\beta = 0;~z_{\mathrm{cut}} = 0.05}$"]
  else:
    labels = [r"$ \textrm{Anti--}k_{t}\textrm{:}~R = 0.5;\eta<2.4$", r"$p_{T} > " + str(pT_lower_cut) + "~\mathrm{GeV}$", r"$ \textrm{Soft~Drop:}~\boldsymbol{\beta = 0;~z_{\mathrm{cut}} = 0.05}$"]
  plt.gca().legend([extra, extra, extra], labels, loc=7, frameon=0, borderpad=0.1, fontsize=60, bbox_to_anchor=[0.99, 0.70])

  # Legends End.

  ab = AnnotationBbox(OffsetImage(read_png(get_sample_data("/home/aashish/root-6.04.06/macros/MODAnalyzer/mod_logo.png", asfileobj=False)), zoom=0.15, resample=1, dpi_cor=1), (0.23, 0.895), xycoords='figure fraction', frameon=0)
  plt.gca().add_artist(ab)
  preliminary_text = "Prelim. (20\%)"
  plt.gcf().text(0.29, 0.885, preliminary_text, fontsize=50, weight='bold', color='#444444', multialignment='center')

  plt.gcf().set_size_inches(30, 21.4285714, forward=1)

  plt.xlabel('Constituent Multiplicity', fontsize=75)
  plt.ylabel('$\mathrm{A.U.}$', fontsize=55, rotation=0, labelpad=75.)
  
  plt.gcf().set_size_inches(30, 21.4285714, forward=1)

  plt.gca().autoscale(True)
  plt.gca().set_ylim(0., 1.1 * plt.gca().get_ylim()[1])

  plt.gca().xaxis.set_minor_locator(MultipleLocator(5))
  plt.gca().yaxis.set_minor_locator(MultipleLocator(0.002))
  plt.tick_params(which='major', width=5, length=25, labelsize=70)
  plt.tick_params(which='minor', width=3, length=15)

  plt.tight_layout(pad=1.08, h_pad=1.08, w_pad=1.08)

  print "Printing fractional energy loss with pT > " + str(pT_lower_cut) + " and pT < " + str(pT_upper_cut)

  plt.savefig("plots/" + get_version(input_analysis_file) + "/constituent_multiplicity_softdrop/pT_lower_" + str(pT_lower_cut) + "_pT_upper_" + str(pT_upper_cut) + ".pdf")
  # plt.show()
  plt.clf()




def plot_charged_constituent_multiplicity_softdrop(pT_lower_cut=100, pT_upper_cut=20000):
  properties = parse_file(input_analysis_file, pT_lower_cut=pT_lower_cut, pT_upper_cut=pT_upper_cut)

  multi_before_SD = properties['charged_multiplicity_before_SD']
  multi_after_SD = properties['charged_multiplicity_after_SD']  
  prescales = properties['prescales']

  multi_before_SD_hist = Hist(150, 0, 150, title='Before SoftDrop (Charged Jets)', markersize=3.0, color='black')
  bin_width_before = (multi_before_SD_hist.upperbound() - multi_before_SD_hist.lowerbound()) / multi_before_SD_hist.nbins()

  multi_after_SD_hist = Hist(150, 0, 150, title='After SoftDrop (Charged Jets)', markersize=3.0, color='red')
  bin_width_after = (multi_after_SD_hist.upperbound() - multi_after_SD_hist.lowerbound()) / multi_after_SD_hist.nbins()

  map(multi_before_SD_hist.Fill, multi_before_SD, prescales)
  map(multi_after_SD_hist.Fill, multi_after_SD, prescales)
  
  multi_before_SD_hist.Scale(1.0 / (multi_before_SD_hist.GetSumOfWeights() * bin_width_before))
  multi_after_SD_hist.Scale(1.0 / (multi_after_SD_hist.GetSumOfWeights() * bin_width_after))
  
  pT_before_SD_plot = rplt.errorbar(multi_before_SD_hist, emptybins=False, marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5)
  pT_after_SD_plot = rplt.errorbar(multi_after_SD_hist, emptybins=False, marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5)
  
  # plt.yscale('log')

  # Legends Begin.

  legend = plt.gca().legend(loc=1, frameon=0, fontsize=60, bbox_to_anchor=[1.0, 1.0])
  plt.gca().add_artist(legend)

  extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
  if pT_upper_cut != 20000:
    labels = [r"$ \textrm{Anti--}k_{t}\textrm{:}~R = 0.5;\eta<2.4$", r"$p_{T}\in[" + str(pT_lower_cut) + ", " + str(pT_upper_cut) + "]~\mathrm{GeV}$", r"$ \textrm{Soft~Drop:}~\boldsymbol{\beta = 0;~z_{\mathrm{cut}} = 0.05}$"]
  else:
    labels = [r"$ \textrm{Anti--}k_{t}\textrm{:}~R = 0.5;\eta<2.4$", r"$p_{T} > " + str(pT_lower_cut) + "~\mathrm{GeV}$", r"$ \textrm{Soft~Drop:}~\boldsymbol{\beta = 0;~z_{\mathrm{cut}} = 0.05}$"]
  plt.gca().legend([extra, extra, extra], labels, loc=7, frameon=0, borderpad=0.1, fontsize=60, bbox_to_anchor=[0.86, 0.70])

  # Legends End.

  ab = AnnotationBbox(OffsetImage(read_png(get_sample_data("/home/aashish/root-6.04.06/macros/MODAnalyzer/mod_logo.png", asfileobj=False)), zoom=0.15, resample=1, dpi_cor=1), (0.23, 0.895), xycoords='figure fraction', frameon=0)
  plt.gca().add_artist(ab)
  preliminary_text = "Prelim. (20\%)"
  plt.gcf().text(0.29, 0.885, preliminary_text, fontsize=50, weight='bold', color='#444444', multialignment='center')

  plt.gcf().set_size_inches(30, 21.4285714, forward=1)

  plt.xlabel('Constituent Multiplicity', fontsize=75)
  plt.ylabel('$\mathrm{A.U.}$', fontsize=55, rotation=0, labelpad=75.)
  
  plt.gcf().set_size_inches(30, 21.4285714, forward=1)

  plt.gca().autoscale(True)
  plt.gca().set_ylim(0., 1.1 * plt.gca().get_ylim()[1])

  plt.gca().xaxis.set_minor_locator(MultipleLocator(5))
  plt.gca().yaxis.set_minor_locator(MultipleLocator(0.002))
  plt.tick_params(which='major', width=5, length=25, labelsize=70)
  plt.tick_params(which='minor', width=3, length=15)

  plt.tight_layout(pad=1.08, h_pad=1.08, w_pad=1.08)


  print "Printing charged constituent multiplicity softdrop with pT > " + str(pT_lower_cut) + " and pT < " + str(pT_upper_cut)

  plt.savefig("plots/" + get_version(input_analysis_file) + "/charged_constituent_multiplicity_softdrop/pT_lower_" + str(pT_lower_cut) + "_pT_upper_" + str(pT_upper_cut) + ".pdf")
  # plt.show()
  plt.clf()




def plot_constituent_multiplicity_softdrop_multiple_jet_correction_level(pT_lower_cut=100, pT_upper_cut=20000):
  


  jet_quality_levels = [1, 2, 3]
  titles = [ ["Before SoftDrop (Loose)", "After SoftDrop (Loose)"], ["Before SoftDrop (Medium)", "After SoftDrop (Medium)"], ["Before SoftDrop (Tight)", "Before SoftDrop (Tight)"]]
  colors = [['red', 'green'], ['gray', 'orange'], ['blue', 'magenta']]

  for i in range(0, len(jet_quality_levels)):

    properties = parse_file(input_analysis_file, pT_lower_cut=pT_lower_cut, pT_upper_cut=pT_upper_cut, jet_quality_level=jet_quality_levels[i])

    multi_before_SD = properties['multiplicity_before_SD']
    multi_after_SD = properties['multiplicity_after_SD']  
    prescales = properties['prescales']

    multi_before_SD_hist = Hist(150, 0, 150, title=titles[i][0], markersize=3.0, color=colors[i][0])
    bin_width_before = (multi_before_SD_hist.upperbound() - multi_before_SD_hist.lowerbound()) / multi_before_SD_hist.nbins()

    multi_after_SD_hist = Hist(150, 0, 150, title=titles[i][1], markersize=3.0, color=colors[i][1])
    bin_width_after = (multi_after_SD_hist.upperbound() - multi_after_SD_hist.lowerbound()) / multi_after_SD_hist.nbins()

    map(multi_before_SD_hist.Fill, multi_before_SD, prescales)
    map(multi_after_SD_hist.Fill, multi_after_SD, prescales)
    
    multi_before_SD_hist.Scale(1.0 / (multi_before_SD_hist.GetSumOfWeights() * bin_width_before))
    multi_after_SD_hist.Scale(1.0 / (multi_after_SD_hist.GetSumOfWeights() * bin_width_after))
    
    pT_before_SD_plot = rplt.errorbar(multi_before_SD_hist, alpha=0.5, emptybins=False, marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5)
    pT_after_SD_plot = rplt.errorbar(multi_after_SD_hist, alpha=0.5, emptybins=False, marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5)
  



  # Legends Begin.

  legend = plt.gca().legend(loc=1, frameon=0, fontsize=60, bbox_to_anchor=[1.00, 1.0])
  plt.gca().add_artist(legend)

  extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
  if pT_upper_cut != 20000:
    labels = [r"$ \textrm{Anti--}k_{t}\textrm{:}~R = 0.5;\eta<2.4$", r"$p_{T}\in[" + str(pT_lower_cut) + ", " + str(pT_upper_cut) + "]~\mathrm{GeV}$", r"$ \textrm{Soft~Drop:}~\boldsymbol{\beta = 0;~z_{\mathrm{cut}} = 0.05}$"]
  else:
    labels = [r"$ \textrm{Anti--}k_{t}\textrm{:}~R = 0.5;\eta<2.4$", r"$p_{T} > " + str(pT_lower_cut) + "~\mathrm{GeV}$", r"$ \textrm{Soft~Drop:}~\boldsymbol{\beta = 0;~z_{\mathrm{cut}} = 0.05}$"]
  plt.gca().legend([extra, extra, extra], labels, loc=7, frameon=0, borderpad=0.1, fontsize=60, bbox_to_anchor=[0.99, 0.30])

  # Legends End.

  ab = AnnotationBbox(OffsetImage(read_png(get_sample_data("/home/aashish/root-6.04.06/macros/MODAnalyzer/mod_logo.png", asfileobj=False)), zoom=0.15, resample=1, dpi_cor=1), (0.23, 0.895), xycoords='figure fraction', frameon=0)
  plt.gca().add_artist(ab)
  preliminary_text = "Prelim. (20\%)"
  plt.gcf().text(0.29, 0.885, preliminary_text, fontsize=50, weight='bold', color='#444444', multialignment='center')



  plt.gcf().set_size_inches(30, 21.4285714, forward=1)

  plt.xlabel('Constituent Multiplicity', fontsize=75)
  plt.ylabel('$\mathrm{A.U.}$', fontsize=55, rotation=0, labelpad=75.)
  
  plt.gcf().set_size_inches(30, 21.4285714, forward=1)

  plt.gca().autoscale(True)
  plt.gca().set_ylim(0., 1.1 * plt.gca().get_ylim()[1])

  plt.gca().xaxis.set_minor_locator(MultipleLocator(5))
  plt.gca().yaxis.set_minor_locator(MultipleLocator(0.002))
  plt.tick_params(which='major', width=5, length=25, labelsize=70)
  plt.tick_params(which='minor', width=3, length=15)

  plt.tight_layout(pad=1.08, h_pad=1.08, w_pad=1.08)

  print "Printing fractional energy loss with pT > " + str(pT_lower_cut) + " and pT < " + str(pT_upper_cut)

  plt.savefig("plots/" + get_version(input_analysis_file) + "/constituent_multiplicity_softdrop/multiple_correction_level_pT_lower_" + str(pT_lower_cut) + "_pT_upper_" + str(pT_upper_cut) + ".pdf")
  # plt.show()
  plt.clf()



def plot_fractional_energy_loss(pT_lower_cut=100, pT_upper_cut=20000):
  properties = parse_file(input_analysis_file, pT_lower_cut=pT_lower_cut, pT_upper_cut=pT_upper_cut)

  fractional_energy_loss = properties['fractional_energy_loss']
  prescales = properties['prescales']

  log_fractional_energy_loss = np.log(fractional_energy_loss)
  bins_linear_log = np.linspace(math.log(0.005, math.e), math.log(0.5, math.e), 150)

  fractional_energy_loss_hist = Hist(bins_linear_log, title='Fractional Jet Energy Loss', markersize=3.0, color='black')
  bin_width_before = (fractional_energy_loss_hist.upperbound() - fractional_energy_loss_hist.lowerbound()) / fractional_energy_loss_hist.nbins()

  map(fractional_energy_loss_hist.Fill, log_fractional_energy_loss, prescales)
 
  fractional_energy_loss_hist.Scale(1.0 / (fractional_energy_loss_hist.GetSumOfWeights() * bin_width_before))

  rplt.errorbar(fractional_energy_loss_hist, emptybins=False, marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5)

  # Legends Begin.

  legend = plt.gca().legend(loc=1, frameon=0, fontsize=60)
  plt.gca().add_artist(legend)

  extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
  if pT_upper_cut != 20000:
    labels = [r"$ \textrm{Anti--}k_{t}\textrm{:}~R = 0.5;\eta<2.4$", r"$p_{T}\in[" + str(pT_lower_cut) + ", " + str(pT_upper_cut) + "]~\mathrm{GeV}$", r"$ \textrm{Soft~Drop:}~\boldsymbol{\beta = 0;~z_{\mathrm{cut}} = 0.05}$"]
  else:
    labels = [r"$ \textrm{Anti--}k_{t}\textrm{:}~R = 0.5;\eta<2.4$", r"$p_{T} > " + str(pT_lower_cut) + "~\mathrm{GeV}$", r"$ \textrm{Soft~Drop:}~\boldsymbol{\beta = 0;~z_{\mathrm{cut}} = 0.05}$"]
  plt.gca().legend([extra, extra, extra], labels, loc=7, frameon=0, borderpad=0.1, fontsize=60, bbox_to_anchor=[0.93, 0.75])

  # Legends End.

  ab = AnnotationBbox(OffsetImage(read_png(get_sample_data("/home/aashish/root-6.04.06/macros/MODAnalyzer/mod_logo.png", asfileobj=False)), zoom=0.15, resample=1, dpi_cor=1), (0.23, 0.895), xycoords='figure fraction', frameon=0)
  plt.gca().add_artist(ab)
  preliminary_text = "Prelim. (20\%)"
  plt.gcf().text(0.29, 0.885, preliminary_text, fontsize=50, weight='bold', color='#444444', multialignment='center')

  plt.xlabel('Fractional Energy Loss', fontsize=75)
  plt.ylabel('$\mathrm{A.U.}$', fontsize=75, rotation=0, labelpad=75.)
  
  plt.gcf().set_size_inches(30, 21.4285714, forward=1)

  plt.gca().autoscale(True)
  plt.gca().set_ylim(0., plt.gca().get_ylim()[1] * 1.5)

  x = np.linspace(math.log(0.005, math.e), math.log(0.5, math.e), 5)
  labels = [str(round(math.exp(i), 2)) for i in x]
  plt.xticks(x, labels)


  # plt.gca().xaxis.set_minor_locator(MultipleLocator(0.01))
  plt.gca().yaxis.set_minor_locator(MultipleLocator(2))
  plt.tick_params(which='major', width=5, length=25, labelsize=70)
  plt.tick_params(which='minor', width=3, length=15)

  plt.tight_layout(pad=1.08, h_pad=1.08, w_pad=1.08)

  print "Printing fractional energy loss with pT > " + str(pT_lower_cut) + " and pT < " + str(pT_upper_cut)

  plt.savefig("plots/" + get_version(input_analysis_file) + "/fractional_energy_loss/pT_lower_" + str(pT_lower_cut) + "_pT_upper_" + str(pT_upper_cut) + ".pdf")
  # plt.show()
  plt.clf()







def plot_charged_jet_mass_spectrum(pT_lower_cut=100, pT_upper_cut=20000):
  properties = parse_file(input_analysis_file, pT_lower_cut=pT_lower_cut, pT_upper_cut=pT_upper_cut)

  jet_mass_before_SD = properties['charged_jet_mass_before_SD']
  jet_mass_after_SD = properties['charged_jet_mass_after_SD']  
  prescales = properties['prescales']


  jet_mass_before_SD_hist = Hist(150, 0, 150, title='Before SoftDrop (Charged Jets)', markersize=3.0, color='black')
  bin_width_before = (jet_mass_before_SD_hist.upperbound() - jet_mass_before_SD_hist.lowerbound()) / jet_mass_before_SD_hist.nbins()

  jet_mass_after_SD_hist = Hist(150, 0, 150, title='After SoftDrop (Charged Jets)', markersize=3.0, color='red')
  bin_width_after = (jet_mass_after_SD_hist.upperbound() - jet_mass_after_SD_hist.lowerbound()) / jet_mass_after_SD_hist.nbins()

  map(jet_mass_before_SD_hist.Fill, jet_mass_before_SD, prescales)
  map(jet_mass_after_SD_hist.Fill, jet_mass_after_SD, prescales)
  
  jet_mass_before_SD_hist.Scale(1.0 / (jet_mass_before_SD_hist.GetSumOfWeights() * bin_width_before))
  jet_mass_after_SD_hist.Scale(1.0 / (jet_mass_after_SD_hist.GetSumOfWeights() * bin_width_after))
  
  rplt.errorbar(jet_mass_before_SD_hist, emptybins=False, marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5)
  rplt.errorbar(jet_mass_after_SD_hist, emptybins=False, marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5)

  # Legends Begin.

  legend = plt.gca().legend(loc=1, frameon=0, fontsize=60, bbox_to_anchor=[1.0, 1.0])
  plt.gca().add_artist(legend)

  extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
  
  if pT_upper_cut != 20000:
    labels = [r"$ \textrm{Anti--}k_{t}\textrm{:}~R = 0.5;\eta<2.4$", r"$p_{T}\in[" + str(pT_lower_cut) + ", " + str(pT_upper_cut) + "]~\mathrm{GeV}$", r"$ \textrm{Soft~Drop:}~\boldsymbol{\beta = 0;~z_{\mathrm{cut}} = 0.05}$"]
  else:
    labels = [r"$ \textrm{Anti--}k_{t}\textrm{:}~R = 0.5;\eta<2.4$", r"$p_{T} > " + str(pT_lower_cut) + "~\mathrm{GeV}$", r"$ \textrm{Soft~Drop:}~\boldsymbol{\beta = 0;~z_{\mathrm{cut}} = 0.05}$", r"$ \textrm{Soft~Drop:}~\boldsymbol{\beta = 0;~z_{\mathrm{cut}} = 0.05}$"]
  

  plt.gca().legend([extra, extra, extra], labels, loc=7, frameon=0, borderpad=0.1, fontsize=60, bbox_to_anchor=[0.86, 0.69])

  # # Legends End.

  ab = AnnotationBbox(OffsetImage(read_png(get_sample_data("/home/aashish/root-6.04.06/macros/MODAnalyzer/mod_logo.png", asfileobj=False)), zoom=0.15, resample=1, dpi_cor=1), (0.23, 0.895), xycoords='figure fraction', frameon=0)
  plt.gca().add_artist(ab)
  preliminary_text = "Prelim. (20\%)"
  plt.gcf().text(0.29, 0.885, preliminary_text, fontsize=50, weight='bold', color='#444444', multialignment='center')

  plt.gcf().set_size_inches(30, 21.4285714, forward=1)

  plt.xlabel('Jet Mass', fontsize=75)
  plt.ylabel('$\mathrm{A.U.}$', fontsize=75, rotation=0, labelpad=80.)
  
  plt.gcf().set_size_inches(30, 21.4285714, forward=1)

  plt.gca().xaxis.set_minor_locator(MultipleLocator(5))
  plt.gca().yaxis.set_minor_locator(MultipleLocator(0.005))
  plt.tick_params(which='major', width=5, length=25, labelsize=70)
  plt.tick_params(which='minor', width=3, length=15)

  plt.gca().autoscale(True)
  plt.gca().set_ylim(0., plt.gca().get_ylim()[1] * 1.2)

  plt.tight_layout(pad=1.08, h_pad=1.08, w_pad=1.08)

  print "Printing charged jet mass spectrum with pT > " + str(pT_lower_cut) + " and pT < " + str(pT_upper_cut)

  plt.savefig("plots/" + get_version(input_analysis_file) + "/charged_jet_mass_spectrum/pT_lower_" + str(pT_lower_cut) + "_pT_upper_" + str(pT_upper_cut) + ".pdf")
  # plt.show()
  plt.clf()





def plot_jet_mass_spectrum(pT_lower_cut=100, pT_upper_cut=20000):
  properties = parse_file(input_analysis_file, pT_lower_cut=pT_lower_cut, pT_upper_cut=pT_upper_cut, jet_quality_level=1)

  jet_mass_before_SD = properties['jet_mass_before_SD']
  jet_mass_after_SD = properties['jet_mass_after_SD']  
  prescales = properties['prescales']

  jet_mass_before_SD_hist = Hist(150, 0, 150, title='Before SoftDrop', markersize=3.0, color='black')
  bin_width_before = (jet_mass_before_SD_hist.upperbound() - jet_mass_before_SD_hist.lowerbound()) / jet_mass_before_SD_hist.nbins()

  jet_mass_after_SD_hist = Hist(150, 0, 150, title='After SoftDrop', markersize=3.0, color='red')
  bin_width_after = (jet_mass_after_SD_hist.upperbound() - jet_mass_after_SD_hist.lowerbound()) / jet_mass_after_SD_hist.nbins()

  map(jet_mass_before_SD_hist.Fill, jet_mass_before_SD, prescales)
  map(jet_mass_after_SD_hist.Fill, jet_mass_after_SD, prescales)
  
  jet_mass_before_SD_hist.Scale(1.0 / (jet_mass_before_SD_hist.GetSumOfWeights() * bin_width_before))
  jet_mass_after_SD_hist.Scale(1.0 / (jet_mass_after_SD_hist.GetSumOfWeights() * bin_width_after))
  
  rplt.errorbar(jet_mass_before_SD_hist, emptybins=False, marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5)
  rplt.errorbar(jet_mass_after_SD_hist, emptybins=False, marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5)

  # Legends Begin.

  legend = plt.gca().legend(loc=1, frameon=0, fontsize=60, bbox_to_anchor=[0.89, 1.0])
  plt.gca().add_artist(legend)

  extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
  
  if pT_upper_cut != 20000:
    labels = [r"$ \textrm{Anti--}k_{t}\textrm{:}~R = 0.5;\eta<2.4$", r"$p_{T}\in[" + str(pT_lower_cut) + ", " + str(pT_upper_cut) + "]~\mathrm{GeV}$", r"$ \textrm{Soft~Drop:}~\boldsymbol{\beta = 0;~z_{\mathrm{cut}} = 0.05}$"]
  else:
    labels = [r"$ \textrm{Anti--}k_{t}\textrm{:}~R = 0.5;\eta<2.4$", r"$p_{T} > " + str(pT_lower_cut) + "~\mathrm{GeV}$", r"$ \textrm{Soft~Drop:}~\boldsymbol{\beta = 0;~z_{\mathrm{cut}} = 0.05}$", r"$ \textrm{Soft~Drop:}~\boldsymbol{\beta = 0;~z_{\mathrm{cut}} = 0.05}$"]
  

  plt.gca().legend([extra, extra, extra], labels, loc=7, frameon=0, borderpad=0.1, fontsize=60, bbox_to_anchor=[0.99, 0.69])

  # # Legends End.

  ab = AnnotationBbox(OffsetImage(read_png(get_sample_data("/home/aashish/root-6.04.06/macros/MODAnalyzer/mod_logo.png", asfileobj=False)), zoom=0.15, resample=1, dpi_cor=1), (0.23, 0.895), xycoords='figure fraction', frameon=0)
  plt.gca().add_artist(ab)
  preliminary_text = "Prelim. (20\%)"
  plt.gcf().text(0.29, 0.885, preliminary_text, fontsize=50, weight='bold', color='#444444', multialignment='center')

  plt.gcf().set_size_inches(30, 21.4285714, forward=1)

  plt.xlabel('Jet Mass', fontsize=75)
  plt.ylabel('$\mathrm{A.U.}$', fontsize=75, rotation=0, labelpad=80.)
  
  plt.gcf().set_size_inches(30, 21.4285714, forward=1)

  plt.gca().xaxis.set_minor_locator(MultipleLocator(5))
  plt.gca().yaxis.set_minor_locator(MultipleLocator(0.005))
  plt.tick_params(which='major', width=5, length=25, labelsize=70)
  plt.tick_params(which='minor', width=3, length=15)

  plt.gca().autoscale(True)
  plt.gca().set_ylim(0., plt.gca().get_ylim()[1])

  plt.tight_layout(pad=1.08, h_pad=1.08, w_pad=1.08)

  print "Printing jet mass spectrum with pT > " + str(pT_lower_cut) + " and pT < " + str(pT_upper_cut)

  plt.savefig("plots/" + get_version(input_analysis_file) + "/jet_mass_spectrum/pT_lower_" + str(pT_lower_cut) + "_pT_upper_" + str(pT_upper_cut) + ".pdf")
  # plt.show()
  plt.clf()







def plot_log_jet_mass_spectrum(pT_lower_cut=100, pT_upper_cut=20000):


  properties = parse_file(input_analysis_file, pT_lower_cut=pT_lower_cut, pT_upper_cut=pT_upper_cut, jet_quality_level=1)

  prescales = properties['prescales']

  m_zg_10 = properties['m_zg_10']
  m_zg_11 = properties['m_zg_11']
  m_zg_12 = properties['m_zg_12']
  m_zg_13 = properties['m_zg_13']
  m_zg_14 = properties['m_zg_14']
  m_zg_15 = properties['m_zg_15']


  bins_linear_log = np.linspace(math.log(0.1, math.e), math.log(150, math.e), 30)


  m_zg_10_hist = Hist(bins_linear_log, title='$z_g = 0.10$', markersize=3.0, color='green')
  bin_width_m_zg_10 = (m_zg_10_hist.upperbound() - m_zg_10_hist.lowerbound()) / m_zg_10_hist.nbins()
  map(m_zg_10_hist.Fill, 2*np.log(m_zg_10), prescales)
  m_zg_10_hist.Scale(1.0 / (m_zg_10_hist.GetSumOfWeights() * bin_width_m_zg_10))
  rplt.errorbar(m_zg_10_hist, emptybins=False, marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5)

  m_zg_11_hist = Hist(bins_linear_log, title='$z_g = 0.11$', markersize=3.0, color='red')
  bin_width_m_zg_11 = (m_zg_11_hist.upperbound() - m_zg_11_hist.lowerbound()) / m_zg_11_hist.nbins()
  map(m_zg_11_hist.Fill, 2*np.log(m_zg_11), prescales)
  m_zg_11_hist.Scale(1.0 / (m_zg_11_hist.GetSumOfWeights() * bin_width_m_zg_11))
  rplt.errorbar(m_zg_11_hist, emptybins=False, marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5)

  m_zg_12_hist = Hist(bins_linear_log, title='$z_g = 0.12$', markersize=3.0, color='blue')
  bin_width_m_zg_12 = (m_zg_12_hist.upperbound() - m_zg_12_hist.lowerbound()) / m_zg_12_hist.nbins()
  map(m_zg_12_hist.Fill, 2*np.log(m_zg_12), prescales)
  m_zg_12_hist.Scale(1.0 / (m_zg_12_hist.GetSumOfWeights() * bin_width_m_zg_12))
  rplt.errorbar(m_zg_12_hist, emptybins=False, marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5)

  m_zg_13_hist = Hist(bins_linear_log, title='$z_g = 0.13$', markersize=3.0, color='purple')
  bin_width_m_zg_13 = (m_zg_13_hist.upperbound() - m_zg_13_hist.lowerbound()) / m_zg_13_hist.nbins()
  map(m_zg_13_hist.Fill, 2*np.log(m_zg_13), prescales)
  m_zg_13_hist.Scale(1.0 / (m_zg_13_hist.GetSumOfWeights() * bin_width_m_zg_13))
  rplt.errorbar(m_zg_13_hist, emptybins=False, marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5)

  m_zg_14_hist = Hist(bins_linear_log, title='$z_g = 0.14$', markersize=3.0, color='black')
  bin_width_m_zg_14 = (m_zg_14_hist.upperbound() - m_zg_14_hist.lowerbound()) / m_zg_14_hist.nbins()
  map(m_zg_14_hist.Fill, 2*np.log(m_zg_14), prescales)
  m_zg_14_hist.Scale(1.0 / (m_zg_14_hist.GetSumOfWeights() * bin_width_m_zg_14))
  rplt.errorbar(m_zg_14_hist, emptybins=False, marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5)

  m_zg_15_hist = Hist(bins_linear_log, title='$z_g = 0.15$', markersize=3.0, color='orange')
  bin_width_m_zg_15 = (m_zg_15_hist.upperbound() - m_zg_15_hist.lowerbound()) / m_zg_15_hist.nbins()
  map(m_zg_15_hist.Fill, 2*np.log(m_zg_15), prescales)
  m_zg_15_hist.Scale(1.0 / (m_zg_15_hist.GetSumOfWeights() * bin_width_m_zg_15))
  rplt.errorbar(m_zg_15_hist, emptybins=False, marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5)

  # Legends Begin.

  legend = plt.gca().legend(loc=1, frameon=0, fontsize=60, bbox_to_anchor=[0.89, 1.0])
  plt.gca().add_artist(legend)

  # extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
  
  # if pT_upper_cut != 20000:
    # labels = [r"$ \textrm{Anti--}k_{t}\textrm{:}~R = 0.5;\eta<2.4$", r"$p_{T}\in[" + str(pT_lower_cut) + ", " + str(pT_upper_cut) + "]~\mathrm{GeV}$", r"$ \textrm{Soft~Drop:}~\boldsymbol{\beta = 0;~z_{\mathrm{cut}} = 0.05}$"]
  # else:
    # labels = [r"$ \textrm{Anti--}k_{t}\textrm{:}~R = 0.5;\eta<2.4$", r"$p_{T} > " + str(pT_lower_cut) + "~\mathrm{GeV}$", r"$ \textrm{Soft~Drop:}~\boldsymbol{\beta = 0;~z_{\mathrm{cut}} = 0.05}$", r"$ \textrm{Soft~Drop:}~\boldsymbol{\beta = 0;~z_{\mathrm{cut}} = 0.05}$"]
  

  # plt.gca().legend([extra, extra, extra], labels, loc=7, frameon=0, borderpad=0.1, fontsize=60, bbox_to_anchor=[0.99, 0.69])

  # # # Legends End.

  ab = AnnotationBbox(OffsetImage(read_png(get_sample_data("/home/aashish/root-6.04.06/macros/MODAnalyzer/mod_logo.png", asfileobj=False)), zoom=0.15, resample=1, dpi_cor=1), (0.23, 0.895), xycoords='figure fraction', frameon=0)
  plt.gca().add_artist(ab)
  preliminary_text = "Prelim. (20\%)"
  plt.gcf().text(0.29, 0.885, preliminary_text, fontsize=50, weight='bold', color='#444444', multialignment='center')


  plt.xlabel('$2 \\log{m}$', fontsize=75)
  plt.ylabel('$\mathrm{A.U.}$', fontsize=75, rotation=0, labelpad=80.)
  
  plt.gcf().set_size_inches(30, 21.4285714, forward=1)

  plt.gca().xaxis.set_minor_locator(MultipleLocator(0.25))
  plt.gca().yaxis.set_minor_locator(MultipleLocator(0.05))
  plt.tick_params(which='major', width=5, length=25, labelsize=70)
  plt.tick_params(which='minor', width=3, length=15)

  plt.gca().autoscale(True)
  plt.gca().set_ylim(0., plt.gca().get_ylim()[1]*1.5)

  plt.tight_layout(pad=1.08, h_pad=1.08, w_pad=1.08)

  print "Printing log jet mass spectrum with pT > " + str(pT_lower_cut) + " and pT < " + str(pT_upper_cut)

  plt.savefig("plots/" + get_version(input_analysis_file) + "/log_jet_mass_spectrum/pT_lower_" + str(pT_lower_cut) + "_pT_upper_" + str(pT_upper_cut) + ".pdf")
  # plt.show()
  plt.clf()



def plot_zg():
  properties = parse_file(input_analysis_file, 150)

  zgs = properties['zg_05'] 
  prescales = properties['prescales']



  # plt.gca().set_xscale('log')

  n_bins = 100

  b, a = log_bins(zgs, prescales, n_bins)

  plt.hist(a[:-1], weights=b, bins=n_bins, normed=1)

  plt.show()




def logged_bin(data, weights, number_of_bins=50):
  
  def drop_zeros(a_list):
    return [i for i in a_list if i > 0]

  # min_value = min( drop_zeros(data) )
  # max_value = max(data)

  min_value = math.log( min( drop_zeros(data) ), 10 )
  max_value = math.log( max(data), 10 )

  return np.histogram(data, weights=weights, bins=np.logspace(min_value, max_value, number_of_bins))
  # return np.histogram(data, weights=weights, bins=np.linspace(min_value, max_value, number_of_bins))



def linear_bin(data, weights, number_of_bins=50):
  
  def drop_zeros(a_list):
    return [i for i in a_list if i > 0]

  min_value = min( drop_zeros(data) )
  max_value = max(data)

  return np.histogram(data, weights=weights, bins=np.linspace(min_value, max_value, number_of_bins))




def test():

  n_bins = 50

  # x = np.arange(5, 10, 0.0001)
  x = np.linspace(0, 2, 10000)
  # y = np.reciprocal(x)

  # x = np.log(x)

  # hist, bins = logged_bin(x, y, 25)
  # hist, bins = linear_bin(x, y, n_bins)

  bins = [0, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.96, 0.97, 0.98, 0.99, 1, 2]

  # hist, bins = np.histogram(x, bins=bins, density=True)


  # plt.hist(bins[:-1], weights=hist)

  plt.hist(x, bins=bins, normed=1)


  # plt.hist(bins[:-1], weights=hist, bins=n_bins, color='orange', alpha=0.75, lw=5)
  # plt.errorbar(bins[:-1], hist, lw=0, xerr=True, yerr=True, elinewidth=3, capsize=5, marker="o", markersize=5)


  # plt.gca().set_xscale('log')

  # plt.ylim(0, 8)

  plt.autoscale()

  plt.show()


# test()

def plot_zg_test():
  properties = parse_file(input_analysis_file, 150)

  zgs = properties['zg_02']
  prescales = properties['prescales']

  x = zgs
  y = prescales

  hist, bins = logged_bin(x, y, 25)

  width = 0.7 * (bins[1] - bins[0])
  center = (bins[:-1] + bins[1:]) / 2
  # plt.bar(center, hist, align='center', width=width)

  plt.hist(bins[:-1], weights=hist, color='orange', alpha=0.75, lw=5, bins=200)
  
  # plt.gca().set_xscale('log')

  plt.autoscale()

  plt.show()


def extrap1d(interpolator):
    xs = interpolator.x
    ys = interpolator.y

    def pointwise(x):
        if x < xs[0]:
            return ys[0]+(x-xs[0])*(ys[1]-ys[0])/(xs[1]-xs[0])
        elif x > xs[-1]:
            return ys[-1]+(x-xs[-1])*(ys[-1]-ys[-2])/(xs[-1]-xs[-2])
        else:
            return interpolator(x)

    def ufunclike(xs):
        return array(map(pointwise, array(xs)))

    return ufunclike


def plot_log_zg_th_mc_data(pT_lower_cut, pT_upper_cut, zg_cut, zg_filename, ratio_denominator="theory", data=True, mc=True, theory=True, n_bins=10, y_max_limit=20, y_limit_ratio_plot=0.5):

  zg_cut = float(zg_cut)

  properties = parse_file(input_analysis_file, pT_lower_cut, pT_upper_cut)
  properties_pythia = parse_mc_file("/home/aashish/Dropbox (MIT)/Research/CMSOpenData/Andrew/fastjet_sudakov_safe_pythia_pp2jj_" + str(pT_lower_cut) + "pTcut_7TeV.dat", pT_lower_cut, pT_upper_cut)
  properties_herwig = parse_mc_file("/home/aashish/Dropbox (MIT)/Research/CMSOpenData/Andrew/fastjet_sudakov_safe_herwig_pp2jj_" + str(pT_lower_cut) + "pTcut_7TeV.dat", pT_lower_cut, pT_upper_cut)

  zg_data = properties[zg_filename]
  
  zg_pythias = properties_pythia[zg_filename]
  zg_herwigs = properties_herwig[zg_filename]

  prescales = properties['prescales']

  data_label = "CMS 2010 Open Data"
  pythia_label = "Pythia 8.205" if mc else ""
  herwig_label = "Herwig++ 2.6.3" if mc else ""
  theory_label = "Theory (MLL)" if theory else ""
  
  gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1]) 

  ax0 = plt.subplot(gs[0])
  ax1 = plt.subplot(gs[1])

  def pyplot_hist_to_plot(x, y):
    a = []
    b = []
    for i in range(0, len(x[:-1])):
      # if y[i] != 0 or math.exp(x[i]) >= 0.5:
      # if y[i] != 0:
      if True:
        a.append(x[i])
        b.append(y[i])

    return a, b

  # Theory Plots Begin.
  
  points_th_gluon = parse_theory_file("/home/aashish/Dropbox (MIT)/Research/CMSOpenData/Simone/results_7_24_15/band_gluon_pt" + str(pT_lower_cut) + "_zc" + str(zg_cut).replace(".", "") + ".dat")
  points_th_quark = parse_theory_file("/home/aashish/Dropbox (MIT)/Research/CMSOpenData/Simone/results_7_24_15/band_quark_pt" + str(pT_lower_cut) + "_zc" + str(zg_cut).replace(".", "") + ".dat")

  points = defaultdict(list)

  for x in points_th_gluon:
    points[x] = [ points_th_gluon[x][0], points_th_gluon[x][1], points_th_gluon[x][2], points_th_gluon[x][3], points_th_gluon[x][4], points_th_gluon[x][5] ]
    points[x].extend([ points_th_quark[x][0], points_th_quark[x][1], points_th_quark[x][2], points_th_quark[x][3], points_th_quark[x][4], points_th_quark[x][5] ])

  keys = points.keys()
  keys.sort()

  theory_x = keys
  bins_linear_log = np.linspace(math.log(zg_cut, math.e), math.log(0.5, math.e), n_bins * 5)
  log_theory_x = np.log(theory_x)

  y = []
  for j in range(0, 6):
    y.append([points[i][j] for i in keys])

  # For each x, record three y's viz. max_y, min_y, line_y (i.e. e11 xmu=1).
  weighted_ys = []
  for i in range(0, len(y)):
    area = simps(y[i], theory_x)
    weighted = []
    for j in range(0, len(y[i])):
      weighted.append( y[i][j] / area )    
    weighted_ys.append(weighted)

  # y = weighted_ys

  theory_y_max = []
  theory_y_min = []
  theory_y_line = []
  
  for i in range(0, len(theory_x)):
    y_for_current_x = []
    for j in range(0, 6):
      y_for_current_x.append(y[j][i])

    theory_y_min.append(theory_x[i] * min(y_for_current_x))
    theory_y_line.append(theory_x[i] * y_for_current_x[1])
    theory_y_max.append(theory_x[i] * max(y_for_current_x))
  

  if theory:

    ax0.plot(log_theory_x, theory_y_max, label=theory_label, lw=0, color='red')
    ax0.plot(log_theory_x, theory_y_line, label=theory_label, lw=5, color='red')
    ax0.plot(log_theory_x, theory_y_min, label=theory_label, lw=0, color='red')

    ax0.fill_between(log_theory_x, theory_y_max, theory_y_min, norm=1, where=np.less_equal(theory_y_min, theory_y_max), facecolor='red', interpolate=True, alpha=0.3, linewidth=0.0)
  

  # Theory Plot Ends.  

  def convert_hist_to_line_plot(hist, n_bins):
    a = []
    b = {}
    # bin_width = 0.6 / (6 * n_bins)
    bin_width = (hist.upperbound() - hist.lowerbound()) / hist.nbins()

    for i in range(0, len(list(hist.x()))):
      a.append(round(list(hist.x())[i] - bin_width / 2., 4))
      a.append(round(list(hist.x())[i], 4))
      a.append(round(list(hist.x())[i] + bin_width / 2., 4))

      if round(list(hist.x())[i] - bin_width / 2., 4) not in b.keys():
        b[round(list(hist.x())[i] - bin_width / 2., 4)] = [ list(hist.y())[i] ]
      else:
        b[round(list(hist.x())[i] - bin_width / 2., 4)].append( list(hist.y())[i] )
      
      if round(list(hist.x())[i], 4) not in b.keys():
        b[round(list(hist.x())[i], 4)] = [ list(hist.y())[i] ]
      else:
        b[round(list(hist.x())[i], 4)].append( list(hist.y())[i] )

      if round(list(hist.x())[i] + bin_width / 2., 4) not in b.keys():
        b[round(list(hist.x())[i] + bin_width / 2., 4)] = [ list(hist.y())[i] ]
      else:
        b[round(list(hist.x())[i] + bin_width / 2., 4)].append( list(hist.y())[i] )

    x = sorted(list(Set(a)))
    a.sort()
    
    c = [b[x[i]] for i in range(0, len(x))]

    y = [item for sublist in c for item in sublist]
    
    a_zero_removed = []
    y_zero_removed = []
    for i in range(0, len(a)):
      if round(float(a[i]), 4) >= round(math.log(zg_cut, math.e), 4) and round(float(a[i]), 4) <= round(math.log(0.5, math.e), 4):
        a_zero_removed.append(a[i])
        y_zero_removed.append(y[i])

    return a_zero_removed, y_zero_removed

  # Data Plot Begins.
  log_zg_data = np.log(zg_data)

  zg_data_hist = Hist(bins_linear_log, title=data_label, markersize=2.5, color='black')
  bin_width_data = (zg_data_hist.upperbound() - zg_data_hist.lowerbound()) / zg_data_hist.nbins()
  map(zg_data_hist.Fill, log_zg_data, prescales)
  zg_data_hist.Scale(1.0 / ( zg_data_hist.GetSumOfWeights() * bin_width_data ))


  if data:
    data_plot = rplt.errorbar(zg_data_hist, xerr=1, yerr=1, emptybins=False, axes=ax0, ls='None', marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5, alpha=1.0)
  else:
    data_plot = rplt.errorbar(zg_data_hist, xerr=1, yerr=1, emptybins=False, axes=ax0, ls='None', marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5, alpha=0.0)
  


  data_x_errors, data_y_errors = [], []
  for x_segment in data_plot[2][0].get_segments():
    data_x_errors.append((x_segment[1][0] - x_segment[0][0]) / 2.)
  for y_segment in data_plot[2][1].get_segments():
    data_y_errors.append((y_segment[1][1] - y_segment[0][1]) / 2.)

  data_points_x = data_plot[0].get_xdata()
  data_points_y = data_plot[0].get_ydata()

  data_plot_points_x = []
  data_plot_points_y = []

  for i in range(0, len(data_points_x)):
    if (float(data_points_x[i]) >= float(math.log(zg_cut, math.e))):
      data_plot_points_x.append(data_points_x[i])
      data_plot_points_y.append(data_points_y[i])


  theory_min_interpolate_function = extrap1d(interpolate.interp1d(log_theory_x, theory_y_min))
  theory_line_interpolate_function = extrap1d(interpolate.interp1d(log_theory_x, theory_y_line))
  theory_max_interpolate_function = extrap1d(interpolate.interp1d(log_theory_x, theory_y_max))

  theory_extrapolated_min = theory_min_interpolate_function(data_plot_points_x)
  theory_extrapolated_line = theory_line_interpolate_function(data_plot_points_x)
  theory_extrapolated_max = theory_max_interpolate_function(data_plot_points_x)



  # Data Plots Ends.



  # Simulation Plots Begin. 
  
  # Pythia.
  log_zg_pythias = np.log(zg_pythias)
  y, x = np.histogram(log_zg_pythias, bins=bins_linear_log, normed=True)
  a, b = pyplot_hist_to_plot(x, y)
  log_zg_pythia_hist = Hist(bins_linear_log)
  map(log_zg_pythia_hist.Fill, a, b)
  pythia_line_plot = convert_hist_to_line_plot(log_zg_pythia_hist, len(bins_linear_log))

  if mc:
    pythia_plot = ax0.plot(pythia_line_plot[0], pythia_line_plot[1], label=pythia_label, color='blue', lw=5)
    # pythia_plot = ax0.hist(a, histtype='step', normed=True, weights=b, bins=44, label=pythia_label, lw=5, color='blue')
  else:
    pythia_plot = ax0.plot(pythia_line_plot[0], pythia_line_plot[1], label=pythia_label, color='blue', lw=0)
    # pythia_plot = ax0.hist(a, histtype='step', normed=True, weights=b, bins=44, label=pythia_label, lw=0, color='blue')

  # Pythia Ends.
  
  # Herwig. 
  log_zg_herwigs = np.log(zg_herwigs)
  y, x = np.histogram(log_zg_herwigs, bins=bins_linear_log, normed=True)
  a, b = pyplot_hist_to_plot(x, y)
  log_zg_herwig_hist = Hist(bins_linear_log)
  map(log_zg_herwig_hist.Fill, a, b)
  herwig_line_plot = convert_hist_to_line_plot(log_zg_herwig_hist, len(bins_linear_log))

  if mc:
    herwig_plot = ax0.plot(herwig_line_plot[0], herwig_line_plot[1], color='green', lw=5)
    # herwig_plot = ax0.hist(a, histtype='step', normed=True, weights=b, bins=44, label=herwig_label, lw=5, color='green')
  else:
    herwig_plot = ax0.plot(herwig_line_plot[0], herwig_line_plot[1], lw=0)
    # herwig_plot = ax0.hist(a, histtype='step', normed=True, weights=b, bins=44, label=herwig_label, lw=0, color='green')
  

  # Herwig Ends.

  # Simulation Plots End.




  # Ratio-Over Plot Begins.

  # Theory-Over-Data Plot.
  



  

  if ratio_denominator == "data":

    if mc:
      log_zg_herwig_hist.Divide(zg_data_hist)
      zg_herwig_line_plot = convert_hist_to_line_plot(log_zg_herwig_hist, len(bins_linear_log))
      plt.plot(zg_herwig_line_plot[0], zg_herwig_line_plot[1], linewidth=5, color='green')

      log_zg_pythia_hist.Divide(zg_data_hist)
      zg_pythia_line_plot = convert_hist_to_line_plot(log_zg_pythia_hist, n_bins)
      plt.plot(zg_pythia_line_plot[0], zg_pythia_line_plot[1], linewidth=5, color='blue')

    if data:
      ratio_data_to_data = [None if n == 0 else m / n for m, n in zip(data_plot_points_y, data_plot_points_y)]
      data_to_data_y_err = [(b / m) for b, m in zip(data_y_errors, data_plot_points_y)]
      data_to_data_x_err = [(b / m) for b, m in zip(data_x_errors, [1] * len(data_plot_points_y))]
      
      plt.errorbar(data_plot_points_x, ratio_data_to_data, xerr=data_to_data_x_err, yerr=data_to_data_y_err, ls='None', marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5, color='black')

    if theory:
      ratio_theory_line_to_data = [m / n for m, n in zip(theory_extrapolated_line, data_plot_points_y)]
      ratio_theory_min_to_data = [m / n for m, n in zip(theory_extrapolated_min, data_plot_points_y)]
      ratio_theory_max_to_data = [m / n for m, n in zip(theory_extrapolated_max, data_plot_points_y)]


      zg_theory_line_to_data_hist = Hist(bins_linear_log)
      map(zg_theory_line_to_data_hist.Fill, data_plot_points_x, ratio_theory_line_to_data)
      zg_theory_line_to_data_plot = convert_hist_to_line_plot(zg_theory_line_to_data_hist, n_bins)
      plt.plot(zg_theory_line_to_data_plot[0], zg_theory_line_to_data_plot[1], linewidth=5, color='red')

      zg_theory_min_to_data_hist = Hist(bins_linear_log)
      map(zg_theory_min_to_data_hist.Fill, data_plot_points_x, ratio_theory_min_to_data)
      zg_theory_min_to_data_plot = convert_hist_to_line_plot(zg_theory_min_to_data_hist, n_bins)
      plt.plot(zg_theory_min_to_data_plot[0], zg_theory_min_to_data_plot[1], linewidth=0, color='orange')

      zg_theory_max_to_data_hist = Hist(bins_linear_log)
      map(zg_theory_max_to_data_hist.Fill, data_plot_points_x, ratio_theory_max_to_data)
      zg_theory_max_to_data_plot = convert_hist_to_line_plot(zg_theory_max_to_data_hist, n_bins)
      plt.plot(zg_theory_max_to_data_plot[0], zg_theory_max_to_data_plot[1], linewidth=0, color='magenta')

      ax1.fill_between(zg_theory_max_to_data_plot[0], zg_theory_max_to_data_plot[1], zg_theory_min_to_data_plot[1], where=np.less_equal(zg_theory_min_to_data_plot[1], zg_theory_max_to_data_plot[1]), facecolor='red', interpolate=True, alpha=0.3, linewidth=0.0)
  
  elif ratio_denominator == "theory":

    zg_theory_line_hist = Hist(bins_linear_log, color='red')
    map(zg_theory_line_hist.Fill, data_plot_points_x, theory_extrapolated_line)

    zg_theory_min_hist = Hist(bins_linear_log, color='pink')
    map(zg_theory_min_hist.Fill, data_plot_points_x, theory_extrapolated_min)

    zg_theory_max_hist = Hist(bins_linear_log, color='red')
    map(zg_theory_max_hist.Fill, data_plot_points_x, theory_extrapolated_max)

  
    if mc:
      log_zg_herwig_hist.Divide(zg_theory_line_hist)
      zg_herwig_line_plot = convert_hist_to_line_plot(log_zg_herwig_hist, n_bins)
      plt.plot(zg_herwig_line_plot[0], zg_herwig_line_plot[1], linewidth=5, color='green')

      log_zg_pythia_hist.Divide(zg_theory_line_hist)
      zg_pythia_line_plot = convert_hist_to_line_plot(log_zg_pythia_hist, n_bins)
      plt.plot(zg_pythia_line_plot[0], zg_pythia_line_plot[1], linewidth=5, color='blue')


    if data:
      zg_data_to_th_y = [b / m for b, m in zip(data_plot_points_y, theory_extrapolated_line)]
      zg_data_to_th_y_err = [b / m for b, m in zip(data_y_errors, theory_extrapolated_line)]
      data_to_th_x_err = [(b / m) for b, m in zip(data_x_errors, [1] * len(zg_data_to_th_y_err))]

      plt.errorbar(data_plot_points_x, zg_data_to_th_y, xerr=data_to_th_x_err, yerr=zg_data_to_th_y_err, ls='None', marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5, color='black')
  

    if theory:
      
      zg_theory_min_hist.Divide(zg_theory_line_hist)
      zg_theory_max_hist.Divide(zg_theory_line_hist)

      zg_theory_min_plot = convert_hist_to_line_plot(zg_theory_min_hist, n_bins)
      zg_theory_max_plot = convert_hist_to_line_plot(zg_theory_max_hist, n_bins)

      zg_theory_min_line, = plt.plot(zg_theory_min_plot[0], zg_theory_min_plot[1], linewidth=0)
      zg_theory_max_line, = plt.plot(zg_theory_max_plot[0], zg_theory_max_plot[1], linewidth=0)
      
      x_min, y_min = zg_theory_min_line.get_xdata(), zg_theory_min_line.get_ydata()
      x_max, y_max = zg_theory_max_line.get_xdata(), zg_theory_max_line.get_ydata()

      ax1.fill_between(x_max, y_max, y_min, norm=1, where=np.less_equal(y_min, y_max), facecolor='red', interpolate=True, alpha=0.3, linewidth=0.0)

      zg_theory_line_hist.Divide(zg_theory_line_hist)
      zg_theory_line_plot = convert_hist_to_line_plot(zg_theory_line_hist, n_bins)
      plt.plot(zg_theory_line_plot[0], zg_theory_line_plot[1], linewidth=5, color='red')

  else:
    raise ValueError("Only 'theory' or 'data' are valid options for calculating ratios!")
  

  # Normalized-Over-Data Plot Ends.

  ax0.set_xlabel("$z_g$", fontsize=95)
  ax0.set_ylabel("$\displaystyle \\frac{z_g}{\sigma} \\frac{ \mathrm{d} \sigma}{ \mathrm{d} z_g}$", fontsize=80, rotation=0, labelpad=115, y=0.39)
  
  ax1.set_xlabel("$z_g$", fontsize=95)
  
  if ratio_denominator == "data":
    label_pad = 135
  else:
    label_pad = 115

  plt.ylabel("Ratio           \nto           \n" + ratio_denominator.capitalize() + "           ", fontsize=55, rotation=0, labelpad=label_pad, y=0.31, axes=ax1)

  # Legend.

  th_line, = ax0.plot(range(1), linewidth=5, color='red')
  th_patch = mpatches.Patch(facecolor='red', alpha=0.3, linewidth=5, edgecolor='red')

  if mc:
    pythia_line, = ax0.plot(range(1), linewidth=5, color='blue')
    herwig_line, = ax0.plot(range(1), linewidth=5, color='green')
  else:
    pythia_line, = ax0.plot(range(1), linewidth=5, color='blue', alpha=0)
    herwig_line, = ax0.plot(range(1), linewidth=5, color='green', alpha=0)

  handles = [data_plot, (th_patch, th_line), pythia_line, herwig_line]
  labels = [data_label, theory_label, pythia_label, herwig_label]

  first_legend = ax0.legend(handles, labels, fontsize=60, handler_map = {th_line : HandlerLine2D(marker_pad = 0), pythia_line : HandlerLine2D(marker_pad = 0), herwig_line : HandlerLine2D(marker_pad = 0)}, frameon=0, borderpad=0.1, bbox_to_anchor=[0.90, 0.98])
  ax = ax0.add_artist(first_legend)

  for txt in first_legend.get_texts():
    if ( not data) and txt.get_text() == data_label:
      txt.set_color("white") 

  # Info about R, pT_cut, etc.
  extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
  handles = [extra, extra]
  # labels = [r"$ \textrm{Anti--}k_{t}\textrm{:}~\boldsymbol{R = 0.5;~p_{T} > " + str(pT_lower_cut) + "~\mathrm{GeV};" + "\\abs{ \eta } < 3" + "}$", r"$ \textrm{Soft~Drop:}~\boldsymbol{\beta = 0;~z_{\mathrm{cut}} = " + str(zg_cut) + "}$"]
  labels = [r"$ \textrm{Anti--}k_{t}\textrm{:}~\boldsymbol{R = 0.5;~p_{T} > " + str(pT_lower_cut) + "~\mathrm{GeV}}$", r"$ \textrm{Soft~Drop:}~\boldsymbol{\beta = 0;~z_{\mathrm{cut}} = " + str(zg_cut) + "}$"]
  ax0.legend(handles, labels, loc=7, frameon=0, borderpad=0.1, fontsize=60, bbox_to_anchor=[0.99, 0.58])

  # Legend Ends.

  ax0.autoscale(True)
  ax1.autoscale(True)
  
  ax0.set_xlim(math.log(float(zg_cut), math.e), math.log(0.6, math.e))
  ax1.set_xlim(math.log(float(zg_cut), math.e), math.log(0.6, math.e))

  ax0.set_ylim(0.6 * min(data_plot_points_y), 1.7 * max(data_plot_points_y))
  ax1.set_ylim(1.0 - y_limit_ratio_plot, 1.0 + y_limit_ratio_plot)

  if data:
    ab = AnnotationBbox(OffsetImage(read_png(get_sample_data("/home/aashish/root-6.04.06/macros/MODAnalyzer/mod_logo.png", asfileobj=False)), zoom=0.15, resample=1, dpi_cor=1), (0.23, 0.9249985), xycoords='figure fraction', frameon=0)
    plt.gca().add_artist(ab)
    preliminary_text = "Prelim. (20\%)"
    plt.gcf().text(0.29, 0.9178555, preliminary_text, fontsize=50, weight='bold', color='#444444', multialignment='center')
  else:
    preliminary_text = ""
    plt.gcf().text(0.29, 0.9178555, preliminary_text, fontsize=50, weight='bold', color='#444444', multialignment='center')


  
  plt.gcf().set_size_inches(30, 30, forward=1)

  ax0.xaxis.set_tick_params(width=5, length=20, labelsize=70)
  ax0.yaxis.set_tick_params(width=5, length=20, labelsize=70)

  ax1.xaxis.set_tick_params(width=5, length=20, labelsize=70)
  ax1.yaxis.set_tick_params(width=5, length=20, labelsize=70)


  plt.sca(ax0)
  # plt.gca().xaxis.set_minor_locator(MultipleLocator(5))
  plt.gca().yaxis.set_minor_locator(MultipleLocator(0.05))
  plt.tick_params(which='major', width=5, length=25, labelsize=70)
  plt.tick_params(which='minor', width=3, length=15)

  plt.sca(ax1)
  if y_limit_ratio_plot < 1:
    plt.gca().yaxis.set_major_locator(MultipleLocator(0.2))
  else:
    plt.gca().yaxis.set_major_locator(MultipleLocator(0.5))

  # .01 * .02 * .03 .04 .05 * .06 .07 .08 .09 .1 * .2 * .3 .4 .5 * .6 .7 .8 .9 1 *
  # tick_positions = [math.log(0.01, math.e), math.log(0.02, math.e), math.log(0.03, math.e), math.log(0.04, math.e), math.log(0.05, math.e), math.log(0.06, math.e), math.log(0.07, math.e), math.log(0.08, math.e), math.log(0.09, math.e), math.log(0.1, math.e), math.log(0.2, math.e), math.log(0.3, math.e), math.log(0.4, math.e), math.log(0.5, math.e), math.log(0.6, math.e), math.log(0.7, math.e), math.log(0.8, math.e), math.log(0.9, math.e), math.log(1., math.e)]
  tick_positions = [math.log(0.01, math.e), math.log(0.02, math.e), math.log(0.05, math.e), math.log(0.1, math.e), math.log(0.2, math.e), math.log(0.5, math.e), math.log(1., math.e)]

  # x = np.linspace(math.log(zg_cut, math.e), math.log(0.5, math.e), 6)
  x = tick_positions
  labels = [str(round(math.exp(i), 5)) for i in x]

  plt.sca(ax0)
  plt.xticks(x, labels)

  plt.sca(ax1)
  plt.xticks(x, labels)

  # ax0.xaxis.set_minor_locator(FixedLocator(x))
  # ax0.xaxis.set_minor_locator(LogLocator(base=math.e))


  plt.gcf().set_snap(True)
  plt.tight_layout(pad=1.08, h_pad=1.08, w_pad=1.08)

  print "Writing log_zg_cut_" + str(zg_filename) + "_pt_cut_" + str(pT_lower_cut) + "_ratio_over_" + ratio_denominator + "_th_" + str(theory) + "_mc_" + str(mc) + "_data_" + str(data) + ".pdf"
  filename = "plots/" + get_version(input_analysis_file) + "/log_zg/log_zg_cut_" + str(zg_filename) + "_pt_cut_" + str(pT_lower_cut) + "_ratio_over_" + ratio_denominator + "_th_" + str(theory) + "_mc_" + str(mc) + "_data_" + str(data) + ".pdf"
  
  plt.savefig(filename)
  # plt.show()
  plt.clf()



def plot_pts_variable_bin():
  pT_lower_cut = 150
  properties = parse_file(input_analysis_file, pT_lower_cut)

  pTs = properties['uncorrected_hardest_pts']
  corrected_pTs = properties['corrected_hardest_pts']
  prescales = properties['prescales']

  event_numbers = properties['event_number']
  run_numbers = properties['run_number']

  print max(pTs)

  # for i in range(0, len(pTs)):
    # if pTs[i] > 10000:
  #     print int(event_numbers[i]), int(run_numbers[i])


  herwig_pTs = parse_mc_pt_file("/home/aashish/Dropbox (MIT)/Research/CMSOpenData/Andrew/fastjet_pt_herwig_pp2jj_150pTcut_7TeV.dat")
  pythia_pTs = parse_mc_pt_file("/home/aashish/Dropbox (MIT)/Research/CMSOpenData/Andrew/fastjet_pt_pythia_pp2jj_150pTcut_7TeV.dat")

  bins = [80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 340, 380, 420, 460, 500, 600, 700, 800, 900, 1000]

  pythia_pt_hist = Hist(bins, title="Pythia 8.205", linewidth=5, markersize=5.0, color="blue")
  herwig_pt_hist = Hist(bins, title="Herwig++ 2.6.3", linewidth=5, markersize=5.0, color="green")
  corrected_pt_hist = Hist(bins, title='Corrected', markersize=3.0, color='black')
  uncorrected_pt_hist = Hist(bins, title='Uncorrected', markersize=3.0, color='orange')

  map(uncorrected_pt_hist.Fill, pTs, prescales)
  map(corrected_pt_hist.Fill, corrected_pTs, prescales)
  
  map(pythia_pt_hist.Fill, pythia_pTs)
  map(herwig_pt_hist.Fill, herwig_pTs)


  corrected_pt_hist = normalize_hist(corrected_pt_hist)
  uncorrected_pt_hist = normalize_hist(uncorrected_pt_hist)
  pythia_pt_hist = normalize_hist(pythia_pt_hist)
  herwig_pt_hist = normalize_hist(herwig_pt_hist)

  
  gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1]) 

  ax0 = plt.subplot(gs[0])
  ax1 = plt.subplot(gs[1])


  data_plot = rplt.errorbar(corrected_pt_hist, axes=ax0, emptybins=False, marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5)
  uncorrected_data_plot = rplt.errorbar(uncorrected_pt_hist, axes=ax0, emptybins=False, marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5)
  rplt.hist(pythia_pt_hist, axes=ax0, emptybins=False, marker='o',  markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5)
  rplt.hist(herwig_pt_hist, axes=ax0, emptybins=False, marker='o',  markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5)
  

  data_x_errors, data_y_errors = [], []
  for x_segment in data_plot[2][0].get_segments():
    data_x_errors.append((x_segment[1][0] - x_segment[0][0]) / 2.)
  for y_segment in data_plot[2][1].get_segments():
    data_y_errors.append((y_segment[1][1] - y_segment[0][1]) / 2.)

  data_points_x = data_plot[0].get_xdata()
  data_points_y = data_plot[0].get_ydata()

  data_plot_points_x = []
  data_plot_points_y = []
  for i in range(0, len(data_points_x)):
    data_plot_points_x.append(data_points_x[i])
    data_plot_points_y.append(data_points_y[i])



  uncorrected_data_x_errors, uncorrected_data_y_errors = [], []
  for x_segment in uncorrected_data_plot[2][0].get_segments():
    uncorrected_data_x_errors.append((x_segment[1][0] - x_segment[0][0]) / 2.)
  for y_segment in uncorrected_data_plot[2][1].get_segments():
    uncorrected_data_y_errors.append((y_segment[1][1] - y_segment[0][1]) / 2.)

  uncorrected_data_points_x = uncorrected_data_plot[0].get_xdata()
  uncorrected_data_points_y = uncorrected_data_plot[0].get_ydata()

  uncorrected_data_plot_points_x = []
  uncorrected_data_plot_points_y = []
  for i in range(0, len(uncorrected_data_points_x)):
    uncorrected_data_plot_points_x.append(uncorrected_data_points_x[i])
    uncorrected_data_plot_points_y.append(uncorrected_data_points_y[i])




  data_to_data_y_err = [(b / m) for b, m in zip(data_y_errors, data_plot_points_y)]
  data_to_data_x_err = [(b / m) for b, m in zip(data_x_errors, [1] * len(data_plot_points_y))]

  uncorrected_to_corrected_y_err = [(b / m) for b, m in zip(uncorrected_data_y_errors, data_plot_points_y)]
  uncorrected_to_corrected_x_err = [(b / m) for b, m in zip(uncorrected_data_x_errors, [1] * len(data_plot_points_y))]


  ax0.autoscale(True)
  ax0.set_yscale('log')


  # Legends Begin.

  legend = ax0.legend(loc=1, frameon=0, fontsize=60, bbox_to_anchor=[0.98, 1.0])
  ax0.add_artist(legend)

  extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
  labels = [r"$ \textrm{Anti--}k_{t}\textrm{:}~R = 0.5;\eta<2.4$", r"$p_{T} > 150~\mathrm{GeV}$"]
  ax0.legend([extra], labels, loc=7, frameon=0, borderpad=0.1, fontsize=60, bbox_to_anchor=[1.0, 0.62])

  # Legends End.



  ax0.set_xlabel('$p_T~\mathrm{(GeV)}$', fontsize=75)
  ax1.set_xlabel('$p_T~\mathrm{(GeV)}$', fontsize=75)
  ax0.set_ylabel('$\mathrm{A.U.}$', fontsize=75, rotation=0, labelpad=75.)
  ax1.set_ylabel("Ratio           \nto           \n" + "Data" + "           ", fontsize=55, rotation=0, labelpad=115, y=0.31)


  ab = AnnotationBbox(OffsetImage(read_png(get_sample_data("/home/aashish/root-6.04.06/macros/MODAnalyzer/mod_logo.png", asfileobj=False)), zoom=0.15, resample=1, dpi_cor=1), (0.23, 0.9249985), xycoords='figure fraction', frameon=0)
  plt.gca().add_artist(ab)
  preliminary_text = "Prelim. (20\%)"
  plt.gcf().text(0.29, 0.9178555, preliminary_text, fontsize=50, weight='bold', color='#444444', multialignment='center')

  # Ratio Plot.
  pythia_pt_hist.Divide(corrected_pt_hist)
  herwig_pt_hist.Divide(corrected_pt_hist)
  uncorrected_pt_hist.Divide(corrected_pt_hist)
  corrected_pt_hist.Divide(corrected_pt_hist)

  rplt.hist(pythia_pt_hist, axes=ax1, linewidth=5)
  rplt.hist(herwig_pt_hist, axes=ax1, linewidth=5)
  
  rplt.errorbar(corrected_pt_hist, xerr=data_to_data_x_err, yerr=data_to_data_y_err, axes=ax1, emptybins=False, marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5)
  rplt.errorbar(uncorrected_pt_hist, xerr=uncorrected_to_corrected_x_err, yerr=uncorrected_to_corrected_y_err, axes=ax1, emptybins=False, marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5)

  ax1.autoscale(True)
  
  ax0.set_ylim(10e-8, 10e-1)
  ax1.set_ylim(0., 2.)


  plt.gcf().set_size_inches(30, 30, forward=1)


  plt.sca(ax0)
  plt.gca().xaxis.set_minor_locator(MultipleLocator(100))
  plt.tick_params(which='major', width=5, length=25, labelsize=70)
  plt.tick_params(which='minor', width=3, length=15)
  
  plt.sca(ax1)
  plt.gca().xaxis.set_minor_locator(MultipleLocator(100))
  plt.tick_params(which='major', width=5, length=25, labelsize=70)
  plt.tick_params(which='minor', width=3, length=15)


  plt.tight_layout(pad=1.08, h_pad=1.08, w_pad=1.08)

  plt.savefig("plots/" + get_version(input_analysis_file) + "/pT_distribution_var_bin.pdf")
  # plt.show()
  plt.clf()




def plot_delta_R(pT_lower_cut=150, dr_cut='0.05', dr_filename='dr_05'):
  dr_cut = float(dr_cut)

  properties = parse_file(input_analysis_file, pT_lower_cut=pT_lower_cut)

  dr = properties[dr_filename]
  charged_dr = properties['chrg_' + dr_filename]
  prescales = properties['prescales']

  dr_data_hist = Hist(6 * 8, 0.0, 0.6, title="All PF Candidates", markersize=2.5, color='black')
  bin_width_data = (dr_data_hist.upperbound() - dr_data_hist.lowerbound()) / dr_data_hist.nbins()
  map(dr_data_hist.Fill, dr, prescales)
  dr_data_hist.Scale(1.0 / ( dr_data_hist.GetSumOfWeights() * bin_width_data ))
  rplt.errorbar(dr_data_hist, xerr=1, yerr=1, emptybins=False, ls='None', marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5, alpha=1.0)

  chrg_dr_data_hist = Hist(6 * 8, 0.0, 0.6, title="Charged", markersize=2.5, color='red')
  bin_width_data = (chrg_dr_data_hist.upperbound() - chrg_dr_data_hist.lowerbound()) / chrg_dr_data_hist.nbins()
  map(chrg_dr_data_hist.Fill, charged_dr, prescales)
  chrg_dr_data_hist.Scale(1.0 / ( chrg_dr_data_hist.GetSumOfWeights() * bin_width_data ))
  rplt.errorbar(chrg_dr_data_hist, xerr=1, yerr=1, emptybins=False, ls='None', marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5, alpha=1.0)

  legend = plt.gca().legend(loc=1, frameon=0, fontsize=60, bbox_to_anchor=[0.91, 1.0])
  plt.gca().add_artist(legend)

  extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
  labels = [r"$ \textrm{Anti--}k_{t}\textrm{:}~R = 0.5;\eta<2.4$", r"$p_{T} > " + str(pT_lower_cut) + "~\mathrm{GeV}$", r"$ \textrm{Soft~Drop:}~\boldsymbol{\beta = 0;~z_{\mathrm{cut}} = " + str(dr_cut) + "}$"]
  plt.gca().legend([extra, extra, extra], labels, loc=7, frameon=0, borderpad=0.1, fontsize=60, bbox_to_anchor=[0.97, 0.70])


  plt.gca().set_xlabel("$R_g$", fontsize=75)
  plt.gca().set_ylabel("$\displaystyle \\frac{1}{\sigma} \\frac{ \mathrm{d} \sigma}{ \mathrm{d} R_g}$", fontsize=75, rotation=0, labelpad=115, y=0.39)
  
  plt.gca().autoscale(True)
  plt.gca().set_xlim(0.0, 0.8)

  plt.gcf().set_size_inches(30, 21.4285714, forward=1)

  ab = AnnotationBbox(OffsetImage(read_png(get_sample_data("/home/aashish/root-6.04.06/macros/MODAnalyzer/mod_logo.png", asfileobj=False)), zoom=0.15, resample=1, dpi_cor=1), (0.23, 0.9249985), xycoords='figure fraction', frameon=0)
  plt.gca().add_artist(ab)
  preliminary_text = "Prelim. (20\%)"
  plt.gcf().text(0.29, 0.9178555, preliminary_text, fontsize=50, weight='bold', color='#444444', multialignment='center')

  plt.gcf().set_snap(True)
  plt.tight_layout(pad=1.08, h_pad=1.08, w_pad=1.08)


  plt.savefig("plots/" + get_version(input_analysis_file) + "/delta_R/" + "/" + dr_filename + "_pT_" + str(pT_lower_cut) + ".pdf")

  plt.clf()





def plot_log_delta_R(pT_lower_cut=150, dr_cut='0.05', dr_filename='dr_05'):
  dr_cut = float(dr_cut)

  properties = parse_file(input_analysis_file, pT_lower_cut=pT_lower_cut)

  dr = properties[dr_filename]
  charged_dr = properties['chrg_' + dr_filename]
  prescales = properties['prescales']
  
  logged_dr = np.log(dr)
  logged_charged_dr = np.log(charged_dr)

  bins_linear_log = np.linspace(math.log(0.01, math.e), math.log(0.6, math.e), 48) 
  
  dr_data_hist = Hist(bins_linear_log, title="All PF Candidates", markersize=2.5, color='black')
  bin_width_data = (dr_data_hist.upperbound() - dr_data_hist.lowerbound()) / dr_data_hist.nbins()
  map(dr_data_hist.Fill, logged_dr, prescales)
  dr_data_hist.Scale(1.0 / ( dr_data_hist.GetSumOfWeights() * bin_width_data ))

  rplt.errorbar(dr_data_hist, xerr=1, yerr=1, emptybins=False, ls='None', marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5, alpha=1.0)


  chrg_dr_data_hist = Hist(bins_linear_log, title="Charged", markersize=2.5, color='red')
  bin_width_data = (chrg_dr_data_hist.upperbound() - chrg_dr_data_hist.lowerbound()) / chrg_dr_data_hist.nbins()
  map(chrg_dr_data_hist.Fill, logged_charged_dr, prescales)
  chrg_dr_data_hist.Scale(1.0 / ( chrg_dr_data_hist.GetSumOfWeights() * bin_width_data ))

  rplt.errorbar(chrg_dr_data_hist, xerr=1, yerr=1, emptybins=False, ls='None', marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5, alpha=1.0)
  

  legend = plt.gca().legend(loc=1, frameon=0, fontsize=60, bbox_to_anchor=[0.91, 1.0])
  plt.gca().add_artist(legend)

  extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
  labels = [r"$ \textrm{Anti--}k_{t}\textrm{:}~R = 0.5;\eta<2.4$", r"$p_{T} > " + str(pT_lower_cut) + "~\mathrm{GeV}$", r"$ \textrm{Soft~Drop:}~\boldsymbol{\beta = 0;~z_{\mathrm{cut}} = " + str(dr_cut) + "}$"]
  plt.gca().legend([extra, extra, extra], labels, loc=7, frameon=0, borderpad=0.1, fontsize=60, bbox_to_anchor=[0.97, 0.70])


  plt.gca().set_xlabel("$R_g$", fontsize=75)
  plt.gca().set_ylabel("$\displaystyle \\frac{R_g}{\sigma} \\frac{ \mathrm{d} \sigma}{ \mathrm{d} R_g}$", fontsize=75, rotation=0, labelpad=115, y=0.39)
  
  plt.gca().autoscale(True)
  plt.gca().set_ylim(0.0, 1.3)

  x = np.linspace(math.log(0.01, math.e), math.log(0.6, math.e), 6)
  labels = [str(round(math.exp(i), 3)) for i in x]
  plt.xticks(x, labels)


  plt.gcf().set_size_inches(30, 21.4285714, forward=1)

  ab = AnnotationBbox(OffsetImage(read_png(get_sample_data("/home/aashish/root-6.04.06/macros/MODAnalyzer/mod_logo.png", asfileobj=False)), zoom=0.15, resample=1, dpi_cor=1), (0.23, 0.9249985), xycoords='figure fraction', frameon=0)
  plt.gca().add_artist(ab)
  preliminary_text = "Prelim. (20\%)"
  plt.gcf().text(0.29, 0.9178555, preliminary_text, fontsize=50, weight='bold', color='#444444', multialignment='center')

  plt.gcf().set_snap(True)
  plt.tight_layout(pad=1.08, h_pad=1.08, w_pad=1.08)


  plt.savefig("plots/" + get_version(input_analysis_file) + "/log_delta_R/" + "/" + dr_filename + "_pT_" + str(pT_lower_cut) + ".pdf")

  plt.clf()




def plot_2d_zg_delta_R(pT_lower_cut=150, dr_cut='0.05', dr_filename='dr_05', zg_cut='0.05', zg_filename='zg_05'):
  dr_cut = float(dr_cut)
  zg_cut = float(zg_cut)

  properties = parse_file(input_analysis_file, pT_lower_cut=pT_lower_cut)

  zg = properties[zg_filename]
  dr = properties[dr_filename]
  prescales = properties['prescales']  


  H, xedges, yedges = np.histogram2d(dr, zg, bins=25, weights=prescales, normed=1, range=[[0.0, max(dr)], [0.0, max(zg)]] )

  H_normalized = []
  for i in range(0, 25):
    current_row = []
    factor = sum(H[i])
    for j in range(0, 25):
      current_row.append(H[i][j] / factor)

    H_normalized.append(current_row)


  H_normalized = np.array(H_normalized)
  H = H_normalized

  H = np.rot90(H)
  H = np.flipud(H)

  for a in range(0, len(H)):
    for b in range(0, len(H[j])):
      if str(H[a][b]) == "nan":
        H[a][b] = 0.
  
  Hmasked = np.ma.masked_where(H == 0, H) # Mask pixels with a value of zero

  plt.pcolormesh(xedges,yedges, Hmasked)

  cbar = plt.colorbar()
  cbar.ax.set_ylabel('Counts')

  plt.xlabel('$R_g$', fontsize=75)
  plt.ylabel('$z_g$', rotation=0, fontsize=75, labelpad=30)


  plt.gcf().set_size_inches(30, 30, forward=1)
  plt.gcf().set_snap(True)


  plt.savefig("plots/" + get_version(input_analysis_file) + "/zg_against_dr/" + dr_filename + "_pT_" + str(pT_lower_cut) + ".pdf")

  plt.clf()




def plot_2d_zg_charged_delta_R(pT_lower_cut=150, dr_cut='0.05', dr_filename='dr_05', zg_cut='0.05', zg_filename='zg_05'):
  dr_cut = float(dr_cut)
  zg_cut = float(zg_cut)

  properties = parse_file(input_analysis_file, pT_lower_cut=pT_lower_cut)

  zg = properties[zg_filename]
  charged_dr = properties['chrg_' + dr_filename]
  prescales = properties['prescales']  

  H, xedges, yedges = np.histogram2d(charged_dr, zg, bins=25, weights=prescales, normed=1, range=[[0.0, max(charged_dr)], [0.0, max(zg)]] )

  H_normalized = []
  for i in range(0, 25):
    current_row = []
    factor = sum(H[i])
    for j in range(0, 25):
      current_row.append(H[i][j] / factor)

    H_normalized.append(current_row)


  H_normalized = np.array(H_normalized)
  H = H_normalized

  H = np.rot90(H)
  H = np.flipud(H)

  for a in range(0, len(H)):
    for b in range(0, len(H[j])):
      if str(H[a][b]) == "nan":
        H[a][b] = 0.
  
  Hmasked = np.ma.masked_where(H == 0, H) # Mask pixels with a value of zero

  plt.pcolormesh(xedges,yedges, Hmasked)

  cbar = plt.colorbar()
  cbar.ax.set_ylabel('Counts')

  plt.xlabel('$R_g$', fontsize=75)
  plt.ylabel('$z_g$', rotation=0, fontsize=75, labelpad=30)


  plt.gcf().set_size_inches(30, 30, forward=1)
  plt.gcf().set_snap(True)


  plt.savefig("plots/" + get_version(input_analysis_file) + "/zg_against_charged_dr/" + dr_filename + "_pT_" + str(pT_lower_cut) + ".pdf")

  plt.clf()




def plot_2d_charged_zg_charged_delta_R(pT_lower_cut=150, dr_cut='0.05', dr_filename='dr_05', zg_cut='0.05', zg_filename='zg_05'):
  dr_cut = float(dr_cut)
  zg_cut = float(zg_cut)

  properties = parse_file(input_analysis_file, pT_lower_cut=pT_lower_cut)

  charged_zg = properties[zg_filename[0:2] + "_charged_" + zg_filename[3: len(zg_filename)]]
  charged_dr = properties['chrg_' + dr_filename]
  prescales = properties['prescales']  


  H, xedges, yedges = np.histogram2d(charged_dr, charged_zg, bins=25, weights=prescales, normed=1, range=[[0.0, max(charged_dr)], [0.0, max(charged_zg)]] )

  H_normalized = []
  for i in range(0, 25):
    current_row = []
    factor = sum(H[i])
    for j in range(0, 25):
      current_row.append(H[i][j] / factor)

    H_normalized.append(current_row)


  H_normalized = np.array(H_normalized)
  H = H_normalized

  H = np.rot90(H)
  H = np.flipud(H)

  for a in range(0, len(H)):
    for b in range(0, len(H[j])):
      if str(H[a][b]) == "nan":
        H[a][b] = 0.
  
  Hmasked = np.ma.masked_where(H == 0, H) # Mask pixels with a value of zero

  plt.pcolormesh(xedges,yedges, Hmasked)

  cbar = plt.colorbar()
  cbar.ax.set_ylabel('Counts')

  plt.xlabel('$R_g$', fontsize=75)
  plt.ylabel('$z_g$', rotation=0, fontsize=75, labelpad=30)


  plt.gcf().set_size_inches(30, 30, forward=1)
  plt.gcf().set_snap(True)


  plt.savefig("plots/" + get_version(input_analysis_file) + "/charged_zg_against_charged_dr/" + dr_filename + "_pT_" + str(pT_lower_cut) + ".pdf")

  plt.clf()




def zg_different_pT_cuts(pT_lower_cut=150, zg_cut='0.05', zg_filename='zg_05'):
   # uncorrected_pT_lower_cut = 0.00, softdrop_pT_lower_cut = 0.00, 

  zg_cut = float(zg_cut)

  properties_uncorrected_pT = parse_file(input_analysis_file, pT_lower_cut=pT_lower_cut)
  properties_corrected_pT = parse_file(input_analysis_file, uncorrected_pT_lower_cut=pT_lower_cut)
  
  properties_SD_pT_unc = parse_file(input_analysis_file, softdrop_unc_pT_lower_cut=pT_lower_cut)
  properties_SD_pT_cor = parse_file(input_analysis_file, softdrop_cor_pT_lower_cut=pT_lower_cut)

  zg_data_unc = properties_uncorrected_pT[zg_filename]
  prescales_unc = properties_uncorrected_pT['prescales']

  zg_data_cor = properties_corrected_pT[zg_filename]
  prescales_cor = properties_corrected_pT['prescales']

  zg_data_SD_unc = properties_SD_pT_unc[zg_filename]
  prescales_SD_unc = properties_SD_pT_unc['prescales']

  zg_data_SD_cor = properties_SD_pT_cor[zg_filename]
  prescales_SD_cor = properties_SD_pT_cor['prescales']
  



  zg_data_hist = Hist(6 * 8, 0.0, 0.6, title="Cut on Uncorrected pT", markersize=2.5, color='black')
  bin_width_data = (zg_data_hist.upperbound() - zg_data_hist.lowerbound()) / zg_data_hist.nbins()
  map(zg_data_hist.Fill, zg_data_unc, prescales_unc)
  zg_data_hist.Scale(1.0 / ( zg_data_hist.GetSumOfWeights() * bin_width_data ))
  rplt.errorbar(zg_data_hist, xerr=1, yerr=1, emptybins=False, ls='None', marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5, alpha=1.0)


  zg_data_hist = Hist(6 * 8, 0.0, 0.6, title="Cut on Corrected pT", markersize=2.5, color='red')
  bin_width_data = (zg_data_hist.upperbound() - zg_data_hist.lowerbound()) / zg_data_hist.nbins()
  map(zg_data_hist.Fill, zg_data_cor, prescales_cor)
  zg_data_hist.Scale(1.0 / ( zg_data_hist.GetSumOfWeights() * bin_width_data ))
  rplt.errorbar(zg_data_hist, xerr=1, yerr=1, emptybins=False, ls='None', marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5, alpha=1.0)


  zg_data_hist = Hist(6 * 8, 0.0, 0.6, title="Cut on Uncorrected SD pT", markersize=2.5, color='green')
  bin_width_data = (zg_data_hist.upperbound() - zg_data_hist.lowerbound()) / zg_data_hist.nbins()
  map(zg_data_hist.Fill, zg_data_SD_unc, prescales_SD_unc)
  zg_data_hist.Scale(1.0 / ( zg_data_hist.GetSumOfWeights() * bin_width_data ))
  rplt.errorbar(zg_data_hist, xerr=1, yerr=1, emptybins=False, ls='None', marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5, alpha=1.0)


  zg_data_hist = Hist(6 * 8, 0.0, 0.6, title="Cut on Corrected SD pT", markersize=2.5, color='blue')
  bin_width_data = (zg_data_hist.upperbound() - zg_data_hist.lowerbound()) / zg_data_hist.nbins()
  map(zg_data_hist.Fill, zg_data_SD_cor, prescales_SD_cor)
  zg_data_hist.Scale(1.0 / ( zg_data_hist.GetSumOfWeights() * bin_width_data ))
  rplt.errorbar(zg_data_hist, xerr=1, yerr=1, emptybins=False, ls='None', marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5, alpha=1.0)


  legend = plt.gca().legend(loc=1, frameon=0, fontsize=60, bbox_to_anchor=[1.0, 1.0])
  plt.gca().add_artist(legend)

  extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
  labels = [r"$ \textrm{Anti--}k_{t}\textrm{:}~R = 0.5;\eta<2.4$", r"$p_{T} > " + str(pT_lower_cut) + "~\mathrm{GeV}$", r"$ \textrm{Soft~Drop:}~\boldsymbol{\beta = 0;~z_{\mathrm{cut}} = " + str(zg_cut) + "}$"]
  plt.gca().legend([extra, extra], labels, loc=7, frameon=0, borderpad=0.1, fontsize=60, bbox_to_anchor=[0.88, 0.58])


  plt.gca().set_xlabel("$z_g$", fontsize=95)
  plt.gca().set_ylabel("$\displaystyle \\frac{1}{\sigma} \\frac{ \mathrm{d} \sigma}{ \mathrm{d} z_g}$", fontsize=80, rotation=0, labelpad=115, y=0.39)
  
  plt.gca().autoscale(True)
  plt.gca().set_xlim(0.0, 0.6)
  plt.gca().set_ylim(0.0, 19)

  plt.gcf().set_size_inches(30, 21.4285714, forward=1)

  ab = AnnotationBbox(OffsetImage(read_png(get_sample_data("/home/aashish/root-6.04.06/macros/MODAnalyzer/mod_logo.png", asfileobj=False)), zoom=0.15, resample=1, dpi_cor=1), (0.23, 0.9249985), xycoords='figure fraction', frameon=0)
  plt.gca().add_artist(ab)
  preliminary_text = "Prelim. (20\%)"
  plt.gcf().text(0.29, 0.9178555, preliminary_text, fontsize=50, weight='bold', color='#444444', multialignment='center')

  plt.gcf().set_snap(True)
  plt.tight_layout(pad=1.08, h_pad=1.08, w_pad=1.08)


  plt.savefig("plots/" + get_version(input_analysis_file) + "/zg_different_pT_cuts/" + "/" + zg_filename + "_pT_" + str(pT_lower_cut) + ".pdf")

  plt.clf()

  

def zg_new_mc():
  
  properties = parse_file(input_analysis_file, pT_lower_cut=150)
  
  zg_data = properties['zg_05']
  pT_data = properties['corrected_hardest_pts']
  prescales = properties['prescales']

  monte_carlo_file_name = "/home/aashish/MODMonteCarlo/data/zg_output.dat"

  f = open(monte_carlo_file_name, 'r')
  lines = f.read().split("\n")
  
  zg_mc = []
  pT_mc = []
  for line in lines:  
    if len(line.strip()) != 0:
      numbers = line.split(", ")
      pT_mc.append(float(numbers[0]))
      zg_mc.append(float(numbers[1]))

  zg_data_hist = Hist(20, 0, 0.5, title="Data")
  bin_width_data = (zg_data_hist.upperbound() - zg_data_hist.lowerbound()) / zg_data_hist.nbins()
  map(zg_data_hist.Fill, zg_data, prescales)
  zg_data_hist.Scale(1.0 / ( zg_data_hist.GetSumOfWeights() * bin_width_data ))

  
  rplt.errorbar(zg_data_hist, xerr=1, yerr=1, emptybins=False, ls='None', marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5, alpha=1.0)
  
  plt.hist(zg_mc, color="red", histtype='step', normed=1, lw=5, label="Pythia 8.212")

  plt.legend()

  plt.xlabel("$z_g$")

  plt.gca().autoscale(True)
  # plt.gca().set_xlim(0.0, 0.5)
  # plt.gca().set_ylim(0.0, 19)

  plt.gcf().set_size_inches(30, 21.4285714, forward=1)

  plt.gcf().set_snap(True)
  plt.tight_layout(pad=1.08, h_pad=1.08, w_pad=1.08)

  plt.savefig("plots/" + get_version(input_analysis_file) + "/zg_new_MC.pdf")

  plt.clf()



  print min(pT_mc)
  print max(pT_mc)
  pT_data_hist = Hist(20, 0, 7000, title="Data")
  bin_width_data = (pT_data_hist.upperbound() - pT_data_hist.lowerbound()) / pT_data_hist.nbins()
  map(pT_data_hist.Fill, pT_data, prescales)
  pT_data_hist.Scale(1.0 / ( pT_data_hist.GetSumOfWeights() * bin_width_data ))

  
  # rplt.errorbar(pT_data_hist, xerr=1, yerr=1, emptybins=False, ls='None', marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5, alpha=1.0)
  
  plt.hist(pT_mc, color="red", bins=50, histtype='step', normed=True, lw=5, label="Pythia 8.212")

  plt.legend()

  plt.xlabel("$p_T$")

  plt.gca().autoscale(True)
  # plt.gca().set_xlim(0.0, 0.5)
  plt.gca().set_ylim(0.0, 0.002)

  plt.gcf().set_size_inches(30, 21.4285714, forward=1)

  plt.gcf().set_snap(True)
  plt.tight_layout(pad=1.08, h_pad=1.08, w_pad=1.08)

  plt.savefig("plots/" + get_version(input_analysis_file) + "/pT_new_MC.pdf")

  plt.clf()



def weird_pt(reco=True):

  if reco:
    tag = "reco"
  else:
    tag = "truth"

  pythia_properties = parse_mc("/home/aashish/pythia_" + tag + ".dat")
  herwig_properties = parse_mc("/home/aashish/herwig_" + tag + ".dat")
  sherpa_properties = parse_mc("/home/aashish/sherpa_" + tag + ".dat")

  pythia_pTs = pythia_properties['hardest_pts']
  herwig_pTs = herwig_properties['hardest_pts']
  sherpa_pTs = sherpa_properties['hardest_pts']

  plt.hist(pythia_pTs, bins=25, histtype="step", lw=5, label="Pythia 8.212")
  plt.hist(herwig_pTs, bins=25, histtype="step", lw=5, label="Herwig++ 2.7.1")
  plt.hist(sherpa_pTs, bins=25, histtype="step", lw=5, label="Sherpa 2.2.0")

  plt.legend()

  plt.title(tag.capitalize() + " pT Distribution")

  plt.gca().set_ylim(0, plt.gca().get_ylim()[1] * 1.25)
  plt.xlabel("$p_T / GeV$")

  plt.gcf().set_size_inches(30, 21.4285714, forward=1)
  
  plt.savefig("plots/" + get_version(input_analysis_file) + "/pT_" + tag + ".pdf")
  plt.clf()


def plot_jet_eta():
  pT_lower_cut = 100
  properties = parse_file(input_analysis_file, pT_lower_cut)
  
  pythia_properties = parse_mc("/home/aashish/pythia_reco.dat", pT_lower_cut)
  herwig_properties = parse_mc("/home/aashish/herwig_reco.dat", pT_lower_cut)
  sherpa_properties = parse_mc("/home/aashish/sherpa_reco.dat", pT_lower_cut)

  jet_eta = properties['eta']
  prescales = properties['prescales']

  pythia_eta = pythia_properties['eta']
  herwig_eta = herwig_properties['eta']
  sherpa_eta = sherpa_properties['eta']


  data_hist = Hist(50, -5, 5, title="Data")
  map(data_hist.Fill, jet_eta, prescales)
  bin_width_data = (data_hist.upperbound() - data_hist.lowerbound()) / data_hist.nbins()
  data_hist.Scale(1.0 / ( data_hist.GetSumOfWeights() * bin_width_data ))

  pythia_hist = Hist(50, -5, 5, title="Pythia 8.212", color="red")
  map(pythia_hist.Fill, pythia_eta)
  bin_width_pythia = (pythia_hist.upperbound() - pythia_hist.lowerbound()) / pythia_hist.nbins()
  pythia_hist.Scale(1.0 / ( pythia_hist.GetSumOfWeights() * bin_width_pythia ))

  herwig_hist = Hist(50, -5, 5, title="Herwig++ 2.7.1", color="green")
  map(herwig_hist.Fill, herwig_eta)
  bin_width_herwig = (herwig_hist.upperbound() - herwig_hist.lowerbound()) / herwig_hist.nbins()
  herwig_hist.Scale(1.0 / ( herwig_hist.GetSumOfWeights() * bin_width_herwig ))

  sherpa_hist = Hist(50, -5, 5, title="Sherpa 2.2.0", color="blue")
  map(sherpa_hist.Fill, sherpa_eta)
  bin_width_sherpa = (sherpa_hist.upperbound() - sherpa_hist.lowerbound()) / sherpa_hist.nbins()
  sherpa_hist.Scale(1.0 / ( sherpa_hist.GetSumOfWeights() * bin_width_sherpa ))

  


  rplt.errorbar(data_hist, xerr=1, yerr=1, emptybins=False, ls='None', marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5, alpha=1.0)
  rplt.errorbar(pythia_hist, xerr=1, yerr=1, emptybins=False, ls='None', marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5, alpha=1.0)
  rplt.errorbar(herwig_hist, xerr=1, yerr=1, emptybins=False, ls='None', marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5, alpha=1.0)
  rplt.errorbar(sherpa_hist, xerr=1, yerr=1, emptybins=False, ls='None', marker='o', markersize=10, pickradius=8, capthick=5, capsize=8, elinewidth=5, alpha=1.0)
  
  plt.xlabel('$\\eta$', fontsize=75)
  plt.ylabel('A.U.', fontsize=75, rotation=0, labelpad=100.)

  ab = AnnotationBbox(OffsetImage(read_png(get_sample_data("/home/aashish/root-6.04.06/macros/MODAnalyzer/mod_logo.png", asfileobj=False)), zoom=0.15, resample=1, dpi_cor=1), (0.23, 0.895), xycoords='figure fraction', frameon=0)
  plt.gca().add_artist(ab)
  preliminary_text = "Prelim. (20\%)"
  plt.gcf().text(0.29, 0.885, preliminary_text, fontsize=50, weight='bold', color='#444444', multialignment='center')

  plt.gcf().set_size_inches(30, 21.4285714, forward=1)

  legend = plt.gca().legend(loc=1, frameon=0, fontsize=60)
  plt.gca().add_artist(legend)

  

  plt.gca().xaxis.set_minor_locator(MultipleLocator(0.2))
  plt.gca().yaxis.set_minor_locator(MultipleLocator(0.01))
  plt.tick_params(which='major', width=5, length=25, labelsize=70)
  plt.tick_params(which='minor', width=3, length=15)

  plt.tight_layout(pad=1.08, h_pad=1.08, w_pad=1.08)

  plt.savefig("plots/" + get_version(input_analysis_file) + "/jet_eta.pdf")

  plt.clf()



plot_jet_eta()



# zg_different_pT_cuts(pT_lower_cut=150, zg_cut='0.05', zg_filename='zg_05')
# zg_different_pT_cuts(pT_lower_cut=150, zg_cut='0.1', zg_filename='zg_1')
# zg_different_pT_cuts(pT_lower_cut=150, zg_cut='0.2', zg_filename='zg_2')

# zg_different_pT_cuts(pT_lower_cut=300, zg_cut='0.05', zg_filename='zg_05')
# zg_different_pT_cuts(pT_lower_cut=300, zg_cut='0.1', zg_filename='zg_1')
# zg_different_pT_cuts(pT_lower_cut=300, zg_cut='0.2', zg_filename='zg_2')

# zg_different_pT_cuts(pT_lower_cut=600, zg_cut='0.05', zg_filename='zg_05')
# zg_different_pT_cuts(pT_lower_cut=600, zg_cut='0.1', zg_filename='zg_1')
# zg_different_pT_cuts(pT_lower_cut=600, zg_cut='0.2', zg_filename='zg_2')

# Version 3 Begins Here.

# plot_jet_mass_spectrum()
# plot_jet_mass_spectrum(pT_lower_cut=100, pT_upper_cut=200)
# plot_jet_mass_spectrum(pT_lower_cut=200, pT_upper_cut=400)
# plot_jet_mass_spectrum(pT_lower_cut=400)


# plot_log_jet_mass_spectrum(100)
# plot_log_jet_mass_spectrum(200)
# plot_log_jet_mass_spectrum(300)
# plot_log_jet_mass_spectrum(400)


# plot_charged_jet_mass_spectrum()
# plot_charged_jet_mass_spectrum(pT_lower_cut=100, pT_upper_cut=200)
# plot_charged_jet_mass_spectrum(pT_lower_cut=200, pT_upper_cut=400)
# plot_charged_jet_mass_spectrum(pT_lower_cut=400)


# plot_fractional_energy_loss()
# plot_fractional_energy_loss(pT_lower_cut=100, pT_upper_cut=200)
# plot_fractional_energy_loss(pT_lower_cut=200, pT_upper_cut=400)
# plot_fractional_energy_loss(pT_lower_cut=400)

# plot_constituent_multiplicity_softdrop()
# plot_constituent_multiplicity_softdrop(pT_lower_cut=100, pT_upper_cut=200)
# plot_constituent_multiplicity_softdrop(pT_lower_cut=200, pT_upper_cut=400)
# plot_constituent_multiplicity_softdrop(pT_lower_cut=400)

# plot_charged_constituent_multiplicity_softdrop()
# plot_charged_constituent_multiplicity_softdrop(pT_lower_cut=100, pT_upper_cut=200)
# plot_charged_constituent_multiplicity_softdrop(pT_lower_cut=200, pT_upper_cut=400)
# plot_charged_constituent_multiplicity_softdrop(pT_lower_cut=400)






# plot_jet_area()

# plot_hardest_pt_softdrop()

# plot_pts()

# plot_pts_variable_bin()

# plot_jec_eta_2d()

# plot_JEC()

# plot_delta_R(pT_lower_cut=150, dr_cut='0.05', dr_filename='dr_05')
# plot_delta_R(pT_lower_cut=150, dr_cut='0.1', dr_filename='dr_1')
# plot_delta_R(pT_lower_cut=150, dr_cut='0.2', dr_filename='dr_2')

# plot_delta_R(pT_lower_cut=300, dr_cut='0.05', dr_filename='dr_05')
# plot_delta_R(pT_lower_cut=300, dr_cut='0.1', dr_filename='dr_1')
# plot_delta_R(pT_lower_cut=300, dr_cut='0.2', dr_filename='dr_2')

# plot_delta_R(pT_lower_cut=600, dr_cut='0.05', dr_filename='dr_05')
# plot_delta_R(pT_lower_cut=600, dr_cut='0.1', dr_filename='dr_1')
# plot_delta_R(pT_lower_cut=600, dr_cut='0.2', dr_filename='dr_2')





# plot_log_delta_R(pT_lower_cut=150, dr_cut='0.05', dr_filename='dr_05')
# plot_log_delta_R(pT_lower_cut=150, dr_cut='0.1', dr_filename='dr_1')
# plot_log_delta_R(pT_lower_cut=150, dr_cut='0.2', dr_filename='dr_2')

# plot_log_delta_R(pT_lower_cut=300, dr_cut='0.05', dr_filename='dr_05')
# plot_log_delta_R(pT_lower_cut=300, dr_cut='0.1', dr_filename='dr_1')
# plot_log_delta_R(pT_lower_cut=300, dr_cut='0.2', dr_filename='dr_2')

# plot_log_delta_R(pT_lower_cut=600, dr_cut='0.05', dr_filename='dr_05')
# plot_log_delta_R(pT_lower_cut=600, dr_cut='0.1', dr_filename='dr_1')
# plot_log_delta_R(pT_lower_cut=600, dr_cut='0.2', dr_filename='dr_2')







# plot_2d_zg_delta_R(pT_lower_cut=150, dr_cut='0.05', dr_filename='dr_05', zg_cut='0.05', zg_filename='zg_05')
# plot_2d_zg_delta_R(pT_lower_cut=150, dr_cut='0.1', dr_filename='dr_1', zg_cut='0.1', zg_filename='zg_1')
# plot_2d_zg_delta_R(pT_lower_cut=150, dr_cut='0.2', dr_filename='dr_2', zg_cut='0.2', zg_filename='zg_2')

# plot_2d_zg_delta_R(pT_lower_cut=300, dr_cut='0.05', dr_filename='dr_05', zg_cut='0.05', zg_filename='zg_05')
# plot_2d_zg_delta_R(pT_lower_cut=300, dr_cut='0.1', dr_filename='dr_1', zg_cut='0.1', zg_filename='zg_1')
# plot_2d_zg_delta_R(pT_lower_cut=300, dr_cut='0.2', dr_filename='dr_2', zg_cut='0.2', zg_filename='zg_2')

# plot_2d_zg_delta_R(pT_lower_cut=600, dr_cut='0.05', dr_filename='dr_05', zg_cut='0.05', zg_filename='zg_05')
# plot_2d_zg_delta_R(pT_lower_cut=600, dr_cut='0.1', dr_filename='dr_1', zg_cut='0.1', zg_filename='zg_1')
# plot_2d_zg_delta_R(pT_lower_cut=600, dr_cut='0.2', dr_filename='dr_2', zg_cut='0.2', zg_filename='zg_2')




# plot_2d_zg_charged_delta_R(pT_lower_cut=150, dr_cut='0.05', dr_filename='dr_05', zg_cut='0.05', zg_filename='zg_05')
# plot_2d_zg_charged_delta_R(pT_lower_cut=150, dr_cut='0.1', dr_filename='dr_1', zg_cut='0.1', zg_filename='zg_1')
# plot_2d_zg_charged_delta_R(pT_lower_cut=150, dr_cut='0.2', dr_filename='dr_2', zg_cut='0.2', zg_filename='zg_2')

# plot_2d_zg_charged_delta_R(pT_lower_cut=300, dr_cut='0.05', dr_filename='dr_05', zg_cut='0.05', zg_filename='zg_05')
# plot_2d_zg_charged_delta_R(pT_lower_cut=300, dr_cut='0.1', dr_filename='dr_1', zg_cut='0.1', zg_filename='zg_1')
# plot_2d_zg_charged_delta_R(pT_lower_cut=300, dr_cut='0.2', dr_filename='dr_2', zg_cut='0.2', zg_filename='zg_2')

# plot_2d_zg_charged_delta_R(pT_lower_cut=600, dr_cut='0.05', dr_filename='dr_05', zg_cut='0.05', zg_filename='zg_05')
# plot_2d_zg_charged_delta_R(pT_lower_cut=600, dr_cut='0.1', dr_filename='dr_1', zg_cut='0.1', zg_filename='zg_1')
# plot_2d_zg_charged_delta_R(pT_lower_cut=600, dr_cut='0.2', dr_filename='dr_2', zg_cut='0.2', zg_filename='zg_2')




# plot_2d_charged_zg_charged_delta_R(pT_lower_cut=150, dr_cut='0.05', dr_filename='dr_05', zg_cut='0.05', zg_filename='zg_05')
# plot_2d_charged_zg_charged_delta_R(pT_lower_cut=150, dr_cut='0.1', dr_filename='dr_1', zg_cut='0.1', zg_filename='zg_1')
# plot_2d_charged_zg_charged_delta_R(pT_lower_cut=150, dr_cut='0.2', dr_filename='dr_2', zg_cut='0.2', zg_filename='zg_2')

# plot_2d_charged_zg_charged_delta_R(pT_lower_cut=300, dr_cut='0.05', dr_filename='dr_05', zg_cut='0.05', zg_filename='zg_05')
# plot_2d_charged_zg_charged_delta_R(pT_lower_cut=300, dr_cut='0.1', dr_filename='dr_1', zg_cut='0.1', zg_filename='zg_1')
# plot_2d_charged_zg_charged_delta_R(pT_lower_cut=300, dr_cut='0.2', dr_filename='dr_2', zg_cut='0.2', zg_filename='zg_2')

# plot_2d_charged_zg_charged_delta_R(pT_lower_cut=600, dr_cut='0.05', dr_filename='dr_05', zg_cut='0.05', zg_filename='zg_05')
# plot_2d_charged_zg_charged_delta_R(pT_lower_cut=600, dr_cut='0.1', dr_filename='dr_1', zg_cut='0.1', zg_filename='zg_1')
# plot_2d_charged_zg_charged_delta_R(pT_lower_cut=600, dr_cut='0.2', dr_filename='dr_2', zg_cut='0.2', zg_filename='zg_2')





plot_zg_th_mc_data(pT_lower_cut=150, pT_upper_cut=10000, zg_cut='0.05', zg_filename='zg_05', ratio_denominator='theory', theory=1, mc=1, data=1, n_bins=8, y_max_limit=18, y_limit_ratio_plot=0.5)

plot_zg_th_mc_data(pT_lower_cut=150, pT_upper_cut=10000, zg_cut='0.1', zg_filename='zg_1', ratio_denominator='theory', theory=1, mc=0, data=0, n_bins=8, y_max_limit=10, y_limit_ratio_plot=0.5)
plot_zg_th_mc_data(pT_lower_cut=150, pT_upper_cut=10000, zg_cut='0.1', zg_filename='zg_1', ratio_denominator='theory', theory=1, mc=1, data=0, n_bins=8, y_max_limit=10, y_limit_ratio_plot=0.5)
plot_zg_th_mc_data(pT_lower_cut=150, pT_upper_cut=10000, zg_cut='0.1', zg_filename='zg_1', ratio_denominator='theory', theory=1, mc=1, data=1, n_bins=8, y_max_limit=10, y_limit_ratio_plot=0.5)
plot_zg_th_mc_data(pT_lower_cut=150, pT_upper_cut=10000, zg_cut='0.1', zg_filename='zg_1', ratio_denominator='data', theory=1, mc=1, data=1, n_bins=8, y_max_limit=10, y_limit_ratio_plot=0.5)

plot_zg_th_mc_data(pT_lower_cut=150, pT_upper_cut=10000, zg_cut='0.2', zg_filename='zg_2', ratio_denominator='theory', theory=1, mc=1, data=1, n_bins=8, y_max_limit=10, y_limit_ratio_plot=0.5)



plot_zg_th_mc_data(pT_lower_cut=300, pT_upper_cut=10000, zg_cut='0.05', zg_filename='zg_05', ratio_denominator='theory', theory=1, mc=1, data=1, n_bins=4, y_max_limit=15, y_limit_ratio_plot=1.0)
plot_zg_th_mc_data(pT_lower_cut=300, pT_upper_cut=10000, zg_cut='0.1', zg_filename='zg_1', ratio_denominator='theory', theory=1, mc=1, data=1, n_bins=4, y_max_limit=15, y_limit_ratio_plot=1.0)
plot_zg_th_mc_data(pT_lower_cut=300, pT_upper_cut=10000, zg_cut='0.2', zg_filename='zg_2', ratio_denominator='theory', theory=1, mc=1, data=1, n_bins=4, y_max_limit=15, y_limit_ratio_plot=1.0)

# plot_zg_th_mc_data(pT_lower_cut=600, pT_upper_cut=10000, zg_cut='0.05', zg_filename='zg_05', ratio_denominator='theory', theory=1, mc=1, data=1, n_bins=2, y_max_limit=15, y_limit_ratio_plot=1.0)
# plot_zg_th_mc_data(pT_lower_cut=600, pT_upper_cut=10000, zg_cut='0.1', zg_filename='zg_1', ratio_denominator='theory', theory=1, mc=1, data=1, n_bins=2, y_max_limit=15, y_limit_ratio_plot=1.0)
# plot_zg_th_mc_data(pT_lower_cut=600, pT_upper_cut=10000, zg_cut='0.2', zg_filename='zg_2', ratio_denominator='theory', theory=1, mc=1, data=1, n_bins=2, y_max_limit=15, y_limit_ratio_plot=1.0)









# plot_log_zg_th_mc_data(pT_lower_cut=150, pT_upper_cut=10000, zg_cut='0.05', zg_filename='zg_05', ratio_denominator='theory', theory=1, mc=1, data=1, n_bins=8, y_max_limit=18, y_limit_ratio_plot=0.6)
# plot_log_zg_th_mc_data(pT_lower_cut=150, pT_upper_cut=10000, zg_cut='0.1', zg_filename='zg_1', ratio_denominator='theory', theory=1, mc=1, data=1, n_bins=8, y_max_limit=10, y_limit_ratio_plot=0.5)
# plot_log_zg_th_mc_data(pT_lower_cut=150, pT_upper_cut=10000, zg_cut='0.2', zg_filename='zg_2', ratio_denominator='theory', theory=1, mc=1, data=1, n_bins=8, y_max_limit=10, y_limit_ratio_plot=0.5)

# plot_log_zg_th_mc_data(pT_lower_cut=300, pT_upper_cut=10000, zg_cut='0.05', zg_filename='zg_05', ratio_denominator='theory', theory=1, mc=1, data=1, n_bins=4, y_max_limit=15, y_limit_ratio_plot=0.7)
# plot_log_zg_th_mc_data(pT_lower_cut=300, pT_upper_cut=10000, zg_cut='0.1', zg_filename='zg_1', ratio_denominator='theory', theory=1, mc=1, data=1, n_bins=4, y_max_limit=15, y_limit_ratio_plot=0.5)
# plot_log_zg_th_mc_data(pT_lower_cut=300, pT_upper_cut=10000, zg_cut='0.2', zg_filename='zg_2', ratio_denominator='theory', theory=1, mc=1, data=1, n_bins=4, y_max_limit=15, y_limit_ratio_plot=0.5)

# plot_log_zg_th_mc_data(pT_lower_cut=600, pT_upper_cut=10000, zg_cut='0.05', zg_filename='zg_05', ratio_denominator='theory', theory=1, mc=1, data=1, n_bins=2, y_max_limit=15, y_limit_ratio_plot=1.0)
# plot_log_zg_th_mc_data(pT_lower_cut=600, pT_upper_cut=10000, zg_cut='0.1', zg_filename='zg_1', ratio_denominator='theory', theory=1, mc=1, data=1, n_bins=2, y_max_limit=15, y_limit_ratio_plot=0.5)
# plot_log_zg_th_mc_data(pT_lower_cut=600, pT_upper_cut=10000, zg_cut='0.2', zg_filename='zg_2', ratio_denominator='theory', theory=1, mc=1, data=1, n_bins=2, y_max_limit=15, y_limit_ratio_plot=1.0)



# plot_log_zg_th_mc_data(pT_lower_cut=150, pT_upper_cut=10000, zg_cut='0.05', zg_filename='zg_05', ratio_denominator='data', theory=1, mc=1, data=1, n_bins=8, y_max_limit=18, y_limit_ratio_plot=0.6)
# plot_log_zg_th_mc_data(pT_lower_cut=150, pT_upper_cut=10000, zg_cut='0.1', zg_filename='zg_1', ratio_denominator='data', theory=1, mc=1, data=1, n_bins=8, y_max_limit=10, y_limit_ratio_plot=0.5)
# plot_log_zg_th_mc_data(pT_lower_cut=150, pT_upper_cut=10000, zg_cut='0.2', zg_filename='zg_2', ratio_denominator='data', theory=1, mc=1, data=1, n_bins=8, y_max_limit=10, y_limit_ratio_plot=0.5)

# plot_log_zg_th_mc_data(pT_lower_cut=300, pT_upper_cut=10000, zg_cut='0.05', zg_filename='zg_05', ratio_denominator='data', theory=1, mc=1, data=1, n_bins=4, y_max_limit=15, y_limit_ratio_plot=0.7)
# plot_log_zg_th_mc_data(pT_lower_cut=300, pT_upper_cut=10000, zg_cut='0.1', zg_filename='zg_1', ratio_denominator='data', theory=1, mc=1, data=1, n_bins=4, y_max_limit=15, y_limit_ratio_plot=0.5)
# plot_log_zg_th_mc_data(pT_lower_cut=300, pT_upper_cut=10000, zg_cut='0.2', zg_filename='zg_2', ratio_denominator='data', theory=1, mc=1, data=1, n_bins=4, y_max_limit=15, y_limit_ratio_plot=0.5)

# plot_log_zg_th_mc_data(pT_lower_cut=600, pT_upper_cut=10000, zg_cut='0.05', zg_filename='zg_05', ratio_denominator='data', theory=1, mc=1, data=1, n_bins=2, y_max_limit=15, y_limit_ratio_plot=1.0)
# plot_log_zg_th_mc_data(pT_lower_cut=600, pT_upper_cut=10000, zg_cut='0.1', zg_filename='zg_1', ratio_denominator='data', theory=1, mc=1, data=1, n_bins=2, y_max_limit=15, y_limit_ratio_plot=0.5)
# plot_log_zg_th_mc_data(pT_lower_cut=600, pT_upper_cut=10000, zg_cut='0.2', zg_filename='zg_2', ratio_denominator='data', theory=1, mc=1, data=1, n_bins=2, y_max_limit=15, y_limit_ratio_plot=1.0)






# plot_charged_and_all_zgs(pT_lower_cut=150, pT_upper_cut=10000, zg_cut='0.05', zg_filename='zg_05', n_bins=8, y_max_limit=14)
# plot_charged_and_all_zgs(pT_lower_cut=150, pT_upper_cut=10000, zg_cut='0.1', zg_filename='zg_1', n_bins=8, y_max_limit=10)
# plot_charged_and_all_zgs(pT_lower_cut=150, pT_upper_cut=10000, zg_cut='0.2', zg_filename='zg_2', n_bins=8, y_max_limit=10)

# plot_charged_and_all_zgs(pT_lower_cut=300, pT_upper_cut=10000, zg_cut='0.05', zg_filename='zg_05', n_bins=4, y_max_limit=15)
# plot_charged_and_all_zgs(pT_lower_cut=300, pT_upper_cut=10000, zg_cut='0.1', zg_filename='zg_1', n_bins=4, y_max_limit=15)
# plot_charged_and_all_zgs(pT_lower_cut=300, pT_upper_cut=10000, zg_cut='0.2', zg_filename='zg_2', n_bins=4, y_max_limit=15)

# plot_charged_and_all_zgs(pT_lower_cut=600, pT_upper_cut=10000, zg_cut='0.05', zg_filename='zg_05', n_bins=2, y_max_limit=15)
# plot_charged_and_all_zgs(pT_lower_cut=600, pT_upper_cut=10000, zg_cut='0.1', zg_filename='zg_1', n_bins=2, y_max_limit=15)
# plot_charged_and_all_zgs(pT_lower_cut=600, pT_upper_cut=10000, zg_cut='0.2', zg_filename='zg_2', n_bins=2, y_max_limit=15)



# plot_zg_pfc_pt_cut(pT_lower_cut=150, pT_upper_cut=10000, zg_cut='0.05', zg_filename='zg_05', n_bins=8, y_max_limit=18)
# plot_zg_pfc_pt_cut(pT_lower_cut=150, pT_upper_cut=10000, zg_cut='0.1', zg_filename='zg_1', n_bins=8, y_max_limit=10)
# plot_zg_pfc_pt_cut(pT_lower_cut=150, pT_upper_cut=10000, zg_cut='0.2', zg_filename='zg_2', n_bins=8, y_max_limit=10)

# plot_zg_pfc_pt_cut(pT_lower_cut=300, pT_upper_cut=10000, zg_cut='0.05', zg_filename='zg_05', n_bins=4, y_max_limit=15)
# plot_zg_pfc_pt_cut(pT_lower_cut=300, pT_upper_cut=10000, zg_cut='0.1', zg_filename='zg_1', n_bins=4, y_max_limit=15)
# plot_zg_pfc_pt_cut(pT_lower_cut=300, pT_upper_cut=10000, zg_cut='0.2', zg_filename='zg_2', n_bins=4, y_max_limit=15)

# plot_zg_pfc_pt_cut(pT_lower_cut=600, pT_upper_cut=10000, zg_cut='0.05', zg_filename='zg_05', n_bins=2, y_max_limit=15)
# plot_zg_pfc_pt_cut(pT_lower_cut=600, pT_upper_cut=10000, zg_cut='0.1', zg_filename='zg_1', n_bins=2, y_max_limit=15)
# plot_zg_pfc_pt_cut(pT_lower_cut=600, pT_upper_cut=10000, zg_cut='0.2', zg_filename='zg_2', n_bins=2, y_max_limit=15)



# plot_trigger_efficiency_curves("HLT_Jet30U", "HLT_Jet15U", pT_upper_limit=200)
# plot_trigger_efficiency_curves("HLT_Jet50U", "HLT_Jet30U", pT_upper_limit=300)
# plot_trigger_efficiency_curves("HLT_Jet70U", "HLT_Jet50U", pT_upper_limit=350)
# plot_trigger_efficiency_curves("HLT_Jet100U", "HLT_Jet70U", pT_upper_limit=800)
# plot_trigger_efficiency_curves("HLT_Jet140U", "HLT_Jet100U", pT_upper_limit=800)
# plot_trigger_efficiency_curves("HLT_Jet180U", "HLT_Jet140U", pT_upper_limit=1200)


# plot_all_trigger_efficiency_curves()


# plot_turn_on_curves()


# Version 3 Ends Here.


# call(["python", "/home/aashish/root-6.04.06/macros/MODAnalyzer/utilities/sync_plots.py"])