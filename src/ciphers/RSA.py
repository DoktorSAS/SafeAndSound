"""
    # This code has been inspired and adapted from the insightful work at TheAlgorithms/Python repository.
    # A heartfelt thank you to the dedicated contributors of https://github.com/TheAlgorithms/Python 
    # for generously sharing their expertise on cipher algorithms, enhancing our project with their open-source spirit. 
"""

import os
import sys

DEFAULT_BLOCK_SIZE = 128
BYTE_SIZE = 256

def get_blocks_from_text(
    message: str, block_size: int = DEFAULT_BLOCK_SIZE
) -> list[int]:
    message_bytes = message.encode("ascii")

    block_ints = []
    for block_start in range(0, len(message_bytes), block_size):
        block_int = 0
        for i in range(block_start, min(block_start + block_size, len(message_bytes))):
            block_int += message_bytes[i] * (BYTE_SIZE ** (i % block_size))
        block_ints.append(block_int)
    return block_ints


def get_text_from_blocks(
    block_ints: list[int], message_length: int, block_size: int = DEFAULT_BLOCK_SIZE
) -> str:
    message: list[str] = []
    for block_int in block_ints:
        block_message: list[str] = []
        for i in range(block_size - 1, -1, -1):
            if len(message) + i < message_length:
                ascii_number = block_int // (BYTE_SIZE**i)
                block_int = block_int % (BYTE_SIZE**i)
                block_message.insert(0, chr(ascii_number))
        message.extend(block_message)
    return "".join(message)


def encrypt_message(
    message: str, key: tuple[int, int], block_size: int = DEFAULT_BLOCK_SIZE
) -> list[int]:
    encrypted_blocks = []
    n, e = key

    for block in get_blocks_from_text(message, block_size):
        encrypted_blocks.append(pow(block, e, n))
    return encrypted_blocks


def decrypt_message(
    encrypted_blocks: list[int],
    message_length: int,
    key: tuple[int, int],
    block_size: int = DEFAULT_BLOCK_SIZE,
) -> str:
    decrypted_blocks = []
    n, d = key
    for block in encrypted_blocks:
        decrypted_blocks.append(pow(block, d, n))
    return get_text_from_blocks(decrypted_blocks, message_length, block_size)


def read_key_file(key_filename: str) -> tuple[int, int, int]:
    with open(key_filename) as fo:
        content = fo.read()
    key_size, n, eor_d = content.split(",")
    return (int(key_size), int(n), int(eor_d))


def encrypt_and_write_to_file(
    message_filename: str,
    key_filename: str,
    message: str,
    block_size: int = DEFAULT_BLOCK_SIZE,
) -> str:
    key_size, n, e = read_key_file(key_filename)
    if key_size < block_size * 8:
        sys.exit(
            f"ERROR: Block size is {block_size * 8} bits and key size is {key_size} "
            "bits. The RSA cipher requires the block size to be equal to or greater "
            "than the key size. Either decrease the block size or use different keys."
        )

    encrypted_blocks = [str(i) for i in encrypt_message(message, (n, e), block_size)]

    encrypted_content = ",".join(encrypted_blocks)
    encrypted_content = f"{len(message)}_{block_size}_{encrypted_content}"
    with open(message_filename, "w") as fo:
        fo.write(encrypted_content)
    return encrypted_content


def read_from_file_and_decrypt(message_filename: str, key_filename: str) -> str:
    key_size, n, d = read_key_file(key_filename)
    with open(message_filename) as fo:
        content = fo.read()
    message_length_str, block_size_str, encrypted_message = content.split("_")
    message_length = int(message_length_str)
    block_size = int(block_size_str)

    if key_size < block_size * 8:
        sys.exit(
            f"ERROR: Block size is {block_size * 8} bits and key size is {key_size} "
            "bits. The RSA cipher requires the block size to be equal to or greater "
            "than the key size. Were the correct key file and encrypted file specified?"
        )

    encrypted_blocks = []
    for block in encrypted_message.split(","):
        encrypted_blocks.append(int(block))

    return decrypt_message(encrypted_blocks, message_length, (n, d), block_size)