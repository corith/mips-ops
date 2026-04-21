# mips-ops

`mips-ops` is a small command-line tool for encoding and decoding single MIPS
instructions. It is designed around one instruction at a time, not whole source
files, and it is useful for checking coursework examples, verifying field
splits, and round-tripping between machine code and canonical assembly.

The current implementation supports canonical R-type and I-type instructions.
It does not support J-type instructions, labels, pseudo-instructions, multiple
lines of assembly, or symbolic register aliases such as `$t0` and `$a1`.

## What The Tool Does

The tool has two commands:

- `decode`: take a 32-bit machine word and print its fields plus canonical
  assembly.
- `encode`: take canonical assembly and print the 8-digit hexadecimal word plus
  the 32-bit binary word.

The decoder is table-driven. It normalizes the input into a 32-bit bitstring,
splits the instruction into the standard MIPS fields, resolves the opcode and
optional funct value, and then renders the canonical assembly form for that
instruction.

The encoder uses the same instruction tables in reverse. That keeps encode and
decode behavior aligned and makes round-trip validation possible.

## Supported Scope

Supported today:

- Single-instruction decode from:
  - 8 hexadecimal digits such as `00412820`
  - `0x`-prefixed hexadecimal such as `0x8ca30004`
  - 32 bits of binary such as `10001100101000110000000000000100`
- Single-instruction encode from canonical assembly
- Numeric register syntax only: `$0` through `$31`
- Decimal and hexadecimal immediate values in assembly
- Negative signed immediates where the instruction format allows them

Not supported today:

- J-type instructions such as `j` and `jal`
- Labels or symbolic branch targets
- Pseudo-instructions such as `move`
- Multi-line source files or assembler directives
- Symbolic register names such as `$t0`, `$s1`, or `$ra`

## Installation And Requirements

No third-party packages are required. The project uses only the Python standard
library.

Requirements:

- Python 3.10 or newer

Run commands from the repository root:

```text
cd /home/cory/code/mips-ops
```

## Command-Line Usage

### Decode A Machine Word

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

Decode also accepts binary input:

```text
python3 main.py decode 10001100101000110000000000000100
family: I
opcode: 100011
rs: 00101 ($5)
rt: 00011 ($3)
immediate: 0000000000000100 (4)
assembly: lw $3, 4($5)
```

And `0x`-prefixed hexadecimal:

```text
python3 main.py decode 0xaca70005
family: I
opcode: 101011
rs: 00101 ($5)
rt: 00111 ($7)
immediate: 0000000000000101 (5)
assembly: sw $7, 5($5)
```

### Encode Assembly

```text
python3 main.py encode 'sw $7, 5($5)'
hex: aca70005
binary: 10101100101001110000000000000101
```

Another example:

```text
python3 main.py encode 'add $12, $1, $11'
hex: 002b6020
binary: 00000000001010110110000000100000
```

### Important Shell Quoting Note

When you pass assembly on the command line, quote it with single quotes.
Registers use `$`, and most shells will try to expand `$5`, `$11`, and similar
tokens if you use double quotes or no quotes.

Use this:

```text
python3 main.py encode 'lw $11, 16($0)'
```

Do not rely on this:

```text
python3 main.py encode "lw $11, 16($0)"
```

## Canonical Assembly Syntax

The encoder intentionally accepts a narrow, predictable syntax. It is designed
to accept the same canonical strings that the decoder emits.

General rules:

- Mnemonics must be lowercase.
- Registers must be numeric: `$0` through `$31`.
- Operands must appear in canonical order.
- Commas are required between operands.
- Memory operands use `offset(base)` syntax such as `4($5)`.
- Immediate values can be decimal or hexadecimal.

Examples by operand layout:

- `add $5, $2, $1`
- `sub $4, $3, $0`
- `sll $8, $9, 4`
- `jr $31`
- `mfhi $2`
- `mult $4, $5`
- `addi $8, $8, -1`
- `andi $3, $3, 0xff`
- `lw $11, 16($0)`
- `sw $7, 5($5)`
- `beq $1, $2, -4`
- `lui $3, 0x1000`

## Immediate Semantics

Not every immediate is interpreted the same way. The tool follows the
instruction table in `isa.py`.

Signed 16-bit immediates:

- `addi`
- `addiu`
- `slti`
- `sltiu`
- `beq`
- `bne`
- `blez`
- `bgtz`
- `lb`
- `lh`
- `lw`
- `lbu`
- `lhu`
- `sb`
- `sh`
- `sw`

Unsigned 16-bit immediates:

- `andi`
- `ori`
- `xori`
- `lui`

That means:

- `addi $8, $8, -1` is valid.
- `sw $7, -4($29)` is valid.
- `andi $3, $3, -1` is rejected because `andi` is treated as an unsigned
  16-bit immediate operation.

## Supported Mnemonics

R-type:

- `add`
- `addu`
- `and`
- `div`
- `divu`
- `jr`
- `mfhi`
- `mthi`
- `mflo`
- `mtlo`
- `mult`
- `multu`
- `nor`
- `or`
- `sll`
- `slt`
- `sltu`
- `sra`
- `srl`
- `sub`
- `subu`
- `xor`

I-type:

- `addi`
- `addiu`
- `andi`
- `beq`
- `bgtz`
- `blez`
- `bne`
- `lb`
- `lbu`
- `lh`
- `lhu`
- `lui`
- `lw`
- `ori`
- `sb`
- `sh`
- `slti`
- `sltiu`
- `sw`
- `xori`

## Error Behavior

The tool fails with a user-readable error message and a non-zero exit code when
the input is malformed or unsupported.

Examples:

```text
python3 main.py decode 412820
error: machine word must be 8 hex digits or 32 bits of binary, got '412820'
```

```text
python3 main.py decode 08000010
error: unsupported primary opcode 0x02 for input 08000010
```

```text
python3 main.py encode 'add $32, $2, $1'
error: invalid register '$32'
```

## Validation

Run the automated test suite from the repository root:

```text
python3 -m unittest discover -s tests -v
```

The test suite currently covers:

- bitfield normalization
- field splitting
- golden decode cases from the sample corpus
- golden encode cases
- round-trip encode/decode behavior
- CLI output and CLI error handling

## Project Layout

- `main.py`: thin executable entrypoint
- `cli.py`: command-line parsing and user-facing output
- `bitfields.py`: input normalization, bit splitting, and sign extension helpers
- `isa.py`: canonical instruction tables and operand layouts
- `decoder.py`: machine-word to assembly conversion
- `encoder.py`: assembly to machine-word conversion
- `models.py`: decoded instruction data model
- `IOpsEnum.py`: integer opcode enum used by the instruction table
- `RfuncEnum.py`: integer funct enum used by the instruction table
- `tests/`: unit and CLI tests
- `.agent/mips-ops-execplan.md`: living implementation plan for the current MVP

## Development Notes

The project is intentionally narrow. The current codebase solves the
single-instruction round-trip problem first:

1. normalize machine code
2. split fields
3. resolve instruction metadata
4. render canonical assembly
5. encode canonical assembly back into the same machine word

If you extend the project later, the most natural next steps are:

1. add J-type instruction support
2. add symbolic register aliases
3. add labels and multi-line parsing
4. add pseudo-instruction expansion
