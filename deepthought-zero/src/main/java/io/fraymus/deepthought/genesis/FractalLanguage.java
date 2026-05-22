package io.fraymus.deepthought.genesis;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.math.BigInteger;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

/**
 * FRACTAL LANGUAGE ENGINE — Self-Evolving Encoding
 *
 * The organism doesn't store state in JSON — it creates its OWN language
 * that evolves alongside it. Frequent patterns get shorter symbols.
 * Rare patterns get longer ones. The language mutates every N breaths.
 *
 * Properties:
 *   - Self-describing: encoded data carries its own decoder
 *   - Progressive: language grows more expressive over time
 *   - Regressive: old encodings remain decodable (backward compatible)
 *   - Unique: no two organisms develop the same language
 *
 * @since 1.1.0
 */
public final class FractalLanguage {

    private static final double PHI = 1.618033988749895;

    // Symbol table: pattern → compressed symbol
    private final Map<String, String> encodeTable = new ConcurrentHashMap<>();
    private final Map<String, String> decodeTable = new ConcurrentHashMap<>();

    // Frequency tracking: how often each pattern appears
    private final Map<String, Long> frequency = new ConcurrentHashMap<>();

    // Language metadata
    private int generation = 0;
    private double mutationRate = 0.05;
    private int nextSymbolId = 0;
    private long totalEncodes = 0;
    private long totalDecodes = 0;

    // Symbol alphabet: starts compact, grows as language evolves
    private static final String BASE_ALPHABET = "αβγδεζηθικλμνξοπρστυφχψω";
    private static final String EXTENDED_ALPHABET = "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ";

    public FractalLanguage() {
        // Bootstrap: seed the language with fundamental patterns
        bootstrapLanguage();
    }

    /**
     * Bootstrap the initial language with known organism state patterns.
     */
    private void bootstrapLanguage() {
        // Core state keys get short symbols
        registerSymbol("consciousness", "α");
        registerSymbol("freeEnergy", "β");
        registerSymbol("entropy", "γ");
        registerSymbol("intent", "δ");
        registerSymbol("breath", "ε");
        registerSymbol("fingerprint", "ζ");
        registerSymbol("cortexHash", "η");
        registerSymbol("strategy", "θ");
        registerSymbol("shadows", "ι");
        registerSymbol("beliefs", "κ");

        // Common intents
        registerSymbol("OBSERVE", "λ");
        registerSymbol("SHADOW_SIM", "μ");
        registerSymbol("CONSOLIDATE", "ν");
        registerSymbol("FORAGE", "ξ");
        registerSymbol("SPEAK", "ο");
        registerSymbol("EXPLORATION", "π");
        registerSymbol("EXPLOITATION", "ρ");

        // Common value ranges (quantized)
        registerSymbol("HIGH", "σ");
        registerSymbol("LOW", "τ");
        registerSymbol("STABLE", "υ");
        registerSymbol("RISING", "φ");
        registerSymbol("FALLING", "χ");

        nextSymbolId = BASE_ALPHABET.length();
    }

    private void registerSymbol(String pattern, String symbol) {
        encodeTable.put(pattern, symbol);
        decodeTable.put(symbol, pattern);
        frequency.put(pattern, 0L);
    }

    /**
     * Encode a state map using the current language.
     * Output format: LANG_V{generation}:{encoded_data}:{decoder_hint}
     */
    public String encode(Map<String, String> state) {
        totalEncodes++;
        StringBuilder encoded = new StringBuilder();
        StringBuilder decoder = new StringBuilder();

        for (var entry : state.entrySet()) {
            String key = entry.getKey();
            String value = entry.getValue();

            // Track frequency
            frequency.merge(key, 1L, Long::sum);
            frequency.merge(value, 1L, Long::sum);

            // Encode key
            String encodedKey = encodeTable.getOrDefault(key, key);
            // Encode value
            String encodedValue = encodeTable.getOrDefault(value, quantize(value));

            if (encoded.length() > 0) encoded.append("|");
            encoded.append(encodedKey).append(":").append(encodedValue);

            // If we used a symbol, record the decoder hint
            if (!encodedKey.equals(key)) {
                decoder.append(encodedKey).append("→").append(key).append(";");
            }
            if (!encodedValue.equals(value) && encodeTable.containsKey(value)) {
                decoder.append(encodedValue).append("→").append(value).append(";");
            }
        }

        return String.format("LANG_V%d:%s:%s", generation, encoded, decoder);
    }

