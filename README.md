# File Obfuscator & Uploader Helper

This very simple tool helps you bypass file upload restrictions for LLM models and other web apps placed by your network admin by:

- Base64-encoding any file  
- Obfuscating it using a fixed character shift  
- Splitting the result into 10 untyped segment files (`part_0` through `part_9`)  
- Generating a `README.txt` that documents how to reconstruct the original  
- Packaging everything into a single `.zip`


## Features

- Works with any file type: `.py`, `.pdf`, `.zip`, `.jpg`, you name it.
- No dangerous encryption—just safe obfuscation.
- Reconstructable by ChatGPT/Other LLM or locally.



## How It Works

1. Base64-encode the original file  
2. Shift each character’s ASCII value forward by a number you choose (e.g. `+3`)  
3. Save the result as 10 sequential parts (`part_0` to `part_9`)  
4. Create a `README.txt` with metadata:
   - Original filename
   - Shift value
   - Segment list
5. Zip everything into `[originalname]_obfuscated.zip`


## How to Use

```bash
python obfuscate_and_package.py
```

Then follow the prompts:
- Select your file
- Enter a shift value (e.g. 3)
- Upload the obfuscated zip should work. For heavily restricted env, upload the extensionless individual files



## To Reconstruct the File with ChatGPT

Upload all `part_*` files and `README.txt`, then paste this prompt:

```
Hi ChatGPT! I’ve used a custom Base64 + character shift obfuscation program to split a file into 10 segments. Each segment is named part_0 through part_9 and has no file extension. I’ve also included a README.txt in the same format generated by the tool, which tells you the original filename and the shift value.

Please:
1. Reconstruct the file by reading the parts in order.
2. Shift the characters **back** using the shift value from the README.
3. Base64-decode the result and save it using the filename from the README.
4. Show me a preview if you can.

Thanks!
```


## Local Reconstruction Script

Want a local decoder? You can write one like this:

```python
def shift_deobfuscate(data: str, shift: int) -> str:
    return ''.join(chr((ord(c) - shift) % 256) for c in data)
```

Just reverse the process:
- Concatenate the parts in order
- Deobfuscate using the same shift
- Base64-decode
- Save as the original file


## Output Example

```
output_20250408_183320/
├── part_0
├── part_1
├── ...
├── part_9
├── README.txt
└── sample_test_obfuscated.zip
```
