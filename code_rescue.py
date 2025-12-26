#!/usr/bin/env python3
"""
UWC2-PYTHON Code Rescue Tool

A tool to help students preserve their coursework by forking repositories
from the UWC2-PYTHON GitHub Classroom organization to their personal accounts
before losing access.

Author: Eric Fisher & GitHub Copilot
"""

import subprocess
from github import Github, Auth
from typing import List


def get_github_token() -> str:
    """Get GitHub token from CLI or manual input."""
    try:
        result = subprocess.run(['gh', 'auth', 'token'],
                                capture_output=True, text=True, check=True)
        token = result.stdout.strip()
        print("✅ Found existing GitHub CLI token")
        return token
    except subprocess.CalledProcessError:
        print("\n🔑 GitHub CLI not authenticated.")
        print("Please choose your authentication method:")
        print()
        print("1. Use GitHub CLI (recommended for SSO)")
        print("2. Enter Personal Access Token manually")
        print()

        choice = input("Choose option (1 or 2): ").strip()

        if choice == "1":
            return setup_github_cli_with_sso()
        else:
            return get_manual_token()


def setup_github_cli_with_sso() -> str:
    """Set up GitHub CLI with SSO support."""
    print("\n🔧 Setting up GitHub CLI with SSO support...")
    print("=" * 50)
    print("GitHub CLI can handle SSO authorization automatically.")
    print("This should allow access to your UWC2-PYTHON repositories.")
    print()

    # First, try to login with GitHub CLI
    print("Step 1: Authenticate with GitHub CLI")
    print("The following command will open your browser for authentication:")
    print()
    print("gh auth login --web --scopes repo,read:org")
    print()

    proceed = input("Ready to authenticate? (y/N): ").strip().lower()
    if proceed != 'y':
        print("❌ Authentication cancelled. Falling back to manual token.")
        return get_manual_token()

    try:
        # Run the auth login command
        subprocess.run([
            'gh', 'auth', 'login',
            '--web',
            '--scopes', 'repo,read:org'
        ], check=True, text=True)

        print("✅ GitHub CLI authentication completed!")

        # Get the token
        token_result = subprocess.run(['gh', 'auth', 'token'],
                                      capture_output=True, text=True,
                                      check=True)
        token = token_result.stdout.strip()

        print("\nStep 2: Testing SSO access...")
        return test_sso_access(token)

    except subprocess.CalledProcessError as e:
        print(f"❌ GitHub CLI authentication failed: {e}")
        print("Falling back to manual token entry.")
        return get_manual_token()


def test_sso_access(token: str) -> str:
    """Test if the token has SSO access to UWC2-PYTHON."""
    print("🔍 Testing access to UWC2-PYTHON repositories...")

    try:
        auth = Auth.Token(token)
        g = Github(auth=auth)

        # Try to access a known student repository pattern
        print("Attempting to search for your repositories in UWC2-PYTHON...")
        user = g.get_user()
        username = user.login

        # Try to search for repositories with the user's name
        search_query = f"org:UWC2-PYTHON {username} in:name"
        repos = list(g.search_repositories(search_query))

        if repos:
            print(f"🎉 SUCCESS! Found {len(repos)} repositories:")
            for repo in repos[:5]:  # Show first 5
                print(f"   - {repo.name}")
            if len(repos) > 5:
                print(f"   ... and {len(repos) - 5} more")
            print("\n✅ SSO access is working! Your repositories should be")
            print("   accessible.")
        else:
            print("⚠️  No repositories found in search, but this might be")
            print("   normal.")
            print("   We'll proceed and see if direct access works.")

        return token

    except Exception as e:
        if "SAML enforcement" in str(e) or "403" in str(e):
            print("\n❌ SSO authorization still needed!")
            return handle_sso_authorization_needed(token)
        else:
            print(f"⚠️  Unexpected error: {e}")
            print("   Proceeding anyway - the tool will provide manual")
            print("   instructions if needed.")
            return token


