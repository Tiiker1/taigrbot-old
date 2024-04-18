import os
import json
import discord
import requests
from datetime import datetime

# GitHub repository information
GITHUB_USERNAME = 'yourgithubusername'
REPOSITORY_NAME = 'yourreponame'
REPOSITORY_URL = f'https://github.com/{GITHUB_USERNAME}/{REPOSITORY_NAME}'
COMMIT_DATA_DIR = 'commit_data'

# Function to fetch recent commits from GitHub
def fetch_recent_commits():
    try:
        response = requests.get(f'https://api.github.com/repos/{GITHUB_USERNAME}/{REPOSITORY_NAME}/commits')
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except Exception as e:
        print(f"Failed to fetch commits: {e}")
        return []

# Function to load commit data from a JSON file
def load_commit_data():
    try:
        with open(os.path.join(COMMIT_DATA_DIR, 'commits.json'), 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Function to save commit data to a JSON file
def save_commit_data(commits):
    try:
        os.makedirs(COMMIT_DATA_DIR, exist_ok=True)
        with open(os.path.join(COMMIT_DATA_DIR, 'commits.json'), 'w') as file:
            json.dump(commits, file, indent=4)
    except Exception as e:
        print(f"Failed to save commit data: {e}")

# Function to create an embed message for a commit
def create_commit_embed(commit):
    try:
        commit_date = datetime.strptime(commit["commit"]["author"]["date"], "%Y-%m-%dT%H:%M:%SZ").strftime(
            "%b %d, %Y %I:%M %p UTC")
        github_username = commit["commit"]["author"].get("username", commit["commit"]["author"]["name"])

        embed = discord.Embed(
            title="New Commit",
            description=f"**{commit['commit']['message'].splitlines()[0]}**",
            color=0x6e5494,
        )
        embed.set_author(name=commit["commit"]["author"]["name"], icon_url=commit["author"]["avatar_url"])
        embed.set_thumbnail(url="https://github.githubassets.com/images/modules/logos_page/Octocat.png")
        embed.set_footer(text=f"{github_username} | {commit_date}")
        embed.add_field(name="\u200b", value=f"[View Commit on GitHub]({REPOSITORY_URL}/commit/{commit['sha']})",
                        inline=False)

        return embed
    except Exception as e:
        print(f"Failed to create commit embed: {e}")
        return None

# Function to check for new commits and send message to Discord
async def check_commits_and_send_message(bot):
    try:
        # Fetch recent commits from GitHub
        commits = fetch_recent_commits()
        if not commits:
            print("No commits found.")
            return

        # Reverse the order of commits to process them from oldest to newest
        commits.reverse()

        # Load previously sent commits
        sent_commits = load_commit_data()

        # Filter out already sent commits
        unsent_commits = [commit for commit in commits if commit['sha'] not in sent_commits]

        # Send messages for unsent commits
        for commit in unsent_commits:
            embed = create_commit_embed(commit)
            if embed:
                channel_id = 3242342342342324  # Replace this with the actual channel ID
                channel = bot.get_channel(channel_id)
                await channel.send(embed=embed)

        # Update the list of sent commits
        all_commits = sent_commits + [commit['sha'] for commit in unsent_commits]
        save_commit_data(all_commits)
    except Exception as e:
        print(f"Failed to check commits and send message: {e}")
