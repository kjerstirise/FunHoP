#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from collections import Counter


def load_SINGLE(fnm):

    infile = open(fnm,'r')
    lines = infile.readlines()
    nms = []
    for line in lines:
        nms.append(line.strip())
    nms = np.array(nms)

    return(nms)


def in1d2(a,b):

    idbol = np.array([item in b for item in a])
    idbin = np.zeros(len(a), int)
    idd = np.where(idbol == 1)[0]
    idbin[idd] = 1

    return(idbin)


def load_FILE(fname, spt = '\t'):

    infile = open(fname,'r')
    lines = infile.readlines()
    peaks = []
    for line in lines:
        cols = line.split(spt)
        cols[-1] = cols[-1].strip()
        peaks.append(cols)
    peaks = np.array(peaks)

    return(peaks)


def replace_gnms_single2(gnms, gsmb):

    # which gene-names to replace
    idd0 = in1d2(gnms,gsmb[:,0])
    idd0 = np.where(idd0 == 1)[0]
    ngnms = gnms.copy()
    rptbl = []
    # replace selected gene-names
    for i in idd0:
        gni = gnms[i]
        idd1 = np.where(gsmb[:,0] == gni)[0]
        gnn = gsmb[idd1, 2]
        # Check if gene already exist
        idd2 = np.where(ngnms == gnn[0])[0]
        if len(idd2) == 0:
            ngnms[i] = gnn[0]
            vec = [gni,'replaced by',gnn[0],'accepted']
        if len(idd2) > 0:
            vec = [gni,'replaced by',gnn[0],'rejected']
        rptbl.append(vec)
    rptbl = np.array(rptbl)
        
    return(ngnms, rptbl)


 
def load_genenames(expression_path):
    gnms = load_FILE(expression_path)[1:,0]
    
    return(gnms)


def load_countdata(count_file_path, gnms, correct):
    # count-data
    exprs = load_FILE(count_file_path)
    valst = exprs.astype(float)
    if correct:
        valst = correcting_on_genelength(gnms = gnms, 
                                         gene_length_path = 'gene_length_nov16.txt',
                                         valst = valst)

    return(valst)


def define_groups(meta_data_path):
    # metadata
    metad = load_FILE(meta_data_path)[1:]

    # cancer and normal samples
    canid = np.where(metad[:,6] == 'TP')[0]
    ctrid = np.where(metad[:,6] == 'NT')[0]

    return(canid, ctrid)


def load_KEGG_pathway_info(genelist_path):
    pthw = load_SINGLE(genelist_path)
    unpw = np.unique(pthw)
    return(unpw)




def correcting_on_genelength(gnms, gene_length_path, valst):

    # load gene-length table
    gsz = load_FILE(gene_length_path)
    #glns = gsz[:, 1].astype(np.double)
    glns = gsz[:, 1].astype(float)
    mgln = np.mean(glns)

    # gene lengths for each gene in gnms
    gzrt = []
    for i in np.arange(len(gnms)):

        gni = gnms[i]
        idi = np.where(gsz[:,0] == gni)[0]
        if len(idi) == 0:
            gzrt.append(1.0)
        if len(idi) > 0:
            rti = mgln/glns[idi]
            gzrt.append(rti)
    gzrt = np.array(gzrt)
    gzrt = gzrt.flatten()
    valst = valst * gzrt
    return(valst)


def update_genenames(gnms, changed_name_path):
    gsmb = load_FILE(changed_name_path)
    idd = np.where(gsmb[:,1] == 'Previous symbol')[0]
    gsmb = gsmb[idd]

    gnmst2,rptbt = replace_gnms_single2(gnms,gsmb)

    return(gnmst2)



def create_boxexpression_and_boxinfo(unpw, gnms, vals):
    ntbl = []
    vnames = []
    templist = []
    templist2 = []
    vnmi2 = ""
    for i in np.arange(len(unpw)):

        bxi = unpw[i]

        if bxi[:4] == '----':
            continue

        cols = bxi.split(' ')
        # only one gene
        if len(cols) == 1:
            gnmi = cols[0]
            vnmi = gnmi + '-B' + str(len(cols))
            idi = np.where(gnms == gnmi)[0]
            # gene not found
            if len(idi) == 0:
                vi = -1 * np.ones(len(vals))
            if len(idi) > 0:
                vi = vals[:, idi].flatten()
            ntbl.append(vi)
            vec = [bxi, vnmi]
            vnames.append(vec)
        if len(cols) > 1:
            gnmm = cols[0]
            nmbg = len(cols)

            vnmi = gnmm + '-B' + str(nmbg)
            while vnmi in templist:
                number = templist.count(vnmi)
                vnmi2 = vnmi + "-" + str(number+1)

            templist.append(vnmi)
            vnmi = vnmi2
            """
            templist2.append(vnmi)
            counts = Counter(templist2) 
            for s,num in counts.items():
                if num > 1: # ignore strings that only appear once
                    for suffix in range(2, num + 1): # suffix starts at 1 and increases by 1 each time
                        templist2[templist2.index(s)] = s + '-' + str(suffix)
            vnmi = templist2[-1]
            """
            
            #if vnmi in templist2:
            #    vnmi = vnmi + "-2"
            #    templist.append(vnmi)
           
            vi = np.zeros(len(vals))
            cnt = 0
            for j in np.arange(len(cols)):
                gnmj = cols[j]
                idj = np.where(gnms == gnmj)[0]
                if len(idj) == 0:
                    continue
                vi = vi + vals[:,idj].flatten()
                cnt += 1
            # no genes found
            if cnt == 0:
                vi = -1 * np.ones(len(vals))
            ntbl.append(vi)
         
            vec = [bxi, vnmi]
            vnames.append(vec)


            
    ntbl = np.array(ntbl)
    vnames = np.array(vnames)
    return(ntbl, vnames)
    

