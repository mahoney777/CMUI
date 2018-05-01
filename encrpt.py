def VernamCipherFunction(text, key):
      result = "";
      ptr = 0;
      for char in text:
            result = result + chr(ord(char) ^ ord(key[ptr]));
            ptr = ptr + 1;
            if ptr == len(key):
                  ptr = 0;
      return result
                      
encryption_key = "fwkbfkwbifwbbw828";
 
while True:
      input_text = input("\nEnter Text To Encrypt:\t");
      encryption = VernamCipherFunction(input_text, encryption_key);
      print("\nEncrypted Vernam Cipher Text:\t" + encryption);
      decryption = VernamCipherFunction(encryption, encryption_key);
      print("\nDecrypted Vernam Cipher Text:\t" + decryption);


