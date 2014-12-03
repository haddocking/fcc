#!/usr/bin/env python
# -*- coding: UTF-8  -*-

"""
Asymmetric Taylor-Butina Disjoint Clustering Algorithm.

Authors:
           RODRIGUES Joao
           TRELLET Mikael
           MELQUIOND Adrien
"""

class Element(object):
    """Defines a 'clusterable' Element"""

    def __init__(self, name):
        self.name = name
        self.cluster = 0
        self.neighbors = []


    def add_neighbor(self, neighbor):
        """Adds another element to the neighbor list"""
        nlist = self.neighbors
        nlist.append(neighbor)

    def assign_cluster(self, clust_id):
        """Assigns the Element to Cluster. 0 if unclustered"""
        self.cluster = clust_id

class Cluster(object):
    """Defines a Cluster. A Cluster is created with a name and a center (Element class)"""

    def __init__(self, name, center):
        
        self.name = name
        self.center = center

        self.members = []
        self.fs_members = []
        
        self.populate()
        
    def __len__(self):
        return len(self.members)+len(self.fs_members)+1 # +1 Center
    
    def populate(self):
        """
        Populates the Cluster member list through the 
        neighbor list of its center.
        """

        name = self.name
        # Assign center
        ctr = self.center
        ctr.assign_cluster(name)
        
        mlist = self.members
        # Assign members
        ctr_nlist = (n for n in ctr.neighbors if not n.cluster)
        for e in ctr_nlist:
            mlist.append(e)
            e.assign_cluster(name)
    
    def add_member(self, element, fs=False):
        """
        Adds one single element to the cluster.
        Allows signaling of fs
        """
        if fs:
            l = self.fs_members
        else:
            l = self.members
            
        l.append(element)
        element.assign_cluster(self.name)

def read_matrix(path, cutoff):
    """ 
    Reads in a four column matrix (1 2 0.123 0.456\n) 
    and creates an dictionary of Elements.
    """

    cutoff = float(cutoff)

    elements = {}

    f = open(path, 'r')
    for line in f:
        ref, mobi, dRM, dMR = line.split()
        ref = int(ref)
        mobi = int(mobi)
        dRM = float(dRM)
        dMR = float(dMR)

        # Create or Retrieve Elements
        if ref not in elements:
            r = Element(ref)
            elements[ref] = r
        else:
            r = elements[ref]
        
        if mobi not in elements:
            m = Element(mobi)
            elements[mobi] = m
        else:
            m = elements[mobi]    

        # Assign neighbors
        if dRM > cutoff:
            r.add_neighbor(m)
        if dMR > cutoff:
            m.add_neighbor(r)

    f.close()

    return elements

def remove_true_singletons(element_pool):
    """ Removes from the pool elements without any neighbor """
    
    ep = element_pool

    ts = set([e for e in ep if not ep[e].neighbors])
    for e in ts:
        del ep[e]
    
    return (ts, ep)

def cluster_elements(element_pool, threshold):
    """ 
    Groups Elements within a given threshold 
    together in the same cluster.
    """
    
    clusters = []
    threshold -= 1 # Account for center
    ep = element_pool
    cn = 1 # Cluster Number
    while 1:
        # Clusterable elements
        ce = [e for e in ep if not ep[e].cluster]
        if not ce: # No more elements to cluster
            break
        
        # Select Cluster Center
        # Element with largest neighbor list
        ctr_nlist, ctr = sorted([(len([se for se in ep[e].neighbors if not se.cluster]), e) for e in ce])[-1]
        
        # Cluster until length of remaining elements lists are above threshold
        if ctr_nlist < threshold:
            break
        
        # Create Cluster
        c = Cluster(cn, ep[ctr])
        cn += 1
        clusters.append(c)

    return (ep, clusters)

def find_false_singletons(element_pool, true_singletons):
    
    ep = element_pool
    ts = true_singletons
    
    unclustered = (e for e in ep if not ep[e].cluster)

    # Filter True Singleton Orphans while searching
    fs_list = [e for e in unclustered if not set([se.name for se in ep[e].neighbors]).intersection(ts)]

    return fs_list

