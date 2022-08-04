import lists
import functions_db

def main_shop(name, item, client):
  x, points = functions_db.grand_counter(name)
  id, product_name = get_shop_id(item)
  prices = get_price()

  if id == -1:
    return("I couldnt find that item...")
  elif prices[id] > points:
    return("You dont have enough points")
  else:
    new_points = functions_db.remove_points(name, prices[id])
    functions_db.add_purchase(name, product_name, client)
    string = "Purchased!" + '\n' + "New point balance: " + str(new_points)
    return(string)

def get_price():
  
  shop = lists.get_shop()
  prices = []
  for item, emoji in shop.items():
    price = ""
    for character in item:
      if character.isdigit():
        price = price + str(character)
    prices.append(int(price))

  return (prices)

def get_shop_id(to_buy):

  shop = lists.get_shop()
  names = []
  counter = 0
  for item, emoji in shop.items():
    name = ""
    for character in item:
      if (character != ':'):
        name = name + str(character)
      else:
        if name == to_buy:
          return counter, name
        names.append(name)
    counter += 1
  if to_buy == "get all":
    return names
  else:
    return -1

  