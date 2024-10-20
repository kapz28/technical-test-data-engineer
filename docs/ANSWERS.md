# Guide d'installation et d'utilisation du pipeline de données MoovitaMix de Kapilan

## Utilisation de la solution

### Dépendance

- Assurez-vous d'avoir **Python 3.7 ou une version supérieure** installé sur votre système.

### Configuration de l'environnement

1. **Installez `virtualenv`** si ce n'est pas déjà fait :

   > pip install virtualenv

2. **Créez un nouvel environnement virtuel** :

   > virtualenv venv

3. **Activez l'environnement virtuel** :

   - Sur Windows :

     > venv\Scripts\activate

   - Sur macOS et Linux :

     > source venv/bin/activate

4. **Naviguez vers le répertoire racine du projet et installez le package** :

   > pip install .

### Configuration des variables d'environnement

Avant d'exécuter le pipeline, vous pouvez définir les variables d'environnement suivantes pour personnaliser le comportement :

- `BASE_URL` : L'URL de base du serveur (par défaut, une valeur prédéfinie `DEFAULT_BASE_URL`)
- `SCHEDULED_TIME` : L'heure à laquelle le pipeline doit s'exécuter quotidiennement (par défaut, une valeur prédéfinie `DEFAULT_SCHEDULED_TIME`)
- `DATABASE_NAME` : Le nom du fichier de base de données (par défaut, une valeur prédéfinie `DEFAULT_DATABASE_NAME`)

Vous pouvez définir ces variables dans votre shell ou créer un fichier `.env` dans le répertoire racine avec le contenu suivant :

```
BASE_URL=your_custom_base_url
SCHEDULED_TIME=your_custom_time
DATABASE_NAME=your_custom_database_name
```

### Exécution de l'application

1. **Démarrez le serveur** :

   Ouvrez un terminal et exécutez :

   > start-server

2. **Exécutez le pipeline une fois** :

   Ouvrez un autre terminal et exécutez :

   > start-pipeline --test

3. **Exécutez le pipeline selon le planning** :

   Ouvrez un autre terminal et exécutez :

   > start-pipeline

4. **Exécutez les tests** :

   Ouvrez un autre terminal et exécutez :

   > run-tests

### Commandes supplémentaires

- Pour voir l'écran d'aide du pipeline :

  > start-pipeline -h

### Remarques

- La commande `start-pipeline` attendra par défaut jusqu'à l'heure programmée pour s'exécuter. Utilisez l'option `--test` pour contourner cette attente et exécuter immédiatement.

- Assurez-vous que le serveur et le pipeline sont tous deux en cours d'exécution pour la pleine fonctionnalité de l'application.

- La commande `run-tests` exécutera tous les tests pytest du projet.

## Questions (étapes 4 à 7)

### Étape 4

_votre réponse ici_

### Étape 5

_votre réponse ici_

### Étape 6

_votre réponse ici_

### Étape 7

_votre réponse ici_
