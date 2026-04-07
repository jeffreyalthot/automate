# Automate IA local (≤ 1 GB RAM)

Ce projet fournit une base **prête à étendre** pour créer un automate IA local qui :
- charge un modèle depuis **Hugging Face** ;
- reste dans une contrainte mémoire d’environ **1 GB RAM max** (via modèle GGUF quantifié) ;
- dispose d’une liste variée d’outils (web, extraction, formulaires, stockage sécurisé, etc.) ;
- peut mémoriser des informations importantes de manière sécurisée.

> ⚠️ Sécurité : ce projet inclut un coffre chiffré pour secrets, mais il est recommandé d’utiliser un gestionnaire de secrets dédié (Vault, 1Password CLI, etc.) en production.

---

## Roadmap (détaillée)

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

### Phase 6 — Navigation web autonome (à faire)
- [ ] Ajouter un moteur de navigation guidée par objectif (plan → action → vérification).
- [ ] Gérer les sessions persistantes (cookies chiffrés, profil navigateur isolé).
- [ ] Implémenter limites anti-abus : timeout, max étapes, allowlist de domaines.
- [ ] Ajouter extraction structurée (tables, liens, métadonnées) en plus du texte brut.

### Phase 7 — Automatisation de formulaires avancée (à faire)
- [ ] Détecter automatiquement les champs (`input`, `select`, `textarea`) et leur type.
- [ ] Implémenter une stratégie “dry-run” (prévisualiser les valeurs avant soumission).
- [ ] Ajouter modes de soumission : manuel confirmé / automatique conditionnel.
- [ ] Capturer preuve d’exécution (capture écran + log horodaté).

### Phase 8 — Mémoire utile & gouvernance des données (à faire)
- [ ] Classifier les données stockées : secret / personnel / temporaire / public.
- [ ] Ajouter expiration (TTL) et suppression planifiée des données sensibles.
- [ ] Introduire chiffrement au repos des journaux contenant données utilisateur.
- [ ] Export/import sécurisé du coffre pour migration locale.

### Phase 9 — Fiabilisation produit (à faire)
- [ ] Définir profils d’exécution : `dev`, `safe`, `autonomous`.
- [ ] Mettre en place tests E2E (navigation, formulaires, secrets).
- [ ] Ajouter métriques de performance (latence, RAM max, taux d’échec outil).
- [ ] Documenter procédure de reprise après incident (crash, corruption coffre).

### Phase 10 — Documentation d’architecture (à faire)
- [ ] Écrire une spec d’architecture (`docs/architecture.md`) avec :
  - [ ] flux “prompt → plan → outil → vérification” ;
  - [ ] séparation des responsabilités (LLM, orchestrateur, toolkit, coffre secrets) ;
  - [ ] surfaces d’attaque et contre-mesures.
- [ ] Décrire un **threat model local** (machine compromise, phishing formulaire, fuite logs).
- [ ] Ajouter un diagramme de séquence pour une action sensible (ex: soumission formulaire avec confirmation utilisateur).
- [ ] Documenter les limites connues de confidentialité (navigation web + données envoyées aux sites tiers).

### Phase 11 — Catalogage des outils IA (à faire)
- [ ] Créer un registre unique `docs/tools-catalog.md` :
  - [ ] nom outil ;
  - [ ] permissions requises ;
  - [ ] entrées/sorties ;
  - [ ] niveau de risque (low/medium/high) ;
  - [ ] besoin de confirmation utilisateur.
- [ ] Ajouter des catégories minimales :
  - [ ] Web (search, open, extract, screenshot) ;
  - [ ] Formulaires (analyze, fill, submit, dry-run) ;
  - [ ] Fichiers locaux (read/write/convert) ;
  - [ ] Système (commandes “safe” en sandbox).
- [ ] Définir un contrat d’outil standard JSON pour simplifier l’ajout de nouveaux connecteurs.

### Phase 12 — Gestion des identifiants & données sensibles (à faire)
- [ ] Mettre en place 2 niveaux de coffre :
  - [ ] `secrets` (mots de passe, tokens API, cookies) ;
  - [ ] `private_data` (notes perso, préférences utilisateur).
- [ ] Forcer chiffrement + contrôle d’accès logique par scope (`user`, `session`, `tool`).
- [ ] Ajouter une commande de rotation des secrets (ex: `secret:rotate:key_name`).
- [ ] Ajouter politique “ne jamais auto-remplir un mot de passe sans consentement explicite”.
- [ ] Ajouter journal d’accès sensible : qui, quoi, quand, pourquoi (sans exposer la valeur du secret).

