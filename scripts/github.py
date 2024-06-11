import discord
import requests
import os
from datetime import datetime
import pytz
import json
import asyncio
import sqlite3

# Define your GitHub repository information
GITHUB_USERNAME = 'username'
REPOSITORY_NAME = 'reponame'
REPOSITORY_URL = f'https://github.com/{GITHUB_USERNAME}/{REPOSITORY_NAME}'
DATABASE_PATH = 'databases/github_data.db'

# Define Helsinki timezone
helsinki_tz = pytz.timezone('Europe/Helsinki')

# Ensure the database directory exists
os.makedirs('databases', exist_ok=True)

# Function to initialize the SQLite database
def init_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS commits (
            sha TEXT PRIMARY KEY
        )
    ''')
    conn.commit()
    conn.close()

# Function to fetch all commits from GitHub with pagination
def fetch_all_commits():
    commits = []
    page = 1
    while True:
        try:
            response = requests.get(
                f'https://api.github.com/repos/{GITHUB_USERNAME}/{REPOSITORY_NAME}/commits',
                params={'page': page, 'per_page': 100}
            )
            response.raise_for_status()  # Raise an error for bad responses
            page_commits = response.json()
            if not page_commits:
                break
            commits.extend(page_commits)
            page += 1
        except Exception as e:
            print(f"Failed to fetch commits: {e}")
            break
    return commits

# Function to load commit data from the SQLite database
def load_commit_data():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT sha FROM commits')
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]

# Function to save commit data to the SQLite database
def save_commit_data(commits):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.executemany('INSERT OR IGNORE INTO commits (sha) VALUES (?)', [(commit,) for commit in commits])
    conn.commit()
    conn.close()

# Function to create an embed message for a commit
def create_commit_embed(commit):
    try:
        commit_date = datetime.strptime(commit["commit"]["author"]["date"], "%Y-%m-%dT%H:%M:%SZ")
        commit_date = commit_date.replace(tzinfo=pytz.utc).astimezone(helsinki_tz)  # Convert to Helsinki timezone
        commit_date_str = commit_date.strftime("%b %d, %Y %I:%M %p %Z")

        github_username = commit["commit"]["author"].get("username", commit["commit"]["author"]["name"])

        embed = discord.Embed(
            title="New Commit",
            description=f"**{commit['commit']['message'].splitlines()[0]}**",
            color=0x6e5494,
        )
        embed.set_author(name=commit["commit"]["author"]["name"], icon_url=commit["author"]["avatar_url"])
        embed.set_thumbnail(url="https://github.githubassets.com/images/modules/logos_page/Octocat.png")
        embed.set_footer(text=f"{github_username} | {commit_date_str}")
        embed.add_field(name="\u200b", value=f"[View Commit on GitHub]({REPOSITORY_URL}/commit/{commit['sha']})",
                        inline=False)

        return embed
    except Exception as e:
        print(f"Failed to create commit embed: {e}")
        return None

async def check_commits_and_send_message(client):
    try:
        print("Fetching recent commits from GitHub...")
        commits = fetch_all_commits()
        print("Recent commits fetched.")

        if not commits:
            print("No commits found.")
            return

        print(f"Total commits fetched: {len(commits)}")

        # Reverse the order of commits to process them from oldest to newest
        commits.reverse()

        # Load previously sent commits
        sent_commits = load_commit_data()

        print(f"Total sent commits: {len(sent_commits)}")

        # Filter out already sent commits
        unsent_commits = [commit for commit in commits if commit['sha'] not in sent_commits]

        print(f"Total unsent commits: {len(unsent_commits)}")

        # Send messages for unsent commits
        for commit in unsent_commits:
            embed = create_commit_embed(commit)
            if embed:
                channel_id = 345345345353334543534 # Replace this with the actual channel ID
                channel = client.get_channel(channel_id)
                print(f"Sending message to channel: {channel_id}")
                await channel.send(embed=embed)
                print("Message sent successfully.")

        # Update the list of sent commits
        save_commit_data([commit['sha'] for commit in unsent_commits])
    except Exception as e:
        print(f"Failed to check commits and send message: {e}")

# Initialize the database
init_db()
