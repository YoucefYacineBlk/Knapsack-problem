from collections import namedtuple
from random import Random, randint, random
from timeit import default_timer
Item = namedtuple("Item", ['index', 'value', 'weight'])

def depth_search(sort_list,list_value,item_count,capacity,items,value,weight,taken,index,last_index,best,start,taken_best):
    taken_=taken.copy()
    value_=value
    weight_=weight
    weight_best=0
    end=default_timer()
    if(end-start>30) : 
        if(index==1) : 
            print("arret en force")
        return taken,0,weight
    index_search=sort_list[index]
    best_value=0
    initial_value=taken[items[index_search].index]
    actual_value = randint(0,1) 
    for i in [actual_value,1-actual_value] :
        trial_taken=taken_.copy()
        trial_value=value_
        trial_weight=weight_
        trial_taken[items[index_search].index] = i
        trial_value += items[index_search].value*i  
        trial_weight += items[index_search].weight*i 

        if trial_weight  > capacity:
            continue
       
        if (trial_weight==capacity or index==last_index) :    
            if(trial_value>=best_value) :
                taken=trial_taken.copy()
                value=trial_value
                weight=trial_weight 
                best_value=trial_value  
                if(trial_value>best): 
                    best=trial_value  
                    taken_best=taken.copy()
                    weight_best=trial_weight

        else : 
            remainig_weight=capacity-trial_weight
            cpt=index+1
            estimate=trial_value
            while(remainig_weight>0 and cpt!=last_index+1) : 
                additive=remainig_weight/items[sort_list[cpt]].weight
                estimate+=min(1,additive)*items[sort_list[cpt]].value
                remainig_weight-=items[sort_list[cpt]].weight
                cpt+=1
            if (estimate>best) : 
                trial_taken,trial_value,trial_weight=depth_search(sort_list,list_value,item_count,capacity,items,trial_value,trial_weight,trial_taken,index+1,last_index,best,start,taken_best)
                if(trial_value>=best_value) :
                    taken=trial_taken.copy()
                    value=trial_value
                    weight=trial_weight 
                    best_value=trial_value 
                    if(best<value):
                        best=value 
                        taken_best=taken.copy()  
                        weight_best=trial_weight
    return taken_best,best,weight_best
    
def solve_it(input_data):
    # parse the input
    lines = input_data.split('\n')
    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])
    items = []
    weight_coef = []
    value_coef  = []
    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))
        weight_coef.append(int(parts[1]))
        value_coef.append(int(parts[0]))

    # a trivial algorithm for filling the knapsack
    # it fill the knapsack with the most promising item that maximize the ratio ( value/weight )
    value = 0
    weight = 0
    taken = [0]*len(items)
    index_list = [x for x in range(item_count)]
    value_list = [x.value/x.weight for x in items]
    sort_list = [i for _,i in sorted(zip(value_list,index_list),reverse=True)]
    stop = False
    value_list=sorted(value_list,reverse=True)
    j=0
    i=sort_list[j]
    while (not stop) : 
         if weight + items[i].weight <= capacity:
            taken[items[i].index] = 1
            value += items[i].value
            weight += items[i].weight
         if (j==item_count-1 or weight==capacity): 
            stop=True
         else : 
            j+=1
            i=sort_list[j]
    start=default_timer()
    value=0
    weight=0
    best=0
    taken_best=taken.copy()
    index = 0
    if (item_count>=1000) : 
        index = item_count - 990
        for i in range(item_count) : 
            item = sort_list[i] 
            if (i <index): 
                value += items[item].value * taken[items[item].index]
                weight += items[item].weight * taken[items[item].index]
            else : 
                taken[items[item].index]= 0 
           
    taken,value,weight=depth_search(sort_list,value_list,item_count,capacity,items,value,weight,taken,index,item_count-1,best,start,taken_best)    
    weight=0
    value=0
    for num1,num2 in  zip(weight_coef,taken):
        weight+=(num1*num2)
    for num1,num2 in  zip(value_coef,taken):
        value+=(num1*num2)
   
    output_data = 'the best value found is '+ str(value) + ' with weight  ' + str(weight) + '\n' + 'solution is : '+' '.join(map(str, taken))
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python knapsack_problem.py ./data/ks_4_0)')

