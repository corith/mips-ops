import unittest

from decoder import decode_word


class DecoderTest(unittest.TestCase):
    def test_decode_add_word(self) -> None:
        decoded = decode_word("00412820")
        self.assertEqual(decoded.family, "R")
        self.assertEqual(decoded.mnemonic, "add")
        self.assertEqual(decoded.assembly, "add $5, $2, $1")

    def test_decode_lw_word(self) -> None:
        decoded = decode_word("8ca30004")
        self.assertEqual(decoded.family, "I")
        self.assertEqual(decoded.mnemonic, "lw")
        self.assertEqual(decoded.immediate, 4)
        self.assertEqual(decoded.assembly, "lw $3, 4($5)")

    def test_decode_sw_word(self) -> None:
        decoded = decode_word("aca70005")
        self.assertEqual(decoded.assembly, "sw $7, 5($5)")

    def test_decode_binary_word(self) -> None:
        decoded = decode_word("10001100101000110000000000000100")
        self.assertEqual(decoded.assembly, "lw $3, 4($5)")

    def test_decode_add_with_zero_register(self) -> None:
        decoded = decode_word("00602020")
        self.assertEqual(decoded.assembly, "add $4, $3, $0")

    def test_decode_load_from_zero_base(self) -> None:
        decoded = decode_word("8c0b0010")
        self.assertEqual(decoded.assembly, "lw $11, 16($0)")

    def test_decode_rejects_unsupported_opcode(self) -> None:
        with self.assertRaisesRegex(ValueError, "unsupported primary opcode"):
            decode_word("08000010")


if __name__ == "__main__":
    unittest.main()
