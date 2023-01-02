# Import dependencies
import streamlit as st
from dataclasses import dataclass
from typing import Any, List
import datetime as datetime
import pandas as pd
import hashlib

# Define the Record data class


@dataclass
class Record:
    sender: str
    receiver: str
    amount: float

# Define the Block data class


@dataclass
class Block:
    # The `record` attribute consists of a `Record` object
    record: Record
    creator_id: int
    prev_hash: str = "0"
    timestamp: str = datetime.datetime.utcnow().strftime("%H:%M:%S")
    nonce: int = 0

    def hash_block(self) -> str:
        """
        Create a hash value for the block using the SHA-256 algorithm
        """
        sha = hashlib.sha256()

        # Hash the record data
        record = str(self.record).encode()
        sha.update(record)

        # Hash the creator_id
        creator_id = str(self.creator_id).encode()
        sha.update(creator_id)

        # Hash the timestamp
        timestamp = str(self.timestamp).encode()
        sha.update(timestamp)

        # Hash the prev_hash
        prev_hash = str(self.prev_hash).encode()
        sha.update(prev_hash)

        # Hash the nonce
        nonce = str(self.nonce).encode()
        sha.update(nonce)

        # Return the hexadecimal representation of the hash
        return sha.hexdigest()

# Define the PyChain class


@dataclass
class PyChain:
    chain: List[Block]
    difficulty: int = 4

    def proof_of_work(self, block: Block) -> Block:
        """
        Find a nonce value that, when hashed with the other block attributes,
        results in a hash value that starts with a certain number of zeros.
        """
        calculated_hash = block.hash_block()

        num_of_zeros = "0" * self.difficulty

        while not calculated_hash.startswith(num_of_zeros):
            block.nonce += 1
            calculated_hash = block.hash_block()

        print("Winning Hash", calculated_hash)
        return block

    def add_block(self, candidate_block: Block) -> None:
        """
        Add a block to the PyChain if it has a valid proof of work.
        """
        block = self.proof_of_work(candidate_block)
        self.chain += [block]

    def is_valid(self):
        block_hash = self.chain[0].hash_block()

        for block in self.chain[1:]:
            if block_hash != block.prev_hash:
                print("Blockchain is invalid!")
                return False

            block_hash = block.hash_block()

        print("Blockchain is Valid")
        return True

# Streamlit Code
# Adds the cache decorator for Streamlit


@st.cache(allow_output_mutation=True)
def setup():
    """
    Initializes the PyChain object with the Genesis Block
    """
    print("Initializing Chain")
    return PyChain([Block("Genesis", 0)])


st.markdown("# PyChain")
st.markdown("## Store a Transaction Record in the PyChain")

# Initialize the PyChain object
pychain = setup()

# Add relevant user inputs to the Streamlit interface
# Get the input data
input_data = st.text_input("Block Data")

if st.button("Add Block"):
    # Get the previous block and its hash
    prev_block = pychain.chain[-1]
    prev_block_hash = prev_block.hash_block()

    # Create a new block with the relevant attributes
    new_block = Block(
        data=input_data,
        creator_id=42,
        prev_hash=prev_block_hash
    )

    # Add the block to the PyChain
    pychain.add_block(new_block)
    st.balloons()

# Display the PyChain ledger
st.markdown("## The PyChain Ledger")
pychain_df = pd.DataFrame(pychain.chain).astype(str)
st.write(pychain_df)

# Allow the user to adjust the difficulty of the proof of work
difficulty = st.sidebar.slider("Block Difficulty", 1, 5, 2)
pychain.difficulty = difficulty

# Allow the user to inspect individual blocks
st.sidebar.write("# Block Inspector")
selected_block = st.sidebar.selectbox(
    "Which block would you like to see?", pychain.chain
)
st.sidebar.write(selected_block)

# Validate the PyChain
if st.button("Validate Chain"):
    st.write(pychain.is_valid())
