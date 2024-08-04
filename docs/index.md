# Welcome to the Blockchain Based Voting System

This is a simple Voting System built in Vyper programming language for building a blockchain backend side.

Used base components are:

    * Vyper
    * APE
    * Web3.py
    * Ruff
    * Pytest

Detail about using technologies for this project:

    * Vyper => Is a python based programming language for building a smart contract based applications
    * APE => Web3 development tool. Users can compile, test, and interact with smart contracts all in one command line session
    * Web3.py => A Python library for interacting with Ethereum
    * Ruff => Is a fast and powerful Python linter and code formatter
    * Pytest => Is a powerful and popular testing framework for Python. It is a widely used tool for writing and running unit tests, integration tests, and other types of tests for Python applications

## Directory structure

This is the directory structure of the example.

    📂 voting_blockchain
    ├──📃 .gitignore
    ├──📃 ape-config.yaml
    ├──📃 Makefile
    ├──📃 mkdocs.yml
    ├──📃 README.md
    ├──📃 requirements.txt
    └──📂 contracts
       ├──📃 DelegateVotingApp.vy
       ├──📃 VotingApp.vy
    └──📂 docs
        ├──📂 images
            ├──📃 coverage.png
            ├──📃 overview.png
            ├──📃 pytest_cov_shell.png
        ├──📂 extra
            ├──📃 feedback.js
            ├──📃 fluff.js
            ├──📃 terminal.css
            ├──📃 tweaks.css
        ├──📃 index.md
        ├──📃 pytest_ini.md
        ├──📃 test_data_files.md
    └──📂 tests
        ├──📃 conftest.py
        ├──📃 test_delegate_voting_app.py
        ├──📃 test_voting_app.py
        └──📃 __init__.py