def handle_sso_authorization_needed(token: str) -> str:
    """Handle the case where SSO authorization is still needed."""
    print("🔐 SSO Authorization Required")
    print("=" * 40)
    print("Your GitHub CLI token needs to be authorized for the")
    print("UWC2-PYTHON organization.")
    print()
    print("Please follow these steps:")
    print("1. Open: https://github.com/orgs/UWC2-PYTHON/sso")
    print("2. Look for your GitHub CLI token in the list")
    print("3. Click 'Authorize' next to it")
    print("4. Complete any SSO authentication steps")
    print()
    print("Alternative method:")
    print("1. Go to: https://github.com/settings/tokens")
    print("2. Find your GitHub CLI token")
    print("3. Click 'Configure SSO' next to it")
    print("4. Authorize it for UWC2-PYTHON")
    print()

    input("Press Enter after completing SSO authorization...")

    # Test again
    print("\n🔍 Testing SSO access again...")
    try:
        auth = Auth.Token(token)
        g = Github(auth=auth)

        # Try a simple organization access
        org = g.get_organization("UWC2-PYTHON")
        print(f"✅ SSO authorization successful! Can access {org.name}")
        return token

    except Exception as e:
        print(f"❌ SSO authorization still not working: {e}")
        print("\nThe tool will still work, but repositories will need to")
        print("be rescued manually.")
        print("Don't worry - manual rescue is just as effective!")
        return token


def get_manual_token() -> str:
    """Get token through manual entry."""
    print("\n🔑 Manual Token Entry")
    print("Please enter your Personal Access Token.")
    print("(Create one at: https://github.com/settings/tokens)")
    print("Required scopes: repo, read:org")
    print()
    print("⚠️  Note: Manual tokens may need separate SSO authorization")
    print("   at https://github.com/orgs/UWC2-PYTHON/sso")

    token = input("\nPAT: ").strip()
    if not token:
        print("❌ No token provided. Exiting.")
        exit(1)
    return token


def verify_token(g: Github) -> bool:
    """Verify the token works and can access UWC2-PYTHON."""
    try:
        user = g.get_user()
        print(f"✅ Token verified for user: {user.login}")

        # Test UWC2-PYTHON access
        org = g.get_organization("UWC2-PYTHON")
        print(f"✅ Can access organization: {org.name}")
        return True

    except Exception as e:
        print(f"❌ Token verification failed: {e}")
        return False


def discover_repositories(g: Github) -> tuple[List, List, List]:
    """Discover personal and organization repositories."""
    print("\n🔍 Discovering repositories...")

    # Personal repositories (only those owned by the user, not org repos)
    user = g.get_user()
    all_user_repos = list(user.get_repos())
    personal_repos = [repo for repo in all_user_repos
                      if repo.owner.login == user.login]

    print(f"✅ Found {len(personal_repos)} personal repositories")
    print(f"   (filtered from {len(all_user_repos)} total accessible repos)")

    # UWC2-PYTHON repositories (API accessible)
    api_accessible_repos = []
    try:
        org = g.get_organization("UWC2-PYTHON")
        api_accessible_repos = list(org.get_repos())
        print(f"✅ Found {len(api_accessible_repos)} UWC2-PYTHON repositories "
              "via API")

        if len(api_accessible_repos) > 10:  # Good SSO access
            print("🎉 Great! Your SSO authorization is working properly!")

    except Exception as e:
        print(f"❌ Could not access UWC2-PYTHON repositories via API: {e}")

    # Check for repositories that might already be rescued
    # (only in actual personal repos)
    # Note: This excludes UWC2-PYTHON org repos where you're a collaborator
    rescued_repos = []
    # Common patterns for course repositories - focus on course numbers
    course_patterns = ['uwc2', 'UWC2', '310-', '320-', '330-',
                       'lesson-', 'assignment-', 'exercise-', 'lab-',
                       'rescued-', 'class-', 'course-']

    for repo in personal_repos:
        for pattern in course_patterns:
            if pattern.lower() in repo.name.lower():
                rescued_repos.append(repo)
                break

    print(f"🔍 Found {len(rescued_repos)} potentially rescued course "
          "repos in personal account")

    return personal_repos, api_accessible_repos, rescued_repos


