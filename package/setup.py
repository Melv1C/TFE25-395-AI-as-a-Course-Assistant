from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='ai_course_assistant',
    version='1.1.1',
    description='A course assistant that provides feedback on student answers using a chatbot.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Claes Melvyn',
    author_email="melvyn.claes@student.uclouvain.be",
    package_dir={'': 'app'},
    packages=find_packages(where='app'),
    install_requires=[
        'requests'
    ],
    extras_require={
        'dev': [
            'pytest',
            'twine'
        ]
    },
    python_requires='>=3.6',
    license='MIT',

)
