# Release Process

Dieses Dokument beschreibt den automatisierten Release-Prozess für die BAUERGROUP S3 Compatible Backup Integration.

## Voraussetzungen

- Python 3.7 oder höher
- Git installiert und konfiguriert
- Schreibrechte auf das GitHub Repository

## Release Script

Das `release.py` Script automatisiert den gesamten Release-Prozess:

### Features

✅ **Automatische Versionsaktualisierung** in:
- `custom_components/bauergroup_s3compatiblebackup/manifest.json`
- `SCHNELLSTART.md`
- `PROJECT_SUMMARY.md` (falls vorhanden)
- `README.md` (Version Badge, falls vorhanden)

✅ **Git-Operationen**:
- Prüfung auf uncommittete Änderungen
- Automatischer Commit: `chore: Bump version to v0.x.x`
- Git Tag erstellen: `v0.x.x`
- Push zu Remote (GitHub)
- Automatisches GitHub Release erstellen

✅ **Validierung**:
- Semantic Versioning (z.B. 0.1.0)
- Check für existierende Tags
- Überprüfung des Working Directory Status

## Verwendung

### Standard Release

```bash
python release.py 0.1.1
```

Das Script wird:
1. Version auf `0.1.1` aktualisieren in allen relevanten Dateien
2. Änderungen committen
3. Tag `v0.1.1` erstellen
4. Nach Bestätigung zu GitHub pushen
5. Automatisch GitHub Release erstellen (via `gh` CLI)

### Interaktive Eingabe

```bash
python release.py
```

Das Script fragt nach der Versionsnummer.

### Nur lokal (ohne Push)

```bash
python release.py 0.1.1 --no-push
```

Erstellt Commit und Tag lokal, pusht aber nicht zu GitHub.

### Ohne GitHub Release

```bash
python release.py 0.1.1 --no-github-release
```

Pusht zu GitHub, erstellt aber kein Release (nur Tag).

## Schritt-für-Schritt Anleitung

### 1. Vorbereitung

Stelle sicher, dass alle Änderungen committed sind:

```bash
git status
```

Falls uncommittete Änderungen vorhanden sind:

```bash
git add .
git commit -m "fix: Your changes"
```

### 2. Release erstellen

```bash
python release.py 0.1.1
```

Ausgabe wird etwa so aussehen:

```
ℹ Starting release process for version v0.1.1

✓ No uncommitted changes found

▶ Updating version to 0.1.1 in all files...
✓ Updated custom_components/bauergroup_s3compatiblebackup/manifest.json
✓ Updated SCHNELLSTART.md
✓ Updated PROJECT_SUMMARY.md
✓ Updated README.md

▶ Staging updated files...
✓ Staged 4 files

▶ Committing version bump...
✓ Created commit: chore: Bump version to v0.1.1

▶ Creating git tag v0.1.1...
✓ Created tag v0.1.1

ℹ Ready to push to remote repository
This will push:
  - Latest commits to main branch
  - Tag v0.1.1

Continue? (y/n): y

▶ Pushing to remote...

✓ Pushed commits to main branch

✓ Pushed tag v0.1.1

✓ Release v0.1.1 completed successfully!

ℹ Next steps:
  1. Create a GitHub release at: https://github.com/bauer-group/IP-HomeassistantS3CompatibleBackup/releases/new?tag=v0.1.1
  2. Wait for HACS to recognize the new version
  3. Test installation via HACS

✓ Done!
```

### 3. GitHub Release wird automatisch erstellt

Das Script erstellt automatisch ein GitHub Release mit:

- **Title**: `Release v0.1.1`
- **Release Notes**: Automatisch generiert mit Installationsanleitung
- **Tag**: `v0.1.1`

**Voraussetzung**: GitHub CLI (`gh`) muss installiert sein

- Installation: <https://cli.github.com/>
- Nach Installation: `gh auth login`

Falls `gh` nicht verfügbar ist, wird ein Link zum manuellen Erstellen angezeigt.

### 4. HACS Update testen

1. Öffne HACS in Home Assistant
2. Gehe zu "Integrationen"
3. Suche nach "S3 Compatible Backup"
4. Prüfe ob neue Version angezeigt wird
5. Teste Installation/Update

## Semantic Versioning

Wir verwenden [Semantic Versioning](https://semver.org/) (MAJOR.MINOR.PATCH):

- **MAJOR** (1.0.0): Breaking Changes (nicht rückwärtskompatibel)
- **MINOR** (0.1.0): Neue Features (rückwärtskompatibel)
- **PATCH** (0.0.1): Bug Fixes (rückwärtskompatibel)

### Beispiele

```bash
# Bug Fix
python release.py 0.1.1

# Neues Feature
python release.py 0.2.0

# Breaking Change
python release.py 1.0.0
```

## Fehlerbehandlung

### Tag existiert bereits

```
[ERROR] Tag v0.1.1 already exists!
Do you want to delete and recreate it? (y/n):
```

**Optionen:**
- `y`: Löscht existierenden Tag und erstellt neu
- `n`: Bricht ab (wähle andere Version)

### Uncommittete Änderungen

```
[ERROR] You have uncommitted changes. Please commit or stash them first.
```

**Lösung:**
```bash
# Änderungen committen
git add .
git commit -m "Your changes"

# Oder stashen
git stash
```

### Ungültiges Versionsformat

```
[ERROR] Invalid version format: 0.1
[ERROR] Version must follow semantic versioning (e.g., 0.1.0)
```

**Lösung:** Verwende korrektes Format: `MAJOR.MINOR.PATCH` (z.B. `0.1.0`)

## Manueller Rollback

Falls ein Release rückgängig gemacht werden muss:

```bash
# Tag lokal löschen
git tag -d v0.1.1

# Tag von Remote löschen
git push origin --delete v0.1.1

# Letzten Commit rückgängig machen (falls nötig)
git reset --hard HEAD~1
git push origin main --force
```

**⚠️ Vorsicht:** Force Push nur verwenden wenn Release noch nicht von anderen genutzt wird!

## Troubleshooting

### Python nicht gefunden

```bash
python --version
# oder
python3 --version
```

Falls Python nicht installiert: https://www.python.org/downloads/

### Git Konfiguration

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Proxy/Firewall Probleme

```bash
# Git Proxy konfigurieren (falls nötig)
git config --global http.proxy http://proxy.example.com:8080
git config --global https.proxy https://proxy.example.com:8080
```

## Support

Bei Problemen:
1. Prüfe [GitHub Issues](https://github.com/bauer-group/IP-HomeassistantS3CompatibleBackup/issues)
2. Erstelle ein neues Issue mit Debug-Ausgabe
3. Nutze `--help` für weitere Optionen: `python release.py --help`
