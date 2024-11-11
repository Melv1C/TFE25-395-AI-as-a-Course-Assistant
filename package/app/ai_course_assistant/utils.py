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
    """Generate an HTML block with AI feedback, a gradient header, and a thumbs up/down feedback system."""
    return f'''
.. raw:: html

    <div style="font-family: Arial, sans-serif; max-width: 500px; margin-top: 20px;">
        <button id="feedbackButton" class="feedback-btn" onclick="getFeedback('{id}')">Ask feedback from an AI</button>
        
        <div id="feedback" class="feedback-output" style="display: none;">
            <!-- Feedback content including header and message -->
            <div id="feedbackHeader" class="feedback-header">
                AI Course Assistant
            </div>
            
            <div id="feedbackContent" class="feedback-text"></div>
        </div>
        
        <div id="feedbackRating" class="feedback-rating" style="display: none; align-items: center; justify-content: center; margin-top: 10px;">
            <div>Was the feedback useful?</div>
            <button onclick="sendFeedbackRating('{id}', true)" class="thumb-up">👍</button>
            <button onclick="sendFeedbackRating('{id}', false)" class="thumb-down">👎</button>
            <div id="ratingResponse" style="margin-top: 5px; font-size: 14px;"></div>
        </div>
    </div>

    <script>
        function getFeedback(id) {{
            const feedbackButton = document.getElementById('feedbackButton');
            const feedback = document.getElementById('feedback');
            const feedbackContent = document.getElementById('feedbackContent');
            const feedbackRating = document.getElementById('feedbackRating');
            
            // Hide button and show loading spinner
            feedbackButton.style.display = 'none';
            feedback.style.display = 'block'; // Show feedback block
            feedbackContent.innerHTML = '<div class="loading-circle"></div>';
            feedbackContent.style.display = 'block';

            fetch('{url}/getFeedbackAsync/' + encodeURIComponent(id))
                .then(response => response.json())
                .then(data => {{
                    feedbackContent.innerHTML = data.data; // Show feedback message
                    feedbackRating.style.display = 'flex'; // Show thumbs up/down buttons
                }})
                .catch(error => {{
                    console.error('Error:', error);
                    feedbackContent.innerHTML = '<div class="feedback-error">Failed to load feedback.</div>';
                    //feedbackButton.style.display = 'flex';
                }});
        }}

        function sendFeedbackRating(id, isUseful) {{
            fetch('{url}/getFeedbackAsync/' + encodeURIComponent(id), {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json'
                }},
                body: JSON.stringify({{ useful: isUseful }})
            }})
            .then(response => response.json())
            .then(data => {{
                document.getElementById('ratingResponse').innerHTML = 'Thank you for your feedback!';
                document.getElementById('feedbackRating').style.display = 'none';
            }})
            .catch(error => {{
                console.error('Error:', error);
                document.getElementById('ratingResponse').innerHTML = '<div style="color: red;">Error submitting feedback. Please try again.</div>';
            }});
        }}

        // CSS styles for components
        const style = document.createElement('style');
        style.innerHTML = `
            .feedback-btn {{
                padding: 8px 12px;
                border-radius: 5px;
                border: none;
                background: linear-gradient(90deg, rgb(76, 27, 107) 0%, rgb(176, 132, 204) 58%, rgb(86, 221, 249) 100%);
                color: white;
                cursor: pointer;
            }}
            .loading-circle {{
                display: inline-block;
                width: 24px;
                height: 24px;
                border: 3px solid #4c1b6b;
                border-top: 3px solid transparent;
                border-radius: 50%;
                animation: spin 1s linear infinite;
            }}
            .feedback-output {{
                font-size: 14px;
                background-color: #f1f0f0;
                color: #333;
                border-radius: 10px;
                overflow: hidden;
            }}
            .feedback-text {{
                padding: 10px;
            }}
            .feedback-header {{
                display: block;
                padding: 10px;
                color: white;
                font-size: 18px;
                font-weight: bold;
                text-align: center;
                background: linear-gradient(90deg, rgb(76, 27, 107) 0%, rgb(176, 132, 204) 58%, rgb(86, 221, 249) 100%);
            }}
            .feedback-error {{
                color: red;
            }}
            .thumb-up, .thumb-down {{
                font-size: 20px;
                background: none;
                border: none;
                cursor: pointer;
                margin: 0 5px;
            }}
            @keyframes spin {{
                0% {{ transform: rotate(0deg); }}
                100% {{ transform: rotate(360deg); }}
            }}
        `;
        document.head.appendChild(style);
    </script>
    '''
