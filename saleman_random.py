from __future__ import division
import random, numpy, copy, matplotlib.pyplot as plt
import string, os,  math, time

cities_no = 9
cities = [random.sample(range(100), 2) for x in range(cities_no)]
all_distances = []
print "oryginalne city ", cities

# ----------------------------------------------------
# DO TESTOW | zahardkodowane wspolrzedne miast | minimalna trasa 164.63
# cities = [[80, 39], [72, 60], [11, 52], [78, 58],[45,72]]
# cities_no = len(cities)
# ----------------------------------------------------
cities = [[16, 50], [62, 91], [39, 92], [43, 8], [11, 71], [34, 31], [71, 24], [36, 69], [21, 98]]
cities_no = len(cities)
# ----------------------------------------------------
# -- GAS STATIONS ---
gas_station = [[70, 56], [85, 34], [83, 21], [38, 23], [94, 32], [83, 35], [47, 23]]


def draw_chart(path, duration=0.5):
    path.append(path[0])
    labels = ['miasto_{}'.format(i + 1) for i in range(len(cities))]
    plt.plot(*zip(*path), marker='x')
    i = 0
    for cor in path:
        plt.annotate(labels[i-1], xy=(cor[0], cor[1]), xytext=(2, 2), textcoords='offset points')
        i += 1
    plt.show(block=False)
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


def add_gasStation(new_tour, city):
        print "find the nearest gas station"
        distances_to_gas_stations = []
        print "stacje paliw -> ", gas_station
        print "miasto ->", city
        for cor in gas_station:
            distances_to_gas_stations.append(round(math.sqrt((city[0]-cor[0])**2 + (city[1]-cor[1])**2), 2))
        print "odleglosci ->", distances_to_gas_stations
        closest_station = distances_to_gas_stations.index(min(distances_to_gas_stations))
        print "najblizsza stacja  ->", gas_station[closest_station]
        city_id = cities.index(city)
        new_tour += min(distances_to_gas_stations)
        cities.insert(city_id + 1, gas_station[closest_station])
        print "cities z nowa satcja ", cities



        # TODO count distances to all station -  done
        # TODO find the nearest gas station - done
        # TODO add distance station->next_city to new tour - done
        # TODO put new element-clostest_station   into cities table next to city - done
        # TODO add distance to the closest next hop city
        # TODO set bak to full
        time.sleep(100)
        return new_tour


def count_distance(cities, tour, zlamane_iteracje):
    tracer = 0
    bak = 500
    bak_treshold = 50
    count_sum = True
    new_tour = 0
    for i in range(cities_no):

        if i == cities_no-1:
            dis.append(round(math.sqrt((cities[i][0] - cities[0][0])**2 + ((cities[i][1] - cities[0][1])**2)), 2))
        else:
            dis.append(round(math.sqrt((cities[i][0] - cities[i+1][0])**2 + ((cities[i][1] - cities[i+1][1])**2)), 2))
        new_tour = new_tour + dis[i]
        bak = bak - dis[i]*0.05      #zmienijszenie backu

        # wyrazenie warunkowe obnizajace koszty obliczeniowe w skrypcie
        # jezeli w czasie obliczen kosztu nowej trasy napotkamy na wartosc, ktora JUZ przekracza ostatnia najoptymalniejsza, to przestajemy juz dalej ja liczyc
        if new_tour > bak_treshold:     #kiedy new_tour przekroczy bak
           new_tour = add_gasStation(new_tour, cities[i])
        if tour <= new_tour:
            count_sum = False
            zlamane_iteracje = zlamane_iteracje +1
            print "zlamana petal"
            break

    return cities, count_sum, zlamane_iteracje, new_tour


# zmienne do stystyk
zlamane_iteracje = 0
checkPoint= 0
# dane poczatkowe
sum_dis = 10000
tour = 500
temperature = 9999999
cooling_rate = 0.003
best_cities = []

# glowna petla szukajaca optymalnej trasy
while(temperature > 1):
    dis = []
    checkPoint += 1       #sprawdza iteracje petli
    swap(cities)
    # random.shuffle(cities)          #ustatwie nowa, calkowicie losowa trase
    cities, count_sum, zlamane_iteracje, new_tour = count_distance(cities, tour, zlamane_iteracje)
    # draw_chart(cities)  #do ogladania jak optymalizuje  nam sie trasa

    if count_sum == True:
        sum_dis = sum(dis)
        print sum_dis
        # if math.exp((tour - sum_dis)/temperature ) > (random.randint(0,100)*5) or sum_dis < tour :
        tour = new_tour
        tour = sum_dis
        best_cities = cities[:]
        print "best cities ", best_cities

    temperature = temperature*(1 - cooling_rate)

# stystyki
print "przebyty deystans to ", tour
print "przejsc petli  ", checkPoint
print "zlamanych iteracji  ", zlamane_iteracje
print "stosunek zlamanych petli do clakowitych, narazie jedyny czynnik optymalizacyjny:", zlamane_iteracje/checkPoint #ostatnie wykonanie whila wprowadza count_sum na true

# koncowa trasa
draw_chart(best_cities, 7)


