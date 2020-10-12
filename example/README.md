## Example

```bash
$ cd pdbs

$ gunzip *

$ python ../../scripts/make_contacts.py `ls *pdb`

$ python ../../scripts/calc_fcc_matrix.py `ls *contacts` > fcc.matrix
 + BEGIN: Mon Oct 12 16:01:59 2020
 + Parsing 200 contact files
 + Calculating Matrix
 + Writing matrix to <stdout>
 + END: Mon Oct 12 16:01:59 2020 [  0.09 seconds elapsed]

$ python ../../scripts/cluster_fcc.py fcc.matrix 0.7 > cluster.out   
 + BEGIN: Mon Oct 12 16:02:34 2020
 + Read 200x200 distance matrix in 0 seconds
 + Writing 2 Clusters
 + Coverage 4.00% (8/200)
 + END: Mon Oct 12 16:02:34 2020 [0.03 seconds]

$ cat cluster.out 
Cluster 1 -> 179 2 123 142 
Cluster 2 -> 50 5 38 149 
```
