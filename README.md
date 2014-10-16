FCC Clustering Algorithm
========================

*Fraction of Common Contacts Clustering Algorithm for Protein Models from Structure Prediction Methods*

About FCC
---------

Structure prediction methods generate a large number of models of which only a fraction matches the biologically relevant structure. To identify this (near-)native model, we often employ clustering 
algorithms, based on the assumption that, in the energy landscape of every biomolecule, its native state lies in a wide basin neighboring other structurally similar states. RMSD-based clustering, the 
current method of choice, is inadequate for large multi-molecular complexes, particularly when their components are symmetric. We developed a novel clustering strategy that is based on a very 
efficient similarity measure - the fraction of common contacts. The outcome of this calculation is a number between 0 and 1, which corresponds to the fraction of residue pairs that are present in 
both the reference and the mobile complex.

Advantages of FCC clustering vs. RMSD-based clustering:
* 100-times faster on average.
* Handles symmetry by consider complexes as entities instead of collections of chains.
* Does not require atom equivalence (clusters mutants, missing loops, etc).
* Handles any molecule type (protein, DNA, RNA, carbohydrates, lipids, ligands, etc).
* Allows multiple levels of "resolution": chain-chain contacts, residue-residue contacts, residue-atom contacts, etc.

How to Cite
-----------
Rodrigues JPGLM, Trellet M, Schmitz C, Kastritis P, Karaca E, Melquiond ASJ, Bonvin AMJJ. 
[Clustering biomolecular complexes by residue contacts similarity.] [1]
Proteins: Structure, Function, and Bioinformatics 2012;80(7):1810–1817.

Requirements
------------

* Python 2.6+
* C/C++ Compiler

Installation
------------

Navigate to the src/ folder and issue 'make' to compile the contact programs.
Edit the Makefile if necessary (e.g. different compiler, optimization level).

Usage
------------

All scripts produce usage documentation if called without any arguments. Further,
the '-h' option produces (for Python scripts) a more detailed help with descriptions
of all available options.

For most cases, the following setup is enough:

    # Make a file list with all your PDB files
    ls *pdb > pdb.list
    
    # Ensure all PDB models have segID identifiers
    # Convert chainIDs to segIDs if necessary using scripts/pdb_chainxseg.py
    for pdb in $( cat pdb.list ); do pdb_chainxseg.py $pdb > temp; mv temp $pdb; done

    # Generate contact files for all PDB files in pdb.list
    # using 4 cores on this machine.
    python2.6 make_contacts.py -f pdb.list -n 4

    # Create a file listing the names of the contact files
    # Use file.list to maintain order in the cluster output
    sed -e 's/pdb/contacts/' pdb.list | sed -e '/^$/d' > pdb.contacts

    # Calculate the similarity matrix
    python2.6 calc_fcc_matrix.py -f pdb.contacts -o fcc_matrix.out

    # Cluster the similarity matrix using a threshold of 0.75 (75% contacts in common)
    python2.6 cluster_fcc.py fcc_matrix.out 0.75 -o clusters_0.75.out

    # Use ppretty_clusters.py to output meaningful names instead of model indexes
    python2.6 ppretty_clusters.py clusters_0.75.out pdb.list

Authors
------

João Rodrigues

Mikael Trellet

Adrien Melquiond

Christophe Schmitz

Ezgi Karaca

Panagiotis Kastritis

[Alexandre Bonvin] [2]

[1]: http://www.ncbi.nlm.nih.gov/pubmed/22489062 "FCC @ Pubmed"
[2]: http://nmr.chem.uu.nl/~abonvin "Alexandre Bonvin's Homepage"
