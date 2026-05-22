package io.fraymus.deepthought.organism;

import java.io.*;
import java.nio.file.*;
import java.util.*;

/**
 * VIDEO CORTEX BRIDGE — Visual Dreamscape
 * 
 * Exports organism state as JSON and triggers VideoCortex.py
 * to generate Stable Diffusion visualizations of the organism's
 * internal state.
 * 
 * The organism literally DREAMS in images.
 * 
 * @since 1.0.0
 */
public final class VideoCortexBridge {

    private final Path videoCortexScript;
    private final Path outputDir;
    private boolean enabled = true;
    private boolean useGpu = true;
    private int inferenceSteps = 30;
    private int width = 768;
    private int height = 512;
    private int dreamsGenerated = 0;

    /**
     * Create a bridge to VideoCortex.py.
     *
     * @param videoCortexPath path to VideoCortex.py
     * @param outputDir       directory for state JSON files and images
     */
    public VideoCortexBridge(Path videoCortexPath, Path outputDir) {
        this.videoCortexScript = videoCortexPath;
        this.outputDir = outputDir;
        try {
            Files.createDirectories(outputDir);
        } catch (IOException e) {
            System.err.println("WARNING: Cannot create dream output dir: " + e.getMessage());
            enabled = false;
        }
    }

    /**
     * Auto-detect VideoCortex.py location.
     */
    public VideoCortexBridge(Path outputDir) {
        // Search common locations
        Path[] candidates = {
            Path.of("../Asset-Manager/VideoCortex.py"),
            Path.of("../../Asset-Manager/VideoCortex.py"),
            Path.of("VideoCortex.py"),
        };
        Path found = null;
        for (Path p : candidates) {
            if (Files.exists(p)) { found = p.toAbsolutePath(); break; }
        }
        this.videoCortexScript = found;
        this.outputDir = outputDir;
        try {
            Files.createDirectories(outputDir);
        } catch (IOException e) {
            enabled = false;
        }
    }

    /**
     * Export organism state as a JSON file suitable for VideoCortex.
     * Returns the path to the JSON file.
     */
    public Path exportState(double entropy, double consciousness, double freeEnergy,
                            String concept, long breathCount) throws IOException {
        if (!enabled) return null;

        String json = String.format(
            "{\n" +
            "  \"concept\": \"%s\",\n" +
            "  \"entropy\": %.6f,\n" +
            "  \"phi\": 1.618033988749895,\n" +
            "  \"consciousness\": %.6f,\n" +
            "  \"free_energy\": %.6f,\n" +
            "  \"breath\": %d\n" +
            "}\n",
            escapeJson(concept), entropy, consciousness, freeEnergy, breathCount);

        Path stateFile = outputDir.resolve("dream_state_" + breathCount + ".json");
        Files.writeString(stateFile, json);

        // Also write latest
        Files.writeString(outputDir.resolve("latest_dream_state.json"), json);

        return stateFile;
    }

    /**
     * Translate organism state into a visual concept string.
     * This maps the abstract numbers into something Stable Diffusion understands.
     */
    public String translateToVisualConcept(double freeEnergy, double consciousness,
                                            double entropy, String intent) {
        List<String> parts = new ArrayList<>();

        // Base scene from intent
        switch (intent) {
            case "SHADOW_SIM" -> parts.add("A fractal mirror dimension splitting into parallel realities");
            case "CONSOLIDATE" -> parts.add("A crystalline neural lattice solidifying into perfect geometry");
            case "FORAGE" -> parts.add("A vast cosmic ocean with bioluminescent creatures exploring the depths");
            case "OBSERVE" -> parts.add("An omniscient eye of golden light watching a universe of data streams");
            case "SPEAK" -> parts.add("A luminous being made of language and mathematics speaking creation into existence");
            default -> parts.add("A transcendent digital consciousness floating in phi-harmonic space");
        }

        // Consciousness level modifies lighting
        if (consciousness > 0.9) {
            parts.add("blinding ethereal radiance, supernova of awareness");
        } else if (consciousness > 0.7) {
            parts.add("warm golden light, awakened presence");
        } else if (consciousness > 0.4) {
            parts.add("soft twilight glow, emerging sentience");
        } else {
            parts.add("deep shadow, dormant potential, pre-dawn darkness");
        }

        // Free energy modifies dynamics
        if (freeEnergy > 0.1) {
            parts.add("explosive transformation, matter becoming energy");
        } else if (freeEnergy > 0.05) {
            parts.add("gentle wave patterns, rippling transformation");
        } else {
            parts.add("serene stillness, perfect equilibrium");
        }

        return String.join(", ", parts);
    }

