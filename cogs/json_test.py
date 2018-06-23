import sys
sys.path.insert(0, 'utils')

from dataIO import dataIO


test_list = []
for i in range(10):
    test_d = {'Hello':i}
    test_list.append(test_d)

if not dataIO.is_valid_json("../data/test.json"):
    print("Creating empty {}...".format("test.json"))
    dataIO.save_json("../data/test.json", [])

dataIO.save_json("../data/test.json", test_list)

json_test = dataIO.load_json("../data/test.json")

print (json_test)
