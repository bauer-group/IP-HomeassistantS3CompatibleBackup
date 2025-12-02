# S3 Compatible Backup für Home Assistant

[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Kompatibel-blue?style=for-the-badge&logo=home-assistant)](https://www.home-assistant.io/)
[![HACS](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)
[![Lizenz](https://img.shields.io/github/license/bauer-group/IP-HomeassistantS3CompatibleBackup?style=for-the-badge)](LICENSE)
[![GitHub Sterne](https://img.shields.io/github/stars/bauer-group/IP-HomeassistantS3CompatibleBackup?style=for-the-badge)](https://github.com/bauer-group/IP-HomeassistantS3CompatibleBackup/stargazers)
[![GitHub Issues](https://img.shields.io/github/issues/bauer-group/IP-HomeassistantS3CompatibleBackup?style=for-the-badge)](https://github.com/bauer-group/IP-HomeassistantS3CompatibleBackup/issues)

**Sichere deine Home Assistant Backups auf jedem S3-kompatiblen Speicher.**

Diese Integration erweitert die eingebaute Backup-Funktion von Home Assistant um Unterstützung für **jeden S3-kompatiblen Speicher**, nicht nur AWS S3. Funktioniert mit:

- ☁️ **AWS S3**
- 🗄️ **MinIO**
- 💾 **Wasabi**
- 🔒 **Backblaze B2**
- 🌊 **DigitalOcean Spaces**
- ☁️ **Cloudflare R2**
- 🏢 **Synology C2 Object Storage**
- 🖥️ **Selbst gehosteter S3-kompatibler Speicher**
- Und jeder andere S3-kompatible Anbieter!

---

## 🚀 Schnellstart

1. **Installation** über HACS oder manuell (siehe [Installation](#-installation))
2. **Home Assistant neustarten**
3. **Einstellungen** → **Geräte & Dienste** → **Integration hinzufügen**
4. Nach **"BAUERGROUP - S3 Compatible Backup"** suchen
5. Zugangsdaten eingeben:
   - Access Key ID
   - Secret Access Key
   - Bucket-Name (muss bereits existieren!)
   - Endpoint URL
   - Region
6. **Einstellungen** → **System** → **Backups** → S3-Speicher als Backup-Ziel auswählen

---

## ✨ Funktionen

- 📦 **Vollständige Backup-Unterstützung** - Hochladen, Herunterladen, Auflisten und Löschen von Backups
- 🔄 **Multipart-Upload** - Effiziente Verarbeitung großer Backups (>20MB)
- 🌍 **Region-Unterstützung** - Konfiguriere jede Region für deinen S3-Endpunkt
- 🔗 **Benutzerdefinierte Endpunkte** - Funktioniert mit jeder S3-kompatiblen API
- 🔐 **Sicher** - Verwendet Zugangsdaten (Access Key ID + Secret Access Key)
- 🚀 **Asynchron** - Nicht-blockierende Operationen mit aiobotocore
- 💾 **Caching** - Effiziente Backup-Auflistung mit 5-Minuten-Cache
- 🔑 **Re-Authentifizierung** - Automatische Aufforderung bei abgelaufenen Zugangsdaten
- ⚙️ **Rekonfiguration** - Einstellungen ändern ohne die Integration zu entfernen

---

## 📦 Installation

### Methode 1: HACS (Empfohlen)

[![Öffne deine Home Assistant Instanz und öffne ein Repository im Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=bauer-group&repository=IP-HomeassistantS3CompatibleBackup&category=integration)

1. Öffne **HACS** in Home Assistant
2. Gehe zu **Integrationen**
3. Klicke auf das **⋮** Menü → **Benutzerdefinierte Repositories**
4. Repository hinzufügen:
   - **URL:** `https://github.com/bauer-group/IP-HomeassistantS3CompatibleBackup`
   - **Kategorie:** Integration
5. Klicke **Installieren**
6. **Home Assistant neustarten**

### Methode 2: Manuelle Installation

```bash
cd /config/custom_components
git clone https://github.com/bauer-group/IP-HomeassistantS3CompatibleBackup.git bauergroup_s3compatiblebackup
```

Dann Home Assistant neustarten.

---

## ⚙️ Konfiguration

1. **Einstellungen** → **Geräte & Dienste** → **Integration hinzufügen**
2. Suche nach **"S3 Compatible Backup"**
3. Konfiguriere:

| Feld | Beschreibung | Beispiel |
|------|--------------|----------|
| **Access Key ID** | Dein S3 Access Key | `AKIAIOSFODNN7EXAMPLE` |
| **Secret Access Key** | Dein S3 Secret Key | `wJalrXUtnFEMI/K7MDENG/...` |
| **Bucket-Name** | Ziel-Bucket (muss existieren) | `meine-ha-backups` |
| **Endpoint URL** | S3-kompatibler Endpunkt | `https://s3.eu-central-1.amazonaws.com` |
| **Region** | Speicher-Region | `eu-central-1` |
| **Speicher-Präfix** | Stammordner für Backups (optional) | `homeassistant` |

---

## 🔧 Nutzung

Nach der Konfiguration erscheint die Integration automatisch als Backup-Speicherort in Home Assistant:

1. Gehe zu **Einstellungen** → **System** → **Backups**
2. Erstelle ein neues Backup
3. Wähle deinen S3-Speicher als Backup-Ziel
4. Dein Backup wird in deinen S3-Bucket hochgeladen

### Backup-Struktur

Backups werden in einer Ordnerstruktur innerhalb deines Buckets organisiert:

```
mein-bucket/
└── homeassistant/           # Speicher-Präfix (konfigurierbar)
    └── backups/             # Fester Unterordner
        ├── Home_Assistant_2025-12-02.tar
        ├── Home_Assistant_2025-12-02.metadata.json
        ├── Home_Assistant_2025-12-01.tar
        ├── Home_Assistant_2025-12-01.metadata.json
        └── ...
```

Jedes Backup besteht aus zwei Dateien:

- `{backup-name}.tar` - Das eigentliche Backup-Archiv
- `{backup-name}.metadata.json` - Backup-Metadaten für Home Assistant

Der **Speicher-Präfix** ermöglicht:
- Backups von anderen Daten im selben Bucket zu trennen
- Mehrere Home Assistant Instanzen mit verschiedenen Präfixen zu betreiben
- Einen Bucket für verschiedene Anwendungen zu teilen

---

## 🔧 Integration verwalten

### Rekonfigurieren (Einstellungen ändern)

Wenn du deine S3-Konfiguration ändern musst (Bucket, Endpunkt, Zugangsdaten, etc.):

1. Gehe zu **Einstellungen** → **Geräte & Dienste**
2. Finde **BAUERGROUP - S3 Compatible Backup**
3. Klicke auf das **⋮** Menü → **Neu konfigurieren**
4. Aktualisiere deine Einstellungen und speichere

### Re-Authentifizierung

Wenn deine Zugangsdaten ablaufen oder ungültig werden, fordert Home Assistant automatisch zur erneuten Authentifizierung auf:

1. Du siehst eine Benachrichtigung, dass die Authentifizierung fehlgeschlagen ist
2. Klicke auf die Benachrichtigung oder gehe zu **Einstellungen** → **Geräte & Dienste**
3. Klicke auf **Neu konfigurieren** bei der Integration
4. Gib deine neue Access Key ID und Secret Access Key ein

---

## 📚 Anbieter-Einrichtungsanleitungen

### ☁️ AWS S3

#### 1. S3-Bucket erstellen

1. Gehe zur [AWS S3 Konsole](https://s3.console.aws.amazon.com/)
2. Klicke **Bucket erstellen**
3. Gib einen eindeutigen Bucket-Namen ein (z.B. `meine-homeassistant-backups`)
4. Wähle deine bevorzugte Region (z.B. `eu-central-1`)
5. Lasse **Gesamten öffentlichen Zugriff blockieren** aktiviert (empfohlen)
6. Klicke **Bucket erstellen**

#### 2. IAM-Benutzer mit Berechtigungen erstellen

1. Gehe zur [IAM Konsole](https://console.aws.amazon.com/iam/)
2. Klicke **Benutzer** → **Benutzer erstellen**
3. Gib einen Benutzernamen ein (z.B. `homeassistant-backup`)
4. Klicke **Weiter**
5. Wähle **Richtlinien direkt anfügen**
6. Klicke **Richtlinie erstellen** und verwende das JSON unten
7. Füge die erstellte Richtlinie dem Benutzer hinzu
8. Klicke **Benutzer erstellen**
9. Gehe zum Benutzer → **Sicherheitsanmeldeinformationen** → **Zugriffsschlüssel erstellen**
10. Wähle **Anwendung, die außerhalb von AWS ausgeführt wird**
11. Speichere **Access Key ID** und **Secret Access Key**

#### 3. IAM-Richtlinie (Minimal erforderliche Berechtigungen)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "HomeAssistantBackupPermissions",
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObject",
        "s3:ListBucket",
        "s3:AbortMultipartUpload",
        "s3:ListMultipartUploadParts"
      ],
      "Resource": [
        "arn:aws:s3:::DEIN-BUCKET-NAME",
        "arn:aws:s3:::DEIN-BUCKET-NAME/*"
      ]
    }
  ]
}
```

> **Hinweis:** Ersetze `DEIN-BUCKET-NAME` durch deinen tatsächlichen Bucket-Namen.

#### 4. Konfiguration in Home Assistant

| Feld | Wert |
|------|------|
| Access Key ID | `AKIA...` (von IAM) |
| Secret Access Key | `...` (von IAM) |
| Bucket-Name | `meine-homeassistant-backups` |
| Endpoint URL | `https://s3.eu-central-1.amazonaws.com` |
| Region | `eu-central-1` |

**AWS S3 Endpoint-URLs nach Region:**

| Region | Endpoint URL |
|--------|--------------|
| US East (N. Virginia) | `https://s3.us-east-1.amazonaws.com` |
| US West (Oregon) | `https://s3.us-west-2.amazonaws.com` |
| EU (Frankfurt) | `https://s3.eu-central-1.amazonaws.com` |
| EU (Irland) | `https://s3.eu-west-1.amazonaws.com` |
| Asien-Pazifik (Tokio) | `https://s3.ap-northeast-1.amazonaws.com` |
| Asien-Pazifik (Sydney) | `https://s3.ap-southeast-2.amazonaws.com` |

Vollständige Liste: [AWS S3 Endpunkte](https://docs.aws.amazon.com/general/latest/gr/s3.html)

---

### 🗄️ MinIO (Selbst gehostet)

MinIO ist ein leistungsstarker, S3-kompatibler Objektspeicher, den du selbst hosten kannst.

#### 1. MinIO installieren

**Docker:**

```bash
docker run -d \
  --name minio \
  -p 9000:9000 \
  -p 9001:9001 \
  -v /pfad/zu/daten:/data \
  -e "MINIO_ROOT_USER=minioadmin" \
  -e "MINIO_ROOT_PASSWORD=minioadmin" \
  minio/minio server /data --console-address ":9001"
```

**Docker Compose:**

```yaml
version: '3.8'
services:
  minio:
    image: minio/minio
    container_name: minio
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - ./minio-data:/data
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    command: server /data --console-address ":9001"
```

#### 2. Bucket und Access Key erstellen

1. Öffne die MinIO Konsole unter `http://dein-server:9001`
2. Melde dich mit den Root-Zugangsdaten an
3. Gehe zu **Buckets** → **Bucket erstellen**
4. Gib den Bucket-Namen ein (z.B. `homeassistant-backups`)
5. Gehe zu **Access Keys** → **Access Key erstellen**
6. Speichere Access Key und Secret Key

#### 3. Konfiguration in Home Assistant

| Feld | Wert |
|------|------|
| Access Key ID | `dein-access-key` |
| Secret Access Key | `dein-secret-key` |
| Bucket-Name | `homeassistant-backups` |
| Endpoint URL | `http://dein-minio-server:9000` |
| Region | `us-east-1` (Standard für MinIO) |

> **Tipp:** Für HTTPS konfiguriere MinIO mit TLS-Zertifikaten oder verwende einen Reverse Proxy.

---

### 💾 Wasabi

Wasabi bietet Hot Cloud Storage ohne Egress-Gebühren.

#### 1. Bucket erstellen

1. Melde dich bei der [Wasabi Konsole](https://console.wasabisys.com/) an
2. Klicke **Bucket erstellen**
3. Gib Bucket-Name ein und wähle Region
4. Klicke **Bucket erstellen**

#### 2. Access Keys erstellen

1. Gehe zu **Access Keys** → **Neuen Access Key erstellen**
2. Lade die Zugangsdaten herunter oder kopiere sie

#### 3. Konfiguration in Home Assistant

| Feld | Wert |
|------|------|
| Access Key ID | `dein-wasabi-access-key` |
| Secret Access Key | `dein-wasabi-secret-key` |
| Bucket-Name | `dein-bucket-name` |
| Endpoint URL | `https://s3.eu-central-1.wasabisys.com` |
| Region | `eu-central-1` |

**Wasabi Endpoint-URLs nach Region:**

| Region | Endpoint URL |
|--------|--------------|
| US East 1 (N. Virginia) | `https://s3.us-east-1.wasabisys.com` |
| US East 2 (N. Virginia) | `https://s3.us-east-2.wasabisys.com` |
| US Central 1 (Texas) | `https://s3.us-central-1.wasabisys.com` |
| US West 1 (Oregon) | `https://s3.us-west-1.wasabisys.com` |
| EU Central 1 (Amsterdam) | `https://s3.eu-central-1.wasabisys.com` |
| EU Central 2 (Frankfurt) | `https://s3.eu-central-2.wasabisys.com` |
| EU West 1 (London) | `https://s3.eu-west-1.wasabisys.com` |
| EU West 2 (Paris) | `https://s3.eu-west-2.wasabisys.com` |
| AP Northeast 1 (Tokio) | `https://s3.ap-northeast-1.wasabisys.com` |
| AP Northeast 2 (Osaka) | `https://s3.ap-northeast-2.wasabisys.com` |
| AP Southeast 1 (Singapur) | `https://s3.ap-southeast-1.wasabisys.com` |
| AP Southeast 2 (Sydney) | `https://s3.ap-southeast-2.wasabisys.com` |

---

### 🔒 Backblaze B2

Backblaze B2 ist eine günstige Cloud-Speicherlösung mit S3-kompatibler API.

#### 1. Bucket erstellen

1. Melde dich bei [Backblaze B2](https://secure.backblaze.com/b2_buckets.htm) an
2. Klicke **Bucket erstellen**
3. Gib einen eindeutigen Bucket-Namen ein
4. Setze **Dateien im Bucket sind:** auf **Privat**
5. Klicke **Bucket erstellen**
6. Notiere den **Endpunkt** (z.B. `s3.us-west-004.backblazeb2.com`)

#### 2. Application Key erstellen

1. Gehe zu **App Keys** → **Neuen Application Key hinzufügen**
2. Gib einen Namen ein (z.B. `homeassistant-backup`)
3. Wähle **Zugriff auf Bucket(s) erlauben:** deinen Bucket
4. Aktiviere diese Fähigkeiten:
   - `listBuckets`
   - `listFiles`
   - `readFiles`
   - `writeFiles`
   - `deleteFiles`
5. Klicke **Neuen Key erstellen**
6. **Wichtig:** Kopiere den `applicationKey` sofort (wird nur einmal angezeigt!)
7. Notiere die `keyID` (das ist deine Access Key ID)

#### 3. Konfiguration in Home Assistant

| Feld | Wert |
|------|------|
| Access Key ID | `keyID` vom Application Key |
| Secret Access Key | `applicationKey` vom Application Key |
| Bucket-Name | `dein-bucket-name` |
| Endpoint URL | `https://s3.us-west-004.backblazeb2.com` |
| Region | `us-west-004` |

> **Wichtig:** Die Region muss zum Endpunkt passen. Extrahiere sie aus der Endpunkt-URL (z.B. `s3.us-west-004.backblazeb2.com` → Region ist `us-west-004`).

---

### 🌊 DigitalOcean Spaces

DigitalOcean Spaces ist ein S3-kompatibler Objektspeicherdienst.

#### 1. Space erstellen

1. Melde dich bei [DigitalOcean](https://cloud.digitalocean.com/) an
2. Gehe zu **Spaces Object Storage** → **Space erstellen**
3. Wähle eine Rechenzentrumsregion
4. Wähle **Dateiauflistung einschränken** (empfohlen)
5. Gib einen eindeutigen Namen ein
6. Klicke **Space erstellen**

#### 2. Access Keys generieren

1. Gehe zu **API** → **Spaces Keys** → **Neuen Key generieren**
2. Gib einen Namen ein und klicke **Key generieren**
3. Kopiere **Key** und **Secret**

#### 3. Konfiguration in Home Assistant

| Feld | Wert |
|------|------|
| Access Key ID | `DO...` (dein Spaces Key) |
| Secret Access Key | `...` (dein Spaces Secret) |
| Bucket-Name | `dein-space-name` |
| Endpoint URL | `https://fra1.digitaloceanspaces.com` |
| Region | `fra1` |

**DigitalOcean Spaces Endpunkte:**

| Region | Endpoint URL |
|--------|--------------|
| New York (NYC3) | `https://nyc3.digitaloceanspaces.com` |
| San Francisco (SFO3) | `https://sfo3.digitaloceanspaces.com` |
| Amsterdam (AMS3) | `https://ams3.digitaloceanspaces.com` |
| Singapur (SGP1) | `https://sgp1.digitaloceanspaces.com` |
| Frankfurt (FRA1) | `https://fra1.digitaloceanspaces.com` |
| Sydney (SYD1) | `https://syd1.digitaloceanspaces.com` |

---

### ☁️ Cloudflare R2

Cloudflare R2 ist ein S3-kompatibler Objektspeicher ohne Egress-Gebühren.

#### 1. Bucket erstellen

1. Melde dich beim [Cloudflare Dashboard](https://dash.cloudflare.com/) an
2. Gehe zu **R2 Object Storage** → **Bucket erstellen**
3. Gib einen Bucket-Namen ein
4. Klicke **Bucket erstellen**

#### 2. API-Token generieren

1. Gehe zu **R2 Object Storage** → **R2 API-Tokens verwalten**
2. Klicke **API-Token erstellen**
3. Wähle Berechtigungen:
   - **Object Read & Write** für deinen Bucket
4. Klicke **API-Token erstellen**
5. Kopiere **Access Key ID** und **Secret Access Key**

#### 3. Account ID ermitteln

1. Finde deine **Account ID** in der Cloudflare Dashboard-URL oder auf der R2-Übersichtsseite

#### 4. Konfiguration in Home Assistant

| Feld | Wert |
|------|------|
| Access Key ID | `deine-r2-access-key-id` |
| Secret Access Key | `dein-r2-secret-access-key` |
| Bucket-Name | `dein-bucket-name` |
| Endpoint URL | `https://<ACCOUNT_ID>.r2.cloudflarestorage.com` |
| Region | `auto` |

> **Hinweis:** Ersetze `<ACCOUNT_ID>` durch deine Cloudflare Account ID.

---

### 🏢 Synology C2 Object Storage

Synology C2 bietet S3-kompatiblen Cloud-Speicher.

#### 1. Bucket erstellen

1. Melde dich bei [Synology C2 Object Storage](https://object.c2.synology.com/) an
2. Erstelle einen neuen Bucket
3. Notiere die Endpunkt-URL für deine Region

#### 2. Zugangsdaten erstellen

1. Gehe zu deinen Kontoeinstellungen
2. Erstelle neue Zugangsdaten
3. Speichere Access Key und Secret Key

#### 3. Konfiguration in Home Assistant

| Feld | Wert |
|------|------|
| Access Key ID | `dein-c2-access-key` |
| Secret Access Key | `dein-c2-secret-key` |
| Bucket-Name | `dein-bucket-name` |
| Endpoint URL | `https://eu-002.s3.synologyc2.net` |
| Region | `eu-002` |

**Synology C2 Endpunkte:**

| Region | Endpoint URL |
|--------|--------------|
| Europa | `https://eu-002.s3.synologyc2.net` |
| Nordamerika | `https://us-001.s3.synologyc2.net` |
| Taiwan | `https://tw-001.s3.synologyc2.net` |

---

## 🔐 Erforderliche S3-Berechtigungen

Für alle Anbieter benötigen deine Zugangsdaten diese Berechtigungen:

| Berechtigung | Zweck |
|--------------|-------|
| `s3:PutObject` | Backup-Dateien hochladen |
| `s3:GetObject` | Backups herunterladen/wiederherstellen |
| `s3:DeleteObject` | Alte Backups löschen |
| `s3:ListBucket` | Verfügbare Backups auflisten |
| `s3:AbortMultipartUpload` | Fehlgeschlagene Uploads abbrechen |
| `s3:ListMultipartUploadParts` | Multipart-Uploads fortsetzen |

### AWS IAM-Richtlinienvorlage

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "HomeAssistantBackupPermissions",
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObject",
        "s3:ListBucket",
        "s3:AbortMultipartUpload",
        "s3:ListMultipartUploadParts"
      ],
      "Resource": [
        "arn:aws:s3:::DEIN-BUCKET-NAME",
        "arn:aws:s3:::DEIN-BUCKET-NAME/*"
      ]
    }
  ]
}
```

> **Sicherheits-Best-Practice:** Verwende immer die minimal erforderlichen Berechtigungen. Erstelle einen dedizierten Benutzer/Key für Home Assistant Backups.

---

## 🔍 Fehlerbehebung

### Häufige Probleme

#### "Ungültige Zugangsdaten" Fehler

- Überprüfe, ob Access Key ID und Secret Access Key korrekt sind
- Stelle sicher, dass die Zugangsdaten die erforderlichen Berechtigungen haben
- Prüfe, ob die Zugangsdaten nicht abgelaufen oder widerrufen sind

#### "Verbindung nicht möglich" Fehler

- Überprüfe, ob die Endpoint-URL korrekt und erreichbar ist
- Prüfe deine Netzwerkverbindung und Firewall-Regeln
- Bei selbst gehosteten Lösungen (MinIO) stelle sicher, dass der Server läuft

#### "Ungültiger Bucket-Name" Fehler

- Bucket-Namen müssen kleingeschrieben sein
- Bucket-Namen müssen zwischen 3-63 Zeichen lang sein
- Bucket-Namen dürfen nur Buchstaben, Zahlen und Bindestriche enthalten
- Der Bucket muss bereits existieren (diese Integration erstellt keine Buckets)

#### "Ungültige Endpoint-URL" Fehler

- Stelle sicher, dass die URL mit `http://` oder `https://` beginnt
- Prüfe auf Tippfehler in der Endpoint-URL
- Überprüfe, ob die Region zum Endpunkt passt

#### Backups werden nicht angezeigt

- Warte bis zu 5 Minuten (Backup-Liste wird gecacht)
- Prüfe die Home Assistant Logs auf Fehler
- Überprüfe, ob der Bucket `.metadata.json`-Dateien enthält

### Debug-Logging aktivieren

Füge zu `configuration.yaml` hinzu:

```yaml
logger:
  default: info
  logs:
    custom_components.bauergroup_s3compatiblebackup: debug
    aiobotocore: debug
    botocore: debug
```

### Verbindung testen

Du kannst deine S3-Verbindung mit der AWS CLI testen:

```bash
# AWS CLI installieren
pip install awscli

# Zugangsdaten konfigurieren
aws configure --profile homeassistant
# Gib Access Key ID, Secret Access Key und Region ein

# Bucket-Auflistung testen
aws s3 ls s3://dein-bucket-name --profile homeassistant --endpoint-url https://deine-endpoint-url

# Datei-Upload testen
echo "test" > test.txt
aws s3 cp test.txt s3://dein-bucket-name/test.txt --profile homeassistant --endpoint-url https://deine-endpoint-url

# Datei-Download testen
aws s3 cp s3://dein-bucket-name/test.txt test-download.txt --profile homeassistant --endpoint-url https://deine-endpoint-url

# Aufräumen
aws s3 rm s3://dein-bucket-name/test.txt --profile homeassistant --endpoint-url https://deine-endpoint-url
rm test.txt test-download.txt
```

---

## 📊 Speicheranbieter-Vergleich

| Anbieter | Kostenlose Stufe | Egress-Gebühren | Min. Speichergebühr | S3-kompatibel |
|----------|------------------|-----------------|---------------------|---------------|
| AWS S3 | 5 GB (12 Monate) | Ja | Nein | Nativ |
| Backblaze B2 | 10 GB | Kostenlos bis 3x Speicher | Nein | Ja |
| Wasabi | Nein | Nein | Ja (1 TB min) | Ja |
| Cloudflare R2 | 10 GB | Nein | Nein | Ja |
| DigitalOcean Spaces | Nein | Ja | 5$/Monat | Ja |
| MinIO | Selbst gehostet | N/A | N/A | Ja |

---

## 📄 Lizenz

MIT-Lizenz - siehe [LICENSE](LICENSE) Datei für Details.

---

## 🤝 Mitwirken

Beiträge sind willkommen! Bitte eröffne ein Issue oder einen Pull Request.

---

*[English version](README.md)*
