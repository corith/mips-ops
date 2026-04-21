# mips-ops

`mips-ops` is a small command-line tool for encoding and decoding single MIPS
instructions.

The current implementation supports canonical R-type and I-type instructions.
It does not support J-type instructions, labels, pseudo-instructions, or
symbolic register aliases such as `$t0`.

## Supported Input

- Machine code decode input:
  - 8 hexadecimal digits such as `00412820`
  - 32 bits of binary such as `10001100101000110000000000000100`
- Assembly encode input:
  - Canonical lowercase mnemonics
  - Numeric registers only, from `$0` through `$31`
  - Canonical operand order for each instruction family

## Usage

Decode a machine word:

```text
python3 main.py decode 00412820
family: R
opcode: 000000
rs: 00010 ($2)
rt: 00001 ($1)
rd: 00101 ($5)
shamt: 00000
funct: 100000
assembly: add $5, $2, $1
```

Decode a binary word:

```text
python3 main.py decode 10001100101000110000000000000100
family: I
opcode: 100011
rs: 00101 ($5)
rt: 00011 ($3)
immediate: 0000000000000100 (4)
assembly: lw $3, 4($5)
```

Encode an assembly instruction:

```text
python3 main.py encode 'sw $7, 5($5)'
hex: aca70005
binary: 10101100101001110000000000000101
```

## Validation

Run the automated test suite from the repository root:

```text
python3 -m unittest discover -s tests -v
```

## Supported Mnemonics

R-type:
`add`, `addu`, `and`, `div`, `divu`, `jr`, `mfhi`, `mthi`, `mflo`, `mtlo`,
`mult`, `multu`, `nor`, `or`, `slt`, `sltu`, `sll`, `sra`, `srl`, `sub`,
`subu`, `xor`

I-type:
`addi`, `addiu`, `andi`, `beq`, `bgtz`, `blez`, `bne`, `lb`, `lbu`, `lh`,
`lhu`, `lui`, `lw`, `ori`, `sb`, `sh`, `slti`, `sltiu`, `sw`, `xori`
