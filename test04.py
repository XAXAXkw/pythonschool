def main():
    my_name = input("com ta dius?")
    print("hola " + my_name)
    my_age = input("quants anys tens")
    my_age=int(my_age)
    print(type(my_age))
    if my_age<18:
        print("pos que tonto")
    else:
        print("ets un mabuelok, nanu!" + f"{my_age}" +" anys? hahah! loser!")

if __name__ == "__main__":
    main()