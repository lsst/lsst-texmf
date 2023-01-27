.. _overleaf:

##############################
Using lsst-texmf with overleaf
##############################

If you wish to edit and  ``lsst-texmf`` document on Overleaf you must make some changes on overleaf.

- on the Overleaf Menu choose setting and switch the compiler to ``LuaLaTex``
- In the same settings menu choose the Main Document to be the AAATN-NNN.tex
- create ``latexmakerc``  with contents as listed below.

.. code-block:: bash

   $ENV{'TZ'}='America/Los_Angeles';
   $ENV{'TEXMFHOME'}='./texmf';
   $ENV{'TEXINPUTS'}='./texmf//:' . $ENV{'TEXINPUTS'};
   $ENV{'BSTINPUTS'}='./texmf//:' . $ENV{'BSTINPUTS'};

Then overleaf should be able to compile the document. 
