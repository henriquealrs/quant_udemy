# This is a sample Python script.

from math import exp

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

class CouponBond:
    def __init__(self, principal, rate, maturity, interest_rate):
        self.principal = principal
        self.rate = rate/100.
        self.maturity = maturity
        self.interest_rate = interest_rate / 100.0

    def present_value(self, x, n):
        return x * exp(-self.interest_rate * n)
        # return x / ((1 + self.interest_rate) ** n)


    def calculate_price(self):
        price = 0
        for t in (1, self.maturity + 1 ):
            price = price + self.present_value(self.principal * self.rate, t)

        price = price + self.present_value(self.principal, self.maturity)

        return price

class ZeroCouponBond(CouponBond):
    def __init__(self, principal: float, maturity: int, interest_rate: float):
        CouponBond.__init__(self, principal, 0, maturity, interest_rate)
        return



def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    zcBond = ZeroCouponBond(1000.0, 2, 4)
    print(zcBond.calculate_price())
    cBond = CouponBond(1000, 10, 3, 4)
    print(cBond.calculate_price())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
