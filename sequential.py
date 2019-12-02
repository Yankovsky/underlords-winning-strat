from itertools import combinations
import json
import functools
import time

start = time.time()

legion = {'human': 1}
index = 0
bestCombCount = 0


def getHeroesByAlliances(memo, hero):
    for alliance in hero['alliances']:
        if alliance not in memo:
            memo[alliance] = 0

        memo[alliance] += 1

    return memo


with open('data/alliances.json') as alliances_file:
    alliances = json.load(alliances_file)


    def countAlliances(heroesByAlliances):
        res = 0
        for allianceName in heroesByAlliances:
            if heroesByAlliances[allianceName] >= alliances[allianceName]:
                res += 1
        return res


    with open('data/heroes-25-subset.json') as heroes_file:
        heroes = json.load(heroes_file)

        print('start')
        for newComb in combinations(heroes, 9):
            if index == 0:
                print('index:', index)
            index += 1
            if index % 100000 == 0:
                print('index:', index)

            heroesByAlliances = functools.reduce(getHeroesByAlliances, newComb, {})

            if 'human' not in heroesByAlliances:
                heroesByAlliances['human'] = 0
            heroesByAlliances['human'] += 1

            newCount = countAlliances(heroesByAlliances)

            heroesNames = list(map(lambda x: x['name'], newComb))

            if newCount > bestCombCount:
                bestCombCount = newCount
                results = [heroesNames]
            elif newCount == bestCombCount:
                results.append(heroesNames)

end = time.time()
print('time:', end - start)
print('best combinations:', bestCombCount, results)
