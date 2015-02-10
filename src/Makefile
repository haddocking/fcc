#####################################
#                                   #
#         FCC Clustering            #
#             Makefile              #
#                                   #
#####################################

CPP=g++
CPFLAGS=-O2

EXEC=contact_fcc contact_fcc_lig

all: 
	make $(EXEC)

contact_fcc: contact_fcc.cpp
	$(CPP) $(CPFLAGS) -o contact_fcc contact_fcc.cpp

contact_fcc_lig: contact_fcc_lig.cpp
	$(CPP) $(CPFLAGS) -o contact_fcc_lig contact_fcc_lig.cpp

contact_fcc_intra: contact_fcc_intra.cpp
	$(CPP) $(CPFLAGS) -o contact_fcc_intra contact_fcc_intra.cpp

clean :
	/bin/rm $(EXEC)

