import pytest
from ape.exceptions import ContractLogicError


def test_delegate(delegate_contract, deployer, accounts):
    """
    Tests the delegation functionality in the VotingApp contract.

    Args:
        delegate_contract (Contract): The deployed instance of the VotingApp contract, provided by the `delegate_contract` fixture.
        deployer (Account): The account used to deploy the contract and give voting rights, provided by the `deployer` fixture.
        accounts (list): A list of accounts provided by the `accounts` fixture.
    """
    user = accounts[1]
    user2 = accounts[2]
    delegate_contract.giveRightToVote(user, 1, sender=deployer)
    delegate_contract.giveRightToVote(user2, 2, sender=deployer)

    assert delegate_contract.voters(user).weight == 1
    assert delegate_contract.voters(user).voted is False
    assert delegate_contract.voters(user).vote == 0
    assert delegate_contract.voters(user2).weight == 2
    assert delegate_contract.voters(user2).voted is False
    assert delegate_contract.voters(user2).vote == 0
    delegate_contract.delegate(user, sender=user2)
    assert delegate_contract.voters(user).weight == 3
    assert delegate_contract.voters(user).voted is False
    assert delegate_contract.voters(user).vote == 0
    assert delegate_contract.voters(user2).weight == 0
    assert delegate_contract.voters(user2).voted is True
    assert delegate_contract.voters(user2).vote == 0


def test_delegate_2_levels(delegate_contract, deployer, accounts):
    """
    Tests the delegation functionality in the VotingApp contract with two levels of delegation.

    Args:
        delegate_contract (Contract): The deployed instance of the VotingApp contract, provided by the `delegate_contract` fixture.
        deployer (Account): The account used to deploy the contract and give voting rights, provided by the `deployer` fixture.
        accounts (list): A list of accounts provided by the `accounts` fixture.
    """
    user = accounts[1]
    user2 = accounts[2]
    user3 = accounts[3]
    delegate_contract.giveRightToVote(user, 1, sender=deployer)
    delegate_contract.giveRightToVote(user2, 2, sender=deployer)
    delegate_contract.giveRightToVote(user3, 5, sender=deployer)

    assert delegate_contract.voters(user).weight == 1
    assert delegate_contract.voters(user).voted is False
    assert delegate_contract.voters(user).vote == 0
    assert delegate_contract.voters(user2).weight == 2
    assert delegate_contract.voters(user2).voted is False
    assert delegate_contract.voters(user2).vote == 0
    assert delegate_contract.voters(user3).weight == 5
    assert delegate_contract.voters(user3).voted is False
    assert delegate_contract.voters(user3).vote == 0
    delegate_contract.delegate(user, sender=user2)
    delegate_contract.delegate(user2, sender=user3)
    assert delegate_contract.voters(user).weight == 8
    assert delegate_contract.voters(user).voted is False
    assert delegate_contract.voters(user).vote == 0
    assert delegate_contract.voters(user2).weight == 0
    assert delegate_contract.voters(user2).voted is True
    assert delegate_contract.voters(user2).vote == 0
    assert delegate_contract.voters(user3).weight == 0
    assert delegate_contract.voters(user3).voted is True
    assert delegate_contract.voters(user3).vote == 0


def test_vote_after_delegate_2_levels(delegate_contract, deployer, accounts):
    """
    Tests the voting functionality in the VotingApp contract after two levels of delegation.

    Args:
        delegate_contract (Contract): The deployed instance of the VotingApp contract, provided by the `delegate_contract` fixture.
        deployer (Account): The account used to deploy the contract and add proposals, provided by the `deployer` fixture.
        accounts (list): A list of accounts provided by the `accounts` fixture.
    """
    delegate_contract.addProposal("beach", sender=deployer)
    delegate_contract.addProposal("mountain", sender=deployer)
    user = accounts[1]
    user2 = accounts[2]
    user3 = accounts[3]
    delegate_contract.giveRightToVote(user, 1, sender=deployer)
    delegate_contract.giveRightToVote(user2, 2, sender=deployer)
    delegate_contract.giveRightToVote(user3, 5, sender=deployer)
    delegate_contract.delegate(user, sender=user2)
    delegate_contract.delegate(user2, sender=user3)
    delegate_contract.vote(1, sender=user)
    assert delegate_contract.voters(user).weight == 0
    assert delegate_contract.voters(user).voted is True
    assert delegate_contract.voters(user).vote == 1
    assert delegate_contract.winnerName() == "mountain"
    assert delegate_contract.proposals(0).voteCount == 0
    assert delegate_contract.proposals(1).voteCount == 8


