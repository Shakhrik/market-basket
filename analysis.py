import json

import pandas as pd
from apyori import apriori


def analyze():
    marketdf = pd.read_csv("groceries_final.csv",header = None)
    
    final_market_list = prune_dataset(marketdf)
    final_item_df = final_market_list[0]

    final_market_df = final_market_list[1]
    final_market_df_without_null = final_market_list[2]
    output_df = final_market_list[3]

    records = []
    row = final_item_df.shape[0]
    col = final_item_df.shape[1]
    for i in range(0,row):
        records.append([str(final_item_df.values[i,j]) for j in range(0, col)])

    association_rules = apriori(records, min_support=0.0045, min_confidence=0.2, min_lift=3, min_length=2)
    association_results = list(association_rules)

    results = []
    for item in association_results:
        pair = item[0]
        items = [x for x in pair]
        
        consequent = str(items[0])
        antecedent = str(items[1])
        support = str(int(float(str(item[1])[:7]) * 100000))
        confidence = str(item[2][0][2])[:7]
        lift = str(item[2][0][3])[:7]
        
        rows = (consequent,antecedent,support,confidence,lift)
        results.append(rows)
        
        final_result = pd.DataFrame(results,columns=['Consequent','Anticedent','Support','Confidence','Lift'])

    final_result= final_result.sort_values("Support",ascending=False, ignore_index=True)
    final_result = final_result[(final_result["Consequent"] != 'nan') & (final_result["Anticedent"] != 'nan')]
    print(type(final_result.shape))
    response = []
    for i in range(final_result.shape[0]):
        response.append([final_result.Anticedent[i:i+1].values[0], final_result.Consequent[i:i+1].values[0]])

    return response
   
def prune_dataset(input_df,length_trans = 2,total_sales_perc = 0.40):
    final_df2 = pd.DataFrame()
    for i in range(input_df.shape[0]):
        cnt = 0
        new_input = input_df.iloc[:][i:i+1]
        for j in range(new_input.shape[1]):
            if new_input.iloc[:,j].isnull().bool():
                if cnt <= length_trans:
                    break
                if cnt == 31:
                    final_df2 = final_df2.append(new_input,ignore_index=True)
            cnt+=1
    dict2 = dict()
    for i in range(final_df2.shape[1]):
        for j in range(final_df2.shape[0]):
            if final_df2[i][j] == "nan":
                continue
            elif final_df2[i][j] in list(dict2.keys()):
                dict2[final_df2[i][j]] += 1
            else:
                dict2[final_df2[i][j]] =1               
    total_purchase = sum(list(dict2.values()))
    market_sort = []
    for i,j in sorted(dict2.items(), key=lambda item: item[1], reverse = True):
        market_sort.append([i,j,float(int(j) * 100 /total_purchase)])
    new_market_df = pd.DataFrame(market_sort,columns=["item_name","item_count","item_perc"])
    new_market_df2 = new_market_df[new_market_df["item_name"].isnull() == False]
    new_total_purchase = sum(new_market_df2["item_count"])
    new_market_df3 = new_market_df2[["item_name","item_count"]]
    li = []
    for i in range(new_market_df3.shape[0]):
        li.append(float(new_market_df3["item_count"][i:i+1] / new_total_purchase))
    new_market_df3.insert(2,"item_perc",li,True)
    out_df = pd.DataFrame()
    for i in range(new_market_df3.shape[0]):
        if sum(new_market_df3["item_perc"].head(i)) > total_sales_perc:
            out_df = new_market_df3.head(i-1)
            break
    final_list = [final_df2,new_market_df2,new_market_df3,out_df]
    return final_list

