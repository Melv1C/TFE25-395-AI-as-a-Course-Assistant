import sys

@@code@@

if __name__ == "__main__":
    if len(sys.argv) > 1:
        fizz_buzz(int(sys.argv[1]))
    else:
        print("Please provide a number as an argument.")
    