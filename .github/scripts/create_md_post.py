import os
from datetime import datetime
import json

def create_md_with_frontmatter(filename, title, content, tags=None, author=None):
    now = datetime.now()
    date = now.strftime('%Y-%m-%d')
    time = now.strftime('%H:%M:%S')
    
    frontmatter = {
        'title': title,
        'date': date,
        'time': time,
        'tags': tags or [],
        'author': author or 'System',
    }
    
    content_with_frontmatter = f"""---
{json.dumps(frontmatter, indent=2)}
---

{content}
"""
    
    output_dir = os.path.join(os.path.dirname(__file__), '../../api/contents')
    os.makedirs(output_dir, exist_ok=True)
    
    with open(os.path.join(output_dir, filename), 'w') as f:
        f.write(content_with_frontmatter)

# This script is no longer in use.
# The functionality has been moved to the Flask app.
pass
