import argparse
from src import one, bat

def main():
    parser = argparse.ArgumentParser(description="control one.py and bat.py execution")
    parser.add_argument("-o", "--one", metavar="name", help="run one.py with name argument")
    parser.add_argument("-b", "--bat", action="store_true", help="執行 bat.py")

    args = parser.parse_args()

    if args.one:
        one.run_one(args.one)
    elif args.bat:
        bat.run_bat()
    else:
        print("Please use arguments：-o name or -b")

if __name__ == "__main__":
    main()