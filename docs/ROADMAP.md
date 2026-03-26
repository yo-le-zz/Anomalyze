# Roadmap Anomalyze

## Phase 1 (done)
- Collecte process-level (CPU/RAM/fichiers/réseau)
- Baseline moyenne + variance
- Détection z-score
- Score de risque + sévérité
- Logs et baseline persistants

## Phase 2 (next)
- Confiance applicative (ancienneté, fréquence, régularité)
- Détection d'IP/ports inhabituels (profil réseau par app)
- Détection d'accès fichiers sensibles/volumes anormaux

## Phase 3
- Modèle ML léger (Isolation Forest en complément)
- Dashboard local (CLI enrichie ou UI)
- Export JSON/CSV/SIEM des alertes

## Phase 4
- Actions automatiques optionnelles (kill/quarantaine)
- Whitelist et règles custom
- Mode service/daemon multi-plateforme