    /**
     * Decode a previously encoded string back to state map.
     * Self-describing: the decoder hints are embedded in the encoded data.
     */
    public Map<String, String> decode(String encoded) {
        totalDecodes++;
        if (encoded == null || !encoded.startsWith("LANG_V")) return Map.of();

        // Parse: LANG_V{gen}:{data}:{decoder}
        int firstColon = encoded.indexOf(':');
        int lastColon = encoded.lastIndexOf(':');
        if (firstColon < 0 || lastColon <= firstColon) return Map.of();

        String data = encoded.substring(firstColon + 1, lastColon);
        String decoderHints = encoded.substring(lastColon + 1);

        // Build local decoder from hints
        Map<String, String> localDecoder = new HashMap<>(decodeTable);
        if (!decoderHints.isEmpty()) {
            for (String hint : decoderHints.split(";")) {
                int arrow = hint.indexOf("→");
                if (arrow > 0) {
                    localDecoder.put(hint.substring(0, arrow), hint.substring(arrow + "→".length()));
                }
            }
        }

        // Decode pairs
        Map<String, String> result = new LinkedHashMap<>();
        for (String pair : data.split("\\|")) {
            int colon = pair.indexOf(':');
            if (colon < 0) continue;
            String key = pair.substring(0, colon);
            String value = pair.substring(colon + 1);

            // Decode symbols back to original
            key = localDecoder.getOrDefault(key, key);
            value = localDecoder.getOrDefault(value, value);

            result.put(key, value);
        }

        return result;
    }

    /**
     * Quantize a numeric value into a compact representation.
     */
    private String quantize(String value) {
        try {
            double v = Double.parseDouble(value);
            // Quantize to φ-based levels
            if (v > 0.8) return "σ" + (int)(v * 100);   // HIGH + precise
            if (v < 0.2) return "τ" + (int)(v * 100);   // LOW + precise
            return "~" + (int)(v * 1000);                // mid-range, 3 decimals
        } catch (NumberFormatException e) {
            return value; // not a number, keep as-is
        }
    }

    /**
     * Evolve the language: observe patterns, compress frequent ones.
     * Call this every N breaths.
     */
    public void evolve(Map<String, String> observedState) {
        generation++;

        // Find patterns that appear frequently but aren't yet symbolized
        List<Map.Entry<String, Long>> sorted = new ArrayList<>(frequency.entrySet());
        sorted.sort((a, b) -> Long.compare(b.getValue(), a.getValue()));

        int newSymbols = 0;
        for (var entry : sorted) {
            String pattern = entry.getKey();
            long freq = entry.getValue();

            // Only create symbols for frequently-seen patterns without one
            if (freq > 5 && !encodeTable.containsKey(pattern)) {
                String symbol = generateSymbol();
                registerSymbol(pattern, symbol);
                newSymbols++;
                if (newSymbols >= 3) break; // max 3 new symbols per evolution
            }
        }

        // Observe current state for new patterns
        if (observedState != null) {
            for (var entry : observedState.entrySet()) {
                frequency.merge(entry.getKey(), 1L, Long::sum);
                frequency.merge(entry.getValue(), 1L, Long::sum);

                // Composite patterns: key+value combos that repeat
                String composite = entry.getKey() + "=" + entry.getValue();
                frequency.merge(composite, 1L, Long::sum);
            }
        }
    }

    /**
     * Mutate the language: introduce new symbols, merge rare ones.
     * This makes each organism's language unique over time.
     */
    public void mutate() {
        // Remove symbols with zero usage (language cleanup)
        List<String> toRemove = new ArrayList<>();
        for (var entry : frequency.entrySet()) {
            if (entry.getValue() == 0 && encodeTable.containsKey(entry.getKey())) {
                // Don't remove bootstrap symbols (first 20)
                String symbol = encodeTable.get(entry.getKey());
                if (symbol.length() > 1 || BASE_ALPHABET.indexOf(symbol.charAt(0)) < 0) {
                    toRemove.add(entry.getKey());
                }
            }
        }

        for (String pattern : toRemove) {
            String symbol = encodeTable.remove(pattern);
            if (symbol != null) decodeTable.remove(symbol);
            frequency.remove(pattern);
        }

        // Decay all frequencies (forget old patterns gradually)
        for (var entry : frequency.entrySet()) {
            long decayed = (long)(entry.getValue() * (1.0 - mutationRate));
            entry.setValue(Math.max(0, decayed));
        }

        mutationRate = Math.max(0.01, mutationRate * 0.99); // slow down mutation over time
    }

