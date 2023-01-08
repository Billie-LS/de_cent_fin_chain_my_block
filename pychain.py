# PyChain Ledger
################################################################################
# Step 1: Create a Record Data Class
# * Create a new data class named `Record`. This class will serve as the
# blueprint for the financial transaction records that the blocks of the ledger
# will store.

# Step 2: Modify the Existing Block Data Class to Store Record Data
# * Change the existing `Block` data class by replacing the generic `data`
# attribute with a `record` attribute that’s of type `Record`.

# Step 3: Add Relevant User Inputs to the Streamlit Interface
# * Create additional user input areas in the Streamlit application. These
# input areas should collect the relevant information for each financial record
# that you’ll store in the `PyChain` ledger.

# Step 4: Test the PyChain Ledger by Storing Records
# * Test your complete `PyChain` ledger.

################################################################################
# Import dependencies
import sys
import os
import platform
from watermark import watermark

import streamlit as st
from dataclasses import dataclass
from typing import Any, List
import datetime as datetime
import pandas as pd
import hashlib
################################################################################
# Report Technologies
print(f'Python Platform: {platform.platform()}')
print(f'Python {sys.version}')
print(watermark())
print(watermark(iversions=True, globals_=globals()))
################################################################################
# Step 1:
# Create a Record Data Class that consists of the `sender`, `receiver`, and
# `amount` attributes


@dataclass
class Record:
    sender: str
    receiver: str
    amount: float
################################################################################
# Step 2:
# Define the Block data class


@dataclass
class Block:

    # The `record` attribute consists of a `Record` object
    record: Record
    creator_id: int
    prev_hash: str = '0'
    timestamp: str = datetime.datetime.utcnow().strftime('%H:%M:%S')
    nonce: int = 0

    def hash_block(self) -> str:
        # def hash_block(self):
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
        # def proof_of_work(self, block):
        """
        Find a nonce value that, when hashed with the other block attributes,
        results in a hash value that starts with a certain number of zeros.
        """
        calculated_hash = block.hash_block()

        num_of_zeros = '0' * self.difficulty

        while not calculated_hash.startswith(num_of_zeros):
            block.nonce += 1
            calculated_hash = block.hash_block()

        print('Wining Hash', calculated_hash)
        return block

    def add_block(self, candidate_block: Block) -> None:
        # def add_block(self, candidate_block):
        """
        Add a block to the PyChain if it has a valid proof of work.
        """
        block = self.proof_of_work(candidate_block)
        self.chain += [block]

    def is_valid(self) -> bool:
        # def is_valid(self):
        block_hash = self.chain[0].hash_block()

        for block in self.chain[1:]:
            if block_hash != block.prev_hash:
                print('Blockchain is invalid!')
                return False

            block_hash = block.hash_block()

        print('Blockchain is Valid')
        return True

################################################################################
# Streamlit Code

# Adds the cache decorator for Streamlit


@st.cache(allow_output_mutation=True)
def setup() -> PyChain:
    # def setup():
    """
    Initializes the PyChain object with the Genesis Block
    """
    print('Initializing Chain')
    return PyChain([Block('Genesis', 0)])


st.markdown('# PyChain')
st.markdown('## Store a Transaction Record in the PyChain')

# Initialize the PyChain object
pychain = setup()

################################################################################
# Step 3:
# Add relevant user inputs to the Streamlit interface
# Get the input data

# Add an input area where you can get a value for `sender` from the user.
sender_data = st.text_input('Sender')

# Add an input area where you can get a value for `receiver` from the user.
receiver_data = st.text_input('Receiver')

# Add an input area where you can get a value for `amount` from the user.
amount_data = st.text_input('Amount')

seed = 42
if st.button('Add Block'):
    # Get the previous block and its hash
    prev_block = pychain.chain[-1]
    prev_block_hash = prev_block.hash_block()

    # Create a new block with the relevant attributes
    new_block = Block(
        record=Record(sender_data, receiver_data, amount_data),
        creator_id=seed,
        prev_hash=prev_block_hash
    )

    # Add the block to the PyChain
    pychain.add_block(new_block)
    st.balloons()

################################################################################
# Streamlit Code (continues)
# Display the PyChain ledger

st.markdown('## The PyChain Ledger')

pychain_df = pd.DataFrame(pychain.chain).astype(str)
st.write(pychain_df)

# Allow the user to adjust the difficulty of the proof of work
difficulty = st.sidebar.slider('Block Difficulty', 1, 7, 2)
pychain.difficulty = difficulty

# Allow the user to inspect individual blocks
st.sidebar.write('# Block Inspector')
selected_block = st.sidebar.selectbox(
    'Which block would you like to see?', pychain.chain
)
st.sidebar.write(selected_block)

# Validate the PyChain
if st.button('Validate Chain'):
    if pychain.is_valid():
        st.success('This is a valid chain!', icon="✅")
    else:
        st.warning('This is NOT a valid chain!', icon="⚠️")
################################################################################
# Step 4:
# Test the PyChain Ledger by Storing Records

# Test your complete `PyChain` ledger and user interface by running your
# Streamlit application and storing some mined blocks in your `PyChain` ledger.
# Then test the blockchain validation process by using your `PyChain` ledger.
# To do so, complete the following steps:

# 1. In the terminal, navigate to the project folder where you've coded the
#  Challenge.

# 2. In the terminal, run the Streamlit application by
# using `streamlit run pychain.py`.

# 3. Enter values for the sender, receiver, and amount, and then click the "Add
# Block" button. Do this several times to store several blocks in the ledger.

# 4. Verify the block contents and hashes in the Streamlit drop-down menu.
# Take a screenshot of the Streamlit application page, which should detail a
# blockchain that consists of multiple blocks. Include the screenshot in the
# `README.md` file for your Challenge repository.

# 5. Test the blockchain validation process by using the web interface.
# Take a screenshot of the Streamlit application page, which should indicate
# the validity of the blockchain. Include the screenshot in the `README.md`
# file for your Challenge repository.
