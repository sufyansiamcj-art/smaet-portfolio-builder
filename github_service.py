import requests

def get_github_repos(username):
    # رابط API لجلب المستودعات العامة للمستخدم
    url = f"https://api.github.com/users/{username}/repos?sort=updated"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            repos = response.json()
            project_list = []
            for repo in repos:
                # نأخذ فقط المستودعات التي ليست "Fork" (أي التي أنشأها المستخدم بنفسه)
                if not repo['fork']:
                    project_list.append({
                        'name': repo['name'],
                        'description': repo['description'] or "لا يوجد وصف متاح لهذا المشروع حالياً.",
                        'language': repo['language'] or "البرمجية",
                        'url': repo['html_url'],
                        'stars': repo['stargazers_count'],
                        'updated': repo['updated_at'][:10] # تاريخ آخر تحديث
                    })
            return project_list
        else:
            return None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None