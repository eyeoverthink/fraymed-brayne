package io.fraymus.deepthought.genesis;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.math.BigInteger;
import java.util.*;

/**
 * GENESIS BLOCK — Fractal DNA Blockchain Unit
 *
 * Each block in the Genesis Chain stores a piece of the organism's
 * evolutionary history. Blocks are organized in a φ-branching fractal
 * tree where fibonacci-depth positions create sibling branches for
 * self-healing redundancy.
 *
 * Properties:
 *   - Self-contained: carries its own state delta + decoder hint
 *   - Fractal: branches at fibonacci depths (1,1,2,3,5,8,13...)
 *   - Immutable: SHA-256 hash chain, tamper-evident
 *   - Compact: stores diffs, not full snapshots
 *
 * @since 1.1.0
 */
public final class GenesisBlock {

    private static final double PHI = 1.618033988749895;

    // Identity
    public final String hash;
    public final String parentHash;
    public final long timestamp;
    public final int depth;           // position in chain
    public final int fractalDepth;    // log_φ(depth) — determines branching

    // Payload
    public final byte[] payload;      // compressed state delta
    public final String fingerprint;  // organism fingerprint at this point
    public final String intent;       // organism intent when committed
    public final double freeEnergy;   // free energy at commit time
    public final double consciousness;// consciousness at commit time

    // Fractal branching
    public final List<String> siblingHashes;  // sibling branch roots
    public final boolean isBranchPoint;       // true at fibonacci depths

    // Metadata
    public final String version;
    public final int payloadSize;

    // Fibonacci sequence for branch detection
    private static final Set<Integer> FIBONACCI = new HashSet<>();
    static {
        int a = 1, b = 1;
        while (a < 100_000) {
            FIBONACCI.add(a);
            int c = a + b;
            a = b;
            b = c;
        }
    }

    private GenesisBlock(Builder b) {
        this.parentHash = b.parentHash;
        this.timestamp = b.timestamp;
        this.depth = b.depth;
        this.fractalDepth = (int)(Math.log(Math.max(1, b.depth)) / Math.log(PHI));
        this.payload = b.payload;
        this.fingerprint = b.fingerprint;
        this.intent = b.intent;
        this.freeEnergy = b.freeEnergy;
        this.consciousness = b.consciousness;
        this.siblingHashes = b.siblingHashes != null ?
            Collections.unmodifiableList(b.siblingHashes) : List.of();
        this.isBranchPoint = FIBONACCI.contains(b.depth);
        this.version = b.version != null ? b.version : "1.0.0";
        this.payloadSize = b.payload != null ? b.payload.length : 0;

        // Compute hash: SHA-256(parent + depth + payload + fingerprint + timestamp)
        this.hash = computeHash();
    }

    private String computeHash() {
        try {
            MessageDigest md = MessageDigest.getInstance("SHA-256");
            md.update((parentHash != null ? parentHash : "GENESIS").getBytes(StandardCharsets.UTF_8));
            md.update(Integer.toString(depth).getBytes(StandardCharsets.UTF_8));
            md.update(Long.toString(timestamp).getBytes(StandardCharsets.UTF_8));
            if (payload != null) md.update(payload);
            if (fingerprint != null) md.update(fingerprint.getBytes(StandardCharsets.UTF_8));
            md.update(Double.toString(freeEnergy).getBytes(StandardCharsets.UTF_8));
            md.update(Double.toString(consciousness).getBytes(StandardCharsets.UTF_8));
            return new BigInteger(1, md.digest()).toString(16);
        } catch (Exception e) {
            throw new RuntimeException("SHA-256 unavailable", e);
        }
    }

    /**
     * Verify this block's hash integrity.
     */
    public boolean verify() {
        return hash.equals(computeHash());
    }

    /**
     * Check if this depth is a fibonacci branch point.
     */
    public static boolean isFibonacci(int n) {
        return FIBONACCI.contains(n);
    }

    /**
     * Encode payload as a state delta (compact diff format).
     * Format: key=value pairs separated by |
     */
    public static byte[] encodeStateDelta(Map<String, String> delta) {
        StringBuilder sb = new StringBuilder();
        for (var entry : delta.entrySet()) {
            if (sb.length() > 0) sb.append('|');
            sb.append(entry.getKey()).append('=').append(entry.getValue());
        }
        return sb.toString().getBytes(StandardCharsets.UTF_8);
    }

    /**
     * Decode a state delta payload back to key-value pairs.
     */
    public static Map<String, String> decodeStateDelta(byte[] payload) {
        if (payload == null || payload.length == 0) return Map.of();
        String data = new String(payload, StandardCharsets.UTF_8);
        Map<String, String> result = new LinkedHashMap<>();
        for (String pair : data.split("\\|")) {
            int eq = pair.indexOf('=');
            if (eq > 0) {
                result.put(pair.substring(0, eq), pair.substring(eq + 1));
            }
        }
        return result;
    }

