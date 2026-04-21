# Complete The Single-Instruction MIPS Encoder/Decoder CLI

This ExecPlan is a living document. The sections `Progress`, `Surprises & Discoveries`, `Decision Log`, and `Outcomes & Retrospective` must be kept up to date as work proceeds.

This plan was authored in accordance with `/home/cory/code/ios/Silverback/.agent/PLANS.md`. That guidance file is not checked into this repository, so all required context is restated here.

## Purpose / Big Picture

After this work, a user will be able to run one command to decode a single MIPS instruction word into its six bit fields and a canonical assembly string, and run one command to encode the same canonical assembly string back into machine code. The observable outcome is a small, reliable coursework tool: `python3 main.py decode 00412820` reports `add $5, $2, $1`, and `python3 main.py encode "sw $7, 5($5)"` reports `aca70005`.

This plan intentionally finishes the project that is already visible in the repository rather than expanding it into a simulator or full assembler. The repository currently points toward a single-instruction encoder/decoder, and the milestones below complete that path end to end.

## Progress

- [x] (2026-04-21 16:52Z) Read the repository, git history, and `/home/cory/code/ios/Silverback/.agent/PLANS.md` to infer the intended destination and planning format.
- [x] (2026-04-21 16:52Z) Confirmed the current implementation is a prototype decoder with partial opcode tables and a dirty working tree in `main.py`.
- [ ] Freeze the supported instruction subset and correct the opcode/funct tables so the data model is trustworthy.
- [ ] Replace print-driven decode logic with pure parse/decode functions and golden tests based on the worked examples in `instructions.txt`.
- [ ] Add the reverse assembly-to-machine encoder for the same subset and prove round-trip behavior with automated tests.
- [ ] Replace the debug-heavy entrypoint with a clean CLI and update `README.md` so a new user can run the tool without reading the source.

## Surprises & Discoveries

- Observation: `instructions.txt` is not product documentation; it is class-assignment material about forwarding and hazards, but it contains the only realistic sample corpus in the repo.
  Evidence: `instructions.txt` includes forwarding commentary at the top and annotated words such as `00412820`, `8ca30004`, and `aca70005`.

- Observation: the current decoder loses leading zero bits, so R-type instructions with opcode `000000` are sliced incorrectly.
  Evidence: `main.py` uses `bin(int(instruction, 16))[2:]` without left-padding, and `printf '00412820\n' | python3 main.py` currently prints `100000`, `10010`, `10000`, `01000`, `00` instead of a full 32-bit split.

- Observation: the prompt promises more formats than the program can actually parse.
  Evidence: `main.py` asks for “binary or assembly format” but both decode paths immediately call `int(..., 16)`.

- Observation: the opcode tables are incomplete and contain naming/value mistakes that will corrupt later work if they are treated as authoritative without audit.
  Evidence: `IOpsEnum.py` defines `addiu = 0x08` and `lb = 0x09`, and `RfuncEnum.py` uses `nd` and `orr` instead of canonical `and` and `or`.

- Observation: the working tree is already dirty.
  Evidence: `git status --short` reports `M main.py`. Any implementation must preserve or consciously fold forward that change instead of discarding it.

## Decision Log

- Decision: treat the intended end-state as a single-instruction MIPS encoder/decoder CLI, not a pipeline simulator, emulator, or full assembler.
  Rationale: `README.md` promises encoding and decoding, `main.py` is an interactive instruction parser, and there is no execution model, memory model, or pipeline code anywhere in the repo.
  Date/Author: 2026-04-21 / Codex

- Decision: finish a correct R-type and I-type MVP first, and defer J-type instructions and pseudo-instructions to a later extension.
  Rationale: the existing enums and the worked examples in `instructions.txt` are all R-type or I-type, so this is the smallest scope that completes the current project honestly.
  Date/Author: 2026-04-21 / Codex

- Decision: use canonical numeric register syntax in v1 output and tests, such as `$5` and `$11`, rather than symbolic aliases such as `$a1` or `$t3`.
  Rationale: the sample corpus already uses numeric registers, numeric syntax avoids alias ambiguity, and it keeps the first implementation focused on encode/decode correctness.
  Date/Author: 2026-04-21 / Codex

