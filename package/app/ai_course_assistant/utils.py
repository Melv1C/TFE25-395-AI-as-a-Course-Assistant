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
    """ Generate an HTML block with a styled button to get AI feedback asynchronously """
    return f'''
.. raw:: html
    
        <div style="font-family: Arial, sans-serif; max-width: 300px; margin-top: 20px;">
            <h4>Do you need further explanation?</h4>
            <button class="btn btn-primary" style="padding: 8px 12px; border-radius: 5px; border: none; background-color: #007bff; color: white; cursor: pointer;" onclick="getFeedback()">Ask feedback from an AI</button>
            <div id="feedback" style="margin-top: 15px; font-size: 14px;"></div>
        </div>

        <script>
            function getFeedback() {{
                document.getElementById('feedback').innerHTML = '<div class="loading-circle" style="display: inline-block; width: 24px; height: 24px; border: 3px solid #007bff; border-top: 3px solid transparent; border-radius: 50%; animation: spin 1s linear infinite;"></div>';
                
                fetch('{url}/getFeedbackAsync/{id}')
                    .then(response => response.json())
                    .then(data => {{
                        console.log(data);
                        document.getElementById('feedback').innerHTML = '<div style="display: inline-block; background-color: #f1f0f0; color: #333; padding: 10px; border-radius: 10px; max-width: 90%; margin-top: 10px; font-size: 14px;">' + data.data + '</div>';
                    }})
                    .catch(error => {{
                        console.error('Error:', error);
                        document.getElementById('feedback').innerHTML = '<div style="color: red;">Failed to load feedback. Please try again.</div>';
                    }});
            }}

            // CSS for the loading spinner
            const style = document.createElement('style');
            style.innerHTML = `
                @keyframes spin {{
                    0% {{ transform: rotate(0deg); }}
                    100% {{ transform: rotate(360deg); }}
                }}
            `;
            document.head.appendChild(style);
        </script>
    '''


