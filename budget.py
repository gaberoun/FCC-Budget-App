def truncate(n):
  return int(n * 10) / 10


def get_totals(categories):
  total = 0
  breakdown = []
  for category in categories:
    total += category.get_withdrawals()
    breakdown.append(category.get_withdrawals())
  output = list(map(lambda x: truncate(x / total), breakdown))
  return output


def create_spend_chart(categories):
  result = "Percentage spent by category\n"
  i = 100
  totals = get_totals(categories)
  while i >= 0:
    spaces = " "
    for total in totals:
      if total * 100 >= i:
        spaces += "o  "
      else:
        spaces += "   "

    result += str(i).rjust(3) + '|' + spaces + ('\n')
    i -= 10

  dashes = '-' + '---' * len(categories)
  names = []
  x_axis = ""
  for category in categories:
    names.append(category.name)

  maxi = max(names, key=len)

  for x in range(len(maxi)):
    name_str = '     '
    for name in names:
      if x >= len(name):
        name_str += "   "
      else:
        name_str += name[x] + "  "

    if x != len(maxi) - 1:
      name_str += '\n'

    x_axis += name_str

  result += dashes.rjust(len(dashes) + 4) + "\n" + x_axis
  return result


class Category:

  def __init__(self, name):
    self.name = name
    self.ledger = list()

  def __str__(self):
    title = f'{self.name:*^30}\n'
    items = ""
    total = 0
    for item in self.ledger:
      items += f'{item["description"][0:23]:23}' + f'{item["amount"]:>7.2f}' + '\n'
      total += item['amount']

    output = title + items + 'Total: ' + str(total)
    return output

  def deposit(self, amount, description=''):
    self.ledger.append({'amount': amount, 'description': description})

  def withdraw(self, amount, description=''):
    if self.check_funds(amount):
      self.ledger.append({'amount': -amount, 'description': description})
      return True
    return False

  def get_balance(self):
    total_balance = 0
    for item in self.ledger:
      total_balance += item['amount']
    return total_balance

  def transfer(self, amount, category):
    if self.check_funds(amount):
      self.withdraw(amount, 'Transfer to ' + category.name)
      category.deposit(amount, 'Transfer from ' + self.name)
      return True
    return False

  def check_funds(self, amount):
    if amount > self.get_balance():
      return False
    return True

  def get_withdrawals(self):
    total = 0
    for item in self.ledger:
      if item['amount'] < 0:
        total += item['amount']
    return total