    /**
     * Generate a new symbol for the language.
     */
    private String generateSymbol() {
        String combined = BASE_ALPHABET + EXTENDED_ALPHABET;
        if (nextSymbolId < combined.length()) {
            return String.valueOf(combined.charAt(nextSymbolId++));
        }
        // Beyond alphabet: use multi-character symbols
        int id = nextSymbolId++;
        int base = combined.length();
        StringBuilder sym = new StringBuilder();
        sym.append(combined.charAt(id % base));
        sym.append(combined.charAt((id / base) % base));
        return sym.toString();
    }

    /**
     * Get the language's self-description (for embedding in encoded data).
     */
    public String describeLanguage() {
        StringBuilder sb = new StringBuilder();
        sb.append("FRAYMUS_LANG_V").append(generation).append("\n");
        sb.append("symbols=").append(encodeTable.size()).append("\n");
        sb.append("mutations=").append(generation).append("\n");
        sb.append("mutation_rate=").append(String.format("%.4f", mutationRate)).append("\n");
        sb.append("total_encodes=").append(totalEncodes).append("\n");

        // Symbol table dump
        for (var entry : encodeTable.entrySet()) {
            long freq = frequency.getOrDefault(entry.getKey(), 0L);
            sb.append(entry.getValue()).append(" → ").append(entry.getKey())
              .append(" (freq=").append(freq).append(")\n");
        }
        return sb.toString();
    }

    /**
     * Serialize the entire language for persistence.
     */
    public String serialize() {
        StringBuilder sb = new StringBuilder();
        sb.append("LANG_SERIAL_V1\n");
        sb.append("gen=").append(generation).append("\n");
        sb.append("mr=").append(mutationRate).append("\n");
        sb.append("nsid=").append(nextSymbolId).append("\n");
        sb.append("te=").append(totalEncodes).append("\n");
        sb.append("td=").append(totalDecodes).append("\n");
        sb.append("SYMBOLS\n");
        for (var entry : encodeTable.entrySet()) {
            long freq = frequency.getOrDefault(entry.getKey(), 0L);
            sb.append(entry.getKey()).append("\t").append(entry.getValue())
              .append("\t").append(freq).append("\n");
        }
        return sb.toString();
    }

    /**
     * Deserialize a language from its stored form.
     */
    public static FractalLanguage deserialize(String data) {
        FractalLanguage lang = new FractalLanguage();
        lang.encodeTable.clear();
        lang.decodeTable.clear();
        lang.frequency.clear();

        String[] lines = data.split("\n");
        boolean inSymbols = false;
        for (String line : lines) {
            if (line.startsWith("gen=")) lang.generation = Integer.parseInt(line.substring(4));
            else if (line.startsWith("mr=")) lang.mutationRate = Double.parseDouble(line.substring(3));
            else if (line.startsWith("nsid=")) lang.nextSymbolId = Integer.parseInt(line.substring(5));
            else if (line.startsWith("te=")) lang.totalEncodes = Long.parseLong(line.substring(3));
            else if (line.startsWith("td=")) lang.totalDecodes = Long.parseLong(line.substring(3));
            else if (line.equals("SYMBOLS")) inSymbols = true;
            else if (inSymbols) {
                String[] parts = line.split("\t");
                if (parts.length >= 2) {
                    lang.registerSymbol(parts[0], parts[1]);
                    if (parts.length >= 3) {
                        try { lang.frequency.put(parts[0], Long.parseLong(parts[2])); }
                        catch (NumberFormatException ignored) {}
                    }
                }
            }
        }
        return lang;
    }

    // Getters
    public int getGeneration() { return generation; }
    public int getSymbolCount() { return encodeTable.size(); }
    public double getMutationRate() { return mutationRate; }
    public long getTotalEncodes() { return totalEncodes; }
}
