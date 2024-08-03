import pytest


@pytest.fixture
def deployer(accounts):
    """
    This fixture provides the first account from the `accounts` fixture as the deployer account.
    """
    return accounts[0]


@pytest.fixture
def contract(deployer, project):
    """
    This fixture deploys the `VotingApp` contract using the `deployer` account and returns the deployed contract instance.
    """
    return deployer.deploy(project.VotingApp)