- Decision: use only the Python standard library for the completed tool.
  Rationale: the repo has no dependency or packaging setup, and the required work can be handled with `argparse`, `dataclasses`, `enum`, and `unittest`.
  Date/Author: 2026-04-21 / Codex

## Outcomes & Retrospective

Initial planning outcome: the repository appears to be an unfinished coursework-oriented MIPS encoder/decoder. The missing pieces are a trustworthy instruction table, a structured decode model, the reverse encode path, automated tests, and a CLI contract that matches the prompts and README. No implementation work has been performed yet; this document exists to make the next implementation pass self-contained and restartable.

## Context and Orientation

The current repository is very small. `main.py` is the only executable module. It mixes user input, bit slicing, opcode detection, and debug prints in one file. `IOpsEnum.py` and `RfuncEnum.py` are the beginnings of instruction lookup tables, but they are only mnemonic-to-number lists and do not yet describe operand layouts. `README.md` is a two-line statement of intent. `instructions.txt` is the only meaningful corpus of sample instructions and is the best source for golden test cases even though it was clearly written for a separate forwarding assignment.

Several terms matter here. A “primary opcode” is the first six bits of a 32-bit MIPS instruction. An “R-type” instruction is one whose primary opcode is `000000`, where the real operation is chosen by the six-bit “funct” field at the end of the word. An “I-type” instruction uses the primary opcode directly and carries a 16-bit immediate value. A “decoder” takes a machine word such as `00412820` and turns it into a structured description such as `add $5, $2, $1`. An “encoder” does the reverse. A “round-trip” means the tool can decode a word and then encode the resulting assembly back to the original word, or encode an assembly string and decode it back to the same canonical assembly.

The current code does not yet have a stable internal representation for a decoded instruction. That is the main architectural gap. Without a structured instruction object, every new feature becomes more print statements and string comparisons. The first real completion step is to create a data model that everything else can share.

## Milestones

### Milestone 1: Freeze the MVP contract and build a trustworthy instruction model

At the end of this milestone, the repository will have a clear answer to “what does this tool support?” and the core code will no longer depend on ad hoc string slicing in `main.py`. Create a small set of pure modules at the repository root: `models.py` for data classes, `isa.py` for opcode and funct tables, and `bitfields.py` for normalization and field extraction. Preserve the current `main.py` file until the new modules are validated, but stop adding decode logic there. Correct the mnemonic names and opcode values already present in `IOpsEnum.py` and `RfuncEnum.py`, or replace those files with thin compatibility wrappers that import the canonical tables from `isa.py`.

This milestone is accepted when a reader can point to one authoritative instruction table and one authoritative decoded-instruction shape, and when automated tests prove that `00412820` normalizes to a full 32-bit bitstring beginning with `000000` instead of losing its leading zeros.

### Milestone 2: Finish hex and binary decode for the supported subset

At the end of this milestone, the tool will correctly decode one machine instruction word into a structured result and a canonical assembly string. Implement `decode_word(raw: str) -> DecodedInstruction` in `decoder.py`. The function must accept either an 8-digit hexadecimal word such as `8ca30004` or a 32-character binary word such as `10001100101000110000000000000100`. It must reject malformed lengths and unsupported instructions with explicit error messages. Use the six split fields and the instruction tables to dispatch R-type and I-type instructions, and format operands canonically as numeric registers.

This milestone is accepted when the annotated samples in `instructions.txt` decode correctly. At minimum, `00412820` must decode to `add $5, $2, $1`, `8ca30004` to `lw $3, 4($5)`, `aca70005` to `sw $7, 5($5)`, `00602020` to `add $4, $3, $0`, and `002b6020` to `add $12, $1, $11`. Acceptance also requires a test proving that malformed input such as `412820` or an unsupported opcode fails cleanly instead of producing partial output.

### Milestone 3: Add assembly-to-machine encoding for the same subset

At the end of this milestone, the tool will support the reverse direction for the exact same instruction subset. Implement `encode_assembly(text: str) -> str` in `encoder.py`. Support canonical assembly syntax only in v1: lowercase mnemonic names, registers written numerically as `$0` through `$31`, commas between operands, and the standard base+offset form for load/store instructions such as `lw $3, 4($5)`. Do not attempt macro expansion, labels, alias registers, or pseudo-instructions in this milestone.

