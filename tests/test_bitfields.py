import unittest

from bitfields import bits_to_hex, normalize_machine_word, split_field_bits, split_fields


class BitfieldsTest(unittest.TestCase):
    def test_normalize_hex_word_preserves_leading_zeroes(self) -> None:
        bits = normalize_machine_word("00412820")
        self.assertEqual(bits, "00000000010000010010100000100000")

    def test_split_fields_for_lw_word(self) -> None:
        bits = normalize_machine_word("8ca30004")
        self.assertEqual(
            split_field_bits(bits),
            {
                "opcode": "100011",
                "rs": "00101",
                "rt": "00011",
                "rd": "00000",
                "shamt": "00000",
                "funct": "000100",
                "immediate": "0000000000000100",
            },
        )
        self.assertEqual(split_fields(bits)["opcode"], 0x23)
        self.assertEqual(bits_to_hex(bits), "8ca30004")

    def test_rejects_short_machine_word(self) -> None:
        with self.assertRaisesRegex(ValueError, "8 hex digits or 32 bits"):
            normalize_machine_word("412820")


if __name__ == "__main__":
    unittest.main()
