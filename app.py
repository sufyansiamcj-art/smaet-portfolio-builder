import os
from flask import Flask, render_template, request, send_file
from github_service import get_github_repos
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    projects = []
    username = ""
    error_msg = None
    
    if request.method == 'POST':
        username = request.form.get('github_username')
        if username:
            projects = get_github_repos(username)
            if projects is None:
                error_msg = "تعذر العثور على المستخدم أو حدث خطأ في الاتصال."
                
    return render_template('index.html', projects=projects, username=username, error_msg=error_msg)

@app.route('/export', methods=['POST'])
def export_portfolio():
    username = request.form.get('username')
    projects = get_github_repos(username)
    
    # تحويل قالب المحفظة إلى نص HTML
    rendered_html = render_template('portfolio_template.html', projects=projects, username=username)
    
    # إرسال النص كملف قابل للتحميل
    return send_file(
        io.BytesIO(rendered_html.encode('utf-8')),
        mimetype='text/html',
        as_attachment=True,
        download_name=f'{username}_portfolio.html'
    )

if __name__ == '__main__':
    # هام جداً للنشر: تحديد المنفذ تلقائياً
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)