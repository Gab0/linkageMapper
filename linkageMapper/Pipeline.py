#!/bin/python

from ruffus import *
import os
import argparse
import pandas as pd

import linkageMapper
import subprocess

from Bio.Align.Applications import ClustalwCommandline

from linkageMapper.logo import logo

class Options():
    def __init__(self, options):
        self.__dict__.update(options)

@active_if(lambda: options.DoAmplicon)
@subdivide(lambda: options.PrimerFile, formatter(), "*.fasta")
def find_primers(primerFile, outputPath):

    finderOptions = {
        "primerFile": primerFile,
        "outputPath": outputPath,
        "WantedLoci": ""
    }

    linkageMapper.primerFinder.Execute(Options(finderOptions))

@active_if(lambda: options.DoAlignment)
def run_alignment(filePrefix):
    infile = filePrefix + ".fasta"
    outfile = filePrefix + ".aln"

    aln_cmd = ClustalwCommandline("clustalw2", infile=infile, outfile=outfile)
    stdout, stderr = aln_cmd()

    print(stdout)

    infile = filePrefix + ".aln"
    tree_cmd = ClustalwCommandline("clustalw2", infile=infile, tree=True)
    tree_cmd()


def draw_tree(filePrefix):
    infile = filePrefix + ".ph"
    outfile = filePrefix + "pdf"

    treeOptions = Options({
        "InputFile": infile,
        "OutputFile": outfile
    })

    linkageMapper.DrawGraphics.drawTree.Execute(treeOptions)


def run_meshclust(filePrefix):
    subprocess.run(["meshclust",
                    filePrefix + ".fasta",
                    "--output",
                    filePrefix + ".clst",
                    "--id", "0.999",
                    "--align"])


def detect_mutations(filePrefix):
    infile = filePrefix + ".aln"

    mutationsOptions = Options({
        "InputFile": infile,
        "PlotSubtitle": ""
    })

    linkageMapper.detectMutations.Execute(mutationsOptions)


def matrix_analysis(WorkingDirectory):
    analysisOptions = Options({
        "InputDirectory": WorkingDirectory,
        "updateOnly": False
    })

    linkageMapper.compareHeatmap.Execute(analysisOptions)
    linkageMapper.matrixAnalysis.Execute(analysisOptions)


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("-p", dest="PrimerFile")

    parser.add_argument("--noamplicon", dest="DoAmplicon",
                        action="store_false", default=True)

    parser.add_argument("--noalign", dest="DoAlignment",
                        action="store_false", default=True)

    parser.add_argument("--alnmode", dest="AlignmentMode",
                        default="clustal")

    parser.add_argument("--dir", dest="WorkingDirectory")
    options = parser.parse_args()

    return options


def main():
    options = parse_arguments()

    # -- SELECT WORKING DIRECTORY;
    if options.WorkingDirectory:
        WorkingDirectory = options.WorkingDirectory

    else:
        AnalysisCode = os.path.splitext(options.PrimerFile)[0]
        AnalysisCode = os.path.basename(AnalysisCode)

        WorkingDirectory = os.path.join("analysisResults",
                                        AnalysisCode)

    # -- TEST CLUSTALW2 SETUP;
    try:
        # this is giving problems.. maybe ask on Biopython issues.
        if False:
            test_clustal = ClustalwCommandline("clustalw2")
            stdout, stderr = test_clustal()
            print(stdout)
            print(stderr)
    except Exception as e:
        print(e)
        print("Clustalw2 not found! Aborting...")
        exit(1)

    if not os.path.isdir(WorkingDirectory):
        print("Creating %s." % WorkingDirectory)
        os.mkdir(WorkingDirectory)

    # SHOW BEAUTIFUL ASCII ART;
    print(logo)

    ruffusMode = False
    # RUN NORMALLY;
    if not ruffusMode:
        if options.DoAmplicon:
            find_primers(options.PrimerFile, WorkingDirectory)

        AllowedAlignModes = ["clustal"]
        if options.AlignmentMode not in AllowedAlignModes:
            print("Unknown alignment mode %s." % (options.AlignmentMode))
            exit(1)

        MatchedPrimersPath = os.path.join(WorkingDirectory, "MatchedPrimers.csv")
        SucessfulLoci = pd.read_csv(MatchedPrimersPath)["LocusName"]

        if options.DoAlignment:
            for locusName in SucessfulLoci:
                filePrefix = os.path.join(WorkingDirectory, "LOCI_" + locusName)
                print("Running alignment for %s..." % locusName)
                run_alignment(filePrefix)
                # draw_tree(filePrefix)
                detect_mutations(filePrefix)
                run_meshclust(filePrefix)

        matrix_analysis(WorkingDirectory)

    # RUN BY RUFFUS;
    else:
        pipeline_run()


if __name__ == "__main__":
    main()