def test_delegate_after_vote(delegate_contract, deployer, accounts):
    """
    Tests the delegating functionality in the VotingApp contract after a user has already voted.

    Args:
        delegate_contract (Contract): The deployed instance of the VotingApp contract, provided by the `delegate_contract` fixture.
        deployer (Account): The account used to deploy the contract and add proposals, provided by the `deployer` fixture.
        accounts (list): A list of accounts provided by the `accounts` fixture.
    """
    delegate_contract.addProposal("beach", sender=deployer)
    delegate_contract.addProposal("mountain", sender=deployer)
    user = accounts[1]
    user2 = accounts[2]
    user3 = accounts[3]
    delegate_contract.giveRightToVote(user, 1, sender=deployer)
    delegate_contract.giveRightToVote(user2, 2, sender=deployer)
    delegate_contract.giveRightToVote(user3, 5, sender=deployer)
    delegate_contract.vote(1, sender=user)
    delegate_contract.delegate(user, sender=user2)
    delegate_contract.delegate(user2, sender=user3)

    assert delegate_contract.voters(user2).weight == 0
    assert delegate_contract.voters(user2).voted is True
    assert delegate_contract.voters(user2).vote == 0
    assert delegate_contract.voters(user2).delegate == user
    assert delegate_contract.voters(user3).weight == 0
    assert delegate_contract.voters(user3).voted is True
    assert delegate_contract.voters(user2).vote == 0
    assert delegate_contract.voters(user3).delegate == user2

    assert delegate_contract.voters(user).weight == 0
    assert delegate_contract.voters(user).voted is True
    assert delegate_contract.voters(user).vote == 1
    assert (
        delegate_contract.voters(user).delegate
        == "0x0000000000000000000000000000000000000000"
    )

    assert delegate_contract.winnerName() == "mountain"
    assert delegate_contract.proposals(0).voteCount == 0
    assert delegate_contract.proposals(1).voteCount == 8


def test_chairperson(delegate_contract, deployer):
    """
    Tests that the chairperson of the `VotingApp` contract is set to the deployer account.

    Args:
        contract (Contract): The deployed instance of the `VotingApp` contract, provided by the `contract` fixture.
        deployer (Account): The account used to deploy the contract, provided by the `deployer` fixture.

    Raises:
        AssertionError: If the chairperson of the `VotingApp` contract is not set to the deployer account.
    """
    contract = delegate_contract
    chairperson = contract.chairperson()
    assert chairperson == deployer


def test_addProposal(delegate_contract, deployer):
    """
    Tests the `addProposal` function of the `VotingApp` contract.

    Args:
        contract (Contract): The deployed instance of the `VotingApp` contract, provided by the `contract` fixture.
        deployer (Account): The account used to deploy the contract and add the proposal, provided by the `deployer` fixture.

    Raises:
        AssertionError: If the initial number of proposals is not 0, if the initial proposal name is not an empty string, if the number of proposals after adding a proposal is not 1, or if the name of the added proposal is not "Test Proposal".
    """
    contract = delegate_contract
    assert contract.amountProposals() == 0
    assert contract.proposals(0).name == ""
    contract.addProposal("beach", sender=deployer)
    assert contract.amountProposals() == 1
    assert contract.proposals(0).name == "beach"


def test_addProposal_fail(delegate_contract, accounts):
    """
    Tests that the `addProposal` function of the `VotingApp` contract fails when called by an account other than the chairperson.

    Args:
        contract (Contract): The deployed instance of the `VotingApp` contract, provided by the `contract` fixture.
        accounts (list): A list of accounts provided by the `accounts` fixture.

    Raises:
        ContractLogicError: Expected to be raised when the `addProposal` function is called by an account other than the chairperson.
    """
    contract = delegate_contract
    with pytest.raises(ContractLogicError):
        contract.addProposal("beach", sender=accounts[1])


