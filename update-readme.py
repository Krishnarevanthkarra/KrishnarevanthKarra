import requests

username = "Krishna_Revanth_Karra"  # Replace this

query = """
{
  matchedUser(username: "%s") {
    submitStats {
      acSubmissionNum {
        difficulty
        count
      }
    }
    languageProblemCount{
      languageName
      problemsSolved
    }
  }
}
""" % username

response = requests.post(
    "https://leetcode.com/graphql",
    json={"query": query}
)

data = response.json()
stats = {item["difficulty"]: item["count"] for item in data["data"]["matchedUser"]["submitStats"]["acSubmissionNum"]}
langUsed = {item["languageName"] : item["problemsSolved"] for item in data["data"]["matchedUser"]["submitStats"]["languageProblemCount"]}

# Update README
with open("README.md", "r") as file:
    content = file.read()

start_tag = "<!-- LEETCODE_STATS_START -->"
end_tag = "<!-- LEETCODE_STATS_END -->"

new_stats = f"""{start_tag}
🟢 Easy: {stats['Easy']}
🟡 Medium: {stats['Medium']}
🔴 Hard: {stats['Hard']}
\n<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/cplusplus/cplusplus-original.svg" alt="C++" width="40" height="40"/> : {langUsed["C++"]}
\n<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="Python" width="40" height="40"/> : {langUsed["Python3"]}
{end_tag}"""

# Replace old stats
import re
updated_content = re.sub(f"{start_tag}.*?{end_tag}", new_stats, content, flags=re.DOTALL)

with open("README.md", "w") as file:
    file.write(updated_content)
