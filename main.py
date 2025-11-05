from HMM_v0_02IPY import *
import time

def calculation_process(stock1=None, stock2=None, period=None, t=None, shift=None):
    print("\n=============================================")
    print("... Calculating HMM ...")

    time.sleep(2)

    observation_states = generate_observation_states(t)

    print(f"Stock Data      : {stock1} vs {stock2}")        
    print(f"Period          : {period}")
    print(f"Observation (T) : {t}")
    print(f"Shift           : {shift}")
    print("\n--- OUTPUT ---")
    
    data = download_stockData(stock1, stock2, period)
    movements = stock_movement(stock1, stock2, data, shift)
    initial_dist = calc_init_dist(movements)
    prob_trans = calc_prob_trans(movements)
    prob_ems = calc_prob_ems(movements)

    print(initial_dist, "\n")
    print(prob_trans, "\n")
    print(prob_ems, "\n")

    results = calc_best_path(observation_states, prob_ems, prob_trans, t, initial_dist)
    accuracies = calc_accuracies(observation_states, results, movements, t)

    print(accuracies)

    print("=============================================\n")

def get_integer_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("ERROR: Input must be an integer.")

def compare_stock():
    print("\n--- Input Stock Data ---")
    # Input
    stock_ticker_1 = input("Input Stock Ticker 1: ").upper()
    stock_ticker_2 = input("Input Stock Ticker 2: ").upper()
    period = input("Input period (valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max): ")
    observation_t = get_integer_input("Input observations number (T): ")
    shift = get_integer_input("Input shift (i.e. shift data, so compare to n next day): ")

    # calculation process
    calculation_process(stock1=stock_ticker_1, stock2=stock_ticker_2, period=period, t=observation_t, shift=shift)

    while True:
        print("--- Want to continue? ---")
        print("1. Change stock")
        print("2. Change shift")
        print("3. Return to main menu")
        choice = input("Input choice: ")

        if choice == '1':
            print("\n--- Change Stock Ticker ---")
            stock_ticker_1 = input("Input new stock ticker 1: ").upper()
            stock_ticker_2 = input("Input new stock ticker 2: ").upper()
            shift = get_integer_input("Input shift: ")

            calculation_process(stock1=stock_ticker_1, stock2=stock_ticker_2, period=period, t=observation_t, shift=shift)
        elif choice == '2':
            print("... Change shift ...")
            shift = get_integer_input("Input shift: ")
            calculation_process(stock1=stock_ticker_1, stock2=stock_ticker_2, period=period, t=observation_t, shift=shift)
        elif choice == '3':
            print("... Return to main menu ...")
            break
        else:
            print("Choice is invalid.")

def main_menu():
    while True:
        print("\n#################################")
        print("#       HMM STOCK v0.01       #")
        print("#################################")
        print("1. Compare Stock")
        print("2. Exit")
        print("---------------------------------")

        user_choice = input("Input your choice (1/2): ")

        if user_choice == '1':
            compare_stock()
        elif user_choice == '2':
            print("Thank you for using this program. See you soon! :))))")
            break  # exit program
        else:
            print("Choice is invalid. Please try again.")
            time.sleep(1)

# run program
if __name__ == "__main__":
    main_menu()