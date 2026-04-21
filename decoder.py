from bitfields import bits_to_hex, normalize_machine_word, sign_extend, split_fields
from isa import I_TYPE_OPCODES, R_TYPE_FUNCTS, InstructionSpec
from models import DecodedInstruction


def format_register(register: int) -> str:
    return f"${register}"


def _decode_immediate(spec: InstructionSpec, raw_immediate: int) -> int:
    if spec.immediate_mode == "unsigned":
        return raw_immediate
    if spec.immediate_mode == "signed":
        return sign_extend(raw_immediate, 16)
    raise ValueError(f"instruction {spec.mnemonic} does not use an immediate")


def _format_assembly(spec: InstructionSpec, fields: dict[str, int], immediate: int | None) -> str:
    if spec.operand_layout == "rd_rs_rt":
        return (
            f"{spec.mnemonic} {format_register(fields['rd'])}, "
            f"{format_register(fields['rs'])}, {format_register(fields['rt'])}"
        )
    if spec.operand_layout == "rd_rt_shamt":
        return (
            f"{spec.mnemonic} {format_register(fields['rd'])}, "
            f"{format_register(fields['rt'])}, {fields['shamt']}"
        )
    if spec.operand_layout == "rs":
        return f"{spec.mnemonic} {format_register(fields['rs'])}"
    if spec.operand_layout == "rd":
        return f"{spec.mnemonic} {format_register(fields['rd'])}"
    if spec.operand_layout == "rs_rt":
        return (
            f"{spec.mnemonic} {format_register(fields['rs'])}, "
            f"{format_register(fields['rt'])}"
        )
    if spec.operand_layout == "rt_rs_imm":
        return (
            f"{spec.mnemonic} {format_register(fields['rt'])}, "
            f"{format_register(fields['rs'])}, {immediate}"
        )
    if spec.operand_layout == "rt_imm_rs":
        return (
            f"{spec.mnemonic} {format_register(fields['rt'])}, "
            f"{immediate}({format_register(fields['rs'])})"
        )
    if spec.operand_layout == "rs_rt_imm":
        return (
            f"{spec.mnemonic} {format_register(fields['rs'])}, "
            f"{format_register(fields['rt'])}, {immediate}"
        )
    if spec.operand_layout == "rs_imm":
        return f"{spec.mnemonic} {format_register(fields['rs'])}, {immediate}"
    if spec.operand_layout == "rt_imm":
        return f"{spec.mnemonic} {format_register(fields['rt'])}, {immediate}"
    raise ValueError(f"unsupported operand layout {spec.operand_layout!r}")


def decode_word(raw: str) -> DecodedInstruction:
    bits = normalize_machine_word(raw)
    fields = split_fields(bits)
    hex_word = bits_to_hex(bits)
    opcode = fields["opcode"]

    if opcode == 0x00:
        funct = fields["funct"]
        spec = R_TYPE_FUNCTS.get(funct)
        if spec is None:
            raise ValueError(f"unsupported funct 0x{funct:02x} for input {hex_word}")
        assembly = _format_assembly(spec, fields, None)
        return DecodedInstruction(
            family=spec.family,
            mnemonic=spec.mnemonic,
            opcode=opcode,
            rs=fields["rs"],
            rt=fields["rt"],
            rd=fields["rd"],
            shamt=fields["shamt"],
            funct=funct,
            immediate=None,
            binary_word=bits,
            hex_word=hex_word,
            assembly=assembly,
        )

    spec = I_TYPE_OPCODES.get(opcode)
    if spec is None:
        raise ValueError(f"unsupported primary opcode 0x{opcode:02x} for input {hex_word}")

    immediate = _decode_immediate(spec, fields["immediate"])
    assembly = _format_assembly(spec, fields, immediate)
    return DecodedInstruction(
        family=spec.family,
        mnemonic=spec.mnemonic,
        opcode=opcode,
        rs=fields["rs"],
        rt=fields["rt"],
        rd=None,
        shamt=None,
        funct=None,
        immediate=immediate,
        binary_word=bits,
        hex_word=hex_word,
        assembly=assembly,
    )
