import pytest
from ape.exceptions import ContractLogicError


def test_chairperson(contract, deployer):
    """
    Tests that the chairperson of the `VotingApp` contract is set to the deployer account.

    Args:
        contract (Contract): The deployed instance of the `VotingApp` contract, provided by the `contract` fixture.
        deployer (Account): The account used to deploy the contract, provided by the `deployer` fixture.

    Raises:
        AssertionError: If the chairperson of the `VotingApp` contract is not set to the deployer account.
    """
    assert contract.chairperson() == deployer


def test_addProposal(contract, deployer):
    """
    Tests the `addProposal` function of the `VotingApp` contract.

    Args:
        contract (Contract): The deployed instance of the `VotingApp` contract, provided by the `contract` fixture.
        deployer (Account): The account used to deploy the contract and add the proposal, provided by the `deployer` fixture.

    Raises:
        AssertionError: If the initial number of proposals is not 0, if the initial proposal name is not an empty string, if the number of proposals after adding a proposal is not 1, or if the name of the added proposal is not "Test Proposal".
    """
    assert contract.amountProposals() == 0
    assert contract.proposals(0).name == ""
    contract.addProposal("Test Proposal", sender=deployer)
    assert contract.amountProposals() == 1
    assert contract.proposals(0).name == "Test Proposal"


def test_addProposal_fail(contract, accounts):
    """
    Tests that the `addProposal` function of the `VotingApp` contract fails when called by an account other than the chairperson.

    Args:
        contract (Contract): The deployed instance of the `VotingApp` contract, provided by the `contract` fixture.
        accounts (list): A list of accounts provided by the `accounts` fixture.

    Raises:
        ContractLogicError: Expected to be raised when the `addProposal` function is called by an account other than the chairperson.
    """
    with pytest.raises(ContractLogicError):
        contract.addProposal("Fail Proposal", sender=accounts[1])


def test_giveRightToVote(contract, deployer, accounts):
    """
    Tests the `giveRightToVote` function of the `VotingApp` contract.

    Args:
        contract (Contract): The deployed instance of the `VotingApp` contract, provided by the `contract` fixture.
        deployer (Account): The account used to deploy the contract and give voting rights, provided by the `deployer` fixture.
        accounts (list): A list of accounts provided by the `accounts` fixture.

    Raises:
        AssertionError: If the initial voter count is not 0, if the initial voting weight of the first user is not 0, if the voter count after adding the first user is not 1, if the voting weight of the first user is not 15, if the initial voting weight of the second user is not 0, if the voter count after adding the second user is not 2, or if the voting weight of the second user is not 8.
    """
    user = accounts[1]
    assert contract.voterCount() == 0
    assert contract.voters(user).weight == 0
    contract.giveRightToVote(user, 15, sender=deployer)
    assert contract.voterCount() == 1
    assert contract.voters(user).weight == 15
    power_user = accounts[2]
    assert contract.voters(power_user).weight == 0
    contract.giveRightToVote(power_user, 8, sender=deployer)
    assert contract.voterCount() == 2
    assert contract.voters(power_user).weight == 8


def test_giveRightToVote_fail(contract, deployer, accounts):
    """
    Tests that the `giveRightToVote` function of the `VotingApp` contract fails when called by an account other than the chairperson.

    Args:
        contract (Contract): The deployed instance of the `VotingApp` contract, provided by the `contract` fixture.
        deployer (Account): The account used to deploy the contract and give voting rights, provided by the `deployer` fixture.
        accounts (list): A list of accounts provided by the `accounts` fixture.

    Raises:
        ContractLogicError: Expected to be raised when the `giveRightToVote` function is called by an account other than the chairperson.
    """
    user = accounts[1]
    with pytest.raises(ContractLogicError):
        contract.giveRightToVote(user, 15, sender=accounts[2])


