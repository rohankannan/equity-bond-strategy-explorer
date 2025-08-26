import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import utilities

FILEPATH = '~/Programs/Python/Equity-Bond-Balance/data.csv'
INITIAL_FUNDS = 10000
SIMULATION_GRANULARITY = 1000 # number of strategies to simulate, minimum is 2
LEVERED = True # set to true to use leverage to equalize volatility of all strategies
LEVERAGE_INTEREST_RATE = 0.0001627 # rough estimate based on average benchmark interest rate 2016-2024 according to FRED, 1.97% adjusted for monthly compounding

if __name__ =="__main__":

    data = pd.read_csv(FILEPATH)

    # include 0% stocks strategy in our portfolio
    portfolio_strategies = []
    portfolio_strategies.append([0.0,1.0])
    
    # fill the portfolio_strategies array with a variety of evenly spread strategies, the number of which is determined by SIMULATION_GRANULARITY
    for i in range(1, SIMULATION_GRANULARITY):
         strategy = [-1, -1]
         stocks_weight = (i * 1.0) / (SIMULATION_GRANULARITY - 1)
         bonds_weight = 1 - stocks_weight
         strategy[0] = stocks_weight
         strategy[1] = bonds_weight
         {"Strategy"}
         portfolio_strategies.append(strategy)
    
    stocks_rates = []
    bonds_rates = []

    # collect data from the csv to populate stock rates and bond rates
    for i in range(len(data)):
        stock_percentage_change = float(data['Stocks'][i])
        bond_percentage_change = float(data['Bonds'][i])
        
        stocks_rates.append(stock_percentage_change / 100)
        bonds_rates.append(bond_percentage_change / 100)

    # get volatility of 100% stocks strategy to use as a benchmark if LEVERED is set to true
    test_portfolio = utilities.simulate_portfolio(initial_investment = INITIAL_FUNDS, bonds_weight = 0, bonds_rates = bonds_rates, stocks_weight = 1, stocks_rates = stocks_rates)
    benchmark_volatility = float(utilities.calculate_volatility(test_portfolio))

    portfolios = []
    for i in range(len(portfolio_strategies)):

        stocks_weight = portfolio_strategies[i][0]
        bonds_weight = portfolio_strategies[i][1]

        if LEVERED: 
            # compute a dummy portfolio with no leverage to find leverage rate needed to match benchmark volatility
            portfolio = utilities.simulate_portfolio(initial_investment = INITIAL_FUNDS, bonds_weight = bonds_weight, bonds_rates = bonds_rates, stocks_weight = stocks_weight, stocks_rates = stocks_rates)
            volatility = float(utilities.calculate_volatility(portfolio))

            # set leverage rate to match benchmark volatility
            leverage_rate = benchmark_volatility / volatility - 1

            # simulate the portfolio including leverage
            portfolio = utilities.simulate_portfolio(initial_investment = INITIAL_FUNDS, bonds_weight = bonds_weight, bonds_rates = bonds_rates, stocks_weight = stocks_weight, stocks_rates = stocks_rates, leverage_rate = leverage_rate, leverage_interest_rate = LEVERAGE_INTEREST_RATE)

        else:

            # simulate the portfolio with no leverage
            portfolio = utilities.simulate_portfolio(initial_investment = INITIAL_FUNDS, bonds_weight = bonds_weight, bonds_rates = bonds_rates, stocks_weight = stocks_weight, stocks_rates = stocks_rates)

        volatility = round((float(utilities.calculate_volatility(portfolio))) * 100, 2)
        annualized_return = round( (float(utilities.get_annualized_total_return_from_portfolio(portfolio)) * 100), 2 )
        stocks_weight = round(stocks_weight*100,1)
        bonds_weight = round(bonds_weight*100,1)

        if LEVERED:
            portfolios.append({"Content" : portfolio, "Stock Weight" : stocks_weight, "Bonds Weight" : bonds_weight, "Volatility" : volatility, "Annualized Return" : annualized_return, "Leverage Rate" : leverage_rate, 'Label' : str(stocks_weight) + '% : ' + str(bonds_weight) + ' % || ' + str(annualized_return), "End Value" : portfolio[-1], "Worst Monthly Return" : utilities.get_worst_monthly_return(portfolio), "Worst Annual Return" : utilities.get_worst_annual_return(portfolio)})
        else:
            portfolios.append({"Content" : portfolio, "Stock Weight" : stocks_weight, "Bonds Weight" : bonds_weight, "Volatility" : volatility, "Annualized Return" : annualized_return, "Leverage Rate" : 0, 'Label' : str(stocks_weight) + '% : ' + str(bonds_weight) + ' % || ' + str(annualized_return), "End Value" : portfolio[-1], "Worst Monthly Return" : utilities.get_worst_monthly_return(portfolio), "Worst Annual Return" : utilities.get_worst_annual_return(portfolio)})

    # generatae a plot of all portfolios and their funds over time    
    plt.figure()
    for portfolio in portfolios:
        plt.plot(portfolio['Content'], label = portfolio['Label'])
    plt.xlabel('Month')
    plt.ylabel('Portfolio Value')
    plt.title('Monthly Portfolio Value with Varying Stocks:Bonds Strategies')
   # plt.legend()

    # generate a plot of annualized return per stock weight
    stock_weights_used = [strategy[0] for strategy in portfolio_strategies]
    end_returns = [portfolio['Annualized Return'] for portfolio in portfolios]
    plt.figure()
    plt.plot(stock_weights_used, end_returns, marker='o', color='blue')
    plt.xlim(0, 1)
    plt.ylim(min(end_returns)-1, max(end_returns) + 1)
    plt.xlabel('Stock Weight')
    plt.ylabel('Annualized Return (%)')
    plt.title('Annualized Return vs Stock Weight')
    
    # find the best portfolio
    best_portfolio = portfolios[0]
    for portfolio in portfolios:
        if portfolio["Annualized Return"] > best_portfolio["Annualized Return"]:
            best_portfolio = portfolio
    
    # print all data except the portfolio content and label 
    print("Summary of Best Portfolio:\n")
    for key, value in best_portfolio.items():
        if key != "Content" and key != "Label":
            print(f"{key}: {value}")
    
    plt.show()
