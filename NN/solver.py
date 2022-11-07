from solution import Solution


class Solver:
    bag_type_cost = [1.7, 1.75, 6, 25, 200]
    bag_type_co2_production = [30, 24, 36, 42, 60]
    bag_type_co2_transport = [3, 4.2, 1.8, 3.6, 12]
    bag_type_resuable = [0, 1, 5, 9, 12]
    bag_type_wash_time = [1, 2, 3, 5, 7]

    def __init__(self, game_info, bag_type, bag_price, refund_amount, recycle_refund_choice, solve_function):
        self.days = None
        self.population = game_info["population"]
        self.company_budget = game_info["companyBudget"]
        self.behavior = game_info["behavior"]
        self.bag_type = bag_type
        self.bag_price = bag_price
        self.refund_amount = refund_amount
        self.recycle_refund_choice = recycle_refund_choice
        self.solve_function = solve_function

    def Solve(self, days):
        self.days = days
        solution = Solution(recycle_refund_choice = self.recycle_refund_choice,
                            bag_price = self.bag_price, 
                            refund_amount = self.refund_amount,
                            bag_type = self.bag_type)

        for day in range(0, days):
            solution.add_order(self.solve_function(day))
        return solution
