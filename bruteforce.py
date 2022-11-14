import itertools
from timeit import default_timer as timer
import pandas as pd
from tqdm import tqdm


df = pd.read_excel('data.xlsx')

list_of_dict = df.to_dict('records')

wallet = 500
best_rentability = 0
best_action = []

print('Recherche du meilleur investissement')

start = timer()

for i in tqdm(range(len(list_of_dict)+1)):

   for subset in itertools.combinations(list_of_dict,i): # créé des tuples avec toutes les combinaisons entre 0 et 20 actions, on veut combien ils coutent et combien ils rapportent
        # # print(subset)
        total_purchase_values = 0 # valeurs d'achats
        valeurs_totales_vente = 0

        for action in subset:

            action['sellable_price'] = action['price']*(1+action['profit'])
            total_purchase_values += action['price']
            valeurs_totales_vente += action['sellable_price']

            if total_purchase_values <= 500:
                rentabilite = valeurs_totales_vente - total_purchase_values

                if rentabilite > best_rentability:
                    best_rentability = rentabilite
                    best_action = subset

#pour tout les valeurs de 20=pour les sous ensemble dans prix valeur total
# print(best_rentability)
# print(action['Price'])
# print(best_action)
for action in best_action:
    name_action = action['name']
    wallet = wallet - action['price']
    print(f'La meilleur action  : {name_action} il vous reste : {wallet} € ')

end = timer()

print(end-start)