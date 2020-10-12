## Example

```bash
$ cd pdbs

$ gunzip *

$ ls *pdb > pdb.list

$ python ../../scripts/make_contacts.py -f pdb.list -n 4

$ sed -e 's/pdb/contacts/' pdb.list| sed -e '/^$/d' > pdb.contacts

$ python ../../scripts/calc_fcc_matrix.py -f pdb.contacts -o fcc_matrix.out
 + BEGIN: Mon Oct 12 16:11:50 2020
 + Parsing 200 contact files
 + Calculating Matrix
 + Writing matrix to fcc_matrix.out
 + END: Mon Oct 12 16:11:50 2020 [  0.48 seconds elapsed]

$ python ../../scripts/cluster_fcc.py fcc_matrix.out 0.6 -o clusters_0.6.out
 + BEGIN: Mon Oct 12 16:12:45 2020
 + Read 200x200 distance matrix in 0 seconds
 + Writing 2 Clusters
 + Coverage 4.00% (8/200)
 + END: Mon Oct 12 16:12:46 2020 [0.04 seconds]

$ cat clusters_0.6.out 
Cluster 1 -> 179 2 123 142 
Cluster 2 -> 50 5 38 149 
```
