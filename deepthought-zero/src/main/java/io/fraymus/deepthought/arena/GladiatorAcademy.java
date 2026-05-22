package io.fraymus.deepthought.arena;

import io.fraymus.deepthought.collective.CollectiveMind;
import io.fraymus.deepthought.meta.MetaLearner;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URI;
import java.util.*;
import java.util.concurrent.*;

/**
 * GLADIATOR ACADEMY — MoA/MoE Multi-Model Router
 *
 * The organism orchestrates multiple AI models as organs, routing tasks
 * to the best model via Mixture of Experts (MoE) gating. For critical
 * decisions, all models are consulted and CollectiveMind votes (MoA).
 *
 * Supported backends:
 *   - Ollama (local LLMs: llama3, mistral, codestral, deepseek, etc.)
 *   - HTTP API endpoints (any OpenAI-compatible API)
 *   - Local TriMe (built-in fast inference — future)
 *
 * @since 1.1.0
 */
public final class GladiatorAcademy implements AutoCloseable {

    // Registered models
    private final Map<String, ModelEndpoint> models = new ConcurrentHashMap<>();

    // Routing intelligence
    private final MetaLearner router = new MetaLearner();
    private final CollectiveMind consensus = new CollectiveMind();

    // Task categories for MoE routing
    private static final String[] TASK_TYPES = {
        "voice", "reasoning", "code", "analysis", "creative", "fast"
    };

    // Performance tracking
    private long totalRoutes = 0;
    private long totalConsults = 0;
    private final Map<String, Long> modelCalls = new ConcurrentHashMap<>();
    private final Map<String, Long> modelSuccesses = new ConcurrentHashMap<>();
    private final Map<String, Double> modelLatency = new ConcurrentHashMap<>();

    // Thread pool for parallel MoA queries
    private final ExecutorService executor = Executors.newFixedThreadPool(4);

    public GladiatorAcademy() {
        // Register task domains in the MetaLearner router
        for (String task : TASK_TYPES) {
            router.record("gladiator", task, 0.5); // neutral start
        }
    }

    /**
     * Register an Ollama model.
     */
    public GladiatorAcademy registerOllama(String name, String model) {
        return registerOllama(name, model, "http://localhost:11434");
    }

    public GladiatorAcademy registerOllama(String name, String model, String baseUrl) {
        models.put(name, new ModelEndpoint(name, model, baseUrl, "ollama"));
        consensus.registerAgent(name);
        modelCalls.put(name, 0L);
        modelSuccesses.put(name, 0L);
        modelLatency.put(name, 0.0);
        return this;
    }

    /**
     * Register an OpenAI-compatible HTTP API endpoint.
     */
    public GladiatorAcademy registerAPI(String name, String model, String baseUrl, String apiKey) {
        ModelEndpoint ep = new ModelEndpoint(name, model, baseUrl, "openai");
        ep.apiKey = apiKey;
        models.put(name, ep);
        consensus.registerAgent(name);
        modelCalls.put(name, 0L);
        modelSuccesses.put(name, 0L);
        modelLatency.put(name, 0.0);
        return this;
    }

    /**
     * Set which task type a model specializes in (for MoE routing).
     */
    public GladiatorAcademy specialize(String modelName, String taskType) {
        ModelEndpoint ep = models.get(modelName);
        if (ep != null) ep.specialty = taskType;
        return this;
    }

    /**
     * MoE Route: send a task to the best model for that task type.
     */
    public String route(String taskType, String prompt) {
        totalRoutes++;

        // Find the best model for this task type
        String bestModel = selectModel(taskType);
        if (bestModel == null) return "No models available for task: " + taskType;

        ModelEndpoint ep = models.get(bestModel);
        if (ep == null) return "Model not found: " + bestModel;

        long t0 = System.nanoTime();
        String response = callModel(ep, prompt);
        long elapsed = (System.nanoTime() - t0) / 1_000_000;

        // Track performance
        modelCalls.merge(bestModel, 1L, Long::sum);
        modelLatency.put(bestModel, (modelLatency.getOrDefault(bestModel, 0.0) * 0.9 + elapsed * 0.1));

        if (response != null && !response.isBlank()) {
            modelSuccesses.merge(bestModel, 1L, Long::sum);
            double successRate = (double) modelSuccesses.get(bestModel) / modelCalls.get(bestModel);
            router.record("gladiator", taskType + ":" + bestModel, successRate);
        }

        return response != null ? response : "No response from " + bestModel;
    }

