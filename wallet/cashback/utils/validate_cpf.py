import re
import logging

logger = logging.getLogger(__name__)


def validate_cpf(cpf: str) -> bool:
    """
    Check if a cpf is valid or not
    must have 11 positions
    """
    cpf = "".join(re.findall(r"\d", str(cpf)))

    if not cpf or len(cpf) < 11:
        logger.error("Total characteres in  CPF is not valid %s", cpf)
        return False

    old = [int(d) for d in cpf]

    new = old[:9]
    while len(new) < 11:
        rest = sum([v * (len(new) + 1 - i) for i, v in enumerate(new)]) % 11

        dv = 0 if rest <= 1 else 11 - rest

        new.append(dv)

    if new == old:
        return True
    logger.error("CPF number not valid %s", cpf)
    return False
