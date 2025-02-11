def feedback_block(id: str, url: str) -> str:
    return f'''
.. raw:: html

    <div style="font-family: Arial, sans-serif; margin-top: 20px;">
        <button id="feedbackButton_{id}" class="feedback-btn" onclick="getFeedback('{id}')" style="display: none;">
            Demander un feedback AI
        </button>
        
        <div id="feedback_{id}" class="feedback-output" style="display: none;">
            <div class="feedback-header">AI Course Assistant</div>
            <div id="feedbackContent_{id}" class="feedback-text"></div>
        </div>
    </div>

    <script>
        function markdownToHTML(markdown) {{
            return markdown
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
                .replace(/\*(.*?)\*/g, "<em>$1</em>")
                .replace(/```([\s\S]*?)```/g, "<pre><code>$1</code></pre>")
                .replace(/`(.*?)`/g, "<code>$1</code>")
                .replace(/^- (.*)$/gm, "<li>$1</li>")
                .replace(/(<li>.*<\/li>(?:\n<li>.*<\/li>)*)/g, "<ul>$1</ul>")
                .replace(/\n(?!<\/?(ul|ol|li)>)/g, "<br>");
        }}

        function getData(submissionId) {{
            fetch('{url}')
                .then(response => response.ok ? response.json() : Promise.reject('Not found'))
                .then(data => {{
                    if (data.data.submission.feedback) {{
                        document.getElementById(`feedbackButton_${{submissionId}}`).style.display = 'none';
                        document.getElementById(`feedback_${{submissionId}}`).style.display = 'block';
                        document.getElementById(`feedbackContent_${{submissionId}}`).innerHTML = markdownToHTML(data.submission.feedback);
                        return;
                    }}
                    document.getElementById(`feedbackButton_${{submissionId}}`).style.display = 'block';
                }})
                .catch(() => {{
                    document.getElementById(`feedbackButton_${{submissionId}}`).style.display = 'block';
                }});
        }}

        function getFeedback(submissionId) {{
            const feedbackButton = document.getElementById(`feedbackButton_${{submissionId}}`);
            const feedback = document.getElementById(`feedback_${{submissionId}}`);
            const feedbackContent = document.getElementById(`feedbackContent_${{submissionId}}`);

            feedbackButton.style.display = 'none';
            feedback.style.display = 'block';
            feedbackContent.innerHTML = '<div class="loading-circle"></div>';

            fetch('{url}/get_feedback')
                .then(response => response.json())
                .then(data => {{
                    feedbackContent.innerHTML = markdownToHTML(data.data);
                }})
                .catch(() => {{
                    feedbackContent.innerHTML = '<div class="feedback-error">Failed to load feedback.</div>';
                }});
        }}

        getData('{id}');
    </script>
    '''