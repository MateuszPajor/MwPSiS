from __future__ import division
import random, numpy, copy, matplotlib.pyplot as plt
import string, os,  math, time



cities_no = 9
cities = [random.sample(range(100), 2) for x in range(cities_no)];
all_distances = []
print "oryginalne city ", cities

#----------------------------------------------------
#DO TESTOW | zahardkodowane wspolrzedne miast | minimalna trasa 164.63
cities = [[80, 39], [72, 60], [11, 52], [78, 58],[45,72]]
cities_no = len(cities)
#----------------------------------------------------
# cities = [[16, 50], [62, 91], [39, 92], [43, 8], [11, 71], [34, 31], [71, 24],[36,69],[21,98]]
# cities_no = len(cities)
#----------------------------------------------------


def draw_chart(path, duration = 0.5):
    print "path to ", path
    print "path [0] to ", path[0]

    path.append(path[0])
    labels = ['miasto_{}'.format(i + 1) for i in range(len(cities))]
    plt.plot(*zip(*path), marker='x')
    i = 0
    for cor in path:
        plt.annotate(labels[i-1], xy=(cor[0], cor[1]), xytext=(2, 2), textcoords='offset points')
        i += 1
    plt.show(block= False)
    time.sleep(duration)
    plt.close()

def swap(cities):
    swap_tab = range(len(cities))
    city1_id = random.choice(swap_tab)
    swap_tab.remove(city1_id)
    city2_id = random.choice(swap_tab)
    swap_tab.remove(city2_id)

    temp = cities[city1_id]
    cities[city1_id] = cities[city2_id]
    cities[city2_id] = temp


def count_all_dist(cities):
    #niekompletna
    for i in cities:
        dis = []
        for j in cities:
            for k in cities:
                dis.append(round(math.sqrt((i[0]-j[0])**2 + (i[1]-j[1])**2), 2))
        all_distances.append(dis)

#zmienne do stystyk
zlamane_iteracje = 0
checkPoint= 0
#dane poczatkowe
sum_dis = 10000
tour = 500
temperature = 999999999
cooling_rate = 0.003
best_cities = []

#glowna petla szukajaca optymalnej trasy
while(temperature > 1):       #jaka granice wybrac????
    swap_tab = []
    dis = []
    count_sum = True
    new_tour = 0
    checkPoint += 1       #sprawdza iteracje petli


    #  SWAP
    swap(cities)

    # random.shuffle(cities)          #ustatwie nowa, calkowicie losowa trase TODO konieczna optymalizacja

    #Petla liczaca koszt swiezo wylosowanej trasy

    for i in range(cities_no):
        if i == cities_no-1:
            dis.append(round(math.sqrt((cities[i][0] - cities[0][0])**2 + ((cities[i][1] - cities[0][1])**2)), 2))
        else:
            dis.append(round(math.sqrt((cities[i][0] - cities[i+1][0])**2 + ((cities[i][1] - cities[i+1][1])**2)), 2))
        new_tour = new_tour + dis[i]

        #wyrazenie warunkowe obnizajace koszty obliczeniowe w skrypcie
        #jezeli w czasie obliczen kosztu nowej trasy napotkamy na wartosc, ktora JUZ przekracza ostatnia najoptymalniejsza, to przestajemy juz dalej ja liczyc
        # if tour <= new_tour:
        #     count_sum = False
        #     zlamane_iteracje = zlamane_iteracje +1
        #     # print "zlamana petal"
        #     break

    # draw_chart(cities)  #do ogladania jak optymalizuje  nam sie trasa

    if count_sum == True:
        sum_dis = sum(dis)
        print sum_dis
        if math.exp((tour - sum_dis)/temperature ) > (random.randint(0,100)*5) or sum_dis < tour :
            tour = new_tour
            tour = sum_dis
            best_cities = cities[:]
            print "best cities ", best_cities


    temperature = temperature*(1 - cooling_rate)

#stystyki
print "przebyty deystans to ", tour
print "przejsc petli  ", checkPoint
print "zlamanych iteracji  ", zlamane_iteracje
print "stosunek zlamanych petli do clakowitych, narazie jedyny czynnik optymalizacyjny:", zlamane_iteracje/checkPoint #ostatnie wykonanie whila wprowadza count_sum na true

#koncowa trasa
draw_chart(best_cities, 7)