def test_giveRightToVote(delegate_contract, deployer, accounts):
    """
    Tests the `giveRightToVote` function of the `VotingApp` contract.

    Args:
        contract (Contract): The deployed instance of the `VotingApp` contract, provided by the `contract` fixture.
        deployer (Account): The account used to deploy the contract and give voting rights, provided by the `deployer` fixture.
        accounts (list): A list of accounts provided by the `accounts` fixture.

    Raises:
        AssertionError: If the initial voter count is not 0, if the initial voting weight of the first user is not 0, if the voter count after adding the first user is not 1, if the voting weight of the first user is not 15, if the initial voting weight of the second user is not 0, if the voter count after adding the second user is not 2, or if the voting weight of the second user is not 8.
    """
    contract = delegate_contract
    user = accounts[1]
    assert contract.voterCount() == 0
    assert contract.voters(user).weight == 0
    contract.giveRightToVote(user, 1, sender=deployer)
    assert contract.voterCount() == 1
    assert contract.voters(user).weight == 1

    power_user = accounts[2]
    assert contract.voters(power_user).weight == 0
    contract.giveRightToVote(power_user, 9, sender=deployer)
    assert contract.voterCount() == 2
    assert contract.voters(power_user).weight == 9


def test_giveRightToVote_fail(delegate_contract, deployer, accounts):
    """
    Tests that the `giveRightToVote` function of the `VotingApp` contract fails when called by an account other than the chairperson.

    Args:
        contract (Contract): The deployed instance of the `VotingApp` contract, provided by the `contract` fixture.
        deployer (Account): The account used to deploy the contract and give voting rights, provided by the `deployer` fixture.
        accounts (list): A list of accounts provided by the `accounts` fixture.

    Raises:
        ContractLogicError: Expected to be raised when the `giveRightToVote` function is called by an account other than the chairperson.
    """
    contract = delegate_contract
    user = accounts[1]
    with pytest.raises(ContractLogicError):
        contract.giveRightToVote(user, 1, sender=accounts[1])


def test_vote(delegate_contract, deployer, accounts):
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
    contract = delegate_contract
    contract.addProposal("beach", sender=deployer)
    contract.addProposal("mountain", sender=deployer)
    user = accounts[1]
    user2 = accounts[2]
    contract.giveRightToVote(user, 1, sender=deployer)
    contract.giveRightToVote(user2, 1, sender=deployer)

    assert contract.voters(user).weight == 1
    assert contract.voters(user).voted is False
    assert contract.voters(user).vote == 0
    assert contract.proposals(0).voteCount == 0
    contract.vote(0, sender=user)
    assert contract.proposals(0).voteCount == 1
    assert contract.voters(user).weight == 0
    assert contract.voters(user).voted is True
    assert contract.voters(user).vote == 0

    assert contract.voters(user2).weight == 1
    assert contract.voters(user2).voted is False
    assert contract.voters(user2).vote == 0
    assert contract.proposals(1).voteCount == 0
    contract.vote(1, sender=user2)
    assert contract.proposals(1).voteCount == 1
    assert contract.voters(user2).weight == 0
    assert contract.voters(user2).voted is True
    assert contract.voters(user2).vote == 1


def test_vote_fail(delegate_contract, deployer, accounts):
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
    contract = delegate_contract
    contract.addProposal("beach", sender=deployer)
    contract.addProposal("mountain", sender=deployer)
    user = accounts[1]
    contract.giveRightToVote(user, 1, sender=deployer)

    contract.vote(0, sender=user)
    with pytest.raises(ContractLogicError):
        contract.vote(0, sender=user)


def test_winnerName(delegate_contract, deployer, accounts):
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
    contract = delegate_contract
    contract.addProposal("beach", sender=deployer)
    contract.addProposal("mountain", sender=deployer)
    user1 = accounts[1]
    user2 = accounts[2]
    user3 = accounts[3]
    contract.giveRightToVote(user1, 1, sender=deployer)
    contract.giveRightToVote(user2, 1, sender=deployer)
    contract.giveRightToVote(user3, 1, sender=deployer)

    contract.vote(0, sender=user1)
    contract.vote(1, sender=user2)
    contract.vote(1, sender=user3)

    assert contract.proposals(0).voteCount == 1
    assert contract.proposals(1).voteCount == 2
    assert contract.winnerName() == "mountain"
