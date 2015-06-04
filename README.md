# CMSOpenDataAnalyzer

This repository has code to analyze CMS Open Data data produced using [https://github.com/tripatheea/CMSOpenDataProducer][1].

### How to Install/Use
 - Install [FastJet][2]. Note the path to FastJet config. 
 - Open `./Makefile` and paste the path to FastJet config to the **PATH\_TO\_FASTJET** variable.
 - Run [CMSOpenDataProducer][3]. It will output a `.dat` file. Copy it to the `./data/` directory.
 - Compile everything with `make`.
 - Move to the 'bin' directory and run the analyzer. Supply the path to the data file to the analyzer. 

  ``cd bin``
   
   ``./analysis ../data/pfcandidates.dat``

 - The code will output a `DAT` file `./data/output.dat`.
 - To make the plots, move to the directory `./root`.
 - Run root and compile/execute the file `plots.cc`

  ``root ``

  ``.x plots.cc+`` 

## TODO
- [] Add jet energy correction factors to AK5/AK7
- [] Write a simple analysis that double checks that PFCandidates yield the same AK5/7 jets as CMS finds.
- [] Get Pythia 8 up and running and generate simulated data (with simulated triggers)
- [] Figure out if there is any way to get luminosity information.

[1]: https://github.com/tripatheea/CMSOpenDataProducer
  [2]: http://www.fastjet.fr/
  [3]: https://github.com/tripatheea/CMSOpenDataProducer