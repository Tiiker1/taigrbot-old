import discord
import requests
from datetime import datetime

# GitHub repository information
GITHUB_USERNAME = 'your github user name here'
REPOSITORY_NAME = 'your github repo name here'
REPOSITORY_URL = f'https://github.com/{GITHUB_USERNAME}/{REPOSITORY_NAME}'

# Function to fetch recent commits from GitHub
def fetch_recent_commits():
    try:
        response = requests.get(f'https://api.github.com/repos/{GITHUB_USERNAME}/{REPOSITORY_NAME}/commits')
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except Exception as e:
        print(f"Failed to fetch commits: {e}")
        return []

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
        commits = fetch_recent_commits()

        # Check if the commits list is empty
        if not commits:
            print("No commits found.")
            return

        # Get the latest commit
        latest_commit_sha = commits[0]['sha']

        # Check if the latest commit is different from the previous one
        if latest_commit_sha != check_commits_and_send_message.latest_commit:
            check_commits_and_send_message.latest_commit = latest_commit_sha

            # Get the latest commit details
            latest_commit = commits[0]

            # Create an embed message for the latest commit
            embed = create_commit_embed(latest_commit)

            # Post the embed message to the specified Discord channel
            channel_id = putyourchannelid here where bot sends messages  # Replace this with the actual channel ID
            channel = bot.get_channel(channel_id)
            await channel.send(embed=embed)
    except Exception as e:
        print(f"Failed to check commits and send message: {e}")

# Initialize the latest commit variable
check_commits_and_send_message.latest_commit = ''
