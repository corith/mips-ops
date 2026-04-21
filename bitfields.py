import re


_BINARY_WORD_RE = re.compile(r"[01]{32}")
_HEX_WORD_RE = re.compile(r"(?:0x)?[0-9a-fA-F]{8}")


def normalize_machine_word(raw: str) -> str:
    text = raw.strip()
    if _BINARY_WORD_RE.fullmatch(text):
        return text

    if _HEX_WORD_RE.fullmatch(text):
        hex_digits = text[2:] if text.lower().startswith("0x") else text
        return format(int(hex_digits, 16), "032b")

    raise ValueError(
        f"machine word must be 8 hex digits or 32 bits of binary, got {raw!r}"
    )


def split_field_bits(bits: str) -> dict[str, str]:
    if not _BINARY_WORD_RE.fullmatch(bits):
        raise ValueError(f"bitstring must be exactly 32 bits, got {bits!r}")

    return {
        "opcode": bits[0:6],
        "rs": bits[6:11],
        "rt": bits[11:16],
        "rd": bits[16:21],
        "shamt": bits[21:26],
        "funct": bits[26:32],
        "immediate": bits[16:32],
    }


def split_fields(bits: str) -> dict[str, int]:
    return {name: int(value, 2) for name, value in split_field_bits(bits).items()}


def bits_to_hex(bits: str) -> str:
    if not _BINARY_WORD_RE.fullmatch(bits):
        raise ValueError(f"bitstring must be exactly 32 bits, got {bits!r}")
    return format(int(bits, 2), "08x")


def sign_extend(value: int, width: int) -> int:
    sign_bit = 1 << (width - 1)
    full_range = 1 << width
    return value - full_range if value & sign_bit else value
