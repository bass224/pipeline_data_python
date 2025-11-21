
#ici l'idée c'est de pouvoir trouver automatiquement la racine du projet, et donc après tout seul les chemins des fichiers 
#pour eviter que le projet marche juste chez nous pas sur une autre machine. 
#aussi permettre à l'utilisateur de definir tout seul la racine du projet avec export dans une variable d'environnement 



from pathlib import Path
import os 

#Récupérer la racine du projet 
ROOT_PROJECT = Path(__file__).resolve().parents[2]


#permettre à l'utilisateur d'écraser la racine du projet via une variable d'environnement 

CUSTOM_DATA_DIR = os.getenv("DATA_PIPELINE_DATA_DIR")
# L'idée c'est quand le user fait :
# export DATA_PIPELINE_DATA_DIR=/Users/mariamabah/data  #attention a pas mettre d'espace entre avant = et après égal
#si on veut vérifier que la variable est bien exporté : echo $DATA_PIPELINE_DATA_DIR
#si on veut supprimer la variable : unset DATA_PIPELINE_DATA_DIR
#si onv eut la vider : export DATA_PIPELINE_DATA_DIR="" 

#alors la racine du projet sera CUSTOM_DATA_DIR = /Users/mariamabah/data  comme ça l'utilisateur defini sa propre racine 
#sinon ce sera la racine du projet qu'on aura calculé avec : ROOT_PROJECT = Path(__file__).resolve().parents[2]


#donc on va dire : si CUSTOM_DATA_DIR est défini alors ce sra ça le DATA_DIR snon ce sera ROOT_PROJECT

if CUSTOM_DATA_DIR:
    DATA_DIR = Path(CUSTOM_DATA_DIR)
    
else:
    DATA_DIR = ROOT_PROJECT /"data"
   

#Maintenant on défini tous les chemins 


RAW_DATA = DATA_DIR /"raw"
INTERIM_DATA = DATA_DIR /"interim"
PROCESSED_DATA = DATA_DIR /"processed"


#on va faire une création automatique des dossiers s'ils n'existent pas déjà 
#en gros si : data/raw n'existe pas crée le, 
#si data/interim n'existe pas crée le 
#si data/processed n'existe pas crée le 
#avec parents = True, on lui dit crée le dossier raw si son parent data n'existe pas crée le parent aussi 
#avec exist_ok = True, on lui dit, si le dossier existe déjà, ne me dit pas erreur le dossier existe déjà, passe juste à la suite


for d in [RAW_DATA, INTERIM_DATA, PROCESSED_DATA]:
    d.mkdir(parents=True, exist_ok=True)

