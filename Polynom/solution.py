import json

class Solution:
    def __init__(self, recycle_refund_choice, bag_price, refund_amount, bag_type):
        self.mapName = None
        self.recycleRefundChoice = recycle_refund_choice
        self.bagPrice = bag_price
        self.refundAmount = refund_amount
        self.bagType = bag_type
        self.orders = []

    def add_order(self, order):
        self.orders.append(order)

    def add_map_name(self, mapName):
        self.mapName = mapName

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)
