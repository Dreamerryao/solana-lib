from enum import Enum


class Marketplace(str, Enum):
    MAGIC_EDEN_V1 = "MagicEdenV1"
    MAGIC_EDEN_V2 = "MagicEdenV2"


class MagicEdenV1(str, Enum):
    NAME = "MagicEdenV1"
    PROGRAM = "MEisE1HzehtrDpAAT8PnLHjpSSkRYakotTuJRPjTpo8"
    AUTHORITY = "GUfCR9mK6azb9vcpsxgXyj7XRPAKJd4KMHTTVvtncGgp"
    DELISTING_INSTRUCTION = "TE6axTojnp"
    MARKETPLACE = Marketplace.MAGIC_EDEN_V1.value


class MagicEdenV2(str, Enum):
    NAME = "MagicEdenV2"
    PROGRAM = "M2mx93ekt1fmXSVkTrUL9xVFHkmME8HTUi5Cyc5aF7K"
    AUTHORITY = "1BWutmTvYPwDtmw9abTkS4Ssr8no61spGAvW1X6NDix"
    DELISTING_INSTRUCTION = "ENwHiaH9NA"
    LISTING_INSTRUCTION = "2B3vSpRNKZ"
    SALE_INSTRUCTION = "d6iteQtSVr"
    MARKETPLACE = Marketplace.MAGIC_EDEN_V2.value


class Metaplex(str, Enum):
    METADATA_PROGRAM = "metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s"
    CANDY_MACHINE_V2 = "cndy3Z4yapfJBmL3ShUp5exZKqR3z33thTzeNMm2gRZ"


class Token(str, Enum):
    PROGRAM = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
    ASSOCIATE_PROGRAM = "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL"
