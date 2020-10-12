#!/usr/bin/env python
# -*- coding: UTF-8  -*-

"""
Calculates a matrix of fraction of common contacts between two or more structures.

Authors:
        RODRIGUES Joao
        TRELLET Mikael
        MELQUIOND Adrien
"""
import optparse
import sys
from time import time, ctime
import os


# Contact Parsing routines
def parse_contact_file(f_list, ignore_chain):
    """Parses a list of contact files."""

    if ignore_chain:
        contacts = [[int(line[0:5] + line[6:-1]) for line in open(con_f)] for con_f in f_list if con_f.strip()]
    else:
        contacts = [set([int(line) for line in open(con_f)]) for con_f in f_list if con_f.strip()]

    return contacts


# FCC Calculation Routine
def calculate_fcc(list_a, list_b):
    """
    Calculates the fraction of common elements between two lists
    taking into account chain IDs
    """

    cc = len(list_a.intersection(list_b))
    cc_v = len(list_b.intersection(list_a))

    return cc, cc_v


def calculate_fcc_nc(list_a, list_b):
    """
    Calculates the fraction of common elements between two lists
    not taking into account chain IDs. Much Slower.
    """

    largest, smallest = sorted([list_a, list_b], key=len)
    ncommon = len([ele for ele in largest if ele in smallest])
    return ncommon, ncommon


# Matrix Calculation
def calculate_pairwise_matrix(contacts, ignore_chain):
    """ Calculates a matrix of pairwise fraction of common contacts (FCC).
        Outputs numeric indexes.

        contacts: list_of_unique_pairs_of_residues [set/list]
        
        Returns pairwise matrix as an iterator, each entry in the form:
        FCC(cplx_1/cplx_2) FCC(cplx_2/cplx_1)
    """

    contact_lengths = []
    for con in contacts:
        try:
            ic = 1.0 / len(con)
        except ZeroDivisionError:
            ic = 0
        contact_lengths.append(ic)

    if ignore_chain:
        calc_fcc = calculate_fcc_nc
    else:
        calc_fcc = calculate_fcc

    for i in range(len(contacts)):

        for k in range(i + 1, len(contacts)):
            cc, cc_v = calc_fcc(contacts[i], contacts[k])
            fcc, fcc_v = cc * contact_lengths[i], cc * contact_lengths[k]
            yield i + 1, k + 1, fcc, fcc_v


def _output_fcc(output, values, f_buffer):
    buf = []
    for i in values:
        buf.append(i)
        if len(buf) == f_buffer:
            output(''.join(["%s %s %1.3f %1.3f\n" % (i[0], i[1], i[2], i[3]) for i in buf]))
            buf = []
    output(''.join(["%s %s %1.3f %1.3f\n" % (i[0], i[1], i[2], i[3]) for i in buf]))


if __name__ == '__main__':

    USAGE = "%s <contacts file 1> <contacts file 2> ... [options]\n" % os.path.basename(sys.argv[0])

    parser = optparse.OptionParser(usage=USAGE)
    parser.add_option('-o', '--output', dest="output_file", action='store', type='string',
                      default=sys.stdout,
                      help='Output File [default: STDOUT]')
    parser.add_option('-f', '--file', dest="input_file", action='store', type='string',
                      help='Input file (one contact file name per line)')
    parser.add_option('-b', '--buffer_size', dest="buffer_size", action='store', type='string',
                      default=50000,
                      help='Buffer size for writing output. Number of lines to cache before writing to file [default: '
                           '50000]')
    parser.add_option('-i', '--ignore_chain', dest="ignore_chain_char", action='store_true',
                      help='Ignore chain character in residue code. Use for homomeric complexes.')

    (options, args) = parser.parse_args()

    if sys.version_info[0:2] < (3, 8):
        cur_version = "%s.%s" % sys.version_info[0:2]
        sys.stderr.write("- Python version not supported (%s). Please use 3.8 or newer.\n" % cur_version)
        sys.exit(1)

    if options.input_file:
        args = [name.strip() for name in open(options.input_file)]

    if len(args) < 2:
        sys.stderr.write("- Provide (at least) two structures to calculate a matrix. You provided %s.\n" % len(args))
        sys.stderr.write(USAGE)
        sys.exit(1)

    sys.stderr.write("+ BEGIN: %s\n" % ctime())
    if options.ignore_chain_char:
        sys.stderr.write("+ Ignoring chains. Expect a considerable slowdown!!\n")
        exclude_chains = True
    else:
        exclude_chains = False

    t_init = time()
    sys.stderr.write("+ Parsing %i contact files\n" % len(args))

    c = parse_contact_file(args, exclude_chains)

    m = calculate_pairwise_matrix(c, exclude_chains)

    if isinstance(options.output_file, str):
        f = open(options.output_file, 'w')
    else:
        f = options.output_file

    sys.stderr.write("+ Calculating Matrix\n")  # Matrix is calculated when writing. Generator property.
    sys.stderr.write("+ Writing matrix to %s\n" % f.name)
    _output_fcc(f.write, m, options.buffer_size)

    if isinstance(options.output_file, str):
        f.close()
    t_elapsed = time() - t_init
    sys.stderr.write("+ END: %s [%6.2f seconds elapsed]\n" % (ctime(), t_elapsed))
