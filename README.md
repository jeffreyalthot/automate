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

### Backlog détaillé (prochaines itérations)

#### Sprint A — Base documentaire exécutable (1 semaine)
- [ ] Créer `docs/architecture.md` (vue composants + flux de données).
- [ ] Créer `docs/security.md` (menaces, hypothèses, limites).
- [ ] Créer `docs/runbooks/incident-response.md` (procédure en cas d’échec/compromission).
- [ ] Créer `docs/tools-catalog.md` avec format commun de description d’outil.
- [ ] Ajouter un glossaire `docs/glossary.md` (secret, consentement, dry-run, scope).

**Definition of Done (Sprint A)**
- [ ] Chaque document possède : objectif, périmètre, exemples.
- [ ] Les risques “haut niveau” ont au moins une contre-mesure documentée.
- [ ] Les commandes CLI mentionnées dans la doc sont testées localement.

#### Sprint B — Navigation web contrôlée (1 à 2 semaines)
- [ ] Introduire une machine d’états simple : `PLAN -> ACT -> VERIFY -> STOP`.
- [ ] Implémenter une politique de navigation :
  - [ ] allowlist/denylist de domaines ;
  - [ ] limites de redirections ;
  - [ ] blocage des téléchargements automatiques.
- [ ] Ajouter un mode “preuve” :
  - [ ] capture écran horodatée ;
  - [ ] URL finale ;
  - [ ] extrait texte nettoyé.
- [ ] Ajouter une commande `web:plan:<objectif>` avec budget d’étapes.

**Definition of Done (Sprint B)**
- [ ] Un scénario “rechercher puis ouvrir une page” fonctionne en ≤ 5 étapes.
- [ ] Les domaines non autorisés sont refusés avec un message explicite.
- [ ] Chaque action navigateur produit un log corrélé.

#### Sprint C — Formulaires sûrs + consentement (1 à 2 semaines)
- [ ] Construire `form:analyze` pour lister automatiquement les champs détectés.
- [ ] Construire `form:dryrun` pour prévisualiser les valeurs avant soumission.
- [ ] Construire `form:submit` avec double confirmation utilisateur pour champs sensibles.
- [ ] Gérer des stratégies anti-erreur :
  - [ ] validation format email/téléphone ;
  - [ ] détection de champs mot de passe ;
  - [ ] annulation transactionnelle si un champ critique est ambigu.

**Definition of Done (Sprint C)**
- [ ] Aucun mot de passe n’est soumis sans confirmation explicite.
- [ ] Le rapport dry-run reflète exactement les champs modifiés.
- [ ] Un test E2E couvre “analyze -> dryrun -> submit”.

#### Sprint D — Coffre local et gouvernance des secrets (1 semaine)
- [ ] Scinder le stockage en deux espaces : `secrets/` et `private_data/`.
- [ ] Ajouter métadonnées minimales : `owner`, `created_at`, `last_access_at`, `ttl`.
- [ ] Implémenter purge planifiée des secrets expirés.
- [ ] Ajouter une commande de rotation de clé de chiffrement.
- [ ] Créer un journal d’accès masqué (jamais de valeur en clair).

**Definition of Done (Sprint D)**
- [ ] Rotation de clé testée sans perte de données.
- [ ] Les entrées expirées sont supprimées automatiquement.
- [ ] Les logs ne contiennent jamais la valeur d’un secret.

#### Sprint E — Stabilisation produit (1 semaine)
- [ ] Ajouter profils runtime (`dev`, `safe`, `autonomous`) dans un fichier de config.
- [ ] Instrumenter des métriques de base (latence outil, erreurs, mémoire max).
- [ ] Ajouter un rapport Markdown final de session (actions, erreurs, preuves).
- [ ] Mettre en place une CI minimale (lint + tests unitaires + E2E critiques).

