^title String Class

A string is an immutable array of bytes. Strings usually store text, in which
case the bytes are the UTF-8 encoding of the text's code points. But you can put
any kind of byte values in there you want, including null bytes or invalid
UTF-8.

There are a few ways to think of a string:

* As a searchable chunk of text composed of a sequence of textual code points.

* As an iterable sequence of code point numbers.

* As a flat array of directly indexable bytes.

All of those are useful for some problems, so the string API supports all three.
The first one is the most common, so that's what methods directly on the string
class cater to.

In UTF-8, a single Unicode code point&mdash;very roughly a single
"character"&mdash;may encode to one or more bytes. This means you can't
efficiently index by code point. There's no way to jump directly to, say, the
fifth code point in a string without walking the string from the beginning and
counting them as you go.

Because counting code points is relatively slow, the indexes passed to string
methods are *byte* offsets, not *code point* offsets. When you do:

    :::wren
    someString[3]

That means "get the code point starting at *byte* three", not "get the third
code point in the string". This sounds scary, but keep in mind that the methods
on strings *return* byte indexes too. So, for example, this does what you want:

    :::wren
    var metalBand = "Fäcëhämmër"
    var hPosition = metalBand.indexOf("h")
    System.print(metalBand[hPosition]) //> h

If you want to work with a string as a sequence numeric code points, call the
`codePoints` getter. It returns a [Sequence](sequence.html) that decodes UTF-8
and iterates over the code points, returning each as a number.

If you want to get at the raw bytes, call `bytes`. This returns a Sequence that
ignores any UTF-8 encoding and works directly at the byte level.

## Static Methods

### String.**fromCodePoint**(codePoint)

Creates a new string containing the UTF-8 encoding of `codePoint`.

    :::wren
    String.fromCodePoint(8225) //> ‡

It is a runtime error if `codePoint` is not an integer between `0` and
`0x10ffff`, inclusive.

## Methods

### **bytes**

Gets a [`Sequence`](sequence.html) that can be used to access the raw bytes of
the string and ignore any UTF-8 encoding. In addition to the normal sequence
methods, the returned object also has a subscript operator that can be used to
directly index bytes.

    :::wren
    System.print("hello".bytes[1]) //> 101 (for "e")

The `count` method on the returned sequence returns the number of bytes in the
string. Unlike `count` on the string itself, it does not have to iterate over
the string, and runs in constant time instead.

### **codePoints**

Gets a [`Sequence`](sequence.html) that can be used to access the UTF-8 decode
code points of the string *as numbers*. Iteration and subscripting work similar
to the string itself. The difference is that instead of returning
single-character strings, this returns the numeric code point values.

    :::wren
    var string = "(ᵔᴥᵔ)"
    System.print(string.codePoints[0]) //> 40 (for "(")
    System.print(string.codePoints[4]) //> 7461 (for "ᴥ")

If the byte at `index` does not begin a valid UTF-8 sequence, or the end of the
string is reached before the sequence is complete, returns `-1`.

    :::wren
    var string = "(ᵔᴥᵔ)"
    System.print(string.codePoints[2]) //> -1 (in the middle of "ᵔ")

### **contains**(other)

Checks if `other` is a substring of the string.

It is a runtime error if `other` is not a string.

### **count**

Returns the number of code points in the string. Since UTF-8 is a
variable-length encoding, this requires iterating over the entire string, which
is relatively slow.

If the string contains bytes that are invalid UTF-8, each byte adds one to the
count as well.

### **endsWith**(suffix)

Checks if the string ends with `suffix`.

It is a runtime error if `suffix` is not a string.

### **indexOf**(search)

Returns the index of the first byte matching `search` in the string or `-1` if
`search` was not found.

It is a runtime error if `search` is not a string.

### **iterate**(iterator), **iteratorValue**(iterator)

Implements the [iterator protocol](../control-flow.html#the-iterator-protocol)
for iterating over the *code points* in the string:

    :::wren
    var codePoints = []
    for (c in "(ᵔᴥᵔ)") {
      codePoints.add(c)
    }

    System.print(codePoints) //> [(, ᵔ, ᴥ, ᵔ, )]

If the string contains any bytes that are not valid UTF-8, this iterates over
those too, one byte at a time.

### **startsWith**(prefix)

Checks if the string starts with `prefix`.

It is a runtime error if `prefix` is not a string.

### **+**(other) operator

Returns a new string that concatenates this string and `other`.

It is a runtime error if `other` is not a string.

### **==**(other) operator

Checks if the string is equal to `other`.

### **!=**(other) operator

Check if the string is not equal to `other`.

### **[**index**]** operator

Returns a string containing the code point starting at byte `index`.

    :::wren
    System.print("ʕ•ᴥ•ʔ"[5]) //> ᴥ

Since `ʕ` is two bytes in UTF-8 and `•` is three, the fifth byte points to the
bear's nose.

If `index` points into the middle of a UTF-8 sequence or at otherwise invalid
UTF-8, this returns a one-byte string containing the byte at that index:

    :::wren
    System.print("I ♥ NY"[3]) //> (one-byte string [153])

It is a runtime error if `index` is greater than the number of bytes in the
string.