This milestone is accepted when the worked instructions from `instructions.txt` round-trip. `encode_assembly("add $5, $2, $1")` must return `00412820`, `encode_assembly("lw $3, 4($5)")` must return `8ca30004`, and `encode_assembly("sw $7, 5($5)")` must return `aca70005`. In addition, automated tests must prove that `encode_assembly(decode_word(word).assembly)` reproduces the original machine word for the golden corpus.

### Milestone 4: Ship a usable CLI and documentation

At the end of this milestone, a new user will be able to install nothing, read one short README, and use the tool reliably from the command line. Replace the interactive-only behavior in `main.py` with an `argparse` CLI that supports `decode` and `encode` subcommands. Keep the implementation thin by delegating all real work to `decoder.py` and `encoder.py`. If desired, preserve an interactive fallback when no arguments are provided, but the subcommands are the acceptance path because they are testable and unambiguous.

This milestone is accepted when `README.md` documents the exact supported syntax, the exact commands to run, and the expected outputs for at least one decode example and one encode example. It is also accepted only when `python3 -m unittest discover -s tests -v` passes and the CLI produces clean output with no debug leftovers such as the unconditional `add` and `5` currently printed after `main()`.

## Plan of Work

Start by extracting the domain model out of `main.py`. Create `models.py` with a frozen `DecodedInstruction` data class that stores the instruction family, mnemonic, opcode, optional funct, register numbers, optional immediate, the normalized 32-bit binary string, and the canonical 8-digit lowercase hexadecimal string. Create `isa.py` with a small `InstructionSpec` data class or equivalent record that tells the decoder how to interpret operands for each supported mnemonic. The supported operand layouts in v1 should be `rd, rs, rt` for arithmetic R-type instructions, `rt, immediate(rs)` for loads and stores, and `rd, rs, $0`-style cases should still render explicitly as `$0` rather than trying to simplify them.

Once the model exists, implement normalization and field extraction in `bitfields.py`. Define `normalize_machine_word(raw: str) -> str` so it accepts either hex or binary input and always returns a 32-character binary string. Define `split_fields(bits: str) -> dict[str, int]` so it returns integer field values for `opcode`, `rs`, `rt`, `rd`, `shamt`, `funct`, and `immediate`. This module must be pure and easy to test because every later step depends on it.

Then implement `decode_word` in `decoder.py`. Use the normalized bit fields and `isa.py` tables to select the instruction spec and build a `DecodedInstruction`. R-type decode must branch on opcode `0`, then use the funct table. I-type decode must branch on the primary opcode table. Any unsupported opcode or funct value must raise a clear `ValueError` containing the unknown value and input word.

After decode is stable, implement `parse_assembly` and `encode_assembly` in `encoder.py`. Keep the assembly grammar intentionally small. Parse only the canonical syntax that the decoder emits. This is an important design choice because it guarantees the round-trip tests are strict and predictable. Encoding should use the same instruction table as decoding so the mappings cannot drift apart.

With pure encode/decode functions in place, refactor `main.py` into a thin wrapper over `cli.py`. Define `main(argv: list[str] | None = None) -> int` in `cli.py`, wire `argparse` subcommands there, and keep formatting logic out of the parser. `main.py` should become little more than `from cli import main` and `raise SystemExit(main())` or the equivalent `sys.exit(main())`.

Finally, write tests before polishing the README. Create `tests/test_bitfields.py` for normalization and field splitting, `tests/test_decoder.py` for golden decode cases and error handling, `tests/test_encoder.py` for golden encode cases and round-trip behavior, and `tests/test_cli.py` for the user-visible command output. Use the sample machine words already present in `instructions.txt` as fixtures. Expand only as needed to cover every supported operand layout.

## Concrete Steps

Run every command from the repository root:

    cd /home/cory/code/mips-ops

Create the new modules and test directory, then implement the data model and tables:

    mkdir -p tests
    $EDITOR models.py isa.py bitfields.py decoder.py encoder.py cli.py

Run the test suite frequently while building out the pure functions:

    python3 -m unittest discover -s tests -v

During Milestone 2, the expected transcript should include successful decode tests named after the golden corpus:

    test_decode_add_word ... ok
    test_decode_lw_word ... ok
    test_decode_sw_word ... ok
    test_decode_rejects_short_word ... ok
    OK

