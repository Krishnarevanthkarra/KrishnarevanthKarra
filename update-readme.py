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
      ranking
      reputation
      starRating
      countryName
      skillTags
      aboutMe
      company
      school
    }
    submitStats {
      acSubmissionNum {
        difficulty
        count
        submissions
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
    problemsSolvedBeatsStats {
      difficulty
      percentage
    }
    contestBadge {
      name
      expired
      hoverText
      icon
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
        "Easy": "<span style='color:#00B8A3'>Easy</span>",
        "Medium": "<span style='color:#FFC01E'>Medium</span>", 
        "Hard": "<span style='color:#FF375F'>Hard</span>"
    }.get(diff, diff)

def language_icon(lang):
    icons = {
        "C++": "<img src='https://cdn.jsdelivr.net/gh/devicons/devicon/icons/cplusplus/cplusplus-original.svg' width='20'/>",
        "Python3": "<img src='https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg' width='20'/>",
        "MySQL": "<img src='https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mysql/mysql-original-wordmark.svg' width='20'/>",
        "Java": "<img src='https://cdn.jsdelivr.net/gh/devicons/devicon/icons/java/java-original.svg' width='20'/>",
        "JavaScript": "<img src='https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg' width='20'/>"
    }
    return icons.get(lang, "")

def generate_progress_bar(percentage, color):
    return f"""
    <div style="width:100%; background:#e5e5e5; border-radius:4px; margin-top:4px;">
        <div style="width:{percentage}%; background:{color}; height:6px; border-radius:4px;"></div>
    </div>
    <div style="text-align:right; margin-top:-18px; margin-bottom:8px;">
        <small><strong>{percentage}%</strong></small>
    </div>
    """

def write_readme(data):
    profile = data["profile"]
    difficulties = {d["difficulty"]: d for d in data["submitStats"]["acSubmissionNum"]}
    languages = sorted(data["languageProblemCount"], key=lambda x: x["problemsSolved"], reverse=True)
    
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write("<!-- start -->\n\n")
        
        # LeetCode-style Header
        f.write(f"""
<div align="center">
  <img src="https://assets.leetcode.com/static_assets/public/webpack_bundles/images/logo-dark.e99485d9b.svg" width="300"/>
</div>

<div style="display:flex; justify-content:space-between; align-items:center; margin:20px 0;">
  <div style="display:flex; align-items:center; gap:20px;">
    <img src="{profile['userAvatar']}" width="80" style="border-radius:50%; border:2px solid #ffa116"/>
    <div>
      <h1>{profile['realName']}</h1>
      <div style="display:flex; gap:10px; align-items:center;">
        <span style="background:#ffa116; color:black; padding:2px 8px; border-radius:4px; font-weight:bold;">{profile['ranking']}</span>
        <span>🏆 {profile['reputation']} Reputation</span>
      </div>
    </div>
  </div>
  <div style="text-align:right;">
    <div>📍 {profile['countryName']}</div>
    <div>🏫 {profile.get('school', 'Not specified')}</div>
    <div>💼 {profile.get('company', 'Not specified')}</div>
  </div>
</div>
""")

        # Problems Solved Section
        f.write("""
## 🏆 Problems Solved
<div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:16px; margin:20px 0;">
""")
        
        for level in ["All", "Easy", "Medium", "Hard"]:
            diff = difficulties.get(level)
            if not diff: continue
            
            bg_color = {
                "All": "#2c3e50",
                "Easy": "#00B8A3",
                "Medium": "#FFC01E",
                "Hard": "#FF375F"
            }.get(level, "#3498db")
            
            f.write(f"""
<div style="background:white; border-radius:8px; padding:16px; box-shadow:0 2px 8px rgba(0,0,0,0.1);">
  <div style="color:{bg_color}; font-weight:bold; font-size:1.2rem;">{diff['count']}</div>
  <div style="color:#666;">{level}</div>
  {generate_progress_bar(round((diff['count']/difficulties['All']['count'])*100) if level != 'All' else ''}
</div>
""")
        f.write("</div>\n")

        # Languages Section
        f.write("""
## 💻 Languages
<div style="display:grid; grid-template-columns:repeat(auto-fill, minmax(120px, 1fr)); gap:16px; margin:20px 0;">
""")
        for lang in languages[:6]:
            f.write(f"""
<div style="background:white; border-radius:8px; padding:12px; box-shadow:0 2px 8px rgba(0,0,0,0.1); text-align:center;">
  {language_icon(lang['languageName'])}
  <div style="font-weight:bold; margin-top:8px;">{lang['problemsSolved']}</div>
  <div style="color:#666; font-size:0.9rem;">{lang['languageName']}</div>
</div>
""")
        f.write("</div>\n")

        # Skills Section
        if profile.get('skillTags'):
            f.write("""
## 🛠 Skills
<div style="display:flex; flex-wrap:wrap; gap:8px; margin:20px 0;">
""")
            for skill in profile['skillTags']:
                f.write(f"""<span style="background:#e5e5e5; padding:4px 12px; border-radius:12px; font-size:0.9rem;">{skill}</span>""")
            f.write("</div>\n")

        # Tags Section
        f.write("""
## 📌 Problem Tags
<div style="margin:20px 0;">
""")
        
        def write_tag_category(title, tags, color):
            f.write(f"""
<details>
<summary style="font-weight:bold; color:{color}; cursor:pointer; margin:10px 0;">▼ {title}</summary>
<div style="display:flex; flex-wrap:wrap; gap:8px; margin:10px 0;">
""")
            for tag in sorted(tags, key=lambda x: x['problemsSolved'], reverse=True)[:15]:
                f.write(f"""<span style="background:{color}; color:white; padding:4px 12px; border-radius:12px; font-size:0.9rem;">{tag['tagName']} <span style="background:white; color:{color}; border-radius:50%; padding:0 6px; margin-left:4px;">{tag['problemsSolved']}</span></span>""")
            f.write("</div></details>\n")
        
        write_tag_category("Fundamental", data["tagProblemCounts"]["fundamental"], "#3498db")
        write_tag_category("Intermediate", data["tagProblemCounts"]["intermediate"], "#9b59b6")
        write_tag_category("Advanced", data["tagProblemCounts"]["advanced"], "#e74c3c")
        
        f.write("</div>\n")

        # Footer
        f.write(f"""
<div style="text-align:right; color:#999; font-size:0.8rem; margin-top:40px;">
  Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
</div>
""")
        f.write("\n<!-- end -->")

if __name__ == "__main__":
    try:
        leet_data = fetch_leetcode_data(USERNAME)
        write_readme(leet_data)
        print("✅ README.md updated successfully with LeetCode profile!")
    except Exception as e:
        print(f"❌ Error updating README: {str(e)}")