### Priorités exécution (ordre recommandé)
1. **Sécurité d’abord** : Phases 5 + 8 (autorisations, audit, cycle de vie des secrets).
2. **Capacités web robustes** : Phases 6 + 7 (navigation/formulaires fiables).
3. **Industrialisation** : Phase 9 (tests, métriques, modes d’exécution).
4. **Documentation durable** : Phases 10 + 11 (architecture + catalogue outils).
5. **Secrets de niveau production locale** : Phase 12 (coffre, rotation, journal d’accès).

### Critères d’acceptation (MVP v1 local)
- [ ] Démarrage en < 15 s sur machine CPU standard avec limite **≤ 1 GB RAM**.
- [ ] Exécution de 3 outils consécutifs sans crash (search → web → formulaire).
- [ ] Aucun secret affiché en clair dans les logs.
- [ ] Confirmation explicite avant toute action sensible (soumission de formulaire, lecture secret).

### Critères d’acceptation (v1.5 “autonomie contrôlée”)
- [ ] L’agent peut exécuter un mini-plan web en 5 étapes max avec rollback en cas d’échec.
- [ ] Le mode dry-run affiche exactement les champs de formulaire modifiés avant validation.
- [ ] Tous les appels d’outils sont tracés avec ID de corrélation (debug reproductible).
- [ ] Rotation d’un secret critique testée et validée sans downtime.
- [ ] Rapport final d’exécution généré en Markdown (actions, preuves, erreurs, recommandations).

### Jalons livraison recommandés
- **v0.2.0 (Documentation-first)** :
  - Roadmap consolidée ;
  - architecture décrite ;
  - catalogue d’outils normalisé.
- **v0.3.0 (Web + formulaires robustes)** :
  - navigation guidée ;
  - extraction structurée ;
  - dry-run + validation humaine.
- **v0.4.0 (Sécurité renforcée)** :
  - gouvernance des secrets ;
  - audit trail ;
  - politiques d’autorisation strictes.
- **v1.0.0 (Usage quotidien local)** :
  - profils stables ;
  - tests E2E complets ;
  - documentation d’exploitation.

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

## Backlog fonctionnel (documentation-first)

### 1) Outils IA à ajouter (liste variée)
- Connecteurs fichiers : PDF, CSV, JSON, Markdown.
- Connecteur email (lecture brouillons locaux + génération de réponse).
- Outils calendrier/tâches locaux (iCal, rappels).
- Exécution scripts “safe” avec sandbox + quotas.
- Résumeur de pages web longues et extraction d’actions concrètes.

### 2) Gouvernance et conformité locale
- Journal de consentement utilisateur pour actions critiques.
- Masquage automatique des secrets dans traces/debug.
- Politique de rétention configurable (7/30/90 jours).
- Commande “panic” pour purge immédiate des données sensibles.

### 3) Expérience développeur
- Fichier de config unique (`config.yaml`) avec profils.
- Commande `doctor` pour vérifier dépendances (Playwright, modèle, droits FS).
- Templates de prompts système par cas d’usage (assistant perso, scraping, RPA).

### 4) Roadmap technique courte (30 jours)
- **Semaine 1** : audit sécurité, politique d’autorisations, logs structurés.
- **Semaine 2** : navigation web robuste + extraction structurée.
- **Semaine 3** : formulaires avancés + mode dry-run + captures preuve.
- **Semaine 4** : tests E2E, optimisation RAM, publication v0.2.0.

### 5) Roadmap étendue (90 jours, orientée production locale)
- **Mois 1 — Foundations**
  - Stabiliser le noyau LLM ≤ 1 GB RAM (bench CPU + RAM).
  - Finaliser la spec architecture et le contrat des outils.
  - Mettre en place la politique de sécurité par défaut.
- **Mois 2 — Capacités autonomes encadrées**
  - Déployer le planner multi-étapes (plan/replan/stop).
  - Renforcer la navigation web et l’automatisation formulaire.
  - Introduire validation humaine configurable sur actions critiques.
- **Mois 3 — Fiabilité & exploitation**
  - Couvrir les parcours critiques avec E2E.
  - Ajouter monitoring local (latence, crash, RAM max).
  - Préparer release v1.0.0 avec guide opérateur.

### 6) Registre des risques (documentation initiale)
- **Risque** : dépassement RAM > 1 GB sur prompts longs.  
  **Mitigation** : limite stricte `n_ctx`, truncation intelligente, watchdog mémoire.
- **Risque** : fuite de secrets dans logs/erreurs.  
  **Mitigation** : redaction automatique, logs chiffrés, revue sécurité.
- **Risque** : soumission involontaire de formulaire sensible.  
  **Mitigation** : dry-run + confirmation explicite + allowlist domaines.
- **Risque** : outil externe non fiable / indisponible.  
  **Mitigation** : fallback provider + gestion d’erreur standardisée + retry borné.
