# Changelog

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/),
und dieses Projekt folgt [Semantic Versioning](https://semver.org/lang/de/).

## [0.2.1] - 2026-06-18

### 🐛 Fixed

- **formatjs-Fehler beim Setup behoben (`MISSING_VALUE` für `prefix`)**
  - Die `data_description` des Felds `prefix` enthielt ein wörtlich gemeintes `{prefix}`, das vom Home-Assistant-Frontend (formatjs/ICU MessageFormat) als Platzhalter-Variable interpretiert wurde
  - Da kein `prefix`-Platzhalter über `description_placeholders` bereitgestellt wird, warf das Rendering `MISSING_VALUE`
  - Der Fehler führte zusätzlich dazu, dass das benachbarte Label `storage_class` auf seinen Roh-Key zurückfiel, statt übersetzt zu werden
  - `{prefix}` wird nun via ICU-Escape (`'{prefix}'`) als Literal gerendert — angezeigter Text bleibt unverändert
  - Betrifft `strings.json`, `translations/en.json` und `translations/de.json`

---

## [0.2.0] - 2026-06-16

### ✨ Added

- **Konfigurierbare S3 Storage-Klasse** ([#4](https://github.com/bauer-group/IP-HomeassistantS3CompatibleBackup/pull/4))
  - Neue optionale Einstellung "Storage-Klasse" im Setup- und im Reconfigure-Flow
  - Wird als `StorageClass` an `put_object` und `create_multipart_upload` übergeben
  - Ermöglicht die Wahl der Speicherstufe (z.B. `STANDARD`, `STANDARD_IA`, `GLACIER`)
  - Freitext statt fester Auswahlliste, da S3-kompatible Anbieter (MinIO, Wasabi, Backblaze B2) abweichende Klassennamen verwenden
  - Bleibt das Feld leer, wird keine Storage-Klasse gesendet und der Anbieter-Standard greift
  - Beitrag von [@wardpieters](https://github.com/wardpieters)

### 🐛 Fixed

- **Fehlende Übersetzungen für Reauth- und Reconfigure-Flow ergänzt** ([#5](https://github.com/bauer-group/IP-HomeassistantS3CompatibleBackup/issues/5))
  - `en.json` und `de.json` enthielten bisher nur den `user`-Schritt
  - Die Schritte `reauth_confirm` und `reconfigure` fielen auf die `strings.json`-Quelle zurück, statt lokalisierte Labels anzuzeigen
  - Beide Schritte sowie die Meldung `abort.reauth_successful` sind nun vollständig in Deutsch und Englisch übersetzt

---

## [0.1.7] - 2026-03-03

### 🐛 Fixed

- **Hassfest URL-Validierung behoben**
  - URLs in Übersetzungs-Strings durch `description_placeholders` ersetzt
  - Hassfest verbietet direkte URLs in Übersetzungs-Strings

---

## [0.1.6] - 2026-03-03

### 🐛 Fixed

- **"Future attached to a different loop" Fehler behoben** ([#3](https://github.com/bauer-group/IP-HomeassistantS3CompatibleBackup/issues/3))
  - `async_list_backups()` schlug fehl, weil der aiohttp-Response-Body-Stream an den Worker-Thread-Event-Loop gebunden war, aber im Home Assistant Event-Loop gelesen wurde
  - Neue Methode `get_object_body()` liest den gesamten Body im Worker-Thread (für kleine Objekte wie Metadaten-JSON)
  - Neue Methode `get_object_stream()` streamt Body-Chunks über eine thread-sichere Queue zwischen Worker- und Main-Event-Loop (für große Backup-Dateien)
  - Behebt auch einen latenten Fehler in `async_download_backup()`, der beim Wiederherstellen von Backups aufgetreten wäre

---

## [0.1.5] - 2026-01-13

### 🐛 Fixed

- **Blocking Call Warnungen vollständig behoben**
  - Neuer `S3ClientWrapper` führt alle S3-Operationen in dediziertem Worker-Thread aus
  - Behebt alle `Detected blocking call` Warnungen (`listdir`, `open`, `load_verify_locations`)
  - Vorherige Lösung (0.1.4) war unzureichend, da jede AioSession eigenen Loader-Cache hat
  - Worker-Thread mit eigenem Event-Loop vermeidet Blockierung des Home Assistant Event-Loops

---

## [0.1.4] - 2026-01-12

### 🐛 Fixed

- **Blocking Call Warnungen behoben** (teilweise - siehe 0.1.5)
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