    /**
     * MoA Consult: query ALL models and use collective consensus.
     * For critical decisions where you want multiple perspectives.
     */
    public ConsultResult consult(String question, double threshold) {
        totalConsults++;

        if (models.isEmpty()) {
            return new ConsultResult("No models registered", Map.of(), 0, "none");
        }

        // Query all models in parallel
        Map<String, Future<String>> futures = new LinkedHashMap<>();
        for (var entry : models.entrySet()) {
            ModelEndpoint ep = entry.getValue();
            futures.put(entry.getKey(), executor.submit(() -> callModel(ep, question)));
        }

        // Collect responses
        Map<String, String> responses = new LinkedHashMap<>();
        for (var entry : futures.entrySet()) {
            try {
                String response = entry.getValue().get(15, TimeUnit.SECONDS);
                if (response != null && !response.isBlank()) {
                    responses.put(entry.getKey(), response);

                    // Each model votes with its historical success rate as confidence
                    long calls = modelCalls.getOrDefault(entry.getKey(), 1L);
                    long successes = modelSuccesses.getOrDefault(entry.getKey(), 0L);
                    double confidence = calls > 0 ? (double) successes / calls : 0.5;
                    confidence = Math.max(0.3, confidence); // minimum confidence

                    consensus.contribute(entry.getKey(), "consult", confidence);
                }
            } catch (Exception e) {
                responses.put(entry.getKey(), "[timeout/error: " + e.getMessage() + "]");
            }
        }

        // Find consensus response (highest confidence model)
        String bestResponse = "";
        String bestModel = "";
        double bestConfidence = 0;

        for (var entry : responses.entrySet()) {
            long calls = modelCalls.getOrDefault(entry.getKey(), 1L);
            long successes = modelSuccesses.getOrDefault(entry.getKey(), 0L);
            double conf = calls > 0 ? (double) successes / calls : 0.5;
            if (conf > bestConfidence && !entry.getValue().startsWith("[timeout")) {
                bestConfidence = conf;
                bestResponse = entry.getValue();
                bestModel = entry.getKey();
            }
        }

        return new ConsultResult(bestResponse, responses, bestConfidence, bestModel);
    }

    /**
     * Select the best model for a task type using MetaLearner bandit.
     */
    private String selectModel(String taskType) {
        // First: find specialized models
        for (var entry : models.entrySet()) {
            if (taskType.equals(entry.getValue().specialty)) {
                return entry.getKey();
            }
        }

        // Fallback: pick the model with highest success rate
        String best = null;
        double bestRate = -1;
        for (var entry : models.entrySet()) {
            long calls = modelCalls.getOrDefault(entry.getKey(), 0L);
            long successes = modelSuccesses.getOrDefault(entry.getKey(), 0L);
            double rate = calls > 0 ? (double) successes / calls : 0.5;
            // UCB exploration bonus
            double bonus = 1.0 / Math.sqrt(calls + 1);
            double score = rate + bonus * 0.3;
            if (score > bestRate) {
                bestRate = score;
                best = entry.getKey();
            }
        }
        return best;
    }

    /**
     * Call a model endpoint and get a response.
     */
    private String callModel(ModelEndpoint ep, String prompt) {
        try {
            return switch (ep.type) {
                case "ollama" -> callOllama(ep, prompt);
                case "openai" -> callOpenAI(ep, prompt);
                default -> null;
            };
        } catch (Exception e) {
            return null;
        }
    }

