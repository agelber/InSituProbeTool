# InSituProbeTool
Automate primer design for ISH probes, useful if doing large numbers of genes

to run download files, create gene list file `genes.txt`, one gene per line (example included)
run 

`./primergen.sh genes.txt output_directory`

Will not work if you don't run from within directory. Requires `BioPython` and `primer3` python packages.
