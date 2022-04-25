from typing import Union

from solanalib.constants import MagicEdenV1, MagicEdenV2
from solanalib.logger import logger
from solanalib.nft.models import SaleActivity, Transaction

from .util import get_me_lamports_price_from_data

# TODO
# acceptBid eg for MEV1 5g1CLoBX3RYR2YPqGZ3oP7YCN63V68SFm1WF6rTQ12Wfh7X2gYiYPD8R1eRN2ERs466qKYGnhdA6VGvgLrTtF3Qo


def parse_sale_mev1(tx: Transaction, mint: str) -> Union[SaleActivity, None]:
    sale_price = None
    new_token_account = None

    for ix in tx.instructions.outer:
        if not ix.is_program_id(MagicEdenV1.PROGRAM):
            continue
        logger.debug(f"Program is {MagicEdenV1.NAME}")
        marketplace = MagicEdenV1.MARKETPLACE

        if ix.data[0:10] == MagicEdenV1.SALE_INSTRUCTION:
            logger.debug("Is Sale instruction")
            new_authority = ix["accounts"][0]  # 1st account
            old_authority = ix["accounts"][2]  # 3rd account
            new_token_account = ix["accounts"][1]  # 2nd account

            sale_price = get_me_lamports_price_from_data(ix.data, MagicEdenV1.PROGRAM)

            return SaleActivity(
                transaction_id=tx.transaction_id,
                block_time=tx.block_time,
                slot=tx.slot,
                mint=mint,
                new_authority=new_authority,
                old_authority=old_authority,
                new_token_account=new_token_account,
                old_token_account=new_token_account,  # In V1, MagicEden just transfers authority for new token account
                price_lamports=sale_price,
                program=marketplace,
            )
    return None


def parse_accept_bid_mev1(tx: Transaction, mint: str) -> Union[SaleActivity, None]:
    sale_price = None
    new_token_account = None

    for ix in tx.instructions.outer:
        if not ix.is_program_id(MagicEdenV1.PROGRAM):
            continue
        logger.debug(f"Program is {MagicEdenV1.NAME}")
        marketplace = MagicEdenV1.MARKETPLACE

        if ix.data[0:10] == MagicEdenV1.ACCEPT_BID_INSTRUCTION:
            logger.debug("Is AcceptBid instruction")
            old_authority = ix["accounts"][0]
            new_authority = ix["accounts"][1]
            new_token_account = ix["accounts"][2]

            sale_price = get_me_lamports_price_from_data(ix.data, MagicEdenV1.PROGRAM)

            return SaleActivity(
                transaction_id=tx.transaction_id,
                block_time=tx.block_time,
                slot=tx.slot,
                mint=mint,
                new_authority=new_authority,
                old_authority=old_authority,
                new_token_account=new_token_account,
                old_token_account=new_token_account,  # In V1, MagicEden just transfers authority for new token account
                price_lamports=sale_price,
                program=marketplace,
            )
    return None


def parse_sale_mev2(tx: Transaction, mint: str) -> Union[SaleActivity, None]:
    sale_price = None
    new_token_account = None

    for ix in tx.instructions.outer:
        if not ix.is_program_id(MagicEdenV2.PROGRAM):
            continue
        logger.debug(f"Program is {MagicEdenV2.NAME}")
        marketplace = MagicEdenV2.MARKETPLACE

        if ix.data[0:10] == MagicEdenV2.SALE_INSTRUCTION:
            logger.debug("Is Sale instruction")
            new_authority = ix["accounts"][0]  # 1st account
            old_authority = ix["accounts"][1]  # 2nd account
            new_token_account = ix["accounts"][7]  # 8th account
            old_token_account = ix["accounts"][3]  # 4th account
            sale_price = get_me_lamports_price_from_data(ix.data, MagicEdenV2.PROGRAM)

            return SaleActivity(
                transaction_id=tx.transaction_id,
                block_time=tx.block_time,
                slot=tx.slot,
                mint=mint,
                new_authority=new_authority,
                old_authority=old_authority,
                new_token_account=new_token_account,
                old_token_account=old_token_account,
                price_lamports=sale_price,
                program=marketplace,
            )
    return None


# TODO
def parse_sale_auction_house(tx: Transaction, mint: str) -> Union[SaleActivity, None]:
    return None


# TODO see 3q3VzPrCXfjtXnspPaDb3S9L9wNoMBN9skgXzThDF1KDeaRiYmmtqGJZn2eQCMXMaZ2wAUQxR2Vmpsy6K7jf18gT
def parse_sale_digital_eyes(tx: Transaction, mint: str) -> Union[SaleActivity, None]:
    return


def parse_sale(tx: Transaction, mint: str) -> Union[SaleActivity, None]:
    to_parse = {
        "MagicEdenV1 Sale": parse_sale_mev1,
        "MagicEdenV1 AcceptBid": parse_accept_bid_mev1,
        "MagicEdenV2 Sale": parse_sale_mev2,
        "AuctionHouse": parse_sale_auction_house,
        "DigitalEyes": parse_sale_digital_eyes,
    }

    for marketplace, parser in to_parse.items():
        logger.info(f"Checking marketplace {marketplace}")
        activity = parser(tx=tx, mint=mint)
        if activity:
            return activity

    return None