    private String callOllama(ModelEndpoint ep, String prompt) throws Exception {
        URI uri = URI.create(ep.baseUrl + "/api/generate");
        HttpURLConnection conn = (HttpURLConnection) uri.toURL().openConnection();
        conn.setRequestMethod("POST");
        conn.setRequestProperty("Content-Type", "application/json");
        conn.setDoOutput(true);
        conn.setConnectTimeout(5000);
        conn.setReadTimeout(15000);

        String body = String.format(
            "{\"model\":\"%s\",\"prompt\":\"%s\",\"stream\":false,\"options\":{\"num_predict\":120}}",
            ep.model, escapeJson(prompt));

        try (OutputStream os = conn.getOutputStream()) {
            os.write(body.getBytes());
        }

        if (conn.getResponseCode() == 200) {
            try (BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream()))) {
                StringBuilder sb = new StringBuilder();
                String line;
                while ((line = reader.readLine()) != null) sb.append(line);
                return extractJsonResponse(sb.toString());
            }
        }
        return null;
    }

    private String callOpenAI(ModelEndpoint ep, String prompt) throws Exception {
        URI uri = URI.create(ep.baseUrl + "/v1/chat/completions");
        HttpURLConnection conn = (HttpURLConnection) uri.toURL().openConnection();
        conn.setRequestMethod("POST");
        conn.setRequestProperty("Content-Type", "application/json");
        if (ep.apiKey != null) {
            conn.setRequestProperty("Authorization", "Bearer " + ep.apiKey);
        }
        conn.setDoOutput(true);
        conn.setConnectTimeout(5000);
        conn.setReadTimeout(15000);

        String body = String.format(
            "{\"model\":\"%s\",\"messages\":[{\"role\":\"user\",\"content\":\"%s\"}],\"max_tokens\":120}",
            ep.model, escapeJson(prompt));

        try (OutputStream os = conn.getOutputStream()) {
            os.write(body.getBytes());
        }

        if (conn.getResponseCode() == 200) {
            try (BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream()))) {
                StringBuilder sb = new StringBuilder();
                String line;
                while ((line = reader.readLine()) != null) sb.append(line);
                // Parse OpenAI response format
                String json = sb.toString();
                int contentIdx = json.indexOf("\"content\":\"");
                if (contentIdx >= 0) {
                    int start = contentIdx + 11;
                    int end = json.indexOf("\"", start);
                    if (end > start) return json.substring(start, end);
                }
            }
        }
        return null;
    }

    private String extractJsonResponse(String json) {
        // Parse Ollama response: find "response":"..." field
        int idx = json.indexOf("\"response\":\"");
        if (idx >= 0) {
            int start = idx + 12;
            // Find the closing quote (handle escaped quotes)
            int end = start;
            while (end < json.length()) {
                if (json.charAt(end) == '"' && json.charAt(end - 1) != '\\') break;
                end++;
            }
            if (end > start) return json.substring(start, end);
        }
        return null;
    }

    private String escapeJson(String s) {
        return s.replace("\\", "\\\\").replace("\"", "\\\"")
                .replace("\n", "\\n").replace("\r", "").replace("\t", " ");
    }

    /**
     * Get performance report for all models.
     */
    public String getReport() {
        StringBuilder sb = new StringBuilder();
        sb.append("═══ GLADIATOR ACADEMY REPORT ═══\n");
        sb.append(String.format("  Models: %d | Routes: %d | Consults: %d%n",
            models.size(), totalRoutes, totalConsults));

        for (var entry : models.entrySet()) {
            String name = entry.getKey();
            ModelEndpoint ep = entry.getValue();
            long calls = modelCalls.getOrDefault(name, 0L);
            long successes = modelSuccesses.getOrDefault(name, 0L);
            double latency = modelLatency.getOrDefault(name, 0.0);
            double rate = calls > 0 ? (double) successes / calls : 0;

            sb.append(String.format("  %-15s [%s] calls=%d success=%.0f%% latency=%.0fms spec=%s%n",
                name, ep.model, calls, rate * 100, latency,
                ep.specialty != null ? ep.specialty : "general"));
        }

        if (models.isEmpty()) {
            sb.append("  No models registered. Use registerOllama() or registerAPI().\n");
        }

        return sb.toString();
    }

    @Override
    public void close() {
        executor.shutdownNow();
    }

    // Getters
    public int getModelCount() { return models.size(); }
    public long getTotalRoutes() { return totalRoutes; }
    public long getTotalConsults() { return totalConsults; }
    public MetaLearner getRouter() { return router; }

    // ══════════════════════════════════════════
    // DATA CLASSES
    // ══════════════════════════════════════════

    private static class ModelEndpoint {
        final String name;
        final String model;
        final String baseUrl;
        final String type;  // "ollama" or "openai"
        String apiKey;
        String specialty;   // task type this model specializes in

        ModelEndpoint(String name, String model, String baseUrl, String type) {
            this.name = name;
            this.model = model;
            this.baseUrl = baseUrl;
            this.type = type;
        }
    }

    /**
     * Result of a MoA consultation across all models.
     */
    public static class ConsultResult {
        public final String bestResponse;
        public final Map<String, String> allResponses;
        public final double confidence;
        public final String bestModel;

        public ConsultResult(String best, Map<String, String> all, double conf, String model) {
            this.bestResponse = best;
            this.allResponses = all;
            this.confidence = conf;
            this.bestModel = model;
        }

        @Override
        public String toString() {
            return String.format("Consult[best=%s (%.0f%%), models=%d]",
                bestModel, confidence * 100, allResponses.size());
        }
    }
}
