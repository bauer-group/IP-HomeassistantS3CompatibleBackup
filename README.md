# S3 Compatible Backup for Home Assistant

[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Compatible-blue?style=for-the-badge&logo=home-assistant)](https://www.home-assistant.io/)
[![HACS](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)
[![License](https://img.shields.io/github/license/bauer-group/IP-HomeassistantS3CompatibleBackup?style=for-the-badge)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/bauer-group/IP-HomeassistantS3CompatibleBackup?style=for-the-badge)](https://github.com/bauer-group/IP-HomeassistantS3CompatibleBackup/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/bauer-group/IP-HomeassistantS3CompatibleBackup?style=for-the-badge)](https://github.com/bauer-group/IP-HomeassistantS3CompatibleBackup/issues)

**Backup your Home Assistant to any S3-compatible storage provider.**

This integration extends Home Assistant's built-in backup functionality to support **any S3-compatible storage**, not just AWS S3. Works with:

- ☁️ **AWS S3**
- 🗄️ **MinIO**
- 💾 **Wasabi**
- 🔒 **Backblaze B2**
- 🌊 **DigitalOcean Spaces**
- ☁️ **Cloudflare R2**
- 🏢 **Synology C2 Object Storage**
- 🖥️ **Self-hosted S3-compatible storage**
- And any other S3-compatible provider!

---

## ✨ Features

- 📦 **Full backup support** - Upload, download, list, and delete backups
- 🔄 **Multipart upload** - Efficient handling of large backups (>20MB)
- 🌍 **Region support** - Configure any region for your S3 endpoint
- 🔗 **Custom endpoints** - Works with any S3-compatible API
- 🔐 **Secure** - Uses access credentials (Access Key ID + Secret Access Key)
- 🚀 **Async** - Non-blocking operations using aiobotocore
- 💾 **Caching** - Efficient backup listing with 5-minute cache

---

## 📦 Installation

### Method 1: HACS (Recommended)

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=bauer-group&repository=IP-HomeassistantS3CompatibleBackup&category=integration)

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
git clone https://github.com/bauer-group/IP-HomeassistantS3CompatibleBackup.git bauergroup_s3compatiblebackup
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
| **Storage Prefix** | Root folder for backups (optional) | `homeassistant` |

---

## 🔧 Usage

Once configured, the integration automatically appears as a backup location in Home Assistant:

1. Go to **Settings** → **System** → **Backups**
2. Create a new backup
3. Select your S3 storage as the backup location
4. Your backup will be uploaded to your S3 bucket

### Backup Structure

Backups are organized in a folder structure within your bucket:

```
my-bucket/
└── homeassistant/           # Storage Prefix (configurable)
    └── backups/             # Fixed subfolder
        ├── Home_Assistant_2025-12-02.tar
        ├── Home_Assistant_2025-12-02.metadata.json
        ├── Home_Assistant_2025-12-01.tar
        ├── Home_Assistant_2025-12-01.metadata.json
        └── ...
```

Each backup consists of two files:

- `{backup-name}.tar` - The actual backup archive
- `{backup-name}.metadata.json` - Backup metadata for Home Assistant

The **Storage Prefix** allows you to:
- Keep backups separate from other data in the same bucket
- Run multiple Home Assistant instances with different prefixes
- Share a bucket across different applications

---

## 📚 Provider Setup Guides

### ☁️ AWS S3

#### 1. Create an S3 Bucket

1. Go to [AWS S3 Console](https://s3.console.aws.amazon.com/)
2. Click **Create bucket**
3. Enter a unique bucket name (e.g., `my-homeassistant-backups`)
4. Select your preferred region (e.g., `eu-central-1`)
5. Keep **Block all public access** enabled (recommended)
6. Click **Create bucket**

#### 2. Create an IAM User with Permissions

1. Go to [IAM Console](https://console.aws.amazon.com/iam/)
2. Click **Users** → **Create user**
3. Enter a username (e.g., `homeassistant-backup`)
4. Click **Next**
5. Select **Attach policies directly**
6. Click **Create policy** and use the JSON below
7. Attach the created policy to the user
8. Click **Create user**
9. Go to the user → **Security credentials** → **Create access key**
10. Select **Application running outside AWS**
11. Save the **Access Key ID** and **Secret Access Key**

#### 3. IAM Policy (Minimum Required Permissions)

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
        "arn:aws:s3:::YOUR-BUCKET-NAME",
        "arn:aws:s3:::YOUR-BUCKET-NAME/*"
      ]
    }
  ]
}
```

> **Note:** Replace `YOUR-BUCKET-NAME` with your actual bucket name.

#### 4. Configuration in Home Assistant

| Field | Value |
|-------|-------|
| Access Key ID | `AKIA...` (from IAM) |
| Secret Access Key | `...` (from IAM) |
| Bucket Name | `my-homeassistant-backups` |
| Endpoint URL | `https://s3.eu-central-1.amazonaws.com` |
| Region | `eu-central-1` |

**AWS S3 Endpoint URLs by Region:**

| Region | Endpoint URL |
|--------|--------------|
| US East (N. Virginia) | `https://s3.us-east-1.amazonaws.com` |
| US West (Oregon) | `https://s3.us-west-2.amazonaws.com` |
| EU (Frankfurt) | `https://s3.eu-central-1.amazonaws.com` |
| EU (Ireland) | `https://s3.eu-west-1.amazonaws.com` |
| Asia Pacific (Tokyo) | `https://s3.ap-northeast-1.amazonaws.com` |
| Asia Pacific (Sydney) | `https://s3.ap-southeast-2.amazonaws.com` |

Full list: [AWS S3 Endpoints](https://docs.aws.amazon.com/general/latest/gr/s3.html)

---

### 🗄️ MinIO (Self-hosted)

MinIO is a high-performance, S3-compatible object storage that you can self-host.

#### 1. Install MinIO

**Docker:**

```bash
docker run -d \
  --name minio \
  -p 9000:9000 \
  -p 9001:9001 \
  -v /path/to/data:/data \
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

#### 2. Create Bucket and Access Key

1. Open MinIO Console at `http://your-server:9001`
2. Login with root credentials
3. Go to **Buckets** → **Create Bucket**
4. Enter bucket name (e.g., `homeassistant-backups`)
5. Go to **Access Keys** → **Create access key**
6. Save the Access Key and Secret Key

#### 3. Configuration in Home Assistant

| Field | Value |
|-------|-------|
| Access Key ID | `your-access-key` |
| Secret Access Key | `your-secret-key` |
| Bucket Name | `homeassistant-backups` |
| Endpoint URL | `http://your-minio-server:9000` |
| Region | `us-east-1` (default for MinIO) |

> **Tip:** For HTTPS, configure MinIO with TLS certificates or use a reverse proxy.

---

### 💾 Wasabi

Wasabi offers hot cloud storage with no egress fees.

#### 1. Create a Bucket

1. Login to [Wasabi Console](https://console.wasabisys.com/)
2. Click **Create Bucket**
3. Enter bucket name and select region
4. Click **Create Bucket**

#### 2. Create Access Keys

1. Go to **Access Keys** → **Create New Access Key**
2. Download or copy the credentials

#### 3. Configuration in Home Assistant

| Field | Value |
|-------|-------|
| Access Key ID | `your-wasabi-access-key` |
| Secret Access Key | `your-wasabi-secret-key` |
| Bucket Name | `your-bucket-name` |
| Endpoint URL | `https://s3.eu-central-1.wasabisys.com` |
| Region | `eu-central-1` |

**Wasabi Endpoint URLs by Region:**

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
| AP Northeast 1 (Tokyo) | `https://s3.ap-northeast-1.wasabisys.com` |
| AP Northeast 2 (Osaka) | `https://s3.ap-northeast-2.wasabisys.com` |
| AP Southeast 1 (Singapore) | `https://s3.ap-southeast-1.wasabisys.com` |
| AP Southeast 2 (Sydney) | `https://s3.ap-southeast-2.wasabisys.com` |

---

### 🔒 Backblaze B2

Backblaze B2 is an affordable cloud storage solution with S3-compatible API.

#### 1. Create a Bucket

1. Login to [Backblaze B2](https://secure.backblaze.com/b2_buckets.htm)
2. Click **Create a Bucket**
3. Enter a unique bucket name
4. Set **Files in Bucket are:** to **Private**
5. Click **Create a Bucket**
6. Note the **Endpoint** shown (e.g., `s3.us-west-004.backblazeb2.com`)

#### 2. Create Application Key

1. Go to **App Keys** → **Add a New Application Key**
2. Enter a name (e.g., `homeassistant-backup`)
3. Select **Allow access to Bucket(s):** your bucket
4. Enable these capabilities:
   - `listBuckets`
   - `listFiles`
   - `readFiles`
   - `writeFiles`
   - `deleteFiles`
5. Click **Create New Key**
6. **Important:** Copy the `applicationKey` immediately (shown only once!)
7. Note the `keyID` (this is your Access Key ID)

#### 3. Configuration in Home Assistant

| Field | Value |
|-------|-------|
| Access Key ID | `keyID` from Application Key |
| Secret Access Key | `applicationKey` from Application Key |
| Bucket Name | `your-bucket-name` |
| Endpoint URL | `https://s3.us-west-004.backblazeb2.com` |
| Region | `us-west-004` |

> **Important:** The region must match the endpoint. Extract it from the endpoint URL (e.g., `s3.us-west-004.backblazeb2.com` → region is `us-west-004`).

---

### 🌊 DigitalOcean Spaces

DigitalOcean Spaces is an S3-compatible object storage service.

#### 1. Create a Space

1. Login to [DigitalOcean](https://cloud.digitalocean.com/)
2. Go to **Spaces Object Storage** → **Create a Space**
3. Select a datacenter region
4. Choose **Restrict File Listing** (recommended)
5. Enter a unique name
6. Click **Create a Space**

#### 2. Generate Access Keys

1. Go to **API** → **Spaces Keys** → **Generate New Key**
2. Enter a name and click **Generate Key**
3. Copy the **Key** and **Secret**

#### 3. Configuration in Home Assistant

| Field | Value |
|-------|-------|
| Access Key ID | `DO...` (your Spaces key) |
| Secret Access Key | `...` (your Spaces secret) |
| Bucket Name | `your-space-name` |
| Endpoint URL | `https://fra1.digitaloceanspaces.com` |
| Region | `fra1` |

**DigitalOcean Spaces Endpoints:**

| Region | Endpoint URL |
|--------|--------------|
| New York (NYC3) | `https://nyc3.digitaloceanspaces.com` |
| San Francisco (SFO3) | `https://sfo3.digitaloceanspaces.com` |
| Amsterdam (AMS3) | `https://ams3.digitaloceanspaces.com` |
| Singapore (SGP1) | `https://sgp1.digitaloceanspaces.com` |
| Frankfurt (FRA1) | `https://fra1.digitaloceanspaces.com` |
| Sydney (SYD1) | `https://syd1.digitaloceanspaces.com` |

---

### ☁️ Cloudflare R2

Cloudflare R2 is an S3-compatible object storage with zero egress fees.

#### 1. Create a Bucket

1. Login to [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. Go to **R2 Object Storage** → **Create bucket**
3. Enter a bucket name
4. Click **Create bucket**

#### 2. Generate API Token

1. Go to **R2 Object Storage** → **Manage R2 API Tokens**
2. Click **Create API token**
3. Select permissions:
   - **Object Read & Write** for your bucket
4. Click **Create API Token**
5. Copy the **Access Key ID** and **Secret Access Key**

#### 3. Get Your Account ID

1. Find your **Account ID** in the Cloudflare dashboard URL or R2 overview page

#### 4. Configuration in Home Assistant

| Field | Value |
|-------|-------|
| Access Key ID | `your-r2-access-key-id` |
| Secret Access Key | `your-r2-secret-access-key` |
| Bucket Name | `your-bucket-name` |
| Endpoint URL | `https://<ACCOUNT_ID>.r2.cloudflarestorage.com` |
| Region | `auto` |

> **Note:** Replace `<ACCOUNT_ID>` with your Cloudflare account ID.

---

### 🏢 Synology C2 Object Storage

Synology C2 offers S3-compatible cloud storage.

#### 1. Create a Bucket

1. Login to [Synology C2 Object Storage](https://object.c2.synology.com/)
2. Create a new bucket
3. Note the endpoint URL for your region

#### 2. Create Access Credentials

1. Go to your account settings
2. Create new access credentials
3. Save the Access Key and Secret Key

#### 3. Configuration in Home Assistant

| Field | Value |
|-------|-------|
| Access Key ID | `your-c2-access-key` |
| Secret Access Key | `your-c2-secret-key` |
| Bucket Name | `your-bucket-name` |
| Endpoint URL | `https://eu-002.s3.synologyc2.net` |
| Region | `eu-002` |

**Synology C2 Endpoints:**

| Region | Endpoint URL |
|--------|--------------|
| Europe | `https://eu-002.s3.synologyc2.net` |
| North America | `https://us-001.s3.synologyc2.net` |
| Taiwan | `https://tw-001.s3.synologyc2.net` |

---

## 🔐 Required S3 Permissions

For all providers, your access credentials need these permissions:

| Permission | Purpose |
|------------|---------|
| `s3:PutObject` | Upload backup files |
| `s3:GetObject` | Download/restore backups |
| `s3:DeleteObject` | Delete old backups |
| `s3:ListBucket` | List available backups |
| `s3:AbortMultipartUpload` | Cancel failed uploads |
| `s3:ListMultipartUploadParts` | Resume multipart uploads |

### AWS IAM Policy Template

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
        "arn:aws:s3:::YOUR-BUCKET-NAME",
        "arn:aws:s3:::YOUR-BUCKET-NAME/*"
      ]
    }
  ]
}
```

> **Security Best Practice:** Always use the minimum required permissions. Create a dedicated user/key for Home Assistant backups.

---

## 🔍 Troubleshooting

### Common Issues

#### "Invalid credentials" Error

- Verify your Access Key ID and Secret Access Key are correct
- Check that the credentials have the required permissions
- Ensure the credentials are not expired or revoked

#### "Cannot connect" Error

- Verify the Endpoint URL is correct and accessible
- Check your network connection and firewall rules
- For self-hosted solutions (MinIO), ensure the server is running

#### "Invalid bucket name" Error

- Bucket names must be lowercase
- Bucket names must be between 3-63 characters
- Bucket names can only contain letters, numbers, and hyphens
- The bucket must already exist (this integration does not create buckets)

#### "Invalid endpoint URL" Error

- Ensure the URL starts with `http://` or `https://`
- Check for typos in the endpoint URL
- Verify the region matches the endpoint

#### Backups Not Appearing

- Wait up to 5 minutes (backup list is cached)
- Check the Home Assistant logs for errors
- Verify the bucket contains `.metadata.json` files

### Enable Debug Logging

Add to `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.bauergroup_s3compatiblebackup: debug
    aiobotocore: debug
    botocore: debug
```

### Testing Your Connection

You can test your S3 connection using the AWS CLI:

```bash
# Install AWS CLI
pip install awscli

# Configure credentials
aws configure --profile homeassistant
# Enter your Access Key ID, Secret Access Key, and region

# Test listing the bucket
aws s3 ls s3://your-bucket-name --profile homeassistant --endpoint-url https://your-endpoint-url

# Test uploading a file
echo "test" > test.txt
aws s3 cp test.txt s3://your-bucket-name/test.txt --profile homeassistant --endpoint-url https://your-endpoint-url

# Test downloading a file
aws s3 cp s3://your-bucket-name/test.txt test-download.txt --profile homeassistant --endpoint-url https://your-endpoint-url

# Clean up
aws s3 rm s3://your-bucket-name/test.txt --profile homeassistant --endpoint-url https://your-endpoint-url
rm test.txt test-download.txt
```

---

## 📊 Storage Comparison

| Provider | Free Tier | Egress Fees | Min. Storage Fee | S3 Compatible |
|----------|-----------|-------------|------------------|---------------|
| AWS S3 | 5 GB (12 months) | Yes | No | Native |
| Backblaze B2 | 10 GB | Free up to 3x storage | No | Yes |
| Wasabi | No | No | Yes (1 TB min) | Yes |
| Cloudflare R2 | 10 GB | No | No | Yes |
| DigitalOcean Spaces | No | Yes | $5/month | Yes |
| MinIO | Self-hosted | N/A | N/A | Yes |

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or pull request.

## 🙏 Credits

Based on the [AWS S3 integration](https://github.com/home-assistant/core/tree/dev/homeassistant/components/aws_s3) from Home Assistant Core, extended to support any S3-compatible storage provider.
