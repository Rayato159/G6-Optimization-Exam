from CrackBox import Black_Box_Function
import numpy as np

#Function from black box
def f(decode_x1, decode_x2):
    return crack.getFunction(decode_x1, decode_x2)

#Objective Function
def getObjective(chromosome):
    lb_x = -2
    ub_x = 2
    len_x = len(chromosome)//2
    precision_x = (ub_x - lb_x)/(2**len_x - 1)

    z = 0
    t = 1
    x_bit = 0
    x1_bit_sum = 0

    for i in range(len(chromosome)//2):
        x_bit = chromosome[-t]*(2**z)
        x1_bit_sum += x_bit
        z += 1
        t += 1
    
    z = 0
    t = 1 + len(chromosome)//2
    x_bit = 0
    x2_bit_sum = 0

    for i in range(len(chromosome)//2):
        x_bit = chromosome[-t]*(2**z)
        x2_bit_sum += x_bit
        z += 1
        t += 1

    decode_x1 = (x1_bit_sum) * precision_x + lb_x
    decode_x2 = (x2_bit_sum) * precision_x + lb_x

    return (decode_x1, decode_x2, f(decode_x1, decode_x2))

#Tournament selection
def find_parents_ts(all_solution):
    parents = np.empty((0, np.size(all_solution, 1)))

    for i in range(2):
        indices_list = np.random.choice(len(all_solution), 3, replace=False)

        print(f"round {i+1}# {indices_list}", end="\n\n")

        posb_parent_1 = all_solution[indices_list[0]]
        posb_parent_2 = all_solution[indices_list[1]]
        posb_parent_3 = all_solution[indices_list[2]]

        print(posb_parent_1)
        print(posb_parent_2)
        print(posb_parent_3)
        print()

        obj_func_parent_1 = getObjective(posb_parent_1)[2]
        obj_func_parent_2 = getObjective(posb_parent_2)[2]
        obj_func_parent_3 = getObjective(posb_parent_3)[2]

        print(obj_func_parent_1)
        print(obj_func_parent_2)
        print(obj_func_parent_3)
        print()

        min_obj_func = min(obj_func_parent_1, obj_func_parent_2, obj_func_parent_3)

        if min_obj_func == obj_func_parent_1:
            selected_parent = posb_parent_1
        elif min_obj_func == obj_func_parent_2:
            selected_parent = posb_parent_2
        else:
            selected_parent = posb_parent_3
            
        print(f"winner is {selected_parent}")
        print(f"minimum value is {min_obj_func}")
        print("--------------------------------------------------")
        print()

        parents = np.vstack((parents, selected_parent))
    
    parent_1 = parents[0,:]
    parent_2 = parents[1,:]

    return (parent_1, parent_2)

#Crossover
def crossover(parent_1, parent_2, cross_prob=0.8):

    chlid_1 = np.empty((0, len(parent_1)))
    chlid_2 = np.empty((0, len(parent_2)))

    cross_rand_prob = np.random.rand()

    if cross_rand_prob < cross_prob:

        index_1 = np.random.randint(0, len(parent_1))
        index_2 = np.random.randint(0, len(parent_2))

        while index_1 == index_2:
            index_2 = np.random.randint(0, len(parent_2))

        if index_1 > index_2:
            index_1, index_2 = index_2, index_1
        
        #Parent_1
        first_sec_par_1 = parent_1[:index_1]
        mid_sec_par_1 = parent_1[index_1:index_2+1]
        last_sec_par_1 = parent_1[index_2+1:]
        
        #Parent_2
        first_sec_par_2 = parent_2[:index_1]
        mid_sec_par_2 = parent_2[index_1:index_2+1]
        last_sec_par_2 = parent_2[index_2+1:]

        chlid_1 = np.concatenate((first_sec_par_1, mid_sec_par_2, last_sec_par_1))
        chlid_2 = np.concatenate((first_sec_par_2, mid_sec_par_1, last_sec_par_2))

    else:
        chlid_1 = parent_1
        chlid_2 = parent_2

    return (chlid_1, chlid_2)

def mutation(chlid_1, chlid_2, muta_prob=0.2):
    
    #Chlid_1
    mutated_chlid_1 = np.empty((0, len(chlid_1)))

    t = 0
    for i in chlid_1:
        muta_rand_prob = np.random.rand()

        if muta_rand_prob < muta_prob:

            if chlid_1[t] == 0:
                chlid_1[t] = 1
            else:
                chlid_1[t] = 0

            mutated_chlid_1 = chlid_1
            t += 1

        else:
            mutated_chlid_1 = chlid_1
            t += 1

    #Chlid_2
    mutated_chlid_2 = np.empty((0, len(chlid_2)))

    t = 0
    for i in chlid_2:
        muta_rand_prob = np.random.rand()

        if muta_rand_prob < muta_prob:

            if chlid_2[t] == 0:
                chlid_2[t] = 1
            else:
                chlid_2[t] = 0

            mutated_chlid_2 = chlid_2
            t += 1
        
        else:
            mutated_chlid_2 = chlid_2
            t += 1

    return (mutated_chlid_1, mutated_chlid_2)

crack = Black_Box_Function("input2.txt", "output2.txt", "2-6.exe")

#bit >> [0,1,0,1,1,0,1,1,0,1,0,1,1,0,1,0]
chromosome = np.random.randint(high=2, low=0, size=16)

population = 16
all_solution = np.empty((0, len(chromosome)))

for i in range(population):
    np.random.shuffle(chromosome)
    all_solution = np.vstack((all_solution, chromosome))

print(all_solution, end="\n\n")

parents = find_parents_ts(all_solution)
parent_1 = parents[0]
parent_2 = parents[1]

print(f"parent1# {parent_1}")
print(f"parent2# {parent_2}")
print()

chlids = crossover(parent_1, parent_2)
chlid_1 = chlids[0]
chlid_2 = chlids[1]

print(f"chlid1# {chlid_1}")
print(f"chlid2# {chlid_2}")
print()

mutated_chlids = mutation(chlid_1, chlid_2)
mutated_chlid_1 = mutated_chlids[0]
mutated_chlid_2 = mutated_chlids[1]

print(f"mutated_chlid1# {mutated_chlid_1}")
print(f"mutated_chlid2# {mutated_chlid_2}")
print()
