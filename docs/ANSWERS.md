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
  
  
<br />

# Questions (étapes 4 à 7)

## Conception et application de base de données
J'ai remarqué que le schéma que nous utilisons provient de la documentation API générée par FastAPI. C'est une excellente fonctionnalité de FastAPI, car elle génère automatiquement la documentation basée sur la structure de notre code et les annotations de type.

```
CREATE_SONGS_TABLE = '''
CREATE TABLE IF NOT EXISTS songs (
    id INTEGER PRIMARY KEY,
    name TEXT,
    artist TEXT,
    songwriters TEXT,
    duration TEXT,
    genres TEXT,
    album TEXT,
    created_at TEXT,
    updated_at TEXT
)
'''

CREATE_USERS_TABLE = '''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    gender TEXT,
    favorite_genres TEXT,
    created_at TEXT,
    updated_at TEXT
)
'''

CREATE_LISTENING_HISTORY_TABLE = '''
CREATE TABLE IF NOT EXISTS listening_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    items TEXT,
    created_at TEXT,
    updated_at TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
'''
```

Actuellement, nous utilisons SQLite comme fichier de base de données de sortie. Voici quelques avantages et inconvénients que j'ai observés concernant l'utilisation de SQLite dans ce contexte :

Avantages de l'utilisation de SQLite :

1. Simplicité : SQLite ne nécessite pas de processus serveur séparé, ce qui s'aligne parfaitement avec l'objectif de FastAPI d'être simple et facile à utiliser.

2. Support intégré : Python a un support intégré pour SQLite, ce qui en fait un choix naturel pour notre projet FastAPI.

3. Portabilité : Comme toute la base de données est contenue dans un seul fichier, il est facile de la déplacer ou de la sauvegarder, ce qui est très pratique pendant le développement et les tests.

4. Configuration rapide : Je peux démarrer rapidement sans configuration complexe de base de données, ce qui est idéal pour le prototypage rapide.

5. Adapté aux tests : La fonctionnalité de base de données en mémoire de SQLite est excellente pour exécuter des tests, ce qui est crucial pour notre application FastAPI.

Inconvénients de l'utilisation de SQLite :

1. Limitations de concurrence : Un inconvénient est que SQLite a des limitations sur les écritures concurrentes, ce qui pourrait devenir problématique si notre application évolue et gère de nombreux utilisateurs simultanés.

2. Ensemble de fonctionnalités SQL limité : Bien qu'il fonctionne pour de nombreuses applications, SQLite manque de certaines fonctionnalités avancées dont nous pourrions avoir besoin à mesure que le projet se développe.

3. Accès réseau : SQLite ne prend pas en charge les opérations client/serveur sur un réseau, ce qui pourrait limiter nos options de déploiement à l'avenir.

4. Préoccupations de scalabilité : Pour des ensembles de données plus volumineux ou des applications à fort trafic, je ne suis pas sûr que SQLite tiendra aussi bien que d'autres options.

Étant donné que ce schéma provient de la documentation de FastAPI, il est logique pour nous d'utiliser SQLite pour le moment, en particulier pendant la phase de développement initial. C'est parfait pour les petites applications et le développement rapide. Cependant, si nous prévoyons une croissance significative ou avons besoin de fonctionnalités de base de données plus avancées à l'avenir, j'envisagerai certainement de passer à un système plus robuste comme PostgreSQL tout en continuant à profiter des excellentes capacités de génération de schéma et de documentation de FastAPI.

## Système de Surveillance pour le Pipeline

Je mettrais en place un système de journalisation détaillé au sein de la fonction `daily_data_retrieval`. 

Cette journalisation me permettrait de suivre chaque étape du processus, y compris son début et sa fin, les données récupérées, et tout problème rencontré.

En plus de la journalisation, je mettrais en place un système de notification - comme des alertes par e-mail ou des messages via un service tel que Slack - pour nous informer de toute erreur critique ou si le pipeline ne s'exécute pas comme prévu.

### Pour la surveillance, je me concentrerais sur plusieurs métriques clés :

1. **Statut d'exécution** : Je suivrais si chaque exécution quotidienne a réussi ou échoué.

2. **Temps d'exécution** : Mesurer le temps que prend le pipeline pour s'exécuter aiderait à identifier les goulots d'étranglement de performance.

3. **Volume de données** : Je garderais un œil sur le nombre d'enregistrements traités pour chaque type de données - chansons, utilisateurs et historique d'écoute.

4. **Taux d'erreur** : Suivre le nombre et les types d'erreurs rencontrées pendant l'exécution serait crucial pour maintenir la fiabilité.

