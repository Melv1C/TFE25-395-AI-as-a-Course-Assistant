import sys
import ast

@@code@@

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py '[1, 2, 3]'")
        sys.exit(1)

    # Get the argument and parse it as a list
    arg = sys.argv[1]
    try:
        int_list = ast.literal_eval(arg)
        if isinstance(int_list, list) and all(isinstance(i, int) for i in int_list):
            print(compter_batiments_visibles(int_list))
        else:
            raise ValueError
    except Exception:
        print("Invalid input. Please provide a list of integers.")
    