def output_clusters(handle, clusters):
    """Outputs the cluster name, center, and members."""

    write = handle.write

    for c in clusters:
        write( "Cluster %s -> %s " %(c.name, c.center.name) )
        for m in c.members:
            write( "%s " %m.name )
        for fs in c.fs_members:
            write( "%s* "%fs.name)
        write("\n")

if __name__ == "__main__":

    import optparse
    import sys
    from time import time, ctime
    import os

    USAGE="%s <matrix file> <threshold [float]> [options]" %os.path.basename(sys.argv[0])

    parser = optparse.OptionParser(usage=USAGE)
    parser.add_option('-o', '--output', dest="output_handle", action='store', type='str',
                    default=sys.stdout,
                    help='Output File [STDOUT]')
    parser.add_option('-c', '--cluster-size', dest="clus_size", action="store", type="int",
                    default=4, 
                    help="Minimum number of elements in a cluster [4]")
    parser.add_option('-f', '--include-false-singletons', dest="ifs", action="store_true", 
                    default=False,
                    help="Post-clustering step to include false singletons in the existing clusters.[False]")

    (options, args) = parser.parse_args()

    if sys.version_info[0:2] < (2,6):
        cur_version = "%s.%s" %sys.version_info[0:2]
        sys.stderr.write("- Python version not supported (%s). Please use 2.5 or newer.\n" %cur_version )
        sys.exit(1)
    if len(args) != 2:
        sys.stderr.write("- Invalid number of arguments: %i\n" %len(args))
        sys.stderr.write("USAGE: %s\n" %USAGE)
        sys.exit(1)
    
    fmatrix, cutoff = args
    cutoff = float(cutoff)
    
    # Read Matrix
    sys.stderr.write("+ BEGIN: %s\n" %ctime())
    t_init = time()

    try:
        pool = read_matrix(fmatrix, cutoff)
    except IOError:
        sys.stderr.write("File not found: %s\n" %fmatrix)
        sys.exit(1)

    sys.stderr.write("+ Read %ix%i distance matrix in %i seconds\n" %(len(pool), len(pool), int(time()-t_init)))
    
    ts, n_pool = remove_true_singletons(pool)
    sys.stderr.write("+ Detected %i True Singletons\n" %len(ts))

    # Cluster
    element_pool, clusters = cluster_elements(n_pool, options.clus_size)
    
    # Whatever elements are left in the element_pool are
    # considered false singletons and have to be reassigned
    # to relevant clusters
    # Exception are elements that have 0 neighbors, which were neighbors
    # of True Singletons and were not discarded after their signalling.
    if options.ifs:
        ep = element_pool
        fs_list = find_false_singletons(ep, ts)
        sys.stderr.write("+ Reinserting %i False Singletons\n" %len(fs_list))
        for fs in fs_list:
            # Check which cluster is most represented in its neighbors
            clist = [ep[e.name].cluster for e in ep[fs].neighbors]
            max_freq = int(sorted([(clist.count(c), c) for c in clist])[-1][1])
            if not max_freq: # Cluster 0 == no cluster
                continue
            # Append FS to Cluster
            cluster = clusters[max_freq-1]
            cluster.add_member(ep[fs], fs=True)

    # Output Clusters
    o = options.output_handle
    if isinstance(o, str):
        o_handle = open(o, 'w')
    else:
        o_handle = o

    sys.stderr.write("+ Writing %i Clusters\n" %len(clusters))
    output_clusters(o_handle, clusters)
    if isinstance(o, str):
        o_handle.close()

    total_elements = len(element_pool)+len(ts)
    clustered = sum([len(c) for c in clusters])
    # Calculate coverage
    clust_coverage = clustered*100/float(total_elements)
    sys.stderr.write("+ Coverage %3.2f%% (%i/%i)\n" %(clust_coverage, clustered, total_elements))
    t_elapsed = time()-t_init
    sys.stderr.write( "+ END: %s [%3.2f seconds]\n" %(ctime(), t_elapsed))
