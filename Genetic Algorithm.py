import random
from numpy import exp,arange
from pylab import meshgrid,cm,imshow,contour,clabel,colorbar,axis,title,show


def generate_population(size, x_boundaries, y_boundaries):
    lower_x_boundary, upper_x_boundary = x_boundaries
    lower_y_boundary, upper_y_boundary = y_boundaries

    population = []
    for i in range(size):
        individual = {
            'x': random.uniform(lower_x_boundary, upper_x_boundary),
            'y': random.uniform(lower_y_boundary, upper_y_boundary),
        }
        population.append(individual)

    return population

def store_fitness(individual):
    #tirar todos os valores da lista de dict
    x = [dct['x'] for dct in individual]
    y = [dct1['y'] for dct1 in individual]
    
    i = 0
    total = [0,0,0,0,0,0,0,0,0,0]
    for i in range(10):
        total[i] = abs((-(100*(x[i]*x[i] - y[i])*(x[i]*x[i] - y[i]) + (1 - x[i])*(1-x[i]))))
    return total

def fitness(individual):
    x = individual['x']
    y = individual['y']
    
    return abs((-(100 * (x * x - y) * (x * x - y) + (1 - x) * (1 - x))))

def sort_population_by_fitness(population):
    return sorted(population, key=fitness)

def crossover(choice_a, choice_b):
    xa = choice_a['x']
    ya = choice_a['y']
    
    xb = choice_b['x']
    yb = choice_b['y']
    
    xa = (xa+xb)/2
    ya = (ya+yb)/2
    

    return {'x': xa, 'y': ya}

def mutate(new_individual):
    x = new_individual['x']
    y = new_individual['y']

    #flags para estouro
    flagx = 1
    flagy = 1
    
    #realiza a mutação
    new_x = x * (1 + random.uniform(-0.06, 0.06))
    new_y = y * ( 1 + random.uniform(-0.06, 0.06))
    
    
    #Verifica se teve estouro X
    while flagx == 1:
        if (new_x > 2.0) or (new_x < -2.0):

            new_x = x*(1+random.uniform(-0.06, 0.06))

            flagx = 1
        else:
            flagx = 0
    #Verifica se teve estouro Y
    while flagy == 1:
        if(new_y > 2) or (new_y < -2):

            new_x = y * (1 + random.uniform(-0.06, 0.06))

            flagy = 1
        else:
            flagy = 0
    
    return {'x': new_x, 'y': new_y}


def choice_by_roulette(sorted_population, fitness_sum):
    #sorteia valor
    drawn = random.uniform(0, 1)
    #valor acumalado dos sorteios
    accumulated = 0
    
    for individual in sorted_population:
        #fitnessx recebe o fitness do individuo
        fitnessX = fitness(individual)
        #calculo da probabilidade
        probability = fitnessX / fitness_sum
        #acumula o valor
        accumulated += probability
        
        #reliza o sorteio case valor esteja no abaixo do acumulado
        if drawn <= accumulated:
            return individual
        