def prompt_for_manual_repositories() -> List[str]:
    """Prompt user to manually enter repository names from web interface."""
    print("\n📋 Manual Repository Entry")
    print("=" * 50)
    print("Since GitHub's API limits access to private organization")
    print("repositories, please manually enter the names of UWC2-PYTHON")
    print("repositories you want to rescue.")
    print("You can find these at:")
    print("https://github.com/orgs/UWC2-PYTHON/repositories")
    print()
    print("Instructions:")
    print("1. Visit the UWC2-PYTHON organization page")
    print("2. Look for repositories that contain YOUR work")
    print("   (usually have your GitHub username)")
    print("3. Enter repository names one per line")
    print("4. Press Enter on an empty line when done")
    print()

    repo_names = []
    while True:
        prompt = "Repository name (or press Enter to finish): "
        name = input(prompt).strip()
        if not name:
            break
        if name not in repo_names:
            repo_names.append(name)
            print(f"   ✅ Added: {name}")
        else:
            print(f"   ⚠️  Already added: {name}")

    return repo_names


def filter_repositories_for_rescue(rescued_repos: List,
                                   manual_repos: List[str],
                                   org_repos: List) -> List[str]:
    """
    Filter repositories to identify which ones need rescue.
    Uses fork count from organization repos as the primary indicator.
    """
    repos_to_rescue = []

    print("🎯 Repository Filtering")
    print("=" * 30)

    # Create a lookup for org repos by name
    org_repo_lookup = {repo.name: repo for repo in org_repos}

    if manual_repos:
        print(f"🔍 Analyzing {len(manual_repos)} repositories:")
        for repo_name in manual_repos:
            # Check fork count in the organization repository
            if repo_name in org_repo_lookup:
                org_repo = org_repo_lookup[repo_name]
                fork_count = org_repo.forks_count

                if fork_count == 0:
                    print(f"   ✅ {repo_name} - needs rescue (0 forks)")
                    repos_to_rescue.append(repo_name)
                else:
                    print(f"   ⏭️  {repo_name} - already forked "
                          f"({fork_count} fork"
                          f"{'s' if fork_count != 1 else ''})")
            else:
                # Fallback: check personal repos for exact matches
                already_rescued = False
                for rescued in rescued_repos:
                    # Exact match
                    if repo_name.lower() == rescued.name.lower():
                        already_rescued = True
                        print(f"   ⏭️  {repo_name} - exact match with "
                              f"{rescued.name}")
                        print(f"        (created: {rescued.created_at}, "
                              f"fork: {rescued.fork})")
                        break
                    # Rescued with prefix
                    elif (rescued.name.lower() ==
                          f"rescued-{repo_name.lower()}"):
                        already_rescued = True
                        print(f"   ⏭️  {repo_name} - found as {rescued.name}")
                        print(f"        (created: {rescued.created_at}, "
                              f"fork: {rescued.fork})")
                        break

                if not already_rescued:
                    print(f"   ✅ {repo_name} - needs rescue "
                          "(not found in org repos, checking personal)")
                    repos_to_rescue.append(repo_name)

    return repos_to_rescue


def get_fork_destination_options() -> tuple[str, str, str]:
    """Get user preferences for fork destination and naming."""
    print("\n🎯 Fork Destination Options")
    print("=" * 40)

    # Option 1: Where to fork
    print("Where would you like to fork repositories?")
    print("1. Personal account (your username)")
    print("2. Personal organization")

    while True:
        choice = input("Choose destination (1-2): ").strip()
        if choice in ['1', '2']:
            break
        print("Please enter 1 or 2")

    if choice == '1':
        destination = "personal"
        destination_name = None
    else:
        # Get organization name
        while True:
            org_name = input("Enter organization name: ").strip()
            if org_name:
                destination = "organization"
                destination_name = org_name
                break
            print("Please enter a valid organization name")

    # Option 2: Naming prefix
    print("\n📝 Repository Naming")
    print("Would you like to add a prefix to forked repository names?")
    print("1. No prefix (keep original names)")
    print("2. Add custom prefix")
    print("3. Add 'rescued-' prefix")

    while True:
        prefix_choice = input("Choose naming option (1-3): ").strip()
        if prefix_choice in ['1', '2', '3']:
            break
        print("Please enter 1, 2, or 3")

    if prefix_choice == '1':
        name_prefix = None
    elif prefix_choice == '2':
        custom_prefix = input("Enter your custom prefix (without dash): ")
        name_prefix = custom_prefix.strip()
        if name_prefix and not name_prefix.endswith('-'):
            name_prefix += '-'
    else:
        name_prefix = "rescued-"

    return destination, destination_name, name_prefix


