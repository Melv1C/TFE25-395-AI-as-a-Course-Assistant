def feedback_block(id: str, url: str) -> str:
    return f'''
.. raw:: html
    <div style="font-family: Arial, sans-serif; max-width: 500px; margin-top: 20px;">
        <button id="feedbackButton_{id}" class="feedback-btn" onclick="getFeedback_{id}()">Ask feedback from an AI</button>
        
        <div id="feedback_{id}" class="feedback-output" style="display: none;">
            <!-- Feedback content including header and message -->
            <div class="feedback-header">
                AI Course Assistant
            </div>
            
            <div id="feedbackContent_{id}" class="feedback-text"></div>
        </div>
    </div>

    <script>
        function getFeedback() {{
            const feedbackButton = document.getElementById('feedbackButton_{id}');
            const feedback = document.getElementById('feedback_{id}');
            const feedbackContent = document.getElementById('feedbackContent_{id}');
            
            // Hide button and show loading spinner
            feedbackButton.style.display = 'none';
            feedback.style.display = 'block'; // Show feedback block
            feedbackContent.innerHTML = '<div class="loading-circle"></div>';
            feedbackContent.style.display = 'block';

            fetch('{url}')
                .then(response => response.json())
                .then(data => {{
                    feedbackContent.innerHTML = data.data; // Show feedback message
                }})
                .catch(error => {{
                    console.error('Error:', error);
                    feedbackContent.innerHTML = '<div class="feedback-error">Failed to load feedback.</div>';
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
            @keyframes spin {{
                0% {{ transform: rotate(0deg); }}
                100% {{ transform: rotate(360deg); }}
            }}
        `;
        document.head.appendChild(style);
    </script>
    '''