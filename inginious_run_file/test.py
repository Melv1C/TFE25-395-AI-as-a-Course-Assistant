#! /usr/bin/python3
# -*- coding: utf-8 -*-

import subprocess
import gettext
import shlex
import sys
import os
import re
import yaml
from ai_course_assistant import AICourseAssistant, AsyncFeedbackBlock

from inginious_container_api import feedback, rst, input

URL = "http://tfe-claes.info.ucl.ac.be:8080"

# This runner suits for typical exercises of LSINF1101/FSAB1401
# Should be adapted if used in another occasion
# Structure used:
#  -One folder : src with a proposer answer, the tests and a subdirectory containing the templates
#  -A run file
#  -A task file
# Note that beside this structure we use the global folder common (c) and common/student (cs) containing:
#  -The compiler script         (c)
#  -The tests runner script     (c)
#  -The translations folder     (cs)

def init_translations():
    """
        Move the translations files to student directory
        Initialize gettext and translate to the proper language
    """
    lang = input.get_lang()
    try:
        trad = gettext.GNUTranslations(open("../course/common/student/$i18n/" + lang + ".mo", "rb"))
    except FileNotFoundError:
        trad = gettext.NullTranslations()
    trad.install()
    return lang


def compute_code():
    """
        Fills the template file with the student answer
        Returns the task's number of questions
    """
    for file in os.listdir('./src/Templates'):
        input.parse_template('./src/Templates/' + file, './student/' + file + '.py')
    data = input._load_input()
    return len([k for k in data['input'].keys() if '@' not in k])


def compile_code():
    """
        Compiles both the student code and the exercise code
        Provides feedback if there is any compilation error
    """
    pyc_cmd = "python3 ./compiler.py "

    with open('log.out', 'w+', encoding="utf-8") as f:
        subprocess.call(shlex.split(pyc_cmd + './student/'), universal_newlines=True, stderr=f)
        f.seek(0)
        out_student = f.read()

    if out_student != "":
        rawhtml = rst.get_codeblock("", out_student)
        feedback.set_global_result('failed')
        feedback.set_global_feedback(_("Your program does not compile: \n ") + rawhtml + "\n")
        get_AI_feedback()
        sys.exit(0)

    with open('logTests.out', 'w+', encoding="utf-8") as f:
        subprocess.call(shlex.split(pyc_cmd + './src/'), universal_newlines=True, stderr=f)
        f.seek(0)
        out_tests = f.read()

    if out_tests != "":
        rawhtml = rst.get_codeblock("", out_tests)
        feedback.set_global_result('failed')
        feedback.set_global_feedback(_("The program does not compile for external reasons,"
                                       "please contact an administrator asap: \n ") + rawhtml + "\n")
        sys.exit(0)

    with open('logRunner.out', 'w+', encoding="utf-8") as f:
        subprocess.call(shlex.split(pyc_cmd + '../course/common/'), universal_newlines=True, stderr=f)
        f.seek(0)
        out_runner = f.read()

    if out_runner != "":
        rawhtml = rst.get_codeblock("", out_runner)
        feedback.set_global_result('failed')
        feedback.set_global_feedback(_("The program does not compile for external reasons,"
                                       "please contact an administrator asap: \n ") + rawhtml + "\n")
        sys.exit(0)


def cleanup_output(error_content):
    """
        Provides a cleaner output from the error trace

        :param error_content: string returned by the unittest failures
    """
    cleaned_lines = []
    indexes = [match.start() for match in re.finditer('AssertionError: ', error_content)]
    for i in indexes:
        cleaned_lines.append(_('Failed test:\n'))
        cleaned_lines.append(error_content[i + len("AssertionError: "): error_content.find("=" * 70, i)])
    return ''.join(cleaned_lines) if len(indexes) > 0 else error_content


def run_code(n_exercises, lang):
    """
        Runs the student code with the tests
        Provides feedback if it contains errors

        :param n_exercises: the task's number of exercices
        :param lang: the language used by the user
    """
    with open('err.txt', 'w+', encoding="utf-8") as f:
        os.chdir('./student')
        py_cmd = "run_student python3 Runner.pyc " + lang
        try:
            resproc = subprocess.Popen(shlex.split(py_cmd), universal_newlines=True, stderr=f, stdout=subprocess.PIPE)
            resproc.communicate()
            result = resproc.returncode
        except (IOError, BrokenPipeError):
            result = 252
        f.flush()
        f.seek(0)
        errors = f.read()
        print(errors)
        outerr = rst.get_codeblock("python", cleanup_output(errors))

    # expected error code: 252=outofmemory, 253=timedout
    # 127 = code returned by our runner
    if result == 127:
        feedback.set_global_result('success')
    elif result == 252:
        feedback.set_global_result('overflow')
    elif result == 253:
        feedback.set_global_result('timeout')
    else:  # Tests failed
        if n_exercises == 1:
            feedback.set_global_result('failed')
            feedback.set_global_feedback(_("It seems that you have made mistakes in your code…\n\n") + outerr + "\n")
        else:
            for i in range(0, n_exercises + 1):
                regex = '@' + str(i) + '@: ((.+)(\n|\r){1})+'
                regex_question = re.search(regex, errors)
                if regex_question:
                    outerr_question = re.sub('"', '', regex_question.group(0)[5:])
                else:
                    outerr_question = False

                if i == 0:
                    feedback.set_global_result('failed')
                    if outerr_question:
                        feed = _("You have made mistakes: \n\n") + rst.get_codeblock("python", outerr_question) + "\n"
                        feedback.set_global_feedback(feed)
                else:
                    if outerr_question:
                        feed = _("You have made mistakes: \n\n") + rst.get_codeblock("python", outerr_question) + "\n"
                        feedback.set_problem_feedback(feed, "q" + str(i))
                    else:
                        feedback.set_problem_feedback(_("You answered well this question"), "q" + str(i))
                        feedback.set_problem_result('success', "q" + str(i))

        get_AI_feedback()

def get_AI_feedback():

    with open("task.yaml", "r") as f:
            task = yaml.safe_load(f)
            print(task)
        
    context = task["context"]
    question = task["problems"]["q1"]["header"]
    input_student = input.get_input("q1")
    AICourseAssistant.init(URL)
    assistant = AICourseAssistant(context + "\n\n" + question, input_student)
    res = assistant.getFeedbackAsync()
    if res.success:
        feedback.set_global_feedback(AsyncFeedbackBlock(URL, res.id), True)
    else:
        print("Error:", res.message)
        feedback.set_global_feedback("An error occurred while asking for an AI feedback.", True)


if __name__ == '__main__':
    language = init_translations()
    num_exercises = compute_code()
    compile_code()
    run_code(num_exercises, language)