def test_vote(contract, deployer, accounts):
    """
    Tests the voting functionality of the VotingApp contract.

    Args:
        contract (Contract): The deployed instance of the VotingApp contract, provided by the `contract` fixture.
        deployer (Account): The account used to deploy the contract and give voting rights, provided by the `deployer` fixture.
        accounts (list): A list of accounts provided by the `accounts` fixture.

    Steps:
        1. Add two proposals to the contract.
        2. Give voting rights to two users (accounts[1] and accounts[2]).
        3. Verify the initial state of the voters and proposals.
        4. Have the first user (accounts[1]) vote for the first proposal.
        5. Verify the updated state of the voters and proposals after the first vote.
        6. Have the second user (accounts[2]) vote for the second proposal.
        7. Verify the updated state of the voters and proposals after the second vote.
    """
    contract.addProposal("beach", sender=deployer)
    contract.addProposal("mountain", sender=deployer)
    user = accounts[1]
    user2 = accounts[2]
    contract.giveRightToVote(user, 12, sender=deployer)
    contract.giveRightToVote(user2, 18, sender=deployer)
    assert contract.voters(user).weight == 12
    assert contract.voters(user).voted is False
    assert contract.voters(user).vote == 0
    assert contract.proposals(0).voteCount == 0
    contract.vote(0, sender=user)
    assert contract.proposals(0).voteCount == 12
    assert contract.voters(user).weight == 0
    assert contract.voters(user).voted is True
    assert contract.voters(user).vote == 0
    assert contract.voters(user2).weight == 18
    assert contract.voters(user2).voted is False
    assert contract.voters(user2).vote == 0
    assert contract.proposals(1).voteCount == 0
    contract.vote(1, sender=user2)
    assert contract.proposals(1).voteCount == 18
    assert contract.voters(user2).weight == 0
    assert contract.voters(user2).voted is True
    assert contract.voters(user2).vote == 1


def test_vote_fail(contract, deployer, accounts):
    """
    Tests the failure scenario of the voting functionality in the VotingApp contract.

    Args:
        contract (Contract): The deployed instance of the VotingApp contract, provided by the `contract` fixture.
        deployer (Account): The account used to deploy the contract and give voting rights, provided by the `deployer` fixture.
        accounts (list): A list of accounts provided by the `accounts` fixture.

    Steps:
        1. Add two proposals to the contract.
        2. Give voting rights to a user (accounts[1]).
        3. Have the user vote for the first proposal.
        4. Attempt to have the user vote for the first proposal again, which should fail.
    """
    contract.addProposal("beach", sender=deployer)
    contract.addProposal("mountain", sender=deployer)
    user = accounts[1]
    contract.giveRightToVote(user, 5, sender=deployer)
    contract.vote(0, sender=user)
    with pytest.raises(ContractLogicError):
        contract.vote(0, sender=user)


def test_winnerName(contract, deployer, accounts):
    """
    Tests the failure scenario of the voting functionality in the VotingApp contract.

    Args:
        contract (Contract): The deployed instance of the VotingApp contract, provided by the `contract` fixture.
        deployer (Account): The account used to deploy the contract and give voting rights, provided by the `deployer` fixture.
        accounts (list): A list of accounts provided by the `accounts` fixture.

    Steps:
        1. Add two proposals to the contract.
        2. Give voting rights to a user (accounts[1]).
        3. Have the user vote for the first proposal.
        4. Attempt to have the user vote for the first proposal again, which should fail.
    """
    contract.addProposal("beach", sender=deployer)
    contract.addProposal("mountain", sender=deployer)
    user = accounts[1]
    user2 = accounts[2]
    user3 = accounts[3]
    contract.giveRightToVote(user, 12, sender=deployer)
    contract.giveRightToVote(user2, 18, sender=deployer)
    contract.giveRightToVote(user3, 20, sender=deployer)
    contract.vote(0, sender=user)
    contract.vote(1, sender=user2)
    contract.vote(1, sender=user3)
    assert contract.proposals(0).voteCount == 12
    assert contract.proposals(1).voteCount == 38
    assert contract.winnerName() == "mountain"