Once the CLI exists, the main acceptance commands should look like this:

    python3 main.py decode 00412820
    family: R
    opcode: 000000
    rs: 00010 ($2)
    rt: 00001 ($1)
    rd: 00101 ($5)
    shamt: 00000
    funct: 100000
    assembly: add $5, $2, $1

    python3 main.py decode 10001100101000110000000000000100
    family: I
    opcode: 100011
    rs: 00101 ($5)
    rt: 00011 ($3)
    immediate: 0000000000000100 (4)
    assembly: lw $3, 4($5)

    python3 main.py encode "sw $7, 5($5)"
    hex: aca70005
    binary: 10101100101001110000000000000101

If an instruction is outside the supported subset, the CLI must fail explicitly and non-destructively:

    python3 main.py decode 08000010
    error: unsupported primary opcode 0x02 for input 08000010

## Validation and Acceptance

Validation is complete only when the tool proves useful from both directions. Run `python3 -m unittest discover -s tests -v` and expect the golden decode tests, golden encode tests, round-trip tests, and CLI tests to pass. The most important named behaviors are: zero-padded normalization for R-type words, correct decode of the worked examples in `instructions.txt`, correct encode of the same examples, and clean rejection of malformed or unsupported inputs.

Then run the CLI manually from `/home/cory/code/mips-ops`. `python3 main.py decode 00412820` must show the full six-field split and the canonical assembly `add $5, $2, $1`. `python3 main.py encode "add $12, $1, $11"` must produce `002b6020`. `python3 main.py decode 8c0b0010` must show `lw $11, 16($0)`. `python3 main.py encode "lw $11, 16($0)"` must produce `8c0b0010`. These manual checks matter because they verify both the machine-readable logic and the human-readable formatting.

The README is accepted only when a novice can follow it without opening the source. It must name the supported subset, name the unsupported features, and show at least one decode transcript and one encode transcript that match the real CLI output.

## Idempotence and Recovery

The work in this plan is intentionally additive and can be repeated safely. Creating pure modules and tests is idempotent as long as file contents are updated rather than duplicated. The command `python3 -m unittest discover -s tests -v` is safe to rerun after every edit. If the CLI refactor in `main.py` fails midway, keep `main.py` as a thin wrapper over the previous behavior until the new `cli.py` is passing tests, then switch the wrapper in one small change.

The current working tree already contains an uncommitted change to `main.py`. Do not discard it with destructive git commands. Read it carefully, fold any useful intent forward into the new structure, and only remove old code after the new modules and tests cover the same behavior. If the opcode table audit reveals mistakes, fix the tests and the canonical tables in the same commit so the repo never has a knowingly wrong “source of truth.”

## Artifacts and Notes

Current broken behavior worth preserving as a regression test:

    $ printf '00412820\n' | python3 main.py
    32 bit instruction
    100000
    10010
    10000
    01000
    00

Desired decode behavior after Milestone 2:

    $ python3 main.py decode 00412820
    family: R
    opcode: 000000
    rs: 00010 ($2)
    rt: 00001 ($1)
    rd: 00101 ($5)
    shamt: 00000
    funct: 100000
    assembly: add $5, $2, $1

Desired round-trip property after Milestone 3:

    >>> encode_assembly(decode_word("aca70005").assembly)
    'aca70005'

## Interfaces and Dependencies

Use only the Python standard library. No third-party parser, test runner, or CLI package is required.

In `models.py`, define:

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

In `isa.py`, define:

    @dataclass(frozen=True)
    class InstructionSpec:
        mnemonic: str
        family: str
        opcode: int
        funct: int | None
        operand_layout: str

    R_TYPE_FUNCTS: dict[int, InstructionSpec]
    I_TYPE_OPCODES: dict[int, InstructionSpec]

In `bitfields.py`, define:

    def normalize_machine_word(raw: str) -> str: ...
    def split_fields(bits: str) -> dict[str, int]: ...

In `decoder.py`, define:

    def decode_word(raw: str) -> DecodedInstruction: ...

In `encoder.py`, define:

    def parse_assembly(text: str) -> tuple[str, list[str]]: ...
    def encode_assembly(text: str) -> str: ...

In `cli.py`, define:

    def main(argv: list[str] | None = None) -> int: ...

Plan revision note: 2026-04-21. Initial ExecPlan created after repository reconnaissance and agent-assisted intent inference so the project can be completed as a self-contained, milestone-driven MVP.
