# Changelog

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/),
und dieses Projekt folgt [Semantic Versioning](https://semver.org/lang/de/).

## [0.2.3] - 2026-08-23

### 🐛 Fixed

- **Setup schlug unter Home Assistant Core 2026.8 mit `Requirements ... not found` fehl** ([#6](https://github.com/bauer-group/IP-HomeassistantS3CompatibleBackup/issues/6), [#7](https://github.com/bauer-group/IP-HomeassistantS3CompatibleBackup/pull/7))
  - Fehlerbild beim Start: `Setup failed for custom integration 'bauergroup_s3compatiblebackup': Requirements for bauergroup_s3compatiblebackup not found: ['aiobotocore>=2.6.0,<3.0.0']`
  - Ursache war die Versionsobergrenze `<3.0.0` in `manifest.json`, nicht die Integration selbst
  - `aiobotocore` hat sein Versionsschema an die Release-Kadenz von `botocore` angeglichen: Auf `2.26.0` (November 2025) folgte direkt `3.0.0` (Dezember 2025); seitdem erscheinen keine `2.x`-Releases mehr, die zu aktuellen `botocore`-Versionen passen
  - Home Assistant Core hat diesen Sprung in 2026.8.0 nachvollzogen und die selbst mitgelieferte Abhängigkeit von `aiobotocore==2.21.1` (noch in 2026.7.x) auf `aiobotocore==3.7.0` angehoben — zusätzlich wird seither `botocore==1.42.97` in `package_constraints.txt` fest gepinnt, damit eine Requirement-Installation keine unpassende `botocore`-Version nachziehen kann
  - Die von Home Assistant bereitgestellte `3.7.0` erfüllte unsere Obergrenze `<3.0.0` nicht mehr, und der daraufhin ausgelöste Nachinstallations-Versuch scheiterte am `botocore`-Pin — der Resolver meldete die Anforderung als unerfüllbar (die lange Fehlerausgabe im Log stammt von `uv`)
  - Obergrenze auf `<4.0.0` angehoben: Damit erfüllt die von Home Assistant bereitgestellte Version die Anforderung direkt und es wird gar kein Installationsversuch mehr ausgelöst
  - Betroffen waren alle Installationen ab Home Assistant Core 2026.8.0; unter 2026.7.x und älter trat der Fehler nicht auf
  - Gemeldet von [@Sergey842248](https://github.com/Sergey842248); Analyse und Beitrag von [@actuallychris](https://github.com/actuallychris)

### 🔧 Technical

- Abhängigkeit: `aiobotocore>=2.6.0,<4.0.0` (zuvor `>=2.6.0,<3.0.0`)
- Die Untergrenze `>=2.6.0` bleibt bestehen, sodass ältere Home-Assistant-Versionen mit `aiobotocore` 2.x weiterhin unterstützt werden
- Reine Anpassung der Versionsobergrenze — am Integrationscode war keine Änderung nötig, da die genutzte API über die Grenze 2.x → 3.x unverändert ist (`AioSession`, `session.create_client`, `__aenter__`/`__aexit__`, `StreamingBody.read()` / `iter_chunks()`)
- Die Breaking Changes der 3.x-Reihe betreffen diese Integration nicht:
  - `3.0.0` untersagt das Anlegen loser `ClientSession`-Objekte, nachdem ein `AioBaseClient` seinen Kontext verlassen hat — der Client wird hier explizit über `__aenter__()` betreten, über `__aexit__()` geschlossen und danach nicht weiterverwendet
  - `3.8.0` ändert `AioStreamingBody.__aenter__` (liefert `self` statt der rohen `aiohttp`-`ClientResponse`) — der Response-Body wird hier ausschließlich über `read()` und `iter_chunks()` gelesen, nie als Kontextmanager verwendet

---

## [0.2.2] - 2026-06-18

### 🐛 Fixed

- **formatjs-Fehler beim Setup behoben (`MISSING_VALUE` für `prefix`)**
  - Die `data_description` des Felds `prefix` enthielt ein wörtlich gemeintes `{prefix}`, das vom Home-Assistant-Frontend (formatjs/ICU MessageFormat) als Platzhalter-Variable interpretiert wurde
  - Da kein `prefix`-Platzhalter über `description_placeholders` bereitgestellt wird, warf das Rendering `MISSING_VALUE`
  - Der Fehler führte zusätzlich dazu, dass das benachbarte Label `storage_class` auf seinen Roh-Key zurückfiel, statt übersetzt zu werden
  - Die Beschreibung wurde ohne geschweifte Klammern umformuliert, sodass kein Platzhalter mehr interpretiert wird
  - Betrifft `strings.json`, `translations/en.json` und `translations/de.json`
  - **Hinweis:** Ersetzt den fehlerhaften Fix aus 0.2.1, der den ICU-Escape `'{prefix}'` verwendete und an der Hassfest-Validierung scheiterte (Platzhalter in einfachen Anführungszeichen sind nicht erlaubt)

---

## [0.2.1] - 2026-06-18

### 🐛 Fixed

- **Fehlerhafter Fix für den `prefix`-formatjs-Fehler (zurückgezogen)**
  - Verwendete den ICU-Escape `'{prefix}'`, der zur Laufzeit zwar korrekt rendert, aber von Hassfest abgelehnt wird (`placeholders inside single quotes`)
  - Vollständig behoben in 0.2.2

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