**Definition of Done (Sprint E)**
- [ ] Un run complet génère automatiquement un rapport exploitable.
- [ ] Les tests critiques passent en CI.
- [ ] Le profil `safe` bloque toute action sensible non confirmée.

### Plan de documentation (ordre de rédaction recommandé)
1. `docs/architecture.md` — contrat entre modules (LLM, orchestrateur, outils, coffre).
2. `docs/tools-catalog.md` — spécification d’interface des outils et permissions.
3. `docs/security.md` — menaces, politiques d’accès, consentement utilisateur.
4. `docs/runbooks/*.md` — opérations courantes et réponses aux incidents.
5. `docs/adr/` — décisions d’architecture (format ADR court).

### Risques clés à traiter dès maintenant
- **Dérive autonomie** : un agent qui enchaîne trop d’actions web sans validation.
  - Mitigation : budget d’étapes + points de contrôle utilisateur.
- **Fuite de secrets** : logs ou prompts contenant des données sensibles.
  - Mitigation : masquage systématique + classification des données.
- **Dépassement mémoire** (> 1 GB) : contexte trop long ou modèle trop lourd.
  - Mitigation : limites strictes `n_ctx`, monitoring RAM, fallback vers réponse courte.
- **Soumissions involontaires** : formulaires envoyés sur mauvais site/champ.
  - Mitigation : dry-run obligatoire + confirmation explicite + allowlist domaines.

### Indicateurs de succès (KPIs) pour valider la roadmap
- [ ] **Fiabilité outil** : ≥ 95% d’actions outil réussies sur un jeu de scénarios.
- [ ] **Contrainte RAM** : pic mémoire ≤ 1 GB sur profil `safe`.
- [ ] **Sécurité** : 0 secret en clair dans logs/tests d’intégration.
- [ ] **Explicabilité** : 100% des actions sensibles justifiées dans le rapport final.
- [ ] **Ergonomie** : temps moyen de configuration initiale < 20 minutes.

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

### Arborescence actuelle (MVP)

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

### Arborescence cible (niveau production locale)

```txt
.
├─ README.md
├─ requirements.txt
├─ pyproject.toml
├─ .env.example
├─ config/
│  ├─ config.dev.yaml
│  ├─ config.safe.yaml
│  └─ config.autonomous.yaml
├─ models/
│  ├─ README.md
│  └─ manifests/
│     ├─ qwen2.5-0.5b-q4km.yaml
│     └─ tinyllama-1.1b-q2k.yaml
├─ data/
│  ├─ secrets/
│  ├─ private_data/
│  ├─ sessions/
│  ├─ logs/
│  └─ artifacts/
├─ docs/
│  ├─ architecture.md
│  ├─ security.md
│  ├─ tools-catalog.md
│  ├─ operations.md
│  ├─ runbooks/
│  │  ├─ incident-response.md
│  │  ├─ secret-rotation.md
│  │  └─ browser-failure.md
│  └─ adr/
│     ├─ 0001-tool-contract.md
│     └─ 0002-secret-scope-policy.md
├─ scripts/
│  ├─ download_model.py
│  ├─ benchmark_ram.py
│  ├─ doctor.py
│  └─ migrate_store.py
├─ src/
│  ├─ app/
│  │  ├─ cli.py
│  │  ├─ api.py
│  │  └─ lifecycle.py
│  ├─ core/
│  │  ├─ agent_loop.py
│  │  ├─ planner.py
│  │  ├─ policy_engine.py
│  │  └─ report_builder.py
│  ├─ llm/
│  │  ├─ loader.py
│  │  ├─ runtime.py
│  │  └─ prompts/
│  ├─ memory/
│  │  ├─ vault.py
│  │  ├─ private_store.py
│  │  ├─ retention.py
│  │  └─ redaction.py
│  ├─ tools/
│  │  ├─ registry.py
│  │  ├─ contracts.py
│  │  ├─ web/
│  │  │  ├─ navigator.py
│  │  │  ├─ extractor.py
│  │  │  └─ search.py
│  │  ├─ forms/
│  │  │  ├─ analyzer.py
│  │  │  ├─ dry_run.py
│  │  │  └─ submit.py
│  │  ├─ files/
│  │  └─ system/
│  ├─ observability/
│  │  ├─ logging.py
│  │  ├─ metrics.py
│  │  └─ tracing.py
│  └─ security/
│     ├─ consent.py
│     ├─ secrets_policy.py
│     └─ domain_policy.py
├─ tests/
│  ├─ unit/
│  ├─ integration/
│  ├─ e2e/
│  └─ fixtures/
└─ .github/
   └─ workflows/
      ├─ ci.yml
      └─ security-scan.yml
```

