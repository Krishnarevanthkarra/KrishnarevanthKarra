import requests
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
    response = requests.post(url, json={"query": QUERY, "variables": {"username": username}})
    response.raise_for_status()
    return response.json()["data"]["matchedUser"]

def difficulty_icon(diff):
    return {
        "Easy": "🟩",
        "Medium": "🟧", 
        "Hard": "🟥",
        "All": "📊"
    }.get(diff, "⚪")

def language_icon(lang):
    icons = {
        "C++": "https://raw.githubusercontent.com/devicons/devicon/master/icons/cplusplus/cplusplus-original.svg",
        "Python3": "https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg",
        "MySQL": "https://raw.githubusercontent.com/devicons/devicon/master/icons/mysql/mysql-original-wordmark.svg",
        "Pandas": "https://raw.githubusercontent.com/valohai/ml-logos/master/pandas.svg",
        "Java": "https://raw.githubusercontent.com/devicons/devicon/master/icons/java/java-original.svg",
        "JavaScript": "https://raw.githubusercontent.com/devicons/devicon/master/icons/javascript/javascript-original.svg"
    }
    return icons.get(lang, "")

def write_readme(data):
    profile = data["profile"]
    country = profile.get("countryName", "Unknown")
    country_flag = "🇮🇳" if country.lower() == "india" else "🌍"
    difficulties = {d["difficulty"]: d["count"] for d in data["submitStats"]["acSubmissionNum"]}
    languages = sorted(data["languageProblemCount"], key=lambda x: x["problemsSolved"], reverse=True)
    skill_tags = profile.get("skillTags", [])

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write("<!-- start -->\n\n")
        f.write(f"# <img src='https://leetcode.com/_next/static/images/logo-dark-c96c407d175e36c81e236fcfdd682a0b.png' width='40' height='40'> **LeetCode Profile**\n\n")
        
        # Profile Header with Avatar and Stats
        f.write(f"<div align='center'>\n")
        f.write(f"<img src='{profile['userAvatar']}' alt='Profile Picture' width='150' style='border-radius: 50%; border: 3px solid #ffa116;'>\n\n")
        f.write(f"<h1>👨‍💻 <strong>{profile['realName']}</strong></h1>\n")
        f.write(f"<h3>{country_flag} <strong>{country}</strong></h3>\n")
        
        # Skill Tags
        if skill_tags:
            f.write("\n<div style='display: flex; flex-wrap: wrap; gap: 8px; justify-content: center;'>\n")
            for tag in skill_tags:
                f.write(f"<span style='background: #ffa116; color: black; padding: 4px 8px; border-radius: 12px; font-weight: bold;'>{tag}</span>\n")
            f.write("</div>\n")
        f.write("</div>\n\n")

        # Difficulty Stats Cards
        f.write("## 🚀 **Problem Solving Stats**\n\n")
        f.write("<div style='display: flex; flex-wrap: wrap; gap: 16px; justify-content: center;'>\n")
        for level in ["All", "Easy", "Medium", "Hard"]:
            count = difficulties.get(level, 0)
            bg_color = {
                "All": "#2c3e50",
                "Easy": "#2ecc71",
                "Medium": "#f39c12",
                "Hard": "#e74c3c"
            }.get(level, "#3498db")
            
            f.write(f"""
<div style='background: {bg_color}; color: white; padding: 16px; border-radius: 8px; min-width: 120px; text-align: center;'>
    <div style='font-size: 24px; font-weight: bold;'>{difficulty_icon(level)} {count}</div>
    <div style='font-weight: bold;'>{level}</div>
</div>
""")
        f.write("</div>\n\n")

        # Languages Section
        f.write("## 💻 **Top Programming Languages**\n\n")
        f.write("<div style='display: flex; flex-wrap: wrap; gap: 20px; justify-content: center;'>\n")
        for lang in languages[:6]:  # Show top 6 languages
            icon = language_icon(lang["languageName"])
            if icon:
                f.write(f"""
<div style='text-align: center;'>
    <img src='{icon}' alt='{lang["languageName"]}' width='40' height='40'>
    <div style='font-weight: bold; margin-top: 8px;'>{lang["problemsSolved"]}</div>
    <div style='font-size: 0.9em;'>{lang["languageName"]}</div>
</div>
""")
        f.write("</div>\n\n")

        # Tags with Collapsible Sections
        def write_tag_section(title, tags, color):
            f.write(f"<details>\n<summary><b style='color: {color};'>📌 {title} Tags</b></summary>\n\n")
            f.write("<div style='display: flex; flex-wrap: wrap; gap: 8px;'>\n")
            for tag in sorted(tags, key=lambda x: x["problemsSolved"], reverse=True):
                f.write(f"<span style='background: {color}; color: white; padding: 4px 12px; border-radius: 12px; font-weight: bold;'>{tag['tagName']} <span style='background: white; color: {color}; border-radius: 50%; padding: 0 6px; margin-left: 4px;'>{tag['problemsSolved']}</span></span>\n")
            f.write("</div>\n</details>\n\n")

        f.write("## 🔖 **Problem Tags Breakdown**\n\n")
        write_tag_section("Fundamental", data["tagProblemCounts"]["fundamental"], "#3498db")
        write_tag_section("Intermediate", data["tagProblemCounts"]["intermediate"], "#9b59b6")
        write_tag_section("Advanced", data["tagProblemCounts"]["advanced"], "#e74c3c")

        # Last Updated
        f.write("---\n")
        f.write(f"<div align='right' style='font-size: 0.9em; color: #7f8c8d;'>\n")
        f.write(f"⏱ <strong>Last Updated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("</div>\n\n")
        f.write("<!-- end -->")

if __name__ == "__main__":
    try:
        leet_data = fetch_leetcode_data(USERNAME)
        write_readme(leet_data)
    except Exception as e:
        print("❌ Error:", e)
