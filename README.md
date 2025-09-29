# UWC2-PYTHON Code Rescue Tool 🎓

## What is this tool?

This tool helps UWC2-PYTHON students preserve their coursework by forking repositories from the GitHub Classroom organization to their personal accounts before losing access.

## Why do I need this?

When your course ends, you may lose access to the UWC2-PYTHON organization and all the assignment repositories containing your hard work. This tool creates personal copies (forks) of your repositories so you can keep them forever.

## Prerequisites

1. **Python 3.7 or higher** installed on your computer
2. **GitHub CLI** (required for SSO authentication): https://docs.github.com/en/github-cli/github-cli/quickstart
3. Optional: **A GitHub Personal Access Token** as backup (requires manual SSO authorization)

### Installing GitHub CLI

**Why GitHub CLI is needed:** The UWC2-PYTHON organization uses SAML SSO, which GitHub CLI handles automatically. Manual tokens require additional SSO authorization steps that can be tricky.

**Installation:**
- **macOS**: `brew install gh`
- **Windows**: Download from https://github.com/cli/cli/releases
- **Linux**: See https://github.com/cli/cli/blob/trunk/docs/install_linux.md

### Creating a GitHub Personal Access Token (Optional)

**Note:** GitHub CLI is recommended instead of manual tokens for SSO organizations.

If you need to create a manual token:

1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Give it a descriptive name like "UWC2-PYTHON Code Rescue"
4. Select the following scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `read:org` (Read organization and team membership)
5. Click "Generate token"
6. **IMPORTANT**: Copy the token immediately - you won't be able to see it again!

## Installation

1. **Download the tool**:
   ```bash
   git clone <repository-url>
   cd code-rescue
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   
   Or manually:
   ```bash
   pip install PyGithub
   ```

## How to use

### Recommended: GitHub CLI with SSO

This is the easiest method for SSO organizations like UWC2-PYTHON:

1. **Run the tool**:
   ```bash
   python code_rescue.py
   ```

2. **Choose "GitHub CLI" when prompted** - this handles SSO authorization automatically

3. **Complete the browser authentication** when GitHub CLI opens your browser

4. **Authorize SSO access** - the tool will guide you through this process if needed

### Alternative: Manual Token Entry (Advanced)

**Warning:** Manual tokens with SSO can be tricky - GitHub CLI is recommended.

1. **Create a Personal Access Token** (see instructions above)

2. **Authorize it for SSO**:
   - Go to https://github.com/orgs/UWC2-PYTHON/sso
   - Find your token and click "Authorize"
   - OR go to https://github.com/settings/tokens and click "Configure SSO"

3. **Run the tool and choose manual entry**:
   ```bash
   python code_rescue.py
   ```

### What happens during rescue

1. **Discovery**: The tool finds repositories you already have and identifies what might already be rescued
2. **Repository Selection**: The tool automatically finds your student repositories or you can enter them manually
3. **Filtering**: The tool identifies which repositories need to be rescued (vs. already rescued)
4. **Destination Choice**: Choose where to fork your repositories:
   - Personal account (`your-username/repo-name`)
   - Personal organization (`your-org/repo-name`)
5. **Naming Options**: Choose how to name your forked repositories:
   - Keep original names
   - Add a custom prefix (e.g., `backup-`, `class-`)
   - Use the default `rescued-` prefix
6. **Confirmation**: You'll see a preview of what will be created and can choose to proceed
7. **Rescue**: The tool forks each repository automatically
8. **Manual Instructions**: For any repositories that can't be forked automatically, you'll get step-by-step instructions

## Example

Original repository: `UWC2-PYTHON/320-sp25-assignment-08-yourusername`

**Example outcomes based on your choices:**
- Personal + no prefix: `yourusername/320-sp25-assignment-08-yourusername`
- Personal + custom prefix: `yourusername/class-320-sp25-assignment-08-yourusername` 
- Organization + rescued prefix: `my-backup-org/rescued-320-sp25-assignment-08-yourusername`

## Troubleshooting

### "Token verification failed"
- Make sure your Personal Access Token has the correct scopes (`repo` and `read:org`)
- Check that you copied the token correctly (no extra spaces)

### "Failed to fork repository"
- The repository might already be forked in your account
- You might not have access to that specific repository
- Try forking manually through the GitHub web interface

### "Cannot access repository via API" but I can see it on the web
- This is due to GitHub's SAML SSO restrictions on API access
- **Solution**: Use GitHub CLI authentication (recommended) - it handles SSO automatically
- **Alternative**: If using manual tokens, authorize SSO at https://github.com/orgs/UWC2-PYTHON/sso
- The tool will provide manual rescue instructions as a fallback

### "GitHub CLI not found" or "gh command not found"
- Install GitHub CLI from https://docs.github.com/en/github-cli/github-cli/quickstart
- Make sure it's in your system PATH
- Restart your terminal after installation

### "SSO authorization still needed"
- Go to https://github.com/orgs/UWC2-PYTHON/sso
- Look for your GitHub CLI token or Personal Access Token
- Click "Authorize" next to it
- Complete any additional authentication steps required by your organization

## Important Notes

- **This tool is safe** - it only creates forks, it doesn't delete or modify anything
- **Repository names get a prefix** - all rescued repos will be named either the same or prefixed with your chose option (i.e. `rescued-original-name`)
- **Private repositories stay private** - your rescued repositories will have the same visibility as the originals
- **Run this before you lose access** - the tool needs your current organization access to work

## Getting Help

If you run into issues:

1. Make sure you can access https://github.com/orgs/UWC2-PYTHON/repositories in your browser
2. Verify your Personal Access Token is working at https://github.com/settings/tokens
3. Contact your fellow students or instructor for help

## Security

- **Never share your Personal Access Token** with anyone
- **Delete the token** after you're done rescuing your repositories
- The token gives access to your repositories, so keep it private

---

**Created by Eric Fisher for UWC2-PYTHON students** 🐍

Remember: Better safe than sorry - fork your code before it's too late!