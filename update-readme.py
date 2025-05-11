import requests
import json
from datetime import datetime

USERNAME = "Krishna_Revanth_Karra"
README_PATH = "README.md"

QUERY = """
query getUserProfile($username: String!) {
  matchedUser(username: $username) {
    username
    profile {
      realName
      userAvatar
      ranking
      reputation
      starRating
      aboutMe
      countryName
      skillTags
    }
    submitStats {
      acSubmissionNum {
        difficulty
        count
      }
    }
    languageProblemCount {
      languageName
      problemsSolved
    }
    problemsSolvedBeatsStats {
      difficulty
      percentage
    }
    tagProblemCounts {
      fundamental { tagName problemsSolved }
      intermediate { tagName problemsSolved }
      advanced { tagName problemsSolved }
    }
  }
}
"""

def fetch_leetcode_data(username):
    url = "https://leetcode.com/graphql"
    response = requests.post(url, json={
        "query": QUERY,
        "variables": {"username": username}
    })
    response.raise_for_status()
    return response.json()["data"]["matchedUser"]

def difficulty_color(difficulty):
    return {
        "Easy": "🟢",
        "Medium": "🟡",
        "Hard": "🔴"
    }.get(difficulty, "⚪")

def language_icon(language):
    icons = {
        "C++": "https://raw.githubusercontent.com/devicons/devicon/master/icons/cplusplus/cplusplus-original.svg",
        "Python3": "https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg",
        "MySQL": "https://raw.githubusercontent.com/devicons/devicon/master/icons/mysql/mysql-original.svg",
        "Pandas": "https://raw.githubusercontent.com/valohai/ml-logos/master/pandas.svg"
    }
    return icons.get(language, "")

def write_readme(data):
    profile = data["profile"]
    difficulties = {d["difficulty"]: d["count"] for d in data["submitStats"]["acSubmissionNum"]}
    languages = data["languageProblemCount"]

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(f"# 👋 Hello, I'm {profile['realName']}\n\n")
        f.write(f"![Avatar]({profile['userAvatar']})\n\n")

        # Country with flag
        country = profile.get("countryName", "Unknown")
        flag = "🇮🇳" if country.lower() == "india" else ""
        f.write(f"**Country:** {flag} {country}\n\n")

        # Difficulty count with color
        f.write("## 🧠 Problems Solved\n")
        for level in ["Easy", "Medium", "Hard"]:
            f.write(f"- {difficulty_color(level)} **{level}**: {difficulties.get(level, 0)}\n")
        f.write(f"- ⚪ **All**: {difficulties.get('All', 0)}\n\n")

        # Language stats
        f.write("## 💻 Language Stats\n")
        for lang in languages:
            icon = language_icon(lang["languageName"])
            icon_tag = f'<img src="{icon}" alt="{lang["languageName"]}" width="30"/> ' if icon else ""
            f.write(f"{icon_tag}**{lang['languageName']}** — {lang['problemsSolved']} problems solved  \n")
        f.write("\n")

        # Tags
        def write_tags(tag_list, label):
            f.write(f"<details>\n<summary><b>{label} Tags</b></summary>\n\n")
            for tag in tag_list:
                f.write(f"- 🔹 **{tag['tagName']}**: {tag['problemsSolved']}\n")
            f.write("</details>\n\n")

        f.write("## 🏷️ Tags Overview\n")
        write_tags(data["tagProblemCounts"]["fundamental"], "Fundamental")
        write_tags(data["tagProblemCounts"]["intermediate"], "Intermediate")
        write_tags(data["tagProblemCounts"]["advanced"], "Advanced")

        f.write(f"---\n⏱ Updated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    try:
        data = fetch_leetcode_data(USERNAME)
        write_readme(data)
    except Exception as e:
        print("❌ Error:", e)
