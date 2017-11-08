from __future__ import division
import random,  copy, matplotlib.pyplot as plt
import string, os,  math, time
from datetime import datetime


startTime = datetime.now()

cities_no = 10
cities = [random.sample(range(100), 2) for x in range(cities_no)]
all_distances = []
print "oryginalne city ", cities


# ----------------------------------------------------
# DO TESTOW | zahardkodowane wspolrzedne miast |
#--------------------------------------------------------
# cities = [[80, 39], [72, 60], [11, 52], [78, 58],[45,72]]
# cities_no = len(cities)
# ----------------------------------------------------
# cities = [[16, 50], [62, 91],  [43, 8], [11, 71], [34, 31],[23,89],[76,42],[76,90]] #8
cities = [[82, 26], [53, 2], [87, 51], [54, 70], [3, 37], [28, 33], [95, 56], [24, 69], [22, 56], [47, 26]] #10 miast
cities_no = len(cities)
# ----------------------------------------------------
# -- GAS STATIONS ---
gas_station = [(1, 1), (85, 34), (83, 54), (38, 23), (94, 32),  (47, 67)]



def draw_chart(path, added_gasStation, duration=0.5):
    global gas_station
    # added_gasStation = {78:(6,7), 8:(78,93)}
    sorted_ids = sorted(added_gasStation.keys())
    j = len(sorted_ids)-1
    # try :
    for k in sorted_ids:
        key = sorted_ids[j]
        value = added_gasStation[key]
        print "!!!!!!!", value
        value = list(value)
        path.insert(key, value)
        j -= 1

    # except Exception as e:
    #     print "!!!!!!!!!", e
    #     y = sorted_ids[0]
    #     path.insert(added_gasStation[y], y) # slownik od krotki nie dziala
    path.append(path[0])
    labels_gasStation = ['GS_{}'.format(i + 1) for i in range(len(gas_station))]
    labels = ['M_{}'.format(i + 1) for i in range(len(path))]
    plt.plot(*zip(*path), marker='x')
    plt.plot(*zip(*gas_station), marker='o', linestyle=' ')
    i = 0
    for cor in path:
        plt.annotate(labels[i-1], xy=(cor[0], cor[1]), xytext=(2, 2), textcoords='offset points')
        i += 1
    i = 0
    for j in gas_station:
        plt.annotate(labels_gasStation[i], xy=(j[0], j[1]), xytext=(4, 4), textcoords='offset points')
        i += 1
    plt.show(block=True)
    time.sleep(duration)
    plt.close()


def swap():
    swap_tab = range(len(cities))
    city1_id = random.choice(swap_tab)
    swap_tab.remove(city1_id)
    city2_id = random.choice(swap_tab)
    swap_tab.remove(city2_id)

    temp = cities[city1_id]
    cities[city1_id] = cities[city2_id]
    cities[city2_id] = temp


def add_gasStation(new_tour, city1, city2, gasStations_dict):
        global cities
        cities_working_backup = cities[:]
        print "find the nearest gas station"
        distances_to_gas_stations = []
        print "stacje paliw -> ", gas_station
        print "miasto ->", city1
        for cor in gas_station:
            distances_to_gas_stations.append(round(math.sqrt((city1[0]-cor[0])**2 + (city1[1]-cor[1])**2), 2))
        print "odleglosci ->", distances_to_gas_stations
        closest_station = distances_to_gas_stations.index(min(distances_to_gas_stations))
        cor_closest_station = gas_station[closest_station]
        print "najblizsza stacja  ->", cor_closest_station
        city1_id = cities_working_backup.index(city1)
        new_tour += min(distances_to_gas_stations)
        print "new_tour + dystans do stacji ->", new_tour
        cities_working_backup.insert(city1_id + 1, cor_closest_station)
        gasStations_dict[city1_id+1] =  cor_closest_station
        print "cities z nowa satcja ", cities_working_backup

        distances_to_city2 = (round(math.sqrt((city2[0]-cor_closest_station[0])**2 + (city2[1]- cor_closest_station[1])**2), 2))
        new_tour += distances_to_city2
        print "new_tour + dystans ze stacji", cor_closest_station, "do next hop",city2, " -> ", new_tour
        tank = 200
        # TODO count distances to all station -  done
        # TODO find the nearest gas station - done
        # TODO add distance station->next_city to new tour - done
        # TODO put new element-clostest_station   into cities table next to city - done
        # TODO add distance to the closest next hop city - done
        # TODO set tank to full - done
        # time.sleep(80)
        return new_tour, tank, cities_working_backup, gasStations_dict