def fork_repository(g: Github, org_name: str, repo_name: str,
                    destination: str = "personal",
                    destination_name: str = None,
                    name_prefix: str = None) -> bool:
    """Fork a repository with flexible destination and naming options."""
    try:
        # Get the repository to fork
        repo = g.get_repo(f"{org_name}/{repo_name}")

        # Determine the new name
        if name_prefix:
            new_name = f"{name_prefix}{repo_name}"
        else:
            new_name = repo_name

        # Create fork
        if destination == "organization" and destination_name:
            # Fork to organization
            fork = repo.create_fork(organization=destination_name,
                                    name=new_name)
            print(f"✅ Successfully forked to organization: {fork.full_name}")
        else:
            # Fork to personal account
            fork = repo.create_fork(name=new_name)
            print(f"✅ Successfully forked to personal: {fork.full_name}")

        return True

    except Exception as e:
        if "404" in str(e) or "Not Found" in str(e):
            print(f"❌ Cannot access {org_name}/{repo_name} via API")
            print("   This is likely due to private repository restrictions.")
        else:
            print(f"❌ Failed to fork {org_name}/{repo_name}: {e}")
        return False


def rescue_repositories(g: Github, repos_to_rescue: List[str],
                        destination: str = "personal",
                        destination_name: str = None,
                        name_prefix: str = None) -> None:
    """Fork multiple repositories to rescue them."""
    print(f"\n🚀 Starting rescue operation for {len(repos_to_rescue)} "
          "repositories...")

    # Show destination info
    if destination == "organization" and destination_name:
        print(f"📍 Destination: {destination_name} organization")
    else:
        print("📍 Destination: Personal account")

    if name_prefix:
        print(f"🏷️  Prefix: '{name_prefix}'")
    else:
        print("🏷️  Prefix: None (original names)")

    print("=" * 60)

    successful_forks = []
    failed_forks = []

    for i, repo_name in enumerate(repos_to_rescue, 1):
        print(f"\n[{i}/{len(repos_to_rescue)}] Forking: {repo_name}")

        success = fork_repository(g, "UWC2-PYTHON", repo_name,
                                  destination, destination_name, name_prefix)

        if success:
            successful_forks.append(repo_name)
        else:
            failed_forks.append(repo_name)

    # Summary
    print("\n📊 Rescue Operation Complete!")
    print("=" * 40)
    print(f"✅ Successfully rescued: {len(successful_forks)} repositories")
    print(f"❌ Failed to rescue: {len(failed_forks)} repositories")

    if successful_forks:
        print("\n🎉 Successfully rescued repositories:")
        for repo in successful_forks:
            if name_prefix:
                display_name = f"{name_prefix}{repo}"
            else:
                display_name = repo
            print(f"   - {display_name}")

    if failed_forks:
        print("\n⚠️  Failed to rescue:")
        for repo in failed_forks:
            print(f"   - {repo}")

        print("\n📋 Manual Rescue Instructions:")
        print("=" * 40)
        print("For repositories that failed to fork via API, you can rescue")
        print("them manually:")
        print()
        for repo in failed_forks:
            print(f"🔗 {repo}:")
            print(f"   1. Visit: https://github.com/UWC2-PYTHON/{repo}")
            print("   2. Click the 'Fork' button (top right)")
            print("   3. Choose your personal account as the destination")
            if name_prefix:
                suggested_name = f"{name_prefix}{repo}"
                print(f"   4. Optionally rename it to '{suggested_name}'")
            else:
                print("   4. Keep the original name or rename as desired")
            print()

        print("💡 These manual forks will preserve your code just as")
        print("   effectively! The API limitation doesn't affect the web")
        print("   interface.")


