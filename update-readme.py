import time
import re

# LeetCode stats Render link (base URL)
base_url = "https://leetcode-stats-9k4x.onrender.com/leetcode-stats/Krishna_Revanth_Karra"

# Read the current README.md
with open("README.md", "r") as file:
    content = file.read()

# Generate timestamp just before updating
timestamp = int(time.time())  # Fresh timestamp
cache_bust_url = f"{base_url}?cache_bust={timestamp}"
new_content = f"![LeetCode Stats]({cache_bust_url})"

# Define start and end tags
start_tag = "<!-- LEETCODE_STATS_START -->"
end_tag = "<!-- LEETCODE_STATS_END -->"

# Replace content between start and end tags
pattern = f"{start_tag}.*?{end_tag}"
updated_content = re.sub(pattern, f"{start_tag}\n{new_content}\n{end_tag}", content, flags=re.DOTALL)

# Write the updated content back to README.md
with open("README.md", "w") as file:
    file.write(updated_content)

print("README.md updated with fresh LeetCode stats link.")
