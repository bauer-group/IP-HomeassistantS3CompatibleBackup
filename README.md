# S3 Compatible Backup for Home Assistant

[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Compatible-blue?style=for-the-badge&logo=home-assistant)](https://www.home-assistant.io/)
[![HACS](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)
[![License](https://img.shields.io/github/license/bauergroup/bauergroup_s3compatiblebackup?style=for-the-badge)](LICENSE)

**Backup your Home Assistant to any S3-compatible storage provider.**

This integration extends Home Assistant's built-in backup functionality to support **any S3-compatible storage**, not just AWS S3. Works with:

- ☁️ **AWS S3**
- 🗄️ **MinIO**
- 💾 **Wasabi**
- 🔒 **Backblaze B2**
- 🏢 **Self-hosted S3-compatible storage**
- And any other S3-compatible provider!

---

## ✨ Features

- 📦 **Full backup support** - Upload, download, list, and delete backups
- 🔄 **Multipart upload** - Efficient handling of large backups (>20MB)
- 🌍 **Region support** - Configure any region for your S3 endpoint
- 🔗 **Custom endpoints** - Works with any S3-compatible API
- 🔐 **Secure** - Uses AWS credentials (Access Key ID + Secret Access Key)
- 🚀 **Async** - Non-blocking operations using aiobotocore
- 💾 **Caching** - Efficient backup listing with 5-minute cache

---

## 📦 Installation

### Method 1: HACS (Recommended)

1. Open **HACS** in Home Assistant
2. Go to **Integrations**
3. Click the **⋮** menu → **Custom repositories**
4. Add repository:
   - **URL:** `https://github.com/bauer-group/IP-HomeassistantS3CompatibleBackup`
   - **Category:** Integration
5. Click **Install**
6. **Restart Home Assistant**

### Method 2: Manual Installation

```bash
cd /config/custom_components
git clone https://github.com/bauer-group/IP-HomeassistantS3CompatibleBackup.git
```

Then restart Home Assistant.

---

## ⚙️ Configuration

1. **Settings** → **Devices & Services** → **Add Integration**
2. Search for **"S3 Compatible Backup"**
3. Configure:

| Field | Description | Example |
|-------|-------------|---------|
| **Access Key ID** | Your S3 access key | `AKIAIOSFODNN7EXAMPLE` |
| **Secret Access Key** | Your S3 secret key | `wJalrXUtnFEMI/K7MDENG/...` |
| **Bucket Name** | Target bucket (must exist) | `my-ha-backups` |
| **Endpoint URL** | S3-compatible endpoint | `https://s3.eu-central-1.amazonaws.com` |
| **Region** | Storage region | `eu-central-1` |

### Example Configurations

#### AWS S3
```
Endpoint URL: https://s3.eu-central-1.amazonaws.com
Region: eu-central-1
```

#### MinIO (Self-hosted)
```
Endpoint URL: https://minio.example.com:9000
Region: us-east-1
```

#### Wasabi
```
Endpoint URL: https://s3.eu-central-1.wasabisys.com
Region: eu-central-1
```

#### Backblaze B2
```
Endpoint URL: https://s3.eu-central-003.backblazeb2.com
Region: eu-central-003
```

---

## 🔧 Usage

Once configured, the integration automatically appears as a backup location in Home Assistant:

1. Go to **Settings** → **System** → **Backups**
2. Create a new backup
3. Select your S3 storage as the backup location
4. Your backup will be uploaded to your S3 bucket

### Backup Structure

Backups are stored with two files per backup:
- `{backup-name}.tar` - The actual backup archive
- `{backup-name}.metadata.json` - Backup metadata

---

## 🔍 Troubleshooting

### Connection Issues
- Verify your endpoint URL is correct and accessible
- Check that your bucket exists and is writable
- Ensure your credentials have the required S3 permissions

### Required S3 Permissions
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:ListBucket",
        "s3:GetBucketLocation"
      ],
      "Resource": [
        "arn:aws:s3:::your-bucket-name",
        "arn:aws:s3:::your-bucket-name/*"
      ]
    }
  ]
}
```

### Enable Debug Logging

Add to `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.bauergroup_s3compatiblebackup: debug
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or pull request.

## 🙏 Credits

Based on the [AWS S3 integration](https://github.com/home-assistant/core/tree/dev/homeassistant/components/aws_s3) from Home Assistant Core, extended to support any S3-compatible storage provider.
