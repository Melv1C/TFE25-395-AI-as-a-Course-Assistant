# Inherit from the default container, which have all the needed script to launch tasks
FROM    ingi/inginious-c-base

# Set the environment name for tasks
LABEL   org.inginious.grading.name="ai_course_assistant"

# install the needed packages
RUN     pip3.8 install -i https://test.pypi.org/simple/ ai-course-assistant==1.5.0

