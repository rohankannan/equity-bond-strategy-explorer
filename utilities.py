import pandas as pd
import numpy as np

FILEPATH = '~/Programs/Python/Equity-Bond-Balance/data.csv'

def get_annualized_total_return_from_portfolio(portfolio):
     cumulative_return = portfolio[-1]/portfolio[0] - 1

     result = (1 + cumulative_return)
     result = result ** (12 / len(portfolio))
     result = result - 1

     return result

def calculate_volatility(portfolio):
    monthly_returns = [portfolio[1] / portfolio[0] - 1]
    period = len(portfolio)

    for i in range(1,period):
         monthly_returns.append(portfolio[i] / portfolio[i-1] - 1)

    volatility = np.std(monthly_returns, ddof=1) * np.sqrt(12)
    return volatility

def simulate_portfolio(initial_investment, bonds_weight, bonds_rates, stocks_weight, stocks_rates, leverage_rate = 0, leverage_interest_rate = 1.0):
     
     investment_value = initial_investment
     
     # period to simulate, in number of months
     period = len(bonds_rates) 

     # index: month number, value: month portfolio value (index 0 is month 0)
     portfolio = [initial_investment] 

     # the value of investment in bonds and stocks, split by the ratio
     bonds_investment = bonds_weight * investment_value
     stocks_investment = stocks_weight * investment_value

     for i in range(period):
        # new investment value: most recent portfolio entry (previous month)
        investment_value = portfolio[-1] * (1 + leverage_rate)
        leverage_due= investment_value - portfolio[-1]

        leverage_due *= (1 + leverage_interest_rate)

        bonds_investment = bonds_weight * investment_value
        stocks_investment = stocks_weight * investment_value

        bonds_return = simulate_month(bonds_investment, bonds_rates[i])
        stocks_return = simulate_month(stocks_investment, stocks_rates[i])
        total_return = bonds_return + stocks_return - leverage_due

        portfolio.append(total_return)

     return portfolio

def simulate_month(investment, month_rate):
     return investment * (1 + month_rate)

def get_worst_monthly_return(portfolio):
     worst_return = 0
     worst_month = -1
     for i in range(1, len(portfolio)):
          monthly_return = portfolio[i] / portfolio[i-1] - 1
          if monthly_return < worst_return:
               worst_return = monthly_return
               worst_month = i
     return {"month": worst_month, "return": worst_return}

def get_worst_annual_return(portfolio):
     worst_return = 0
     worst_year = -1
     for i in range(12, len(portfolio)):
          annual_return = portfolio[i] / portfolio[i-12] - 1
          if annual_return < worst_return:
               worst_return = annual_return
               worst_year = i // 12 + 2016 # assuming data starts in 2016

     
     return {"year": worst_year, "return": worst_return}
