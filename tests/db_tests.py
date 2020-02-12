import crossmod
from crossmod.db.interface import CrossmodDB

def main():
    print(CrossmodConsts.DB_PATH)
    db = CrossmodDB()

if __name__ == "__main__":
    main()
