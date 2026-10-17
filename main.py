
from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes


# Generar el keystream con la clave y el nonce
def keystream_gen(clave_cifrado, nonce):

    keystream_generator = ChaCha20.new(key=clave_cifrado, nonce=nonce)

    return keystream_generator


# Cifrar el texto plano con ChaCha20
def cifrar_texto_chacha20(texto_plano, keystream_generator):

    texto_cifrado = keystream_generator.encrypt(texto_plano)

    print(f"Texto cifrado en bytes: {texto_cifrado}")
    print(f"Texto cifrado en hexadecimal: {texto_cifrado.hex()}")


# Comprobar el tamaño del nonce y probar uno de 12 bytes
def size_nonce(texto_plano, clave_cifrado, nonce):

    size_original_nonce = len(nonce)

    # Generar un nuevo nonce de 12 bytes
    nuevo_nonce = get_random_bytes(12)
    print(f"Nuevo nonce: {nuevo_nonce} bytes")
    print(f"Nuevo tamaño de nonce: {len(nuevo_nonce)} bytes")

    # Cifrar con el nuevo nonce
    keystream_generator = ChaCha20.new(key=clave_cifrado, nonce=nuevo_nonce)
    texto_cifrado = keystream_generator.encrypt(texto_plano)

    print(f"Texto cifrado en bytes: {texto_cifrado}")
    print(f"Texto cifrado en hexadecimal: {texto_cifrado.hex()}")


# Descifrar el texto cifrado
def descifrar_texto(texto_cifrado, keystream_generator):

    texto_descifrado = keystream_generator.decrypt(texto_cifrado)
    print(f"Este es mi texto descifrado: {texto_descifrado}")


# EXTRA: sincronizar el keystream cuando se pierden 8 bytes
def sincronizar_keystream(texto_cifrado, clave_cifrado, nonce):

    keystream_generator = ChaCha20.new(key=clave_cifrado, nonce=nonce)

    # Saltar los primeros 8 bytes del keystream
    keystream_generator.seek(8)

    texto_descifrado = keystream_generator.decrypt(texto_cifrado)

    print(f"Texto descifrado del EXTRA: {texto_descifrado}")
    print(f"Texto descifrado en hexadecimal: {texto_descifrado.hex()}")


if __name__ == "__main__":

    # Texto plano original
    texto_plano = "Este es un mensaje secreto que quiero cifrar".encode('utf-8')

    # Clave y nonce proporcionados en la actividad
    clave_cifrado = b'z\xe8~"\xcayW\x14g\x18+\x1c+\xf9\x80\x06P\x9ej\x888\xb4G\xdf\xe4\xc50,\x8dY\x80\x19'
    nonce = b'\xd6\x7f6\xc7\xe8i*\xa4'

    # Texto cifrado proporcionado para la Parte 2
    texto_cifrado = b'Ehq0\x83\xcb\x8fo\xab\xed\xd0S\x06\xcc\xbb\xecw\xe9\xec(\x1f\xc5E\xdb\x88\x18`W\xc3yQn\xad3\xec.\x08\x92\x8d\x8e\xbb%\x8f\x1a\xa6\xc9=\x15\x0f5\xaa'

    # Parte 1: cifrado
    keystream_generator = keystream_gen(clave_cifrado, nonce)
    cifrar_texto_chacha20(texto_plano, keystream_generator)

    # Comprobar el tamaño del nonce
    size_nonce(texto_plano, clave_cifrado, nonce)

    # Parte 2: descifrado
    keystream_generator = keystream_gen(clave_cifrado, nonce)
    descifrar_texto(texto_cifrado, keystream_generator)

    # EXTRA: texto cifrado recibido tras perder los primeros 8 bytes
    texto_cifrado_extra = b"\xad\xe2\x9a[C\xca\xa9\xadn\xf9\xaa)\x13\xc2X\x9e\x89\x19`C\xc4n\x1em\xf8?\xe7|\x0b\xd3\xdc\x8f\xacd\x85\x0c\xb8\xc3'\x1a\x12>"

    # Ejecutar el EXTRA
    sincronizar_keystream(texto_cifrado_extra, clave_cifrado, nonce)
