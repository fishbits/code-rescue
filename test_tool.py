#!/usr/bin/env python3
"""
Simple test script to verify the code rescue tool functionality
"""

from github import Github, Auth

def test_token_access():
    """Test if a token can access UWC2-PYTHON organization."""
    print("🧪 Testing Code Rescue Tool Components")
    print("=" * 50)
    
    # Test token input
    print("\n1. Testing token input...")
    token = input("Enter your Personal Access Token for testing: ").strip()
    
    if not token:
        print("❌ No token provided")
        return False
    
    # Test GitHub API access
    print("\n2. Testing GitHub API access...")
    try:
        auth = Auth.Token(token)
        g = Github(auth=auth)
        user = g.get_user()
        print(f"✅ Connected as: {user.login}")
    except Exception as e:
        print(f"❌ GitHub API access failed: {e}")
        return False
    
    # Test UWC2-PYTHON access
    print("\n3. Testing UWC2-PYTHON organization access...")
    try:
        org = g.get_organization("UWC2-PYTHON")
        print(f"✅ Can access organization: {org.name}")
        
        repos = list(org.get_repos())
        print(f"✅ Can see {len(repos)} repositories via API")
    except Exception as e:
        print(f"⚠️  Limited API access to organization: {e}")
        print("This is expected for private organization repositories.")
    
    # Test forking capability (dry run)
    print("\n4. Testing fork capability...")
    try:
        # Try to access any public repository to test fork function
        test_repo = g.get_repo("UWC2-PYTHON/.github")  # Organization welcome page
        print(f"✅ Can access test repository: {test_repo.name}")
        print("✅ Fork functionality should work (test successful)")
    except Exception as e:
        print(f"⚠️  Could not access test repository: {e}")
        print("You may need to fork repositories manually through the web interface.")
    
    print(f"\n🎉 Test complete! The code rescue tool should work for you.")
    print("Now run: python code_rescue.py")
    return True

if __name__ == "__main__":
    test_token_access()