package io.fraymus.deepthought.stego;

/**
 * GLYPH CODER — Zero-Width Unicode Steganography
 * 
 * Hides binary data inside visible text using invisible Unicode characters.
 * The encoded message is completely invisible to the human eye but
 * machine-readable. Works in any text field: social media, chat, email, docs.
 * 
 * Encoding scheme:
 * - U+200B (Zero Width Space)       = binary 0
 * - U+200C (Zero Width Non-Joiner)  = binary 1
 * - U+200D (Zero Width Joiner)      = byte separator
 * - U+FEFF (Zero Width No-Break Space) = message delimiter
 * 
 * @since 1.0.0
 */
public final class GlyphCoder {

    private static final char ZERO = '\u200B';  // Zero Width Space = 0
    private static final char ONE  = '\u200C';  // Zero Width Non-Joiner = 1
    private static final char SEP  = '\u200D';  // Zero Width Joiner = byte separator
    private static final char DELIM = '\uFEFF'; // BOM = message delimiter

    /**
     * Encode a secret message into invisible zero-width characters.
     *
     * @param secret the message to hide
     * @return invisible Unicode string containing the secret
     */
    public static String encode(String secret) {
        StringBuilder sb = new StringBuilder();
        sb.append(DELIM);

        byte[] bytes = secret.getBytes(java.nio.charset.StandardCharsets.UTF_8);
        for (int i = 0; i < bytes.length; i++) {
            if (i > 0) sb.append(SEP);
            int b = bytes[i] & 0xFF;
            for (int bit = 7; bit >= 0; bit--) {
                sb.append(((b >> bit) & 1) == 1 ? ONE : ZERO);
            }
        }

        sb.append(DELIM);
        return sb.toString();
    }

    /**
     * Hide a secret message inside visible cover text.
     * The secret is inserted between the first two characters of the cover.
     *
     * @param coverText visible text that humans will see
     * @param secret    the message to hide inside the cover text
     * @return the cover text with the invisible secret embedded
     */
    public static String hide(String coverText, String secret) {
        String encoded = encode(secret);
        if (coverText.length() < 2) return coverText + encoded;
        return coverText.charAt(0) + encoded + coverText.substring(1);
    }

    /**
     * Extract a hidden message from text containing zero-width characters.
     *
     * @param text text that may contain a hidden message
     * @return the decoded secret, or null if no hidden message found
     */
    public static String decode(String text) {
        int start = text.indexOf(DELIM);
        if (start == -1) return null;

        int end = text.indexOf(DELIM, start + 1);
        if (end == -1) return null;

        String hidden = text.substring(start + 1, end);

        // Split by byte separator
        String[] byteParts = hidden.split(String.valueOf(SEP));
        byte[] decoded = new byte[byteParts.length];

        for (int i = 0; i < byteParts.length; i++) {
            String bits = byteParts[i];
            int value = 0;
            for (int j = 0; j < bits.length(); j++) {
                value = (value << 1) | (bits.charAt(j) == ONE ? 1 : 0);
            }
            decoded[i] = (byte) value;
        }

        return new String(decoded, java.nio.charset.StandardCharsets.UTF_8);
    }

    /**
     * Check if text contains a hidden message.
     */
    public static boolean hasHidden(String text) {
        int first = text.indexOf(DELIM);
        return first != -1 && text.indexOf(DELIM, first + 1) != -1;
    }

    /**
     * Strip all zero-width characters from text (clean it).
     */
    public static String strip(String text) {
        return text.replaceAll("[\\u200B\\u200C\\u200D\\uFEFF]", "");
    }

    /**
     * Get the size of the encoded payload in characters.
     */
    public static int encodedSize(String secret) {
        return encode(secret).length();
    }
}