def main():
    """Main function."""
    print("🎓 UWC2-PYTHON Code Rescue Tool")
    print("=" * 50)
    print("This tool helps you preserve your coursework by forking")
    print("repositories to your personal GitHub account.")
    print()

    # Get and verify token
    token = get_github_token()
    g = Github(auth=Auth.Token(token))

    if not verify_token(g):
        print("❌ Cannot proceed without valid token. Exiting.")
        return

    # Discover repositories
    repos_result = discover_repositories(g)
    personal_repos, api_accessible_repos, rescued_repos = repos_result

    print("\n📊 Summary:")
    print(f"   Personal repositories: {len(personal_repos)}")
    print(f"   UWC2-PYTHON repositories (API accessible): "
          f"{len(api_accessible_repos)}")
    print(f"   Potentially already rescued: {len(rescued_repos)}")

    if api_accessible_repos:
        print("\n🎯 UWC2-PYTHON Repositories Available via API:")
        for repo in api_accessible_repos:
            visibility = "🔒" if repo.private else "🌍"
            updated = repo.updated_at.strftime("%Y-%m-%d")
            print(f"   {visibility} {repo.name} (updated: {updated})")
            if repo.description:
                print(f"      📝 {repo.description}")

    # Get manual repository input or use API discoveries
    if len(api_accessible_repos) >= 10:  # Good API access
        print(f"\n🎉 Great news! We can see {len(api_accessible_repos)} "
              "repositories via API.")
        print("We can automatically identify your student repositories.")

        # Filter for student repositories (containing username)
        user = g.get_user()
        username = user.login

        student_repos = []
        for repo in api_accessible_repos:
            # Skip obvious template/resource repositories
            skip_patterns = ['Resources', '.github', 'accessTestRepo',
                             'README', 'template', 'base-', 'TEMPLATE']
            should_skip = any(pattern.lower() in repo.name.lower()
                              for pattern in skip_patterns)

            if should_skip:
                continue

            # Include repositories with username or common patterns
            has_username = username.lower() in repo.name.lower()
            has_pattern = any(pattern in repo.name.lower()
                              for pattern in ['lesson-', 'assignment-',
                                              'exercise-', 'lab-', '310-',
                                              '320-', '330-'])
            if has_username or has_pattern:
                student_repos.append(repo.name)

        print(f"\n🎯 Found {len(student_repos)} student repositories:")
        for repo_name in student_repos[:10]:  # Show first 10
            print(f"   - {repo_name}")
        if len(student_repos) > 10:
            print(f"   ... and {len(student_repos) - 10} more")

        manual_repos = student_repos
    else:
        print(f"\n⚠️  Note: Due to GitHub API limitations, we can only see "
              f"{len(api_accessible_repos)} of your repositories.")
        print("Let's manually identify the repositories you want to rescue.")
        print("\n💡 If automatic forking fails, don't worry! The tool will")
        print("   provide step-by-step instructions for manual rescue via")
        print("   web interface.")

        manual_repos = prompt_for_manual_repositories()

    if manual_repos:
        repos_to_rescue = filter_repositories_for_rescue(rescued_repos,
                                                         manual_repos,
                                                         api_accessible_repos)

        if repos_to_rescue:
            print(f"\n🚀 Ready to rescue {len(repos_to_rescue)} repositories:")
            for repo_name in repos_to_rescue:
                print(f"   - {repo_name}")

            # Get destination and naming preferences
            options = get_fork_destination_options()
            destination, destination_name, name_prefix = options

            # Ask for confirmation
            if destination == "organization" and destination_name:
                dest_info = f"'{destination_name}' organization"
            else:
                dest_info = "your personal account"

            if name_prefix:
                name_info = f" with '{name_prefix}' prefix"
            else:
                name_info = " (keeping original names)"

            print(f"\n⚠️  This will fork these repositories to {dest_info}"
                  f"{name_info}.")
            confirm = input("Do you want to proceed? (y/N): ").strip().lower()

            if confirm == 'y':
                rescue_repositories(g, repos_to_rescue, destination,
                                    destination_name, name_prefix)
            else:
                print("❌ Rescue operation cancelled.")
        else:
            print("\n✅ All repositories appear to already be rescued!")
    else:
        print("\n👋 No repositories entered. Exiting.")


if __name__ == "__main__":
    main()
