# Automate IA local (≤ 1 GB RAM)

Ce projet fournit une base **prête à étendre** pour créer un automate IA local qui :
- charge un modèle depuis **Hugging Face** ;
- reste dans une contrainte mémoire d’environ **1 GB RAM max** (via modèle GGUF quantifié) ;
- dispose d’une liste variée d’outils (web, extraction, formulaires, stockage sécurisé, etc.) ;
- peut mémoriser des informations importantes de manière sécurisée.

> ⚠️ Sécurité : ce projet inclut un coffre chiffré pour secrets, mais il est recommandé d’utiliser un gestionnaire de secrets dédié (Vault, 1Password CLI, etc.) en production.

---

## Roadmap

### Phase 0 — Documentation & cadrage (ce README)
- [x] Définir les objectifs fonctionnels et non fonctionnels.
- [x] Décrire l’architecture minimale.
- [x] Détailler le plan d’implémentation.

### Phase 1 — Noyau IA local
- [x] Chargement d’un modèle GGUF Hugging Face avec `llama-cpp-python`.
- [x] Paramètres orientés faible mémoire (contexte court, threads limités).
- [x] Interface `generate()` unifiée.

### Phase 2 — Outils IA (tooling)
- [x] Navigation web (GET + extraction texte).
- [x] Recherche web simple (provider libre configurable).
- [x] Remplissage de formulaire web via Playwright.
- [x] Outils système sûrs (lecture/écriture fichier local contrôlée).

### Phase 3 — Mémoire et secrets
- [x] Stockage local chiffré des données sensibles (mot de passe API, credentials, etc.).
- [x] API simple `set_secret/get_secret/list_keys`.

### Phase 4 — Orchestration automate
- [x] Boucle agent avec registre d’outils.
- [x] Exécution d’outils par intention de l’utilisateur.
- [x] CLI de démonstration.

### Phase 5 — Durcissement (à faire)
- [ ] Sandbox stricte des actions navigateur.
- [ ] Journalisation audit des accès secrets.
- [ ] Politique d’autorisation explicite par outil/action.
- [ ] Tests d’intégration + CI.

---

## Choix du modèle (≤ 1 GB RAM)

Configuration proposée :
- Modèle : `Qwen2.5-0.5B-Instruct` en GGUF quantifié (`Q4_K_M`) depuis Hugging Face.
- Runtime : `llama-cpp-python`.
- Empreinte typique : ~0.4 à 0.9 GB RAM selon contexte et OS.

Exemple de repo HF compatible :
- `bartowski/Qwen2.5-0.5B-Instruct-GGUF`

> Astuce RAM : garder `n_ctx` bas (ex: 1024) et éviter de charger plusieurs modèles simultanément.

---

## Arborescence

```txt
.
├─ README.md
├─ requirements.txt
└─ src/
   ├─ agent.py
   ├─ main.py
   ├─ model_loader.py
   ├─ secure_store.py
   └─ toolkit.py
```

---

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
```

Variables d’environnement recommandées :

```bash
export HF_REPO_ID="bartowski/Qwen2.5-0.5B-Instruct-GGUF"
export HF_FILENAME="Qwen2.5-0.5B-Instruct-Q4_K_M.gguf"
export AGENT_DATA_DIR=".agent_data"
```

---

## Lancer l’automate

```bash
python -m src.main
```

Exemples de commandes dans le CLI :
- `web:https://example.com`
- `search:intelligence artificielle locale`
- `secret:set:email_password:mon_mot_de_passe`
- `secret:get:email_password`

---

## Sécurité & bonnes pratiques

- Ne jamais stocker un mot de passe en clair dans le code.
- Le coffre local est chiffré avec une clé Fernet stockée localement (`.agent_data/master.key`) :
  - en prod, placer la clé dans un gestionnaire de secrets externe ;
  - rotation de clé recommandée.
- Restreindre les domaines autorisés pour la navigation/formulaire.
- Ajouter validation des entrées pour éviter les injections de commandes.

---

## Limites actuelles

- Agent orienté prototype (pas encore multi-agent / mémoire long terme avancée).
- Recherche web basique (à brancher sur un provider robuste si nécessaire).
- Le remplissage de formulaire dépend de sélecteurs CSS stables.

---

## Prochaines évolutions recommandées

1. Politique d’autorisations interactive (confirmations par action sensible).
2. Planification de tâches (scheduler + retries).
3. Observabilité (OpenTelemetry, traces, dashboards).
4. Pack Docker CPU-only.
5. Tests E2E sur site de démo de formulaires.
