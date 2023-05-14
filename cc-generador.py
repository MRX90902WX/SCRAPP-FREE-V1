import random
import requests
import json
from randomtimestamp import randomtimestamp
from datetime import datetime
from os import system
system("clear")
system("chmod 777 cc-generador.py")

class CC():
  '''Individual card info and methods.
  '''


  CCDATA = {
    'American': {
      'len_num': 15,
      'len_cvv': 4,
      'pre': [34, 37],
      'remaining': 13
    },
    'Diners': {
      'len_num': 14,
      'len_cvv': 3,
      'pre': [36],
      'remaining': 12
    },
    'Mastercard': {
      'len_num': 16,
      'len_cvv': 3,
      'pre': [51, 55, 54, 52, 53, 57, 56],
      'remaining': 14
    },
    'Visa': {
      'len_num': 16,
      'len_cvv': 3,
      'pre': [42, 41, 44, 40, 46, 45, 49, 48, 47, 43],
      'remaining': 15
    },    
  }

  def __init__(self):
    self.cc_type = None
    self.cc_len = None
    self.cc_num = None
    self.cc_cvv = None
    self.cc_exp = None
    self.cc_prefill = []

  def generate_cc_exp(self):
    '''Generates a card expiration date that is 
    between 1 and 3 years from today. Sets `cc_exp`.
    '''
    self.cc_exp = randomtimestamp(
        start_year = datetime.now().year + 1,
        text = True,
        end_year = datetime.now().year + 3,
        start = None,
        end = None,
        pattern = "%m/%Y")
    
  def generate_cc_cvv(self):
    '''Generates a type-specific CVV number.
    Sets `cc_cvv`. 
    '''
    this = []
    length = self.CCDATA[self.cc_type]['len_cvv']

    for x_ in range(length):
      this.append(random.randint(0, 9))

    self.cc_cvv = ''.join(map(str,this))

  def generate_cc_prefill(self):
    '''Generates the card's starting numbers
    and sets `cc_prefill`.
    '''
    this = self.CCDATA[self.cc_type]['pre']
    self.cc_prefill = random.choices(this)

  def generate_cc_num(self):
    '''Uses Luhn algorithm to generate a theoretically 
    valid credit card number. Sets `cc_num`. 
    ''' 
    remaining = self.CCDATA[self.cc_type]['remaining']
    working = self.cc_prefill + [random.randint(1,9) for x in range(remaining - 1)] 

    check_offset = (len(working) + 1) % 2
    check_sum = 0

    for i, n in enumerate(working):
      if (i + check_offset) % 2 == 0:
        n_ = n*2
        check_sum += n_ -9 if n_ > 9 else n_
      else:
        check_sum += n

    temp = working + [10 - (check_sum % 10)]
    self.cc_num = "".join(map(str,temp)) 

  def return_new_card(self):
    '''Returns a dictionary of card details.
    '''
    return {'cc_type': self.cc_type,
            'cc_num': self.cc_num, 
            'cc_cvv': self.cc_cvv,
            'cc_exp': self.cc_exp}

  def print_new_card(self):
    '''Prints a single card to console.
    '''
    hr = '\033[1;31m----------------------------------------'

    print(f'%s' % hr)
    print(f'\033[1;31m[♆]\033[1;34mMARCA : \033[1;37m%s' % self.cc_type)
    print(f'\033[1;31m[№]\033[1;34mCARD  : \033[1;37m%s' % self.cc_num)
    print(f'\033[1;31m[⌨]\033[1;34mFECHA : \033[1;37m%s' % self.cc_exp)
    print(f'\033[1;31m[✮]\033[1;34mCVV   : \033[1;37m%s' % self.cc_cvv)
    bin = (self.cc_num)

    r = requests.get("https://bin-checker.net/api/" + bin)                                               
    json = r.json()
    country = json["country"]
    pais = country["name"]
    print("\033[1;31m[ϟ]\033[1;34mPAIS  :\033[1;37m", pais)
    print("\033[1;31m[✔]\033[1;34mNIVEL :\033[1;37m", json["level"])
    bank = json["bank"]
    nombre = bank["name"]
    print("\033[1;31m[$]\033[1;34mBANCO :\033[1;37m", nombre)

class CCNumGen(): 
  '''Generates theoretically valid credit card numbers
  with CVV and expiration date. Prints a list of dictionaries. 
  '''
  hr = '\033[1;31m----------------------------------------'

  card_types = ['American','Diners','Mastercard','Visa']

  def __init__(self, type='Visa', number=1):

    self.type = type
    self.num = number
    self.card_list = []

    if self.type not in self.card_types:
      print('Card type not recognized. Task ended.')
      return
    if not isinstance(self.num, int):
      print('Number of cards must be a whole number. Task ended.')
      return

    print(self.hr)
    print(f'\033[1;31mGeneradas %s Tarjetas de %s' % (self.num, self.type))

    for x_ in range(0, self.num):
      new = CC()
      new.cc_type = self.type
      new.generate_cc_exp()
      new.generate_cc_cvv()
      new.generate_cc_prefill()
      new.generate_cc_num()
      self.card_list.append(new.return_new_card())
      new.print_new_card()

    print(self.hr)
    print('Completado.')
    print(self.hr)

  def print_card_list(self):
    '''Prints the list of cards to console.
    '''
    for d in self.card_list:
      print('\033[1;36m------------------------------')
      for k in d:
        print(f'%s: %s' % (k, d[k]))

#Banner
print("\033[1;37m")
print("/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/")
print("╔═╗╔═╗╦═╗╔═╗╔═╗╔═╗   ╔═╗╦═╗╔═╗╔═╗")
print("╚═╗║  ╠╦╝╠═╣╠═╝╠═╝───╠╣ ╠╦╝║╣ ║╣ ")
print("╚═╝╚═╝╩╚═╩ ╩╩  ╩     ╚  ╩╚═╚═╝╚═╝")
print("/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/")

#Menu
print("")
print("")
print(" 1. American Express")
print(" 2. Diners")
print(" 3. Mastercard")
print(" 4. Visa")
print(" 5. Salir")
print("")

card_type = input(" Opción: ")
print("")

if card_type == "1":
   system("clear")
   American = CCNumGen('American', 100)
elif card_type == "2":
   system("clear")
   Diners = CCNumGen('Diners', 100)
elif card_type == "3":
   system("clear")
   Mastercard = CCNumGen('Mastercard', 100)
elif card_type == "4":
   system("clear")
   Visa = CCNumGen('Visa' , 100)
elif card_type == "5":
   exit()
else:
    print(" \033[1;31m[x]Opcion invalida")
    exit()

print("")
indesicion = input("\033[1;34m[\033[1;37m☆\033[1;34m]\033[1;37mDesea extrapolar \033[1;34msi/no: \033[1;37m")
if indesicion == "si":
   system("bash extrapolacion")
else:
   exit()

