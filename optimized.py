# from timeit import default_timer as timer
import pandas as pd
from tqdm import tqdm
import time
import sys
import numpy as np
import matplotlib_inline


start_time = time.time()

def open_file(filename)-> list:
    """Fonction utilisée pour ouvrir le fichier contenant les données"""
    try:
        df = pd.read_csv('dataset1.csv')

    except IndexError:
        print("\nAucun fichier portant ce nom n'a été trouvé. Veuillez réessayer.\n")
        time.sleep(1)
        sys.exit()

    list_of_dict = df.to_dict('records')

    stock_market_action_list = []

    for row in list_of_dict:
        if float(row['price']) <= 0 or float(row['profit']) <= 0:
            pass
        
        else:
            if row['price'] >0 and row['profit'] >=1:
                share = (
                    row['name'],
                    int(float(row['price'])*100),
                    float(float(row['price']) * float(row['profit']) / 100)
                )
                stock_market_action_list.append(share)

    return stock_market_action_list

def find_best_invest(stock_market_action_list: list) -> list:
    """Fonction de recherche du meilleur investissement en utilisant l'algorithme du sac à dos"""

    wallet= int(input('\nQuel est le momtant de votre portefeuille : '))
    max_inv = wallet*100    # capacity
    shares_total = len(stock_market_action_list)
    cost = []               # weights
    profit = []             # values
    
    for share in stock_market_action_list:
        cost.append(share[1])
        profit.append(share[2])

    print('Recherche du meilleur investissement : \n')
    
    #Création de la matrice 
    matrice = [[0 for x in range(max_inv + 1)] for x in range(shares_total + 1)]

    # Utilisation de boucle imbriquée pour parcourir le tableau et remplir des entiers dans chaques cellules
    for i in tqdm(range(1, shares_total + 1)):
    
        for w in range(1, max_inv + 1):
            if cost[i-1] <= w:
                matrice[i][w] = max(profit[i-1] + matrice[i-1][w-cost[i-1]], matrice[i-1][w])
        
            else:
                matrice[i][w] = matrice[i-1][w]    
    best_combinations = []

    while max_inv >= 0 and shares_total >= 0:

        if matrice[shares_total][max_inv] == matrice[shares_total-1][max_inv - cost[shares_total-1]] + profit[shares_total-1]:

            best_combinations.append(stock_market_action_list[shares_total-1])
            max_inv -= cost[shares_total-1]
            print(max_inv)

        shares_total -= 1
    print(best_combinations)
    return best_combinations

def display(best_combinations:list):

    result_cost = []
    result_profit = []

    print("\n\nEn investissent sur la liste des actions ci-dessous : \n\n")
    for item in best_combinations:
            print(f"{item[0]} | {item[1] / 100} € | +{item[2]} €")
            result_cost.append(item[1] / 100)
            result_profit.append(item[2])
    print(result_cost)
    print("\nLe coût total de l'investissement : ", round(sum(result_cost),2), "€\n")
    print("Retour sur investissiment après deux ans: +", round(sum(result_profit),2), "€")
    print("\nTemps d'exécution : ", round(time.time() - start_time,2), "secondes\n")
    print(len(best_combinations))
    

def main():
    
    try:
        filename = 'dataset2.csv'

    except IndexError:
        print("\nAucun fichier portant ce nom n'a été trouvé. Veuillez réessayer.\n")
        time.sleep(1)
        sys.exit()

    stock_market_action_list = open_file(filename)

    display(find_best_invest(stock_market_action_list))


if __name__ == "__main__":
    main()