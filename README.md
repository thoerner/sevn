# Envault

A secure environment variable manager that stores secrets in encrypted files and loads them only when needed.

## Features

- 🔒 Secure storage of environment variables using GPG encryption
- 🔑 Profile-based secret management
- 🐚 Load secrets into current shell or spawn a new secure shell session
- 🧹 No modification of shell startup files (`.bashrc`, etc.)
- 📝 Simple CLI interface for managing secrets

## Installation

### Option 1: Install from PyPI (Recommended)
```bash
# Install system-wide (requires sudo)
sudo pip install envault

# Or install for current user only
pip install --user envault
```

### Option 2: Install from source
```bash
# Clone the repository
git clone https://github.com/thoerner/envault.git
cd envault

# Install system-wide (requires sudo)
sudo pip install .

# Or install for current user only
pip install --user .
```

### Shell Integration (Optional)
For better shell integration, add this to your `.bashrc` or `.zshrc`:

```bash
# Function to load environment variables from a profile
load_env() {
    eval "$(envault load ${1:-default})"
}
```

Then you can simply use:
```bash
load_env myproject
```

## Usage

### Managing Profiles

1. Set a secret in a profile:
   ```bash
   envault set STRIPE_KEY=sk_test_123 --profile myproject
   envault set JWT_SECRET=secret123 --profile myproject
   ```

2. List available profiles:
   ```bash
   envault list
   ```

3. Delete a secret from a profile:
   ```bash
   envault delete myproject --key STRIPE_KEY
   ```

4. Delete an entire profile:
   ```bash
   envault delete myproject
   ```

### Loading Secrets

1. Print export commands (for use with eval):
   ```bash
   eval "$(envault load myproject)"
   ```

2. Spawn a new shell with the profile's environment variables:
   ```bash
   envault load myproject --shell
   ```

## Security

- All secrets are stored in GPG-encrypted files under `~/.apivault/profiles/`
- Files are encrypted using symmetric encryption (requires password)
- Temporary files are secured with appropriate permissions (600)
- No secrets are written to shell startup files
- Secrets are only decrypted when explicitly loaded

## File Structure

```
~/.apivault/
├── profiles/
│   ├── myproject.env.gpg
│   ├── anotherproject.env.gpg
```

## Requirements

- Python 3.8 or later
- GPG (gnupg) installed on the system
- Linux/Unix-based operating system

## License

MIT License