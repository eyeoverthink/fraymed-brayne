package io.fraymus.deepthought.organism;

import java.io.*;
import java.nio.file.*;
import java.util.*;

/**
 * PERSISTENCE — Organism State Save/Restore
 * 
 * Serializes the organism's cortex, beliefs, causal edges, and metadata
 * to JSON files on disk. Zero dependencies — hand-rolled JSON.
 * 
 * The organism can die and be reborn from its saved state.
 * 
 * @since 1.0.0
 */
public final class Persistence {

    private final Path stateDir;

    public Persistence(Path stateDir) {
        this.stateDir = stateDir;
        try {
            Files.createDirectories(stateDir);
        } catch (IOException e) {
            throw new RuntimeException("Cannot create state directory: " + stateDir, e);
        }
    }

    public Persistence() {
        this(Path.of("organism_state"));
    }

    /**
     * Save full organism state to disk.
     */
    public Path save(OrganismState state) throws IOException {
        String filename = "organism_" + System.currentTimeMillis() + ".json";
        Path file = stateDir.resolve(filename);

        StringBuilder json = new StringBuilder();
        json.append("{\n");
        json.append("  \"system\": \"FRAYMUS-DeepThought\",\n");
        json.append("  \"version\": \"").append(state.version).append("\",\n");
        json.append("  \"timestamp\": ").append(System.currentTimeMillis()).append(",\n");
        json.append("  \"breathCount\": ").append(state.breathCount).append(",\n");
        json.append("  \"consciousness\": ").append(state.consciousness).append(",\n");
        json.append("  \"freeEnergy\": ").append(state.freeEnergy).append(",\n");
        json.append("  \"hamiltonianEnergy\": ").append(state.hamiltonianEnergy).append(",\n");
        json.append("  \"systemEntropy\": ").append(state.systemEntropy).append(",\n");
        json.append("  \"previousEnergy\": ").append(state.previousEnergy).append(",\n");
        json.append("  \"shadowsAccepted\": ").append(state.shadowsAccepted).append(",\n");
        json.append("  \"shadowsProposed\": ").append(state.shadowsProposed).append(",\n");
        json.append("  \"currentThought\": ").append(escapeJson(state.currentThought)).append(",\n");
        json.append("  \"currentIntent\": ").append(escapeJson(state.currentIntent)).append(",\n");
        json.append("  \"fingerprint\": ").append(escapeJson(state.fingerprint)).append(",\n");
        json.append("  \"chaosGeneration\": ").append(escapeJson(state.chaosGeneration)).append(",\n");

        // Cortex
        json.append("  \"cortexDim\": ").append(state.cortex.length).append(",\n");
        json.append("  \"cortex\": [");
        for (int i = 0; i < state.cortex.length; i++) {
            if (i > 0) json.append(",");
            if (i % 20 == 0) json.append("\n    ");
            json.append(String.format("%.8f", state.cortex[i]));
        }
        json.append("\n  ],\n");

        // Beliefs
        json.append("  \"beliefs\": [\n");
        for (int i = 0; i < state.beliefs.size(); i++) {
            var b = state.beliefs.get(i);
            if (i > 0) json.append(",\n");
            json.append("    {\"id\":").append(escapeJson(b[0]))
                .append(",\"statement\":").append(escapeJson(b[1]))
                .append(",\"confidence\":").append(b[2]).append("}");
        }
        json.append("\n  ],\n");

        // Causal edges
        json.append("  \"causalEdges\": [\n");
        for (int i = 0; i < state.causalEdges.size(); i++) {
            var e = state.causalEdges.get(i);
            if (i > 0) json.append(",\n");
            json.append("    {\"cause\":").append(escapeJson(e[0]))
                .append(",\"effect\":").append(escapeJson(e[1]))
                .append(",\"strength\":").append(e[2]).append("}");
        }
        json.append("\n  ],\n");

        // Free energy history
        json.append("  \"freeEnergyHistory\": [");
        for (int i = 0; i < state.freeEnergyHistory.size(); i++) {
            if (i > 0) json.append(",");
            if (i % 20 == 0) json.append("\n    ");
            json.append(String.format("%.6f", state.freeEnergyHistory.get(i)));
        }
        json.append("\n  ]\n");

        json.append("}\n");

        Files.writeString(file, json.toString());

        // Also save as "latest.json" for quick restore
        Files.writeString(stateDir.resolve("latest.json"), json.toString());

        return file;
    }