5. **Latence des données** : Je voudrais mesurer le délai entre la collecte des données et leur disponibilité dans la base de données.

6. **Utilisation des ressources** : Surveiller l'utilisation du CPU et de la mémoire pendant l'exécution aiderait à garantir que notre application fonctionne efficacement.

Pour mettre cela en œuvre, je modifierais le code existant pour inclure des déclarations de journalisation aux points critiques de la fonction `daily_data_retrieval`. 

De cette façon, je pourrais capturer des métriques importantes et les enregistrer pour une analyse ultérieure.

Dans l'ensemble, cette approche me permettrait de créer un système de surveillance plus robuste pour notre pipeline de données, nous permettant de réagir rapidement à tout problème et de maintenir des opérations fluides.

## Personnalisation des Recommandations Musicales

Pour personnaliser nos recommandations et les aligner sur les habitudes d'écoute de chaque utilisateur, je mettrai en place une approche basée sur des clusters. 

J'utiliserai l'algorithme K-means pour regrouper les chansons en clusters en fonction de leurs caractéristiques audio et de leurs métadonnées. Ensuite, j'analyserai l'historique d'écoute de chaque utilisateur pour identifier les clusters les plus fréquemment écoutés. 

Lors de la génération des recommandations, je donnerai la priorité aux chansons de ces clusters préférés, en veillant à ce que la prochaine chanson recommandée soit plus susceptible de provenir d'un cluster pour lequel l'utilisateur a montré une forte affinité. 

Cette méthode me permettra de maintenir la pertinence tout en offrant de la variété dans les styles préférés de l'utilisateur. Je mettrai en place un processus de sélection aléatoire pondéré, où les clusters seront choisis avec des probabilités proportionnelles à l'engagement historique de l'utilisateur avec ceux-ci. 

Cette approche équilibrera la familiarité et la découverte, offrant aux utilisateurs des recommandations à la fois confortables et nouvelles. En adaptant les recommandations aux préférences de clusters de chaque utilisateur, je pense que nous améliorerons la personnalisation de l'expérience de découverte musicale, augmentant potentiellement la satisfaction et l'engagement des utilisateurs avec notre plateforme.

## Automatisation du Réentraînement du Modèle de Recommandation

Pour automatiser le réentraînement de notre modèle de recommandation basé sur les clusters, je vais :

1. **Collecter et prétraiter** en continu de nouvelles données de chansons et l'historique d'écoute des utilisateurs.
2. **Mettre en place** un processus hebdomadaire pour mettre à jour l'algorithme de clustering K-means, recalculant les préférences des utilisateurs en fonction de leurs interactions récentes avec les chansons.
3. **Surveiller** des métriques de performance telles que l'engagement des utilisateurs et la cohésion des clusters, avec des alertes pour toute déviation significative.
4. **Déployer automatiquement** le modèle mis à jour s'il montre de meilleures performances lors des tests A/B, tout en ayant un mécanisme de retour en arrière en cas de problème.
5. **Intégrer** les retours des utilisateurs pour affiner les affectations des clusters.
6. **Mettre en œuvre** une détection de dérive pour déclencher un réentraînement complet si nécessaire.

En veillant à ce que notre modèle reste à jour avec l'évolution des tendances et des préférences, nous pourrons améliorer la personnalisation des recommandations musicales, augmentant ainsi la satisfaction et l'engagement des utilisateurs sur notre plateforme.

Pour automatiser le réentraînement de notre modèle de recommandation basé sur les clusters, je collecterai et prétraiterai en continu de nouvelles données de chansons et l'historique d'écoute des utilisateurs. Je mettrai en place un processus hebdomadaire pour mettre à jour l'algorithme de clustering K-means, recalculant les préférences des utilisateurs en fonction de leurs interactions récentes avec les chansons. Des métriques de performance telles que l'engagement des utilisateurs et la cohésion des clusters seront surveillées, avec des alertes pour toute déviation significative. Si le modèle mis à jour montre de meilleures performances lors des tests A/B, il sera automatiquement déployé, tandis qu'un mécanisme de retour en arrière sera en place en cas de problème. De plus, j'intégrerai les retours des utilisateurs pour affiner les affectations des clusters et mettrai en œuvre une détection de dérive pour déclencher un réentraînement complet si nécessaire. En veillant à ce que notre modèle reste à jour avec l'évolution des tendances et des préférences, nous pourrons améliorer la personnalisation des recommandations musicales, augmentant ainsi la satisfaction et l'engagement des utilisateurs sur notre plateforme.