# Calculate total counts and ratios for each box
def calculate_total_counts_and_ratios(vnames, ntbl, gnms, vals, canid, ctrid):
    ntbl2 = []
    for i in np.arange(len(vnames)):

        vnmi = vnames[i]
        gnmi = vnmi[0]
        bvi = ntbl[i]
        #mcnt = mean(bvi)
        mcnt = (np.mean(bvi[canid]) + np.mean(bvi[ctrid]))/2
        gfr = []
        gnmi = gnmi.split(' ')
        for gnm in gnmi:
            idi = np.where(gnms == gnm)[0]
            if len(idi) == 0:
                fri = 'Not-found'
            if len(idi) > 0:
                vi = vals[:, idi].flatten()
                #mci = mean(vi)
                mci = (np.mean(vi[canid]) + np.mean(vi[ctrid]))/2
                fri = mci / mcnt
            gfr.append(fri)
        frcs = ' '.join([str(s) for s in gfr])
        vec = [vnmi[0],vnmi[1],str(mcnt),frcs]
        ntbl2.append(vec)
    ntbl2 = np.array(ntbl2)
    return(ntbl2)

def fix_duplicates(ntbl2):
    # Replace duplicate names metabolism
    ntbl2[29,1] = 'ACOT2-B4-2'
    ntbl2[71,1] = 'AKR1C4-B4-2'
    ntbl2[185,1] = 'B4GALT1-B3-2'
    ntbl2[187,1] = 'B4GALT1-B3-3'
    ntbl2[227,1] = 'CEPT1-B2-2'
    ntbl2[303,1] = 'CYP1A1-B2-2'
    ntbl2[316,1] = 'CYP2A6-B2-2'
    ntbl2[635,1] = 'LPCAT3-B4-2'


##########################################################

def write_boxinfo_table(ntbl2, outfilepath):
    data = pd.DataFrame(data = ntbl2)
    #print(data.head())
    data.to_csv(outfilepath, sep = '\t', mode = 'w', header = False, index = None)
    


def write_expression_table(ntbl2, ntbl, outfilepath):
    rtbl = np.vstack((ntbl2[:,0],ntbl.T))
    rtbl = rtbl.T
    expression_table = pd.DataFrame(data = rtbl)
    expression_table.to_csv(outfilepath, sep = '\t', mode = 'w', header = False, index = None)
    



def calculate_counts(expression_path, meta_data_path, count_file_path,
                     changed_name_path, genelist_path, boxinfo_path, expression_table_path):

    # Load gene names
    gnms = load_genenames(expression_path)
    # Check for unique gene names
    ugnms = np.unique(gnms) # 20502 unique gene-names
    # Handling metadata
    canid, ctrid = define_groups(meta_data_path)
    # Loading RNA-seq data (counts). Correct = True, the counts will be corrected on gene length
    vals = load_countdata(count_file_path = count_file_path, gnms = gnms, correct = False)
    # Updating gene names
    gnms = update_genenames(gnms, changed_name_path)
    # Loading the info about the pathways to analyze
    unpw = load_KEGG_pathway_info(genelist_path)

    # Create the nodes to calculate
    ntbl, vnames = create_boxexpression_and_boxinfo(unpw, gnms, vals)
    # Do the calculations
    ntbl2 = calculate_total_counts_and_ratios(vnames, ntbl, gnms, vals, canid, ctrid)

    # Write the results to file
    write_boxinfo_table(ntbl2 = ntbl2, outfilepath = boxinfo_path)
    write_expression_table(ntbl2 = ntbl2, ntbl = ntbl, outfilepath = expression_table_path)


if __name__ == '__main__':
    calculate_counts(expression_path, meta_data_path, count_file_path, changed_name_path, 
                        genelist_path, boxinfo_path, expression_table_path)
