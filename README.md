Project Overview

This project combines Vigenère cipher encryption and image-based steganography to securely hide and retrieve messages within a 24-bit BMP image. The goal is to first encrypt a message and then embed the encrypted data into an image file, allowing secret communication through media files.

---

Vigenère cipher encryption
-	Takes an input text file and outputs an encrypted or decrypted version.
-	Handles both uppercase and lowercase characters while leaving non-letter characters unchanged.

Image Steganography (BMP File)
-	Encrypting: Embeds ASCII values of the encrypted message into the red component of each pixel at regular intervals.
-	Decrypting: Extracts and reconstructs the hidden message from a specific color channel (red/green/blue) and writes it to output.txt.