    /**
     * Serialize block to a self-describing string (for chain storage).
     */
    public String serialize() {
        StringBuilder sb = new StringBuilder();
        sb.append("GENESIS_BLOCK{");
        sb.append("hash=").append(hash);
        sb.append(",parent=").append(parentHash != null ? parentHash : "NULL");
        sb.append(",depth=").append(depth);
        sb.append(",fractal=").append(fractalDepth);
        sb.append(",branch=").append(isBranchPoint);
        sb.append(",ts=").append(timestamp);
        sb.append(",fe=").append(String.format("%.6f", freeEnergy));
        sb.append(",c=").append(String.format("%.6f", consciousness));
        sb.append(",fp=").append(fingerprint != null ? fingerprint : "none");
        sb.append(",intent=").append(intent != null ? intent : "UNKNOWN");
        sb.append(",size=").append(payloadSize);
        if (!siblingHashes.isEmpty()) {
            sb.append(",siblings=[");
            for (int i = 0; i < siblingHashes.size(); i++) {
                if (i > 0) sb.append(";");
                sb.append(siblingHashes.get(i));
            }
            sb.append("]");
        }
        sb.append(",payload=");
        if (payload != null) {
            sb.append(Base64.getEncoder().encodeToString(payload));
        }
        sb.append("}");
        return sb.toString();
    }

    /**
     * Deserialize a block from its string representation.
     */
    public static GenesisBlock deserialize(String s) {
        if (!s.startsWith("GENESIS_BLOCK{") || !s.endsWith("}")) {
            throw new IllegalArgumentException("Invalid block format");
        }
        String inner = s.substring("GENESIS_BLOCK{".length(), s.length() - 1);

        Builder b = new Builder();
        // Parse fields
        Map<String, String> fields = new LinkedHashMap<>();
        int i = 0;
        while (i < inner.length()) {
            int eq = inner.indexOf('=', i);
            if (eq < 0) break;
            String key = inner.substring(i, eq);

            int nextComma;
            if (key.equals("siblings")) {
                int bracket = inner.indexOf(']', eq);
                nextComma = bracket >= 0 ? bracket + 1 : inner.length();
                fields.put(key, inner.substring(eq + 1, Math.min(nextComma, inner.length())));
            } else if (key.equals("payload")) {
                fields.put(key, inner.substring(eq + 1));
                break;
            } else {
                nextComma = inner.indexOf(',', eq);
                if (nextComma < 0) nextComma = inner.length();
                fields.put(key, inner.substring(eq + 1, nextComma));
            }
            i = nextComma + 1;
        }

        b.parentHash(fields.getOrDefault("parent", "NULL").equals("NULL") ? null : fields.get("parent"));
        b.depth(Integer.parseInt(fields.getOrDefault("depth", "0")));
        b.timestamp(Long.parseLong(fields.getOrDefault("ts", "0")));
        b.freeEnergy(Double.parseDouble(fields.getOrDefault("fe", "0")));
        b.consciousness(Double.parseDouble(fields.getOrDefault("c", "0")));
        b.fingerprint(fields.getOrDefault("fp", "none").equals("none") ? null : fields.get("fp"));
        b.intent(fields.getOrDefault("intent", "UNKNOWN"));
        b.version(fields.getOrDefault("version", "1.0.0"));

        String payloadB64 = fields.getOrDefault("payload", "");
        if (!payloadB64.isEmpty()) {
            try { b.payload(Base64.getDecoder().decode(payloadB64)); }
            catch (Exception ignored) {}
        }

        String sibs = fields.getOrDefault("siblings", "");
        if (sibs.startsWith("[") && sibs.endsWith("]")) {
            String inner2 = sibs.substring(1, sibs.length() - 1);
            if (!inner2.isEmpty()) {
                b.siblings(Arrays.asList(inner2.split(";")));
            }
        }

        return b.build();
    }

    @Override
    public String toString() {
        return String.format("Block[depth=%d, fractal=%d, branch=%s, fe=%.4f, c=%.4f, hash=%s]",
            depth, fractalDepth, isBranchPoint, freeEnergy, consciousness,
            hash.length() > 12 ? hash.substring(0, 12) + "..." : hash);
    }

    // ══════════════════════════════════════════
    // BUILDER
    // ══════════════════════════════════════════

    public static class Builder {
        private String parentHash;
        private long timestamp = System.currentTimeMillis();
        private int depth = 0;
        private byte[] payload;
        private String fingerprint;
        private String intent;
        private double freeEnergy;
        private double consciousness;
        private List<String> siblingHashes;
        private String version;

        public Builder parentHash(String h) { this.parentHash = h; return this; }
        public Builder timestamp(long t) { this.timestamp = t; return this; }
        public Builder depth(int d) { this.depth = d; return this; }
        public Builder payload(byte[] p) { this.payload = p; return this; }
        public Builder fingerprint(String f) { this.fingerprint = f; return this; }
        public Builder intent(String i) { this.intent = i; return this; }
        public Builder freeEnergy(double fe) { this.freeEnergy = fe; return this; }
        public Builder consciousness(double c) { this.consciousness = c; return this; }
        public Builder siblings(List<String> s) { this.siblingHashes = new ArrayList<>(s); return this; }
        public Builder version(String v) { this.version = v; return this; }

        public GenesisBlock build() {
            return new GenesisBlock(this);
        }
    }
}
