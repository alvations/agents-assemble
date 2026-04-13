from setuptools import setup, find_packages

setup(
    name="agents-assemble",
    version="0.1.0",
    description="Trading agents with backtesting and persona-based strategies",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.21.0",
        "yfinance>=0.2.0",
        "requests>=2.25.0",
    ],
    extras_require={
        "dev": ["pytest", "pytest-cov", "pytest-mock", "flask"],
        "test": ["pytest", "pytest-cov", "pytest-mock", "flask"],
    },
    entry_points={
        "console_scripts": [
            "agents-assemble=run_hypotheses:main",
        ],
    },
)