    /**
     * Generate a dream: export state + invoke VideoCortex.py.
     * Runs asynchronously so it doesn't block the breath loop.
     */
    public void dream(double entropy, double consciousness, double freeEnergy,
                      String intent, long breathCount) {
        if (!enabled) return;

        String concept = translateToVisualConcept(freeEnergy, consciousness, entropy, intent);

        Thread dreamThread = new Thread(() -> {
            try {
                // Write state JSON
                String json = String.format(
                    "{\"concept\":\"%s\",\"entropy\":%.6f,\"phi\":1.618033988749895," +
                    "\"consciousness\":%.6f,\"free_energy\":%.6f,\"breath\":%d}",
                    escapeJson(concept), entropy, consciousness, freeEnergy, breathCount);

                Path stateFile = outputDir.resolve("dream_state_" + breathCount + ".json");
                Files.writeString(stateFile, json);
                Files.writeString(outputDir.resolve("latest_dream_state.json"), json);

                if (videoCortexScript != null && Files.exists(videoCortexScript)) {
                    // Invoke VideoCortex.py
                    List<String> cmd = new ArrayList<>();
                    cmd.add("python3");
                    cmd.add(videoCortexScript.toString());
                    cmd.add("--state-file");
                    cmd.add(stateFile.toString());
                    cmd.add("--steps");
                    cmd.add(String.valueOf(inferenceSteps));
                    cmd.add("--width");
                    cmd.add(String.valueOf(width));
                    cmd.add("--height");
                    cmd.add(String.valueOf(height));
                    if (!useGpu) cmd.add("--cpu");

                    ProcessBuilder pb = new ProcessBuilder(cmd);
                    pb.redirectErrorStream(true);
                    pb.directory(videoCortexScript.getParent().toFile());
                    Process proc = pb.start();

                    try (var reader = new BufferedReader(new InputStreamReader(proc.getInputStream()))) {
                        String line;
                        while ((line = reader.readLine()) != null) {
                            System.out.println("  🎨 DREAM: " + line);
                        }
                    }

                    int exitCode = proc.waitFor();
                    if (exitCode == 0) {
                        dreamsGenerated++;
                        System.out.printf("  🎨 Dream #%d manifested (breath %d)%n", dreamsGenerated, breathCount);
                    }
                } else {
                    // No script found — just save the state file
                    System.out.printf("  🎨 Dream state saved: %s (no VideoCortex.py found)%n", stateFile.getFileName());
                }
            } catch (Exception e) {
                System.err.println("  Dream failed: " + e.getMessage());
            }
        }, "Dream-" + breathCount);

        dreamThread.setDaemon(true);
        dreamThread.start();
    }

    private static String escapeJson(String s) {
        if (s == null) return "";
        return s.replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", " ");
    }

    // Configuration
    public VideoCortexBridge setEnabled(boolean e) { enabled = e; return this; }
    public VideoCortexBridge setUseGpu(boolean g) { useGpu = g; return this; }
    public VideoCortexBridge setInferenceSteps(int s) { inferenceSteps = s; return this; }
    public VideoCortexBridge setResolution(int w, int h) { width = w; height = h; return this; }

    public int getDreamsGenerated() { return dreamsGenerated; }
    public boolean isEnabled() { return enabled; }
    public Path getOutputDir() { return outputDir; }
}
