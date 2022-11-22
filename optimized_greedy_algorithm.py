import pandas as pd
from tqdm import tqdm
import time
import sys


start_time = time.time()

def open_file(filename) -> list:

    df = pd.read_csv('data/dataset2.csv')
    df['sellable_price'] = (df['price']*(1+(df['profit'])/100))
    df['marge'] = (df['sellable_price']-(df['price']))
    df['ROI'] = ((df['marge']-df['price'])/df['price'])

    list_of_dict = df.to_dict('records')

    stock_market_action_list = []

    for row in list_of_dict:
        if float(row['price']) <= 0 or float(row['profit']) <= 0:
            pass
        
        else:
            if row['price'] >0 and row['profit'] >=1:
                share = {
                    'name': row['name'],
                    'price': float(float(row['price'])),
                    'profit': float(float(row['profit'])),
                    'sellable_price':float(float(row['sellable_price'])),
                    'marge': float(float(row['marge'])),
                    'ROI': round(float(float(row['ROI'])),2)
                }
                stock_market_action_list.append(share)

    sorter_list = sorted(stock_market_action_list, key=lambda x: x['ROI'], reverse=True)

    return sorter_list


def find_best_invest(sorter_list):

    max_invest = 500
    wallet = 0
    total_marge = 0
    list_of_action = []

    for i in tqdm(range(len(sorter_list))):
        
        if wallet + sorter_list[i]['price'] <= max_invest:
            wallet = wallet + sorter_list[i]['price']
            list_of_action.append(sorter_list[i])
            total_marge += sorter_list[i]['marge']

    return list_of_action

def display(list_of_action):
    """Fonction permettant l'affichage des résultats"""
    
    result_cost = []
    result_profit = []

    print("\n\nEn investissent sur la liste des actions ci-dessous : \n\n")
    for item in list_of_action:
            print(f"Nom : {item['name']} | Prix : {item['price']} € | Marge : {item['marge']} €")
            result_cost.append(item['price'])
            result_profit.append(item['sellable_price'])
    
    print("\nLe coût total de l'investissement : ", sum(result_cost), "€\n")
    print("Retour sur investissiment après deux ans: +", round(sum(result_profit)-500,2), "€")
    print("\nTemps d'exécution : ", round(time.time() - start_time,2), "secondes\n")

    

def main():
    
    try:
        filename = 'data/dataset2.csv'

    except IndexError:
        print("\nAucun fichier portant ce nom n'a été trouvé. Veuillez réessayer.\n")
        time.sleep(1)
        sys.exit()

    stock_market_action_list = open_file(filename)

    display(find_best_invest(stock_market_action_list))

if __name__ == "__main__":
    main()