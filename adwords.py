
import pandas as pd
import numpy as np
import math
import sys
import random

if len(sys.argv) != 2:
  print "python adwords.py greedy|msvv|balance"
  exit(1)
method = sys.argv[1]

bidder_info = pd.read_csv('bidder_dataset.csv')


#filtering only those rows containing the budgets
bid_info=bidder_info.dropna()
  
#making a dictionary of advertisers and their budgets
budget_dict=dict(zip(bid_info.Advertiser,bid_info.Budget))
budget_dict_dup=dict(budget_dict)

#renaming columns
bidder_info.columns=['Advertiser','Keyword','Bid_value','Budget']
  
bidder_info['bid_adv']=zip(bidder_info.Advertiser,bidder_info.Bid_value)
edges={k:list(v) for k,v in bidder_info.groupby("Keyword")["bid_adv"]}
  


def greedy(queries):
  budget_dict=dict(zip(bid_info.Advertiser,bid_info.Budget))

  for k,v in edges.iteritems():
    edges[k]=sorted(v,key=lambda x:x[1],reverse=True)
  
  for query in queries:
    for bidder_tuple in edges[query]:
        if(budget_dict[bidder_tuple[0]]>=bidder_tuple[1]):
          budget_dict[bidder_tuple[0]]=budget_dict[bidder_tuple[0]]-bidder_tuple[1]  
          break

  revenue=0.00
  for bidder in budget_dict:
    revenue=revenue+(budget_dict_dup[bidder]-budget_dict[bidder])
  return revenue
  


def msvv(queries):
  budget_dict=dict(zip(bid_info.Advertiser,bid_info.Budget))

  for query in queries:
    max_scaled_bid=0.00
    matched_bid=0.00
    matched_bidder="none"
    for bidder_tuple in edges[query]:
        budget=budget_dict_dup[bidder_tuple[0]]
        left=budget_dict[bidder_tuple[0]]
        if left<bidder_tuple[1]:
          continue
        xu=(budget-left)/budget
        scaled_bid=(1-(math.exp(xu-1)))*bidder_tuple[1]
        if scaled_bid>max_scaled_bid:
          max_scaled_bid=scaled_bid
          matched_bidder=bidder_tuple[0]
          matched_bid=bidder_tuple[1]
    if matched_bidder!="none":
      budget_dict[matched_bidder]=budget_dict[matched_bidder]-matched_bid


  revenue=0.00
  for bidder in budget_dict:
    revenue=revenue+(budget_dict_dup[bidder]-budget_dict[bidder])
  return revenue
  

def balance(queries):
  budget_dict=dict(zip(bid_info.Advertiser,bid_info.Budget))
  
  for query in queries:
    max_unspent_budget=0.00
    matched_bid=0.00
    matched_bidder="none"
    for bidder_tuple in edges[query]:
        budget=budget_dict_dup[bidder_tuple[0]]
        left=budget_dict[bidder_tuple[0]]
        if left<bidder_tuple[1]:
          continue
        if left>max_unspent_budget:
          max_unspent_budget=left
          matched_bidder=bidder_tuple[0]
          matched_bid=bidder_tuple[1]
    if matched_bidder!="none":
      budget_dict[matched_bidder]=budget_dict[matched_bidder]-matched_bid


  revenue=0.00
  for bidder in budget_dict:
    revenue=revenue+(budget_dict_dup[bidder]-budget_dict[bidder])
  return revenue






def main():
  queries=[]
  queries = [line.rstrip('\n') for line in open('queries.txt')]
  avg_revenue=0.00
  optimal_revenue=0.00
  for bidder in budget_dict_dup:
    optimal_revenue=optimal_revenue+budget_dict_dup[bidder]

  if method=="greedy":
    print "---greedy revenue---"
    print greedy(queries)
    for i in range(100):
      random.shuffle(queries)
      avg_revenue=avg_revenue+greedy(queries)

  if method=="msvv":
    print "---msvv revenue---"
    print msvv(queries)
    for i in range(100):
      random.shuffle(queries)
      avg_revenue=avg_revenue+msvv(queries)

  if method=="balance":
    print "---balance revenue---"
    print balance(queries)
    for i in range(100):
      random.shuffle(queries)
      avg_revenue=avg_revenue+balance(queries)
  avg_revenue=avg_revenue/100
  print "---competitive ratio---"
  print avg_revenue/optimal_revenue
  
	
if __name__ == "__main__":
  main()



