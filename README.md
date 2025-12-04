# Service IA - Recrutement

Service FastAPI pour les fonctionnalités IA de la plateforme de recrutement.

## Structure du projet

Le projet suit la même architecture que le backend Express :

```
Recrutement_ia/
├── main.py                 # Point d'entrée de l'application
├── requirements.txt        # Dépendances Python
├── README.md              # Documentation
└── src/
    ├── Configs/          # Configurations (OpenRouter, etc.)
    │   └── OpenRouter.config.py
    ├── Controllers/       # Contrôleurs (logique métier)
    │   └── AI.controller.py
    ├── Middlewares/       # Middlewares (CORS, etc.)
    │   └── CORS.py
    ├── Routes/            # Routes API
    │   ├── index.py
    │   └── AI.routes.py
    ├── Services/          # Services (logique métier)
    │   └── OpenRouterService.py
    └── Utils/             # Utilitaires
        ├── BaseError.py
        └── Interface/
            └── IModels.py
```

## Installation

```bash
# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Sur Linux/Mac:
source venv/bin/activate
# Sur Windows:
venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

## Configuration

1. Copier `.env.example` vers `.env`
2. Ajouter votre clé API OpenRouter dans `.env`:
   ```
   OPENROUTER_API_KEY=your_key_here
   APP_URL=http://localhost:8000
   ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
   ```

## Lancer le service

```bash
uvicorn main:app --reload --port 8000
```

Le service sera disponible sur `http://localhost:8000`

Documentation API disponible sur `http://localhost:8000/docs`

## Endpoints

- `GET /` - Informations sur le service
- `GET /health` - Vérification de santé
- `GET /models` - Liste des modèles disponibles
- `POST /ai/chat` - Chat avec l'IA
- `POST /ai/analyze-cv` - Analyse de CV
- `POST /ai/generate-job-description` - Génération de description de poste

## Architecture

Le service FastAPI suit la même structure que le backend Express :

- **Routes** : Définition des endpoints API
- **Controllers** : Gestion des requêtes HTTP et validation
- **Services** : Logique métier et communication avec OpenRouter
- **Utils** : Classes utilitaires (erreurs, modèles)
- **Configs** : Configurations (API keys, URLs)
- **Middlewares** : Middlewares (CORS, authentification)

## Notes

- Le service utilise OpenRouter pour accéder aux modèles IA gratuits
- Les modèles par défaut sont configurés dans `src/Configs/OpenRouter.config.py`
- Le backend Express fait un proxy vers ce service pour l'authentification et la sécurité