> Cette arborescence permet d’évoluer vers un vrai mode production local: séparation claire des responsabilités, runbooks opérationnels, gouvernance des secrets et tests E2E.

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


## Extension roadmap — niveau production continue (documentation-first)

### Trimestre 1 (T1) — socle exploitable
- [ ] Formaliser les contrats API internes (`src/tools/contracts.py`, `src/core/policy_engine.py`).
- [ ] Ajouter une politique de permissions explicites par outil (`allow`, `confirm`, `deny`).
- [ ] Définir des profils de ressources (`eco`, `balanced`, `safe`) avec garde-fous RAM ≤ 1 GB.
- [ ] Documenter l’onboarding développeur (setup, conventions, cycle de release).

### Trimestre 2 (T2) — autonomie contrôlée web + formulaires
- [ ] Ajouter un planificateur “objectif → étapes” avec arrêt automatique sur risque élevé.
- [ ] Créer un module de détection de champs sensibles (mot de passe, IBAN, CB, OTP).
- [ ] Mettre en place une preuve d’action systématique (screenshot, URL, hash du rapport).
- [ ] Introduire un mode “approval gate” bloquant toute soumission sans consentement actif.

### Trimestre 3 (T3) — fiabilité production locale
- [ ] Ajouter tests de charge locale CPU/RAM (scénarios 15 min, 30 min, 60 min).
- [ ] Implémenter reprise après crash (journal transactionnel + relecture des tâches).
- [ ] Ajouter rotation automatique des secrets et audit mensuel local.
- [ ] Générer un rapport conformité local (sécurité, confidentialité, disponibilité).

### Trimestre 4 (T4) — packaging et exploitation quotidienne
- [ ] Packaging exécutable (CLI installable + service local démarrable).
- [ ] Versionnement sémantique + notes de release + migration de schéma.
- [ ] Mode “maintenance” pour sauvegarde/restauration du coffre chiffré.
- [ ] Guide opérateur final (checklists quotidiennes + procédures d’urgence).

### Definition of Ready (DoR) pour chaque fonctionnalité
- [ ] Risque sécurité évalué (`low/medium/high`).
- [ ] Budget mémoire estimé et validé (< 1 GB).
- [ ] Stratégie de rollback documentée.
- [ ] Cas de test unitaires + intégration définis.

### Definition of Done (DoD) production
- [ ] Documentation utilisateur et opérateur mise à jour.
- [ ] Logs sans secret en clair (contrôle automatique).
- [ ] Tests critiques validés en CI.
- [ ] Preuve de fonctionnement reproductible (commande + artefacts).


## Commandes CLI disponibles

- `help` : affiche l'aide des commandes.
- `web:<url>` : récupère le texte d'une page web.
- `search:<requête>` : effectue une recherche web simple.
- `secret:set:<clé>:<valeur>` : enregistre un secret chiffré localement.
- `secret:get:<clé>` : lit un secret par sa clé.
- `secret:list` : liste les clés existantes.
- `file:read:<chemin>` : lit un fichier local.
- `file:write:<chemin>:<contenu>` : écrit un fichier local.

Le parsing des commandes est maintenant isolé dans `src/commands/parser.py`, ce qui facilite l'ajout de nouvelles commandes.
