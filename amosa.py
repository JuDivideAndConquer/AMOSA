class AMOSAType:
    i_hardl = int()         # Hardlimit of the archive
    i_softl = int()         # Softlimit of the archive
    i_no_ofiter = int()     # Number of iterations per temperature
    i_hillclimb_no = int()  # Total number of hill_climbing numbers
    i_maxno_bit = int()     # Maximum number of bits used to encode one variable
    i_arrsize = int()       # Total lenght of each string
    i_totalno_var = int()   # Total number of variables of the fucntions
    i_archivesize = int()   # Stores the size of the archive
    i_no_offunc = int()     # Number of functions

    c_problem = str()       # Name of the function to be optimized

    d_tmax = float()        # Maximum temperature
    d_tmin = float()        # Minimum temperature
    d_alpha = float()       # Cooing rate
    dd_solution = []		# Data structure corresponding to binary strings
    dd_archive = []			# Archive
    dd_func_archive = []  	# Variable to store the fucntion values of the archive solutions
    #d_eval = []				# Objective function values
    d_func_range = []		# Range of the functions
    d_min_real_var = []		# Stores minimum value of the real variables
    d_max_real_var = []		# Stores maximum value of the real variables
    i_clustering_type = int()
