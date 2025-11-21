class my_class():
    identity = "meow"

my_dict = {
    "dog": my_class(),
    "cat": my_class()
}

for key in my_dict:
    print(my_dict[key].identity)