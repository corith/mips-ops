from dataclasses import dataclass

from IOpsEnum import Iops
from RfuncEnum import Rfuncs


@dataclass(frozen=True)
class InstructionSpec:
    mnemonic: str
    family: str
    opcode: int
    funct: int | None
    operand_layout: str
    immediate_mode: str = "none"


R_TYPE_FUNCTS: dict[int, InstructionSpec] = {
    int(Rfuncs.add): InstructionSpec("add", "R", 0x00, int(Rfuncs.add), "rd_rs_rt"),
    int(Rfuncs.addu): InstructionSpec(
        "addu", "R", 0x00, int(Rfuncs.addu), "rd_rs_rt"
    ),
    int(Rfuncs.and_): InstructionSpec(
        "and", "R", 0x00, int(Rfuncs.and_), "rd_rs_rt"
    ),
    int(Rfuncs.div): InstructionSpec("div", "R", 0x00, int(Rfuncs.div), "rs_rt"),
    int(Rfuncs.divu): InstructionSpec(
        "divu", "R", 0x00, int(Rfuncs.divu), "rs_rt"
    ),
    int(Rfuncs.jr): InstructionSpec("jr", "R", 0x00, int(Rfuncs.jr), "rs"),
    int(Rfuncs.mfhi): InstructionSpec("mfhi", "R", 0x00, int(Rfuncs.mfhi), "rd"),
    int(Rfuncs.mthi): InstructionSpec("mthi", "R", 0x00, int(Rfuncs.mthi), "rs"),
    int(Rfuncs.mflo): InstructionSpec("mflo", "R", 0x00, int(Rfuncs.mflo), "rd"),
    int(Rfuncs.mtlo): InstructionSpec("mtlo", "R", 0x00, int(Rfuncs.mtlo), "rs"),
    int(Rfuncs.mult): InstructionSpec("mult", "R", 0x00, int(Rfuncs.mult), "rs_rt"),
    int(Rfuncs.multu): InstructionSpec(
        "multu", "R", 0x00, int(Rfuncs.multu), "rs_rt"
    ),
    int(Rfuncs.nor): InstructionSpec("nor", "R", 0x00, int(Rfuncs.nor), "rd_rs_rt"),
    int(Rfuncs.or_): InstructionSpec("or", "R", 0x00, int(Rfuncs.or_), "rd_rs_rt"),
    int(Rfuncs.slt): InstructionSpec("slt", "R", 0x00, int(Rfuncs.slt), "rd_rs_rt"),
    int(Rfuncs.sltu): InstructionSpec(
        "sltu", "R", 0x00, int(Rfuncs.sltu), "rd_rs_rt"
    ),
    int(Rfuncs.sll): InstructionSpec("sll", "R", 0x00, int(Rfuncs.sll), "rd_rt_shamt"),
    int(Rfuncs.sra): InstructionSpec("sra", "R", 0x00, int(Rfuncs.sra), "rd_rt_shamt"),
    int(Rfuncs.srl): InstructionSpec("srl", "R", 0x00, int(Rfuncs.srl), "rd_rt_shamt"),
    int(Rfuncs.sub): InstructionSpec("sub", "R", 0x00, int(Rfuncs.sub), "rd_rs_rt"),
    int(Rfuncs.subu): InstructionSpec(
        "subu", "R", 0x00, int(Rfuncs.subu), "rd_rs_rt"
    ),
    int(Rfuncs.xor): InstructionSpec("xor", "R", 0x00, int(Rfuncs.xor), "rd_rs_rt"),
}

I_TYPE_OPCODES: dict[int, InstructionSpec] = {
    int(Iops.beq): InstructionSpec("beq", "I", int(Iops.beq), None, "rs_rt_imm", "signed"),
    int(Iops.bne): InstructionSpec("bne", "I", int(Iops.bne), None, "rs_rt_imm", "signed"),
    int(Iops.blez): InstructionSpec(
        "blez", "I", int(Iops.blez), None, "rs_imm", "signed"
    ),
    int(Iops.bgtz): InstructionSpec(
        "bgtz", "I", int(Iops.bgtz), None, "rs_imm", "signed"
    ),
    int(Iops.addi): InstructionSpec(
        "addi", "I", int(Iops.addi), None, "rt_rs_imm", "signed"
    ),
    int(Iops.addiu): InstructionSpec(
        "addiu", "I", int(Iops.addiu), None, "rt_rs_imm", "signed"
    ),
    int(Iops.slti): InstructionSpec(
        "slti", "I", int(Iops.slti), None, "rt_rs_imm", "signed"
    ),
    int(Iops.sltiu): InstructionSpec(
        "sltiu", "I", int(Iops.sltiu), None, "rt_rs_imm", "signed"
    ),
    int(Iops.andi): InstructionSpec(
        "andi", "I", int(Iops.andi), None, "rt_rs_imm", "unsigned"
    ),
    int(Iops.ori): InstructionSpec(
        "ori", "I", int(Iops.ori), None, "rt_rs_imm", "unsigned"
    ),
    int(Iops.xori): InstructionSpec(
        "xori", "I", int(Iops.xori), None, "rt_rs_imm", "unsigned"
    ),
    int(Iops.lui): InstructionSpec(
        "lui", "I", int(Iops.lui), None, "rt_imm", "unsigned"
    ),
    int(Iops.lb): InstructionSpec("lb", "I", int(Iops.lb), None, "rt_imm_rs", "signed"),
    int(Iops.lh): InstructionSpec("lh", "I", int(Iops.lh), None, "rt_imm_rs", "signed"),
    int(Iops.lw): InstructionSpec("lw", "I", int(Iops.lw), None, "rt_imm_rs", "signed"),
    int(Iops.lbu): InstructionSpec(
        "lbu", "I", int(Iops.lbu), None, "rt_imm_rs", "signed"
    ),
    int(Iops.lhu): InstructionSpec(
        "lhu", "I", int(Iops.lhu), None, "rt_imm_rs", "signed"
    ),
    int(Iops.sb): InstructionSpec("sb", "I", int(Iops.sb), None, "rt_imm_rs", "signed"),
    int(Iops.sh): InstructionSpec("sh", "I", int(Iops.sh), None, "rt_imm_rs", "signed"),
    int(Iops.sw): InstructionSpec("sw", "I", int(Iops.sw), None, "rt_imm_rs", "signed"),
}

MNEMONIC_TO_SPEC: dict[str, InstructionSpec] = {
    spec.mnemonic: spec for spec in [*R_TYPE_FUNCTS.values(), *I_TYPE_OPCODES.values()]
}
