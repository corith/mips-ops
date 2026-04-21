import re

from bitfields import bits_to_hex
from isa import MNEMONIC_TO_SPEC


_REGISTER_RE = re.compile(r"\$(?:[0-9]|[12][0-9]|3[01])")


def parse_assembly(text: str) -> tuple[str, list[str]]:
    normalized = text.strip().lower()
    if not normalized:
        raise ValueError("assembly text cannot be empty")

    parts = normalized.split(None, 1)
    mnemonic = parts[0]
    operands_text = parts[1] if len(parts) == 2 else ""
    operands = [operand.strip() for operand in operands_text.split(",") if operand.strip()]
    return mnemonic, operands


def _parse_register(token: str) -> int:
    token = token.strip().lower()
    if not _REGISTER_RE.fullmatch(token):
        raise ValueError(f"invalid register {token!r}")
    return int(token[1:])


def _parse_int_literal(token: str) -> int:
    token = token.strip().lower()
    if token.startswith("-0x"):
        return -int(token[3:], 16)
    if token.startswith("+0x"):
        return int(token[1:], 16)
    if token.startswith("0x"):
        return int(token, 16)
    return int(token, 10)


def _encode_immediate(value: int, mode: str) -> int:
    if mode == "unsigned":
        if not 0 <= value <= 0xFFFF:
            raise ValueError(f"immediate {value} is out of range for unsigned 16-bit")
        return value
    if mode == "signed":
        if not -0x8000 <= value <= 0x7FFF:
            raise ValueError(f"immediate {value} is out of range for signed 16-bit")
        return value & 0xFFFF
    raise ValueError("instruction does not use an immediate")


def _parse_memory_operand(token: str) -> tuple[int, int]:
    collapsed = token.replace(" ", "")
    match = re.fullmatch(r"(.+)\((\$[0-9]+)\)", collapsed)
    if match is None:
        raise ValueError(f"invalid memory operand {token!r}")

    immediate = _parse_int_literal(match.group(1))
    base_register = _parse_register(match.group(2))
    return immediate, base_register


def _build_r_word(rs: int, rt: int, rd: int, shamt: int, funct: int) -> str:
    return f"{0:06b}{rs:05b}{rt:05b}{rd:05b}{shamt:05b}{funct:06b}"


def _build_i_word(opcode: int, rs: int, rt: int, immediate: int) -> str:
    return f"{opcode:06b}{rs:05b}{rt:05b}{immediate:016b}"


def encode_assembly(text: str) -> str:
    mnemonic, operands = parse_assembly(text)
    spec = MNEMONIC_TO_SPEC.get(mnemonic)
    if spec is None:
        raise ValueError(f"unsupported mnemonic {mnemonic!r}")

    if spec.family == "R":
        if spec.operand_layout == "rd_rs_rt":
            if len(operands) != 3:
                raise ValueError(
                    f"{mnemonic} expects 3 operands: {mnemonic} $rd, $rs, $rt"
                )
            rd = _parse_register(operands[0])
            rs = _parse_register(operands[1])
            rt = _parse_register(operands[2])
            return bits_to_hex(_build_r_word(rs, rt, rd, 0, spec.funct or 0))

        if spec.operand_layout == "rd_rt_shamt":
            if len(operands) != 3:
                raise ValueError(
                    f"{mnemonic} expects 3 operands: {mnemonic} $rd, $rt, shamt"
                )
            rd = _parse_register(operands[0])
            rt = _parse_register(operands[1])
            shamt = _parse_int_literal(operands[2])
            if not 0 <= shamt <= 0x1F:
                raise ValueError(f"shift amount {shamt} is out of range for 5 bits")
            return bits_to_hex(_build_r_word(0, rt, rd, shamt, spec.funct or 0))

        if spec.operand_layout == "rs":
            if len(operands) != 1:
                raise ValueError(f"{mnemonic} expects 1 operand: {mnemonic} $rs")
            rs = _parse_register(operands[0])
            return bits_to_hex(_build_r_word(rs, 0, 0, 0, spec.funct or 0))

        if spec.operand_layout == "rd":
            if len(operands) != 1:
                raise ValueError(f"{mnemonic} expects 1 operand: {mnemonic} $rd")
            rd = _parse_register(operands[0])
            return bits_to_hex(_build_r_word(0, 0, rd, 0, spec.funct or 0))

        if spec.operand_layout == "rs_rt":
            if len(operands) != 2:
                raise ValueError(f"{mnemonic} expects 2 operands: {mnemonic} $rs, $rt")
            rs = _parse_register(operands[0])
            rt = _parse_register(operands[1])
            return bits_to_hex(_build_r_word(rs, rt, 0, 0, spec.funct or 0))

        raise ValueError(f"unsupported operand layout {spec.operand_layout!r}")

    if spec.operand_layout == "rt_rs_imm":
        if len(operands) != 3:
            raise ValueError(
                f"{mnemonic} expects 3 operands: {mnemonic} $rt, $rs, immediate"
            )
        rt = _parse_register(operands[0])
        rs = _parse_register(operands[1])
        immediate = _encode_immediate(_parse_int_literal(operands[2]), spec.immediate_mode)
        return bits_to_hex(_build_i_word(spec.opcode, rs, rt, immediate))

    if spec.operand_layout == "rt_imm_rs":
        if len(operands) != 2:
            raise ValueError(
                f"{mnemonic} expects 2 operands: {mnemonic} $rt, offset($rs)"
            )
        rt = _parse_register(operands[0])
        immediate_value, rs = _parse_memory_operand(operands[1])
        immediate = _encode_immediate(immediate_value, spec.immediate_mode)
        return bits_to_hex(_build_i_word(spec.opcode, rs, rt, immediate))

    if spec.operand_layout == "rs_rt_imm":
        if len(operands) != 3:
            raise ValueError(
                f"{mnemonic} expects 3 operands: {mnemonic} $rs, $rt, immediate"
            )
        rs = _parse_register(operands[0])
        rt = _parse_register(operands[1])
        immediate = _encode_immediate(_parse_int_literal(operands[2]), spec.immediate_mode)
        return bits_to_hex(_build_i_word(spec.opcode, rs, rt, immediate))

    if spec.operand_layout == "rs_imm":
        if len(operands) != 2:
            raise ValueError(f"{mnemonic} expects 2 operands: {mnemonic} $rs, immediate")
        rs = _parse_register(operands[0])
        immediate = _encode_immediate(_parse_int_literal(operands[1]), spec.immediate_mode)
        return bits_to_hex(_build_i_word(spec.opcode, rs, 0, immediate))

    if spec.operand_layout == "rt_imm":
        if len(operands) != 2:
            raise ValueError(f"{mnemonic} expects 2 operands: {mnemonic} $rt, immediate")
        rt = _parse_register(operands[0])
        immediate = _encode_immediate(_parse_int_literal(operands[1]), spec.immediate_mode)
        return bits_to_hex(_build_i_word(spec.opcode, 0, rt, immediate))

    raise ValueError(f"unsupported operand layout {spec.operand_layout!r}")
