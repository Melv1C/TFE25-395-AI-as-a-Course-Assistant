def feedback_block(id: str, url: str) -> str:
    return f'''\n\n
.. raw:: html

    <div class="feedback">
        <div class="feedback-header">AI Course Assistant</div>
        <div class="feedback-content">
            <button id="feedbackButton_{id}" class="feedback-btn" onclick="getFeedback('{id}')" style="display: none;">
                Demander un feedback IA
            </button>

            <div id="feedbackContent_{id}" class="feedback-text"  style="display: none;"></div>
            
            <!-- Feedback Counter -->
            <div style="margin-top: 20px;">
                <div id="feedbackCounter_{id}" class="feedback-counter"></div>
                <div class="progress-bar-container">
                    <div id="progressBar_{id}" class="progress-bar"></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        function loadShowdown(callback) {{
            if (window.showdown) {{
                // Showdown is already loaded, execute the callback immediately
                callback();
            }} else {{
                // Dynamically load Showdown
                var script = document.createElement('script');
                script.src = "https://cdn.jsdelivr.net/npm/showdown@2.1.0/dist/showdown.min.js";
                script.onload = callback; // Run callback once the script is loaded
                document.body.appendChild(script);
            }}
        }}

        // Function to convert Markdown to HTML using Showdown
        function markdownToHTML(markdown) {{
            var converter = new showdown.Converter({{
                tables: true, 
                simplifiedAutoLink: true, 
                strikethrough: true, 
                tasklists: true 
            }});
            return converter.makeHtml(markdown);
        }}

        function getData(submissionId) {{
            fetch('{url}')
                .then(response => response.json())
                .then(data => {{
                    const feedbackButton = document.getElementById(`feedbackButton_${{submissionId}}`);
                    const feedbackContent = document.getElementById(`feedbackContent_${{submissionId}}`);
                    const feedbackCounter = document.getElementById(`feedbackCounter_${{submissionId}}`);
                    const feedbackCounterValue = document.getElementById(`feedbackCounterValue_${{submissionId}}`);
                    const progressBar = document.getElementById(`progressBar_${{submissionId}}`);

                    if (data.data.submission.feedback) {{
                        loadShowdown(() => {{
                            feedbackContent.innerHTML = markdownToHTML(data.data.submission.feedback.feedback);
                            feedbackContent.style.display = 'block';
                            feedbackButton.style.display = 'none';
                        }});
                    }} else {{
                        feedbackButton.style.display = 'block';
                        feedbackContent.style.display = 'none';
                    }}

                    // Show feedback count with a progress bar
                    const currentFeedbacks = data.data.current_nb_of_feedbacks;
                    const maxFeedbacks = data.data.max_nb_of_feedbacks;

                    feedbackCounter.innerHTML = `Feedbacks générés : <strong>${{currentFeedbacks}} / ${{maxFeedbacks}}</strong>`;
                    progressBar.style.width = `${{(currentFeedbacks / maxFeedbacks) * 100}}%`;

                    if (currentFeedbacks >= maxFeedbacks && feedbackButton.style.display !== 'none') {{
                        feedbackButton.style.display = 'none';
                        feedbackContent.style.display = 'block';
                        feedbackContent.innerHTML = '<div class="feedback-error">Vous avez atteint le nombre maximum de feedbacks générés.</div>';
                    }}
                    
                }})
                .catch((e) => {{
                    console.error(e); 
                    document.getElementById(`feedbackButton_${{submissionId}}`).style.display = 'block';
                    document.getElementById(`feedbackContent_${{submissionId}}`).style.display = 'none';
                }});
        }}

        function getFeedback(submissionId) {{
            const feedbackButton = document.getElementById(`feedbackButton_${{submissionId}}`);
            const feedbackContent = document.getElementById(`feedbackContent_${{submissionId}}`);

            feedbackButton.style.display = 'none';
            feedbackContent.style.display = 'block';
            feedbackContent.innerHTML = '<div class="loading-circle"></div>';

            fetch('{url}/feedback')
                .then(response => response.json())
                .then(data => {{
                    getData(submissionId);
                }})
                .catch(() => {{
                    feedbackContent.innerHTML = '<div class="feedback-error">Failed to load feedback.</div>';
                }});
        }}

        getData('{id}');
    </script>

    <style>
        .feedback {{
            font-family: Arial, sans-serif;
            background-color: #f1f0f0;
            color: #333;
            border-radius: 10px;
            overflow: hidden;
            width: fit-content;
            max-width: 100%;
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

        .feedback-content {{
            padding: 20px;
        }}

        .feedback-btn {{
            padding: 8px 12px;
            border-radius: 5px;
            border: none;
            background: linear-gradient(90deg, rgb(76, 27, 107) 0%, rgb(176, 132, 204) 58%, rgb(86, 221, 249) 100%);
            color: white;
            cursor: pointer;
        }}

        .feedback-btn:hover {{
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
            transform: scale(1.05);
            background: linear-gradient(90deg, rgb(86, 221, 249) 0%, rgb(176, 132, 204) 58%, rgb(76, 27, 107) 100%);
            transition: 0.3s;
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

        .feedback-counter {{
            margin-top: 10px;
            font-size: 14px;
            text-align: center;
        }}

        .progress-bar-container {{
            width: 100%;
            background-color: #ddd;
            border-radius: 5px;
            overflow: hidden;
            margin-top: 5px;
            height: 10px;
        }}

        .progress-bar {{
            height: 10px;
            background: rgb(76, 27, 107);
            width: 0%;
            transition: width 0.5s;
        }}

        .feedback-error {{
            color: red;
        }}
        
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
    </style>
    '''