def make_next_gen(population):
    next_gen = []
    #ordenar a população
    population = sort_population_by_fitness(population)
    #coleta soma
    sum_fitness = sum(fitness(individual)for individual in population)

    choice_1 = choice_by_roulette(population, sum_fitness)
    choice_2 = choice_by_roulette(population, sum_fitness)

    #verificação se as primeiras seleções sao iguais
    while choice_1 == choice_2:
        choice_2 = choice_by_roulette(population, sum_fitness)

    #Armazena a primeira escolha
    old_choice_1 = choice_1
    old_choice_2 = choice_2
    
    #realiza o primeiro cruzamento
    new_individual = crossover(choice_1, choice_2)
    #4 porcento de chance de mutação
    drawn = random.randint(1,10)

    if (drawn == 1) or (drawn == 2) or (drawn == 3) or (drawn == 4):
        new_individual = mutate(new_individual)
    #adiciona o primeiro individuo a lista dos novos individuos
    next_gen.append(new_individual)
    
    for i in range(9):
        choice_1 = choice_by_roulette(population, sum_fitness)

        #impedir que realize a mesma selução
        
        while(choice_1 == old_choice_1) or (choice_1 == old_choice_2):
            choice_1 = choice_by_roulette(population, sum_fitness)

        choice_2 = choice_by_roulette(population, sum_fitness)

        #impedir que realize a mesma seleção
        while((choice_2 == old_choice_1) or (choice_2 == old_choice_2) or (choice_2 == choice_1)):
            choice_2 = choice_by_roulette(population, sum_fitness)

        #atualiza as escolhas anteriores
        old_choice_1 = choice_1
        old_choice_2 = choice_2
        
        #realiza o cruzamento
        new_individual = crossover(choice_1, choice_2)
        #4 porcento de chance de mutação
        drawn = random.randint(1,10)
        
        if (drawn == 1) or (drawn == 2) or (drawn == 3) or (drawn == 4):
            new_individual = mutate(new_individual)
         #adiciona o primeiro individuo a lista dos novos individuos    
        next_gen.append(new_individual)
    
    return next_gen
        
    
        
#Primeiro gera a população
population = generate_population(size=10, x_boundaries=(-2, 2), y_boundaries=(-2, 2))

#Armazena o fitness da população em ordem crescente
#idx 0 == menor fitness = melhor
fitness_pop = store_fitness(population)

#ordena os fitness
fitness_pop = sorted(fitness_pop)
#ordena a população pelo fitness
print("Primeira População: ")
population = sort_population_by_fitness(population)
for individual in population:
    print(individual, fitness(individual))
#Para o eletismo, armazena o melhor individuo e o melhor fitness do individuo
best_individual = population[0]
best_fitness = fitness_pop[0]
    
population = make_next_gen(population)

generations = 1000
i = 2

while True:
    
    #recebe a nova população
    population = make_next_gen(population)
    #ordena população pra garantir ne vai que
    population = sort_population_by_fitness(population)
    print("\n{} Geração\n".format(i))
    for individual in population:
        print(individual, fitness(individual))
    #recebe o fitnes de toda a população
    fitness_pop = store_fitness(population)
    #ordena os fitness ja ordenados pra garantir vai que
    fitness_pop = sorted(fitness_pop)
    #compara melhor individuo antigo com pior individuo novo
    new_worst_individual = population[9]
    #novo PIOR fitness
    new_worst_fitness = fitness_pop[9]
    if(best_fitness < new_worst_fitness):
        population[9] = best_individual
    #ordena nova população
    population = sort_population_by_fitness(population)
    #melhor individuo atual armazenado
    best_individual = population[0]
    #armazena fitness da população atual
    fitness_pop = store_fitness(population)
    fitness_pop = sorted(fitness_pop)
    #melhor fitness atual armazenado
    best_fitness = fitness_pop[0]
    if(i == generations):
        break
    else:
        i += 1
for individual in population:
    print(individual, fitness(individual))
population = sort_population_by_fitness(population)
the_best = population[0]
fitness_pop = store_fitness(population)
print("\nMelhor:")
print(the_best, fitness_pop[0])

def func(x,y):
    return ((-(100 * (x * x - y) * (x * x - y) + (1 - x) * (1 - x))))
    
x = [dct['x'] for dct in population]
y = [dct1['y'] for dct1 in population]

X,Y = meshgrid(x, y) 
Z = func(X, Y) 
im = imshow(Z,cmap=cm.RdBu) 
cset = contour(Z,arange(-1,1.5,0.2),linewidths=2,cmap=cm.Set2)
clabel(cset,inline=True,fmt='%1.1f',fontsize=10)
colorbar(im) 
title('$z=-(100*(x^2 - y) * (x^2 - y) + (1 - x)^2)$')
show()
