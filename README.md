# 🫀 Anomalyze

**Anomalyze** est un outil Python de surveillance comportementale locale. Il observe en temps réel l’activité des applications, apprend leurs patterns normaux et détecte les comportements anormaux, générant des alertes et des logs pour te permettre de réagir rapidement à des menaces nouvelles ou suspectes.

## ✨ Ce que fait la version actuelle (v0.1.0)

- Surveillance par processus : CPU, RAM, fichiers ouverts, connexions réseau.
- Apprentissage continu d'une baseline par application (moyenne + variance).
- Détection d'anomalies par seuils adaptatifs (z-score).
- Détection de rafales de processus.
- Corrélation multi-signaux (CPU + RAM/fichiers/réseau) pour réduire le bruit.
- Score de risque (0-100) + sévérité (`light`, `suspicious`, `critical`).
- Alertes lisibles et historisées dans `.anomalyze/alerts.log`.
- Baseline persistée dans `.anomalyze/baseline.json`.

## 📦 Installation

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
```

## 🚀 Usage

```bash
anomalyze --loops 10 --interval 1.5
```

Options utiles :

- `--loops` : nombre de cycles d'observation (par défaut `3`).
- `--interval` : intervalle de collecte en secondes.
- `--baseline-min-samples` : nombre min. d'échantillons avant détection.
- `--z-threshold` : sensibilité des anomalies (plus bas = plus sensible).

## 🧠 Architecture rapide

- `collectors.py` : collecte système (psutil).
- `baseline.py` : baseline incrémentale (Welford).
- `detector.py` : logique anomalies + scoring.
- `engine.py` : boucle principale et orchestration.
- `cli.py` : interface en ligne de commande.

## ✅ Checklist projet

### 🟢 Base

- [x] Surveiller les processus (CPU / RAM)
- [x] Détecter les nouveaux processus
- [x] Stocker une baseline simple par application
- [x] Mettre en place un système de logs

### 🟡 Comportement

- [x] Ajouter moyenne + variance
- [x] Implémenter des seuils adaptatifs (tolérance)
- [x] Détecter les spikes (changements brusques)
- [x] Garder un historique exploitable

### 🟠 Analyse avancée

- [ ] Suivre l'ancienneté des programmes
- [ ] Créer un système de confiance
- [x] Détecter les répétitions suspectes
- [x] Corréler plusieurs événements

### 🔵 Réseau & fichiers

- [x] Surveiller les connexions réseau
- [ ] Détecter IP/ports inhabituels
- [ ] Surveiller les accès aux fichiers sensibles
- [ ] Détecter l'accès massif ou rapide

### 🔴 Scoring & alertes

- [x] Mettre en place le score global
- [x] Définir les niveaux d'alerte
- [x] Générer des alertes claires
- [x] Historiser les anomalies

### ⚫ Plus tard

- [ ] Machine learning simple (Isolation Forest)
- [ ] Graphiques d'activité
- [ ] Interface
- [ ] Kill automatique + règles de sécurité
- [ ] Whitelist (programmes autorisés)
- [ ] Export des logs

## ⚠️ Limites actuelles

- Projet orienté POC local (pas encore agent système/service).
- Certaines métriques peuvent nécessiter des droits admin selon l'OS.
- La baseline nécessite une période d'apprentissage.

## 📄 Licence

MIT