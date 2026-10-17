# PE 89.1 — Fundamentos ChaCha20

## Descripción

Actividad práctica de criptografía con Python y la librería PyCryptodome. El objetivo es aprender a cifrar y descifrar mensajes utilizando ChaCha20, comprender la importancia de la clave y el nonce y estudiar cómo recuperar la sincronización del keystream.

## Requisitos

- Python 3
- PyCryptodome
- Entorno virtual de Python (`.venv`)

## Preparación del entorno

Activar el entorno virtual:

```bash
source .venv/bin/activate
```

Ejecutar el programa:

```bash
python3 main.py
```

## Parte 1 — Cifrado con ChaCha20

### Datos utilizados

**Texto plano:**

```text
Este es un mensaje secreto que quiero cifrar
```

**Clave de cifrado:**

```python
b'z\xe8~"\xcayW\x14g\x18+\x1c+\xf9\x80\x06P\x9ej\x888\xb4G\xdf\xe4\xc50,\x8dY\x80\x19'
```

**Nonce original:**

```python
b'\xd6\x7f6\xc7\xe8i*\xa4'
```

### Resultado del cifrado

El programa genera el siguiente texto cifrado en hexadecimal:

```text
4568713083cb8f6fabedd05306ccbbec77e9ec281fc545db88186057c379516ead33ec2e08929f92b8778a0d
```

### Preguntas y respuestas

**1. ¿Cuál es el texto cifrado resultante?**

El texto cifrado en hexadecimal es:

```text
4568713083cb8f6fabedd05306ccbbec77e9ec281fc545db88186057c379516ead33ec2e08929f92b8778a0d
```

**2. ¿Qué tamaño tiene el nonce utilizado para cifrar el texto plano?**

El nonce tiene un tamaño de **8 bytes (64 bits)**.

**3. ¿Puedes utilizar un nonce de mayor tamaño, por ejemplo, de 12 o 16 bytes?**

La implementación de ChaCha20 de PyCryptodome admite nonces de 8 o 12 bytes. Por tanto, podemos utilizar uno de 12 bytes, como hemos comprobado en el programa, pero no uno de 16 bytes con esta implementación.

**4. ¿Qué implicaciones de seguridad tiene utilizar un nonce de mayor tamaño?**

Un nonce de mayor tamaño permite disponer de más valores posibles y puede reducir la probabilidad de colisiones cuando se genera correctamente. Sin embargo, un nonce más largo no hace que el cifrado sea automáticamente más seguro. Lo fundamental es no reutilizar la misma combinación de clave y nonce.

**5. ¿Qué riesgos existen si se reutiliza la misma clave y el mismo nonce para cifrar dos mensajes diferentes?**

ChaCha20 genera un flujo de claves (*keystream*) a partir de la clave y el nonce. Si ambos se reutilizan, se vuelve a utilizar el mismo flujo de claves.

Esto puede permitir que un atacante relacione los mensajes cifrados y obtenga información sobre sus contenidos. Si conoce uno de los textos planos, puede utilizarlo para recuperar información del otro.

Por este motivo, es fundamental utilizar un nonce único con cada clave.

**6. ¿Qué diferencias existen entre ChaCha20 y ChaCha20-Poly1305 en cuanto a confidencialidad e integridad?**

- **ChaCha20:** proporciona confidencialidad porque cifra los datos, pero por sí solo no garantiza la integridad ni la autenticidad del mensaje.
- **ChaCha20-Poly1305:** combina el cifrado ChaCha20 con la autenticación Poly1305. Además de proteger la confidencialidad, permite detectar modificaciones no autorizadas y verificar la autenticidad de los datos mediante una etiqueta de autenticación.

## Prueba adicional — Nonce de 12 bytes

En el programa se genera un nuevo nonce de 12 bytes mediante `get_random_bytes(12)`.

El mensaje se cifra utilizando este nuevo nonce y se muestra el resultado en bytes y hexadecimal.

Como el nonce es aleatorio, el texto cifrado puede cambiar en cada ejecución. Para descifrar correctamente el mensaje, es necesario conservar el nonce utilizado durante el cifrado y emplear la misma clave.

## Parte 2 — Descifrado

En esta parte se utiliza el texto cifrado proporcionado por el enunciado, junto con la misma clave y el mismo nonce de la Parte 1.

### Resultado

El programa recupera el siguiente texto plano:

```text
Este es un mensaje secreto que quiero que descifres
```

### Explicación

El texto plano de la Parte 2 es diferente del utilizado en la Parte 1. Esto no es un error: el texto cifrado proporcionado para el descifrado corresponde a otro mensaje.

El resultado demuestra que el programa puede recuperar el contenido original cuando se utiliza la clave y el nonce correctos.

## Parte 3 — Sincronización del keystream (EXTRA)

### Objetivo

Estudiar cómo recuperar la sincronización cuando se pierden los primeros 8 bytes del texto cifrado durante la transmisión.

### Método utilizado

Se utiliza el método `seek()` de PyCryptodome para avanzar hasta una posición concreta del flujo de claves.

```python
keystream_generator.seek(8)
```

Esta instrucción hace que el generador avance 8 bytes en el keystream antes de comenzar el descifrado.

### Resultado obtenido

Al ejecutar el programa, se obtiene el siguiente texto descifrado:

```text
saje ha sufrido un error en la transmision
```

Representación hexadecimal:

```text
73616a65206861207375667269646f20756e206572726f7220656e206c61207472616e736d6973696f6e
```

### Explicación

La pérdida de los primeros 8 bytes del texto cifrado provoca que el receptor ya no tenga el mensaje completo desde su inicio.

El método `seek(8)` permite posicionar el flujo de claves en el desplazamiento correspondiente para descifrar los bytes recibidos.

El texto recuperado es legible y permite comprobar que la sincronización del keystream funciona.

### Conclusión del EXTRA

La práctica demuestra que ChaCha20 permite reposicionar el flujo de claves mediante `seek()`, lo que resulta útil cuando se necesita descifrar datos desde una posición concreta.

No obstante, la sincronización correcta depende de conocer el desplazamiento exacto de los bytes perdidos y de utilizar la misma clave y el mismo nonce.

