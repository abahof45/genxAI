#this script should test the capability of all the ai models at once
#@GenxAI Dev's

#start
from core import core
from api_key_manager import OPENAI_API_KEY
from intel import sim
from model import train_model
from ai2 import core
from data_handler import train_model

a = input("you:")

ans = core(sim(train_model(train_model(core(a, OPENAI_API_KEY)))))

print("response: {ans}")