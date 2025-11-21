
#quand on met if __name__ =="__main__": 
#Ce if permet de dire à Python :
#Si ce fichier est exécuté directement → exécute main() : exemple si on fait python test_ingestion.py (alors il execute main)
#Si ce fichier est importé depuis un autre fichier → ne l’exécute pas.  : cad si on fait : 
#from data_pipeline.scripts.test_ingestion import main alors tu n'exécutes pas le script test_ingestion.py le fichier reste calme 
#si on ne faisait pas le if __name__ == "__main__", alors le simple fait de faire : 
#from data_pipeline.ingestion.ingestion import load_json, load_csv, save_interim  pour utiliser la fonction 
# load_json déclencherait : charger users.json, puis charger sales.csv puis écrire interim en un mot tout lancer automatiquement
#alors qu'on voulait juste charger le module pour utiliser une fonction 
#donc avec le if, les fonctions sont importables, le pipeline ne s'exécute pas


from pathlib import Path
from data_pipeline.ingestion.ingestion import load_json, load_csv, save_interim


def main():
    users = load_json(Path("data/raw/users.json"))
    sales = load_csv(Path("data/raw/sales.csv"))

    save_interim(users, "users_interim.csv")
    save_interim(sales, "sales_interim.csv")


if __name__ == "__main__":
    main()
