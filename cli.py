import argparse

from bitfields import normalize_machine_word, split_field_bits
from decoder import decode_word, format_register
from encoder import encode_assembly


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Encode and decode single MIPS R-type and I-type instructions."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    decode_parser = subparsers.add_parser("decode", help="Decode a machine word")
    decode_parser.add_argument("word", help="8 hex digits or 32 bits of binary")

    encode_parser = subparsers.add_parser("encode", help="Encode an assembly string")
    encode_parser.add_argument(
        "assembly",
        nargs="+",
        help='Canonical assembly such as "add $5, $2, $1"',
    )
    return parser


def _print_decoded_instruction(word: str) -> None:
    decoded = decode_word(word)
    fields = split_field_bits(decoded.binary_word)

    print(f"family: {decoded.family}")
    print(f"opcode: {fields['opcode']}")
    print(f"rs: {fields['rs']} ({format_register(decoded.rs or 0)})")
    print(f"rt: {fields['rt']} ({format_register(decoded.rt or 0)})")

    if decoded.family == "R":
        print(f"rd: {fields['rd']} ({format_register(decoded.rd or 0)})")
        print(f"shamt: {fields['shamt']}")
        print(f"funct: {fields['funct']}")
    else:
        immediate_value = decoded.immediate if decoded.immediate is not None else 0
        print(f"immediate: {fields['immediate']} ({immediate_value})")

    print(f"assembly: {decoded.assembly}")


def _print_encoded_instruction(assembly: str) -> None:
    hex_word = encode_assembly(assembly)
    binary_word = normalize_machine_word(hex_word)
    print(f"hex: {hex_word}")
    print(f"binary: {binary_word}")


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "decode":
            _print_decoded_instruction(args.word)
        elif args.command == "encode":
            _print_encoded_instruction(" ".join(args.assembly))
        else:
            parser.error(f"unsupported command {args.command!r}")
    except ValueError as exc:
        print(f"error: {exc}")
        return 1

    return 0
