#!/usr/bin/env python3
import os
import re
import requests

def extract_plantuml_code(markdown_file):
    with open(markdown_file, 'r') as f:
        content = f.read()
    
    # Find all PlantUML code blocks
    pattern = r'```plantuml\n(.*?)```'
    matches = re.findall(pattern, content, re.DOTALL)
    return matches

def encode_plantuml(puml):
    import zlib
    str_bytes = puml.encode('utf-8')
    compressed = zlib.compress(str_bytes)
    res = ''
    for b in compressed[2:-4]:
        c1 = b >> 4 & 0xF
        c2 = b & 0xF
        res += chr(c1 + 0x30 if c1 < 10 else c1 + 0x57)
        res += chr(c2 + 0x30 if c2 < 10 else c2 + 0x57)
    return res

def main():
    # Create images directory if it doesn't exist
    os.makedirs('images', exist_ok=True)
    
    # Get PlantUML code blocks
    diagrams = extract_plantuml_code('../ResponseStreamingADR.md')
    
    # Generate images
    for i, diagram in enumerate(diagrams):
        output_file = f'images/streaming_{"context" if i == 0 else "container"}.png'
        encoded = encode_plantuml(diagram.strip())
        url = f'http://www.plantuml.com/plantuml/png/{encoded}'
        
        response = requests.get(url)
        if response.status_code == 200:
            with open(output_file, 'wb') as f:
                f.write(response.content)
            print(f'Generated {output_file}')
        else:
            print(f'Failed to generate {output_file}: {response.status_code}')

if __name__ == '__main__':
    main() 