import random

attention = ["HELLO!", "HI!", "*mhuack*", "*licks you*", "你好小猫"]

shop = {"Get purred: 100" : ":drooling_face:",
        "Kitten: 1500": ":heart_eyes_cat:",
        "Woman: 5000": ":dress:"}

def get_shop():
  return shop
  
def get_attention():
  attention_phrase = random.choice(tuple(attention))
  return (attention_phrase)

def get_monke():
  monke_link = random.choice(tuple(monkey_gif))
  return (monke_link)