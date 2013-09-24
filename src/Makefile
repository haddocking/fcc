#####################################
#                                   #
#         FCC Clustering            #
#             Makefile              #
#                                   #
#####################################

CPP=g++
CPFLAGS=-O2

EXEC=contact_inter contact_inter_lig contact_intra_lig

all: 
	make $(EXEC)

contact_inter: contact_inter.cpp
	$(CPP) $(CPFLAGS) -o contact_inter contact_inter.cpp

contact_inter_lig: contact_inter_lig.cpp
	$(CPP) $(CPFLAGS) -o contact_inter_lig contact_inter_lig.cpp

contact_intra_lig: contact_intra_lig.cpp
	$(CPP) $(CPFLAGS) -o contact_intra_lig contact_intra_lig.cpp
	   
clean :
	/bin/rm $(EXEC)

