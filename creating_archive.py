from amosa import AMOSAType
from test_func import evaluate
import copy


def creating_archive(amosaParams):
    '''Initialize the archive according to the dd_solution'''
    dd_area = []
    d_eval = []
    i_flag = []
    # Flag == 0 dominated | Flag == 1 non-dominated

    # Storing the output of the solutions dd_area
    for i in range(amosaParams.i_softl):
        d_eval = evaluate(
            amosaParams.dd_solution[i], amosaParams.c_problem, amosaParams.i_no_offunc)
        d_area = []
        for j in range(amosaParams.i_no_offunc):
            d_area.append(d_eval[j])
        dd_area.append(d_area)
        i_flag.append(1)

    # Checking for dominated solutions, if the solutions are dominated their flag is set to 0
    for i in range(amosaParams.i_softl):
        if(i_flag[i] == 1):
            j = i+1
            while(j in range(i+1, amosaParams.i_softl) and i_flag[i] == 1):
                if(i_flag[j] == 1):
                    count0 = 0
                    count1 = 0
                    for h in range(amosaParams.i_no_offunc):
                        if (dd_area[i][h] >= dd_area[j][h]):
                            count0 = count0 + 1
                        elif (dd_area[i][h] <= dd_area[j][h]):
                            count1 = count1 + 1
                    if(count0 == amosaParams.i_no_offunc):
                        i_flag[i] = 0
                    elif(count1 == amosaParams.i_no_offunc):
                        i_flag[j] = 0
                j = j + 1

    # Storing the non-dominated solutions to the archive
    archive_size = 0
    for i in range(amosaParams.i_softl):
        if(i_flag[i] == 1):
            
            archive = copy.deepcopy(amosaParams.dd_solution[i])
            amosaParams.dd_archive.append(archive)
            
            func_archive = copy.deepcopy(dd_area[i])
            amosaParams.dd_func_archive.append(func_archive)
            
            archive_size = archive_size + 1
    amosaParams.i_archivesize = archive_size
    
    print(len(amosaParams.dd_archive))
    print(len(amosaParams.dd_func_archive))
