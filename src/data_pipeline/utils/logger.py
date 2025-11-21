
#l'idée on va créer un JsonFormatter qui va transformer nos log en un format json exploitable 

#on va créer une classe qui va hérité la classe logging.Formatter de la library logging 
#on va récupérér les infos de base de type :  litme, level, logger, message de la classe logging.Formatter 
#puis on va ajouter dans le json des champs nous mêmes si les valeurs sont renseignés sinon rien  : 
# des champs comme : l'environnement, l'id du run, le composant 
#et à la fin on va restituer un json lisible 

import os
import json
import logging


class JsonFormatter(logging.Formatter):
    """Transforme chaque log en JSON."""
    def format(self, record):
        log_entry = {
            "time": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        # Ajouter le contexte si présent
        for key in ["env", "run_id", "component"]:
            val = getattr(record, key, None)
            if val is not None:
                log_entry[key] = val
        return json.dumps(log_entry)


class ContextAdapter(logging.LoggerAdapter):
    """Ajoute des infos de contexte (env, run_id, component) à chaque log."""
    def process(self, msg, kwargs):
        extra = self.extra.copy()
        prefix = (
            f"[env={extra.get('env')}] "
            f"[run={extra.get('run_id')}] "
            f"[component={extra.get('component')}]"
        )
        return f"{prefix} {msg}", kwargs


def get_logger(name="data_pipeline", env=None, run_id=None, component=None, json_format=False):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    console = logging.StreamHandler()

    # Choix du formatter
    if json_format:
        formatter = JsonFormatter()
    else:
        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    console.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(console)

    env = env or os.getenv("ENV", "dev")

    return ContextAdapter(
        logger,
        {"env": env, "run_id": run_id, "component": component}
    )
