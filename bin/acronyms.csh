#!/bin/csh

####
#Better use ant acronyms from the build.xml in DOCCOMMON.
####


#------------------------------------------------------------------------------
#
#                      Gaia Science Operations Centre
#                     European Space Astronomy Centre
#
#                   (c) 2005-2020 European Space Agency
#
#-----------------------------------------------------------------------------


if(`echo $0|grep /|wc -l` == 1 ) then
  set install_dir=`echo $0 | awk -F\/ '{for(i=1;i<NF;i++) printf("%s/", $i)}'`
else
  set acr = `which $0`
  set install_dir=`echo $acr | awk -F\/ '{for(i=1;i<NF;i++) printf("%s/", $i)}'`
endif

set myacronyms=$install_dir/myacronyms.tex
set skipacronyms=$install_dir/skipacronyms.tex

cat $install_dir/myacronyms.tex >> $$_myacronyms.tex
cat $install_dir/skipacronyms.tex >> $$_skipacronyms.tex

if(-e $PWD/myacronyms.tex) then
	cat $PWD/myacronyms.tex >> $$_myacronyms.tex
endif

if(-e $PWD/skipacronyms.tex) then
	cat $PWD/skipacronyms.tex >> $$_skipacronyms.tex
endif



java -jar $install_dir/GaiaAcr.jar -u https://gaia.esac.esa.int/gpdb/glossary.txt -m $$_myacronyms.tex -s $$_skipacronyms.tex $*


/bin/rm $$_myacronyms.tex $$_skipacronyms.tex
