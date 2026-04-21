from dataclasses import dataclass


@dataclass(frozen=True)
class DecodedInstruction:
    family: str
    mnemonic: str
    opcode: int
    rs: int | None
    rt: int | None
    rd: int | None
    shamt: int | None
    funct: int | None
    immediate: int | None
    binary_word: str
    hex_word: str
    assembly: str
