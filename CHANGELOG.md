# Changelog

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/),
und dieses Projekt folgt [Semantic Versioning](https://semver.org/lang/de/).

## [0.1.4] - 2026-01-12

### 🐛 Fixed

- **Blocking Call Warnungen behoben**
  - S3-Client-Erstellung und Validierung erfolgt nun in einem Executor-Thread
  - Behebt `Detected blocking call to listdir` und ähnliche Warnungen in Home Assistant
  - Betrifft botocore's synchrone I/O-Operationen (listdir, Datei-Lese, SSL-Zertifikat-Laden)
  - Verbesserte Kompatibilität mit Home Assistant's asyncio-Architektur

---

## [0.1.3] - 2025-12-15

### 🐛 Fixed

- **Multipart-Upload für Cloudflare R2 und Garage**
  - Alle nicht-finalen Teile haben nun exakt die gleiche Größe (20 MiB)
  - Behebt `InvalidPart: All non-trailing parts must have the same length` Fehler
  - Verbesserte Kompatibilität mit strengeren S3-kompatiblen Providern

---

## [0.1.2] - 2025-12-08

### 🐛 Fixed

- **Kompatibilität mit Home Assistant 2024.12+**
  - Flexiblere aiobotocore-Versionsanforderung (`>=2.6.0,<3.0.0`) statt fester Version
  - Behebt `ImportError: cannot import name 'register_feature_id'` nach Home Assistant Updates
  - Integration nutzt nun die von Home Assistant bereitgestellte aiobotocore-Version

---

## [0.1.1] - 2025-12-02

### ✨ Added

- **Re-Authentifizierung Flow** (`async_step_reauth`)
  - Automatische Aufforderung zur erneuten Authentifizierung bei ungültigen Credentials
  - UI-Dialog zur Eingabe neuer Access Key ID und Secret Access Key

- **Rekonfiguration Flow** (`async_step_reconfigure`)
  - Vollständige Rekonfiguration bestehender Einträge über die UI
  - Änderung aller Parameter (Bucket, Endpoint, Region, Prefix, Credentials)

### 🔧 Changed

- **Quality Scale**: Bronze → Silver
  - Erfüllt jetzt alle Silver-Anforderungen des Home Assistant Integration Quality Scale
  - Automatischer Reauth-Trigger bei Authentifizierungsfehlern (`ConfigEntryAuthFailed`)

---

## [0.1.0] - 2025-12-02

### Erste Veröffentlichung

Erste Version der S3 Compatible Backup Integration für Home Assistant.

- **S3-kompatibler Backup-Agent** für Home Assistant's eingebautes Backup-System
  - Funktioniert mit jedem S3-kompatiblen Speicher (AWS S3, MinIO, Wasabi, Backblaze B2, etc.)
  - Upload, Download, Auflisten und Löschen von Backups
  - Multipart-Upload für große Backups (>20MB)
  - Backup-Caching mit 5-Minuten TTL

- **Config Flow** für GUI-basierte Konfiguration
  - Access Key ID und Secret Access Key
  - Bucket-Name (muss bereits existieren)
  - Endpoint URL (beliebiger S3-kompatibler Endpunkt)
  - **Region-Parameter** (neu gegenüber AWS S3 Integration)
  - Verbindungsvalidierung beim Setup

- **Übersetzungen**
  - Englisch (EN)
  - Deutsch (DE)

- **Technische Features**
  - Async/await Architektur mit aiobotocore
  - Robuste Fehlerbehandlung mit spezifischen Fehlermeldungen
  - Duplikat-Erkennung für Bucket/Endpoint-Kombinationen

### 🔧 Technical

- Abhängigkeit: `aiobotocore>=2.6.0,<3.0.0`

---

## Links

- [README.md](README.md) - Projekt-Übersicht
