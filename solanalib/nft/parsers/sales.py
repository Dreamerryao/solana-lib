from typing import Union

from solanalib.constants import MagicEdenV1, MagicEdenV2
from solanalib.logger import logger
from solanalib.nft.models import SaleActivity, Transaction

from .util import get_me_listing_price_from_data


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
            buyer = ix["accounts"][0]  # first account
            seller = ix["accounts"][2]  # third account
            new_token_account = ix["accounts"][1]  # second account
            sale_price = get_me_listing_price_from_data(ix.data, MagicEdenV1.PROGRAM)

            return SaleActivity(
                transaction_id=tx.transaction_id,
                block_time=tx.block_time,
                slot=tx.slot,
                mint=mint,
                new_token_account=new_token_account,
                price_lamports=sale_price,
                marketplace=marketplace,
                buyer=buyer,
                seller=seller,
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
            buyer = ix["accounts"][0]  # first account
            seller = ix["accounts"][1]  # second account
            new_token_account = ix["accounts"][7]  # eigth account
            sale_price = get_me_listing_price_from_data(ix.data, MagicEdenV2.PROGRAM)

            return SaleActivity(
                transaction_id=tx.transaction_id,
                block_time=tx.block_time,
                slot=tx.slot,
                mint=mint,
                new_token_account=new_token_account,
                price_lamports=sale_price,
                marketplace=marketplace,
                buyer=buyer,
                seller=seller,
            )
    return None


def parse_sale(tx: Transaction, mint: str) -> Union[SaleActivity, None]:
    to_parse = {
        "MagiEdenV1": parse_sale_mev1,
        "MagiEdenV2": parse_sale_mev2,
    }

    for marketplace, parser in to_parse.items():
        logger.info(f"Checking marketplace {marketplace}")
        activity = parser(tx=tx, mint=mint)
        if activity:
            return activity

    return None
