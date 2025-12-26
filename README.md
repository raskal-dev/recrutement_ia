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
    │   └── OpenRouter_config.py
    ├── Controllers/       # Contrôleurs (logique métier)
    │   └── AI_controller.py
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
2. Ajouter votre clé API OpenRouter et le jeton interne dans `.env`:
   ```
   OPENROUTER_API_KEY=your_key_here
   APP_URL=http://localhost:8000
   ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
   AI_INTERNAL_TOKEN=change_me_securely
   ```

## Lancer le service

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Le service sera disponible sur `http://localhost:8000` (docs: `/docs`).
Le backend Express doit appeler ce service en ajoutant l'en-tête `x-internal-token` avec la valeur de `AI_INTERNAL_TOKEN`.

Documentation API disponible sur `http://localhost:8000/docs`

## Endpoints

- `GET /` - Informations sur le service
- `GET /health` - Vérification de santé
- `GET /models` - Liste des modèles disponibles
- `POST /ai/chat` - Chat avec l'IA (protégé par `x-internal-token`)
- `POST /ai/analyze-cv` - Analyse de CV (protégé)
- `POST /ai/generate-job-description` - Génération de description de poste (protégé)

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
- Les modèles gratuits par défaut (ordre de priorité) sont configurés dans `src/Configs/OpenRouter_config.py` :
  - `qwen/qwen3-coder:free`
  - `qwen/qwen3-235b-a22b:free`
  - `nousresearch/hermes-3-llama-3.1-405b:free`
  - `openai/gpt-oss-120b:free`
- Le backend Express fait un proxy vers ce service pour l'authentification et la sécurité
