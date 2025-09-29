#!/usr/bin/env python3
"""
Test SSO functionality
"""

import subprocess
from github import Github, Auth


def test_sso_flow():
    print("🧪 Testing GitHub CLI SSO Flow")
    print("=" * 40)
    
    # Check if GitHub CLI is available
    try:
        result = subprocess.run(['gh', '--version'], 
                               capture_output=True, text=True, check=True)
        print("✅ GitHub CLI is available")
        print(f"   Version: {result.stdout.split()[2]}")
    except subprocess.CalledProcessError:
        print("❌ GitHub CLI not found")
        return False
    
    # Check current auth status
    try:
        result = subprocess.run(['gh', 'auth', 'status'], 
                               capture_output=True, text=True, check=True)
        print("\n✅ GitHub CLI is authenticated")
        print("Current auth status:")
        for line in result.stdout.split('\n'):
            if line.strip():
                print(f"   {line}")
    except subprocess.CalledProcessError:
        print("\n❌ GitHub CLI not authenticated")
        print("Run: gh auth login --web --scopes repo,read:org")
        return False
    
    # Test token access
    try:
        result = subprocess.run(['gh', 'auth', 'token'], 
                               capture_output=True, text=True, check=True)
        token = result.stdout.strip()
        
        print("\n🔍 Testing repository access with GitHub CLI token...")
        auth = Auth.Token(token)
        g = Github(auth=auth)
        
        user = g.get_user()
        print(f"✅ Token works for user: {user.login}")
        
        # Test organization access
        try:
            org = g.get_organization("UWC2-PYTHON")
            print(f"✅ Can access organization: {org.name}")
            
            # Try to get repositories
            repos = list(org.get_repos())
            print(f"✅ Can access {len(repos)} repositories via API")
            
            return True
            
        except Exception as e:
            if "SAML" in str(e) or "403" in str(e):
                print("❌ SSO authorization needed")
                print("   Go to: https://github.com/orgs/UWC2-PYTHON/sso")
                print("   Authorize your GitHub CLI token")
                return False
            else:
                print(f"⚠️  Organization access limited: {e}")
                return True  # Token works, just limited access
                
    except subprocess.CalledProcessError:
        print("❌ Cannot get GitHub CLI token")
        return False


if __name__ == "__main__":
    test_sso_flow()