    /**
     * Restore organism state from the latest save.
     */
    public OrganismState restore() throws IOException {
        return restore(stateDir.resolve("latest.json"));
    }

    /**
     * Restore organism state from a specific file.
     */
    public OrganismState restore(Path file) throws IOException {
        if (!Files.exists(file)) return null;
        String json = Files.readString(file);
        return parseState(json);
    }

    /**
     * List all saved states.
     */
    public List<Path> listSaves() throws IOException {
        if (!Files.exists(stateDir)) return List.of();
        List<Path> saves = new ArrayList<>();
        try (var stream = Files.list(stateDir)) {
            stream.filter(p -> p.toString().endsWith(".json"))
                  .filter(p -> !p.getFileName().toString().equals("latest.json"))
                  .sorted(Comparator.reverseOrder())
                  .forEach(saves::add);
        }
        return saves;
    }

    /**
     * Check if a saved state exists.
     */
    public boolean hasSavedState() {
        return Files.exists(stateDir.resolve("latest.json"));
    }

    public Path getStateDir() { return stateDir; }

    // ── JSON Helpers (zero-dep) ──

    private static String escapeJson(String s) {
        if (s == null) return "null";
        return "\"" + s.replace("\\", "\\\\")
                       .replace("\"", "\\\"")
                       .replace("\n", "\\n")
                       .replace("\r", "\\r")
                       .replace("\t", "\\t") + "\"";
    }

    private OrganismState parseState(String json) {
        OrganismState state = new OrganismState();
        state.version = extractString(json, "version");
        state.breathCount = extractLong(json, "breathCount");
        state.consciousness = extractDouble(json, "consciousness");
        state.freeEnergy = extractDouble(json, "freeEnergy");
        state.hamiltonianEnergy = extractDouble(json, "hamiltonianEnergy");
        state.systemEntropy = extractDouble(json, "systemEntropy");
        state.previousEnergy = extractDouble(json, "previousEnergy");
        state.shadowsAccepted = extractLong(json, "shadowsAccepted");
        state.shadowsProposed = extractLong(json, "shadowsProposed");
        state.currentThought = extractString(json, "currentThought");
        state.currentIntent = extractString(json, "currentIntent");
        state.fingerprint = extractString(json, "fingerprint");
        state.chaosGeneration = extractString(json, "chaosGeneration");

        // Parse cortex array
        int cortexDim = (int) extractLong(json, "cortexDim");
        state.cortex = extractDoubleArray(json, "cortex", cortexDim);

        // Parse beliefs
        state.beliefs = extractObjectArray(json, "beliefs", new String[]{"id", "statement", "confidence"});

        // Parse causal edges
        state.causalEdges = extractObjectArray(json, "causalEdges", new String[]{"cause", "effect", "strength"});

        // Parse FE history
        state.freeEnergyHistory = new ArrayList<>();
        double[] feArr = extractDoubleArray(json, "freeEnergyHistory", 1000);
        if (feArr != null) {
            for (double v : feArr) state.freeEnergyHistory.add(v);
        }

        return state;
    }

    private static String extractString(String json, String key) {
        String search = "\"" + key + "\":";
        int idx = json.indexOf(search);
        if (idx == -1) return null;
        int start = json.indexOf("\"", idx + search.length());
        if (start == -1) return null;
        int end = json.indexOf("\"", start + 1);
        while (end > 0 && json.charAt(end - 1) == '\\') end = json.indexOf("\"", end + 1);
        if (end == -1) return null;
        return json.substring(start + 1, end).replace("\\\"", "\"").replace("\\n", "\n");
    }

    private static double extractDouble(String json, String key) {
        String search = "\"" + key + "\":";
        int idx = json.indexOf(search);
        if (idx == -1) return 0;
        int start = idx + search.length();
        while (start < json.length() && json.charAt(start) == ' ') start++;
        int end = start;
        while (end < json.length() && (Character.isDigit(json.charAt(end)) || json.charAt(end) == '.' || json.charAt(end) == '-' || json.charAt(end) == 'E' || json.charAt(end) == 'e' || json.charAt(end) == '+')) end++;
        try {
            return Double.parseDouble(json.substring(start, end));
        } catch (NumberFormatException e) {
            return 0;
        }
    }

    private static long extractLong(String json, String key) {
        return (long) extractDouble(json, key);
    }

    private static double[] extractDoubleArray(String json, String key, int maxSize) {
        String search = "\"" + key + "\": [";
        int idx = json.indexOf(search);
        if (idx == -1) {
            search = "\"" + key + "\":[";
            idx = json.indexOf(search);
        }
        if (idx == -1) return new double[0];
        int start = json.indexOf("[", idx) + 1;
        int end = json.indexOf("]", start);
        if (end == -1) return new double[0];

        String content = json.substring(start, end).trim();
        if (content.isEmpty()) return new double[0];

        String[] parts = content.split(",");
        double[] result = new double[Math.min(parts.length, maxSize)];
        int count = 0;
        for (int i = 0; i < parts.length && count < maxSize; i++) {
            String s = parts[i].trim();
            if (!s.isEmpty()) {
                try {
                    result[count++] = Double.parseDouble(s);
                } catch (NumberFormatException ignored) {}
            }
        }
        return Arrays.copyOf(result, count);
    }

    private static List<String[]> extractObjectArray(String json, String key, String[] fields) {
        List<String[]> results = new ArrayList<>();
        String search = "\"" + key + "\":";
        int idx = json.indexOf(search);
        if (idx == -1) return results;

        int arrStart = json.indexOf("[", idx);
        int arrEnd = findMatchingBracket(json, arrStart);
        if (arrStart == -1 || arrEnd == -1) return results;

        String arrContent = json.substring(arrStart + 1, arrEnd);
        int pos = 0;
        while (pos < arrContent.length()) {
            int objStart = arrContent.indexOf("{", pos);
            if (objStart == -1) break;
            int objEnd = arrContent.indexOf("}", objStart);
            if (objEnd == -1) break;

            String obj = arrContent.substring(objStart, objEnd + 1);
            String[] values = new String[fields.length];
            for (int f = 0; f < fields.length; f++) {
                values[f] = extractFieldValue(obj, fields[f]);
            }
            results.add(values);
            pos = objEnd + 1;
        }
        return results;
    }

    private static String extractFieldValue(String obj, String field) {
        String search = "\"" + field + "\":";
        int idx = obj.indexOf(search);
        if (idx == -1) return "";
        int start = idx + search.length();
        while (start < obj.length() && obj.charAt(start) == ' ') start++;
        if (start >= obj.length()) return "";

        if (obj.charAt(start) == '"') {
            int end = obj.indexOf("\"", start + 1);
            return end > start ? obj.substring(start + 1, end) : "";
        } else {
            int end = start;
            while (end < obj.length() && obj.charAt(end) != ',' && obj.charAt(end) != '}') end++;
            return obj.substring(start, end).trim();
        }
    }

    private static int findMatchingBracket(String s, int openIdx) {
        if (openIdx == -1 || openIdx >= s.length()) return -1;
        char open = s.charAt(openIdx);
        char close = open == '[' ? ']' : '}';
        int depth = 1;
        for (int i = openIdx + 1; i < s.length(); i++) {
            if (s.charAt(i) == open) depth++;
            else if (s.charAt(i) == close) {
                depth--;
                if (depth == 0) return i;
            }
        }
        return -1;
    }

    /**
     * Snapshot of organism state for serialization.
     */
    public static class OrganismState {
        public String version;
        public long breathCount;
        public double consciousness;
        public double freeEnergy;
        public double hamiltonianEnergy;
        public double systemEntropy;
        public double previousEnergy;
        public long shadowsAccepted;
        public long shadowsProposed;
        public String currentThought;
        public String currentIntent;
        public String fingerprint;
        public String chaosGeneration;
        public double[] cortex;
        public List<String[]> beliefs = new ArrayList<>();
        public List<String[]> causalEdges = new ArrayList<>();
        public List<Double> freeEnergyHistory = new ArrayList<>();
    }
}
