import unittest

from decoder import decode_word
from encoder import encode_assembly


class EncoderTest(unittest.TestCase):
    def test_encode_add(self) -> None:
        self.assertEqual(encode_assembly("add $5, $2, $1"), "00412820")

    def test_encode_lw(self) -> None:
        self.assertEqual(encode_assembly("lw $3, 4($5)"), "8ca30004")

    def test_encode_sw(self) -> None:
        self.assertEqual(encode_assembly("sw $7, 5($5)"), "aca70005")

    def test_round_trip_golden_corpus(self) -> None:
        golden_words = [
            "00412820",
            "8ca30004",
            "aca70005",
            "00602020",
            "01093020",
            "ac06000c",
            "00c05020",
            "8c0b0010",
            "00000020",
            "002b6020",
        ]
        for word in golden_words:
            with self.subTest(word=word):
                assembly = decode_word(word).assembly
                self.assertEqual(encode_assembly(assembly), word)

    def test_rejects_out_of_range_register(self) -> None:
        with self.assertRaisesRegex(ValueError, "invalid register"):
            encode_assembly("add $32, $2, $1")


if __name__ == "__main__":
    unittest.main()
