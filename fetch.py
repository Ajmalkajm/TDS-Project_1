import requests
import csv
import time

# GitHub API token and headers for authentication
TOKEN = "your_personal_access_token_here"
HEADERS = {"Authorization": f"token {TOKEN}"}

# Helper function to clean company names
def clean_company_name(name):
    if name:
        name = name.strip().lstrip("@").upper()
    return name

# Function to get users in Bangalore with over 100 followers
def get_bangalore_users(min_followers=100, location="Bangalore"):
    users = []
    url = f"https://api.github.com/search/users?q=location:{location}+followers:>{min_followers}&per_page=100"
    page = 1

    while True:
        response = requests.get(f"{url}&page={page}", headers=HEADERS)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            break

        data = response.json()
        items = data.get('items', [])
        if not items:
            break

        for user in items:
            # Fetch detailed user data
            user_details = requests.get(user['url'], headers=HEADERS).json()
            user_info = {
                "login": user_details.get("login", ""),
                "name": user_details.get("name", ""),
                "company": clean_company_name(user_details.get("company", "")),
                "location": user_details.get("location", ""),
                "email": user_details.get("email", ""),
                "hireable": user_details.get("hireable", ""),
                "bio": user_details.get("bio", ""),
                "public_repos": user_details.get("public_repos", ""),
                "followers": user_details.get("followers", ""),
                "following": user_details.get("following", ""),
                "created_at": user_details.get("created_at", "")
            }
            users.append(user_info)
        page += 1
        time.sleep(1)  # Avoid rate limit

    return users

# Function to get up to 500 repositories for each user
def get_user_repositories(username):
    repos = []
    url = f"https://api.github.com/users/{username}/repos?per_page=100"
    page = 1

    while True:
        response = requests.get(f"{url}&page={page}", headers=HEADERS)
        if response.status_code != 200:
            print(f"Error fetching repos for {username}: {response.status_code}")
            break

        data = response.json()
        if not data:
            break

        for repo in data[:500]:  # Limit to 500 repos per user
            repo_info = {
                "login": username,
                "full_name": repo.get("full_name", ""),
                "created_at": repo.get("created_at", ""),
                "stargazers_count": repo.get("stargazers_count", 0),
                "watchers_count": repo.get("watchers_count", 0),
                "language": repo.get("language", ""),
                "has_projects": repo.get("has_projects", False),
                "has_wiki": repo.get("has_wiki", False),
                "license_name": repo.get("license", {}).get("key", "")
            }
            repos.append(repo_info)
        page += 1
        time.sleep(1)  # Avoid rate limit

    return repos

# Function to save user data to CSV
def save_users_to_csv(users, filename="users.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=[
            "login", "name", "company", "location", "email", "hireable", "bio", 
            "public_repos", "followers", "following", "created_at"
        ])
        writer.writeheader()
        writer.writerows(users)

# Function to save repository data to CSV
def save_repos_to_csv(repos, filename="repositories.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=[
            "login", "full_name", "created_at", "stargazers_count", 
            "watchers_count", "language", "has_projects", "has_wiki", "license_name"
        ])
        writer.writeheader()
        writer.writerows(repos)

# Main function
def main():
    # Step 1: Get users from Bangalore with more than 100 followers
    users = get_bangalore_users()
    save_users_to_csv(users)

    # Step 2: Get each user's repositories and save them to repositories.csv
    all_repos = []
    for user in users:
        print(f"Fetching repositories for user: {user['login']}")
        user_repos = get_user_repositories(user["login"])
        all_repos.extend(user_repos)
    
    save_repos_to_csv(all_repos)

if __name__ == "__main__":
    main()
