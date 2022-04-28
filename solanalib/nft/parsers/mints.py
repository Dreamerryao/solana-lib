from typing import Union

from solanalib.constants import Metaplex
from solanalib.logger import logger
from solanalib.nft.transaction import Transaction
from solanalib.nft.activities import MintActivity


def parse_mint_other(tx: Transaction, mint: str) -> Union[MintActivity, None]:
    for ix in tx.instructions.outer:
        if ix.is_mint(mint):
            logger.debug("Is correct mint tx")
            new_authority = ix.info["mintAuthority"]
            new_token_account = ix.info["account"]
            program = ix["program"]

            return MintActivity(
                transaction_id=tx.transaction_id,
                block_time=tx.block_time,
                slot=tx.slot,
                mint=mint,
                new_authority=new_authority,
                new_token_account=new_token_account,
                program=program,
            )
    return None


def parse_mint_candy_machine_v1(
    tx: Transaction, mint: str
) -> Union[MintActivity, None]:
    is_candy_machine_v2 = False
    is_mint = False

    for ix in tx.instructions.outer:
        if ix.is_program_id(Metaplex.CANDY_MACHINE_V1):
            is_candy_machine_v2 = True
            logger.debug("Program is CandyMachineV1")

        if ix.is_mint(mint):
            is_mint = True
            logger.debug("Is correct mint tx")
            new_authority = ix.info["mintAuthority"]
            new_token_account = ix.info["account"]

    if is_candy_machine_v2 and is_mint:
        return MintActivity(
            transaction_id=tx.transaction_id,
            block_time=tx.block_time,
            slot=tx.slot,
            mint=mint,
            new_authority=new_authority,
            new_token_account=new_token_account,
            program="CandyMachineV1",
        )
    return None


def parse_mint_candy_machine_v2(
    tx: Transaction, mint: str
) -> Union[MintActivity, None]:
    is_candy_machine_v2 = False
    is_mint = False

    for ix in tx.instructions.outer:
        if ix.is_program_id(Metaplex.CANDY_MACHINE_V2):
            is_candy_machine_v2 = True
            logger.debug("Program is CandyMachineV2")

        if ix.is_mint(mint):
            is_mint = True
            logger.debug("Is correct mint tx")
            new_authority = ix.info["mintAuthority"]
            new_token_account = ix.info["account"]

    if is_candy_machine_v2 and is_mint:
        return MintActivity(
            transaction_id=tx.transaction_id,
            block_time=tx.block_time,
            slot=tx.slot,
            mint=mint,
            new_authority=new_authority,
            new_token_account=new_token_account,
            program="CandyMachineV2",
        )
    return None


def parse_mint(tx: Transaction, mint: str) -> Union[MintActivity, None]:
    to_parse = {
        "CandyMachineV1": parse_mint_candy_machine_v1,
        "CandyMachineV2": parse_mint_candy_machine_v2,
        "OtherMint": parse_mint_other,
    }

    for marketplace, parser in to_parse.items():
        logger.info(f"Checking mint-program {marketplace}")
        activity = parser(tx=tx, mint=mint)
        if activity:
            return activity

    return None