def count_distance(tour, zlamane_iteracje):
    tank = 180
    tank_treshold = 120
    count_sum = True
    new_tour = 0
    print "count distance cities ", cities
    cities1 = cities[:]
    # cities_backup = cities[:]
    gasStations_dict = {}
    for i in range(cities_no):

        if i == cities_no-1:
            dis.append(round(math.sqrt((cities1[i][0] - cities1[0][0])**2 + ((cities1[i][1] - cities1[0][1])**2)), 2))
            print "trasa od city", i,"do city startowego"
        else:
            dis.append(round(math.sqrt((cities1[i][0] - cities1[i+1][0])**2 + ((cities1[i][1] - cities1[i+1][1])**2)), 2))
            print "trasa od city", i,"do city ", i+1
        new_tour = new_tour + dis[i]
        tank = tank - dis[i]*0.30      #zmienijszenie tank
        print "tank ", tank, "tank tresholdd ", tank_treshold #print do obserwacji zmiany baku

        # wyrazenie warunkowe obnizajace koszty obliczeniowe w skrypcie
        # jezeli w czasie obliczen kosztu nowej trasy napotkamy na wartosc, ktora JUZ przekracza ostatnia najoptymalniejsza, to przestajemy juz dalej ja liczyc
        if tank < tank_treshold:     #kiedy new_tour przekroczy tank
           print "-----------w ifie -------------"
           try:
               new_tour, tank, cities_candidate, gasStations_dict = add_gasStation(new_tour, cities[i], cities[i+1], gasStations_dict)
               print "koordynaty  gas stations - uzupelniony", gasStations_dict
           except Exception as e:
               print e

        if tour <= new_tour:
            count_sum = False
            zlamane_iteracje += 1

            print "zlamana petal"
            break

    print "\n"

    return count_sum, zlamane_iteracje, new_tour, gasStations_dict


# zmienne do stystyk
zlamane_iteracje = 0
checkPoint= 0
# dane poczatkowe
sum_dis = 10000
tour = 600
temperature = 999999999
cooling_rate = 0.003
best_cities = []

# glowna petla szukajaca optymalnej trasy

while(temperature > 10):
    dis = []
    checkPoint += 1       #sprawdza iteracje petli
    stacje = {}
    swap()
    # random.shuffle(cities)          #ustatwie nowa, calkowicie losowa trase
    count_sum, zlamane_iteracje, new_tour, stacje = count_distance(tour, zlamane_iteracje)
    if count_sum:
        sum_dis = sum(dis)
        print sum_dis
        # if math.exp((tour - sum_dis)/temperature ) > (random.randint(0,100)*5) or sum_dis < tour :
        tour = new_tour
        # tour = sum_dis
        best_cities = cities[:]
        best_stations = dict(stacje)     #skopiuj stacje
        print "best cities  to ", cities, "+ stacje benzymnowe ", best_stations
        print "\n\n"
    # cities = cities_backup
    temperature = temperature*(1 - cooling_rate)
    print "temperatura", temperature, "\n\n"

# stystyki
print "przebyty deystans to ", tour
print "przejsc petli  ", checkPoint
print "zlamanych iteracji  ", zlamane_iteracje
print "stosunek zlamanych petli do clakowitych, narazie jedyny czynnik optymalizacyjny:", zlamane_iteracje/checkPoint #ostatnie wykonanie whila wprowadza count_sum na true
print "CZAS ",  datetime.now() - startTime
# koncowa trasa
print "best cities  to ", best_cities, "+ stacje benzymnowe ", best_stations
draw_chart(best_cities, best_stations, 7)

