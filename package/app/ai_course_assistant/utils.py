import re

def get_codeblock(language, text):
    """ Generates rst codeblock for given text and language """
    rst = "\n\n.. code-block:: " + language + "\n\n"
    for line in text.splitlines():
        rst += "\t" + line + "\n"

    rst += "\n"
    return rst

def get_admonition(cssclass, title, text):
    """ Generates rst admonition block given a bootstrap alert css class, title, and text"""
    if cssclass not in ["info", "danger", "warning", "success"]:
        cssclass = "info"

    rst = "\n\n.. admonition:: " + cssclass + "\n"
    rst += "\t:title: " + title + "\n\n"

    for line in text.splitlines():
        rst += "\t" + line + "\n"

    rst += "\n"
    return rst


def toRST(text):
    """ Convert Markdown text to reStructuredText """

    # Convert Markdown code blocks to reStructuredText code blocks
    text = re.sub(r'```(\w+)?\n(.*?)```', lambda m: get_codeblock(m.group(1) or '', m.group(2)), text, flags=re.DOTALL)

    return text

def AIFeedbackBlock(feedback):
    """ Generate an admonition block with AI feedback """
    return get_admonition("info", "AI Feedback", toRST(feedback))


def AsyncFeedbackBlock(url, id):
    """ Generate an HTML block with a button to get AI feedback asynchronously """
    return f'''
.. raw:: html
    
        <div>
            <h4>AI Feedback</h4>
            <button class="btn btn-primary" onclick="getFeedback()">Get Feedback</button>
            <div id="feedback"></div>
        </div>

        <script>
            function getFeedback() {{
                fetch('{url}/getFeedbackAsync/{id}')
                    .then(response => response.json())
                    .then(data => {{
                        document.getElementById('feedback').innerHTML = data.feedback;
                    }})
                    .catch(error => {{
                        console.error('Error:', error);
                    }});
            }}
'''

