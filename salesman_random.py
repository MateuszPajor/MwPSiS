from __future__ import division
import random,  copy, matplotlib.pyplot as plt
import string, os,  math, time
from datetime import datetime

# TODO dodac zmienna mierzaca czas kurierowi
# TODO postoje u klientow i na stacjach
# TODO rozwiazac problem(gdy jest ostatnia iteracja for-a nie mozna do funkcji przeslac cities[i +1]):
#            try:
#                new_tour, tank, gasStations_dict = add_gasStation(new_tour, cities[i], cities[i+1], gasStations_dict)
#                print "koordynaty  gas stations - uzupelniony", gasStations_dict
#            except Exception as e:
#                print e
# TODO zrobic inteligentniejszego swap-a - to jest trudniejsze zadanie

# ALGORYTM
# 1. Ustaw calkiem losowa trase -> tasae wyznaczana jest na podstawie kolejnosc tablicy cities
# 3. licz trase po koleji z wezla n do wezla n+1, gdy bak przekroczy tank treshold, dodaj dystans z obecnego city->najblizszej stacji i z stacji->next hopa, zapisz wspolzedne wybranej stacji do gasStations_dict
# 4. jezeli trasa jest krotsza od ostatnie najlepszej, ustaw ja jako najbardziej optymalna razem z wpisanymi dla tej trasy stacjami
# 5. zrob swapa na dwoch losowych wezlach
# 6. przejdz do 3, jezeli temperatura powyzej tresholdu

startTime = datetime.now()


def draw_chart(path, added_gasStation, duration=0.5):
    global gas_station
    # added_gasStation = {78:(6,7), 8:(78,93)}
    sorted_ids = sorted(added_gasStation.keys())
    path_copy = path[:]
    for k in sorted_ids[::-1]:
        value = added_gasStation[k]
        value = list(value)
        path.insert(k, value)
    path.append(path[0])
    labels_gasStation = ['GS_{}'.format(i + 1) for i in range(len(gas_station))]
    labels = ['M_{}'.format(i + 1) for i in range(len(path)-1)]
    plt.plot(*zip(*path), marker='x')  # * - skrot do przekazywania wielu zmiennym ktore sa zapakowane w np listach lub krotkach najpierw pierwszy element, pozniej drugi element listy  i tak dalej, tak jak bym przekazywala osobne zmienne, * rozbicie pojemnika
    plt.plot(*zip(*gas_station), marker='o', linestyle=' ')
    i = 0
    for cor in path_copy:
        i += 1
        plt.annotate(labels[i-1], xy=(cor[0], cor[1]), xytext=(2, 2), textcoords='offset points')
    i = 0
    for j in gas_station:
        plt.annotate(labels_gasStation[i], xy=(j[0], j[1]), xytext=(2, 2), textcoords='offset points')
        i += 1
    plt.show(block=True)
    time.sleep(duration)
    plt.close()


def swap():
    swap_tab = range(len(cities))
    del swap_tab[0]
    city1_id = random.choice(swap_tab)
    swap_tab.remove(city1_id)
    city2_id = random.choice(swap_tab)
    swap_tab.remove(city2_id)

    temp = cities[city1_id]
    cities[city1_id] = cities[city2_id]
    cities[city2_id] = temp


def add_gasStation(new_tour, city1, city2, gasStations_dict):
        global cities
        global gas_station
        cities_working_backup = cities[:]
        print "find the nearest gas station"
        distances_to_gas_stations = []
        print "stations paliw -> ", gas_station
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
        gasStations_dict[city1_id+1] = cor_closest_station
        print "cities z nowa satcja ", cities_working_backup
        distances_to_city2 = (round(math.sqrt((city2[0]-cor_closest_station[0])**2 + (city2[1] - cor_closest_station[1])**2), 2))
        new_tour += distances_to_city2
        print "new_tour + dystans ze stacji", cor_closest_station, "do next hop", city2, " -> ", new_tour
        tank = 200
        return new_tour, tank, gasStations_dict


def count_distance(tour, zlamane_iteracje, dis):
    tank = 180
    tank_treshold = 120
    count_sum = True
    new_tour = 0
    print "count distance cities ", cities

    cities1 = cities[:]
    gasStations_dict = {}

    for i in range(cities_no):

        if i == cities_no-1:
            dis.append(round(math.sqrt((cities1[i][0] - cities1[0][0])**2 + ((cities1[i][1] - cities1[0][1])**2)), 2))
            print "trasa od city", i, "do city startowego"
        else:
            dis.append(round(math.sqrt((cities1[i][0] - cities1[i+1][0])**2 + ((cities1[i][1] - cities1[i+1][1])**2)), 2))
            print "trasa od city", i, "do city ", i+1
        new_tour = new_tour + dis[i]
        tank = tank - dis[i]*0.30      # zmienijszenie tank
        print "tank ", tank, "tank tresholdd ", tank_treshold    # print do obserwacji zmiany baku

        # wyrazenie warunkowe obnizajace koszty obliczeniowe w skrypcie
        # jezeli w czasie obliczen kosztu nowej trasy napotkamy na wartosc, ktora JUZ przekracza ostatnia najoptymalniejsza, to przestajemy juz dalej ja liczyc
        if tank < tank_treshold:     # kiedy new_tour przekroczy tank
           print "KONCZY SIE BENZYNA"
           try:
               new_tour, tank, gasStations_dict = add_gasStation(new_tour, cities[i], cities[i+1], gasStations_dict)
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




def main():
    # zmienne do stystyk
    temperature = 999999999
    tour = 600
    zlamane_iteracje = 0
    checkPoint = 0
    cooling_rate = 0.003
    best_cities = []
    # glowna petla szukajaca optymalnej trasy
    while(temperature > 10):
        checkPoint += 1       #sprawdza iteracje petli
        dis = []

        swap()
        # random.shuffle(cities)          #ustatwie nowa, calkowicie losowa trase

        count_sum, zlamane_iteracje, new_tour, stations = count_distance(tour, zlamane_iteracje, dis)
        # if przypisujacy najlepsze rozwiazania do finalnych zmiennych
        if count_sum:
            sum_dis = sum(dis)
            print sum_dis
            # if math.exp((tour - sum_dis)/temperature ) > (random.randint(0,100)*5) or sum_dis < tour :
            tour = new_tour
            best_cities = cities[:]
            best_stations = dict(stations)     #skopiuj stations
            print "best cities  to ", cities, "+ stacje  benzymnowe ", best_stations
            print "\n\n"
        temperature = temperature*(1 - cooling_rate)
        print "temperatura", temperature, "\n\n"

    # stystyki
    print "przebyty deystans to ", tour
    print "przejsc petli  ", checkPoint
    print "zlamanych iteracji  ", zlamane_iteracje
    print "stosunek zlamanych petli do clakowitych, narazie jedyny czynnik optymalizacyjny:", zlamane_iteracje/checkPoint #ostatnie wykonanie whila wprowadza count_sum na true
    print "CZAS ",  datetime.now() - startTime
    # koncowa trasa
    print "best cities  to ", best_cities, "+ stations benzymnowe ", best_stations
    draw_chart(best_cities, best_stations, 7)





# GLOBAL VARIABLES
cities_no = 10
cities = [random.sample(range(100), 2) for x in range(cities_no)]
all_distances = []

# ----------------------------------------------------
# DO TESTOW | zahardkodowane wspolrzedne miast |
# --------------------------------------------------------
# cities = [[80, 39], [72, 60], [11, 52], [78, 58],[45,72]]
# cities = [[16, 50], [62, 91],  [43, 8], [11, 71], [34, 31],[23,89],[76,42],[76,90]] #8
cities = [[82, 26], [53, 2], [87, 51], [54, 70], [3, 37], [28, 33], [95, 56], [24, 69], [22, 56], [47, 26]] # 10 miast
cities_no = len(cities)
# ----------------------------------------------------
# -- GAS STATIONS ---
gas_station = [(1, 1), (85, 34), (83, 54), (38, 23), (94, 32), (47, 67)]
print "oryginalne city ", cities

if __name__ == "__main__":
    main()
