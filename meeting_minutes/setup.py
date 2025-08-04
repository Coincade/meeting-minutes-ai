from setuptools import setup, find_packages

setup(
    name="meeting_minutes",
    version="0.1.0",
    description="Meeting minutes generation using CrewAI",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "crewai[tools]>=0.148.0,<1.0.0",
        "streamlit>=1.47.0",
        "openai>=1.97.0",
        "python-dotenv>=1.1.0",
        "pydub>=0.25.0",
        "google-api-python-client>=2.177.0",
        "google-auth-oauthlib>=1.2.2",
        "google-auth-httplib2>=0.2.0",
    ],
    python_requires=">=3.10",
) 