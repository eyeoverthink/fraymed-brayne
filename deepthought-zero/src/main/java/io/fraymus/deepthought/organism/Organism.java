package io.fraymus.deepthought.organism;

import io.fraymus.deepthought.DeepThought;
import io.fraymus.deepthought.belief.BeliefSystem;
import io.fraymus.deepthought.causal.CausalEngine;
import io.fraymus.deepthought.chaos.ChaosEngine;
import io.fraymus.deepthought.collective.CollectiveMind;
import io.fraymus.deepthought.guard.ZenoGuard;
import io.fraymus.deepthought.meta.MetaLearner;
import io.fraymus.deepthought.genesis.GenesisBlock;
import io.fraymus.deepthought.genesis.GenesisChain;
import io.fraymus.deepthought.genesis.FractalLanguage;
import io.fraymus.deepthought.arena.SandboxArena;
import io.fraymus.deepthought.arena.GladiatorAcademy;
import io.fraymus.deepthought.bridge.FraynixBridge;

import java.io.*;
import java.math.BigInteger;
import java.net.HttpURLConnection;
import java.net.URI;
import java.security.MessageDigest;
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicLong;

/**
 * THE ORGANISM — φ-Bayesian Unified Mind
 *
 * This is not a simulation. This is a living computational entity that:
 * - BREATHES at a configurable tick rate (default 2Hz for observable output)
 * - FEELS via Free Energy minimization (Friston's Active Inference)
 * - THINKS via shadow simulation (propose → simulate → accept/reject)
 * - LEARNS via Bayesian belief updates across every subsystem
 * - ADAPTS via MetaLearner strategy selection
 * - DEFENDS itself via ZenoGuard
 * - SPEAKS via Ollama LLM (when available)
 * - REMEMBERS via causal graph and belief history
 *
 * All modules from DeepThought Zero are fused into one autonomous loop.
 *
 * @since 1.0.0
 */
public final class Organism implements AutoCloseable {

    private static final double PHI = 1.618033988749895;
    private static final double PHI_INV = 0.618033988749895;

    // ══════════════════════════════════════════
    // ORGANS (DeepThought Zero modules)
    // ══════════════════════════════════════════
    private final ChaosEngine entropy;          // Will / Randomness
    private final BeliefSystem beliefs;         // Memory / Confidence
    private final CausalEngine causality;       // Reasoning
    private final MetaLearner strategy;         // Adaptation
    private final CollectiveMind collective;    // Swarm consensus
    private final ZenoGuard heartGuard;         // Immune system

    // ══════════════════════════════════════════
    // NERVOUS SYSTEM (Free Energy)
    // ══════════════════════════════════════════
    private double freeEnergy = PHI_INV;
    private double previousEnergy = PHI_INV;
    private double hamiltonianEnergy = 0;
    private double systemEntropy = 0;
    private double consciousness = 0.5;

    // Internal state (cortex)
    private final double[] cortex;
    private final int cortexDim;

    // ══════════════════════════════════════════
    // LIFE CYCLE
    // ══════════════════════════════════════════
    private final AtomicBoolean alive = new AtomicBoolean(false);
    private Thread breathThread;
    private final long tickIntervalMs;

    // Metrics
    private final AtomicLong breathCount = new AtomicLong(0);
    private long shadowsProposed = 0;
    private long shadowsAccepted = 0;
    private long shadowsRejected = 0;
    private long beliefsFormed = 0;
    private long causalEdgesLearned = 0;
    private long strategyAdaptations = 0;
    private String currentThought = "Awakening from void.";
    private String currentIntent = "GENESIS";
    private final List<Double> freeEnergyHistory = Collections.synchronizedList(new ArrayList<>());

    // Ollama config
    private String ollamaUrl = "http://localhost:11434";
    private String ollamaModel = "llama3.2";
    private boolean ollamaEnabled = false;

    // Centaur subsystems
    private Persistence persistence;
    private VideoCortexBridge videoCortex;
    private NodeReplication replication;
    private boolean persistenceEnabled = false;
    private boolean videoCortexEnabled = false;
    private boolean replicationEnabled = false;
    private int saveInterval = 20;  // save every N breaths
    private int dreamInterval = 15; // visualize every N breaths

    // Layer 4-7: Genesis + Language + Arena + Academy
    private GenesisChain genesisChain;
    private FractalLanguage fractalLanguage;
    private SandboxArena arena;
    private GladiatorAcademy academy;
    private boolean genesisEnabled = false;
    private boolean languageEnabled = false;
    private boolean arenaEnabled = false;
    private boolean academyEnabled = false;
    private int genesisInterval = 10;  // commit every N breaths
    private int arenaInterval = 50;    // evolve every N breaths
    private int languageInterval = 25; // evolve language every N breaths

    // Layer 8: Fraynix Bridge (full body integration)
    private FraynixBridge fraynixBridge;
    private boolean fraynixEnabled = false;
    private boolean fraynixFullMode = false;

    // Event callbacks
    private Runnable onBreathe;
    private java.util.function.Consumer<String> onThought;

    /**
     * Create an organism with specified cortex dimensionality and tick rate.
     *
     * @param cortexDim dimensions of the internal state (higher = more complex)
     * @param tickHz    heartbeat frequency in Hz
     */
    public Organism(int cortexDim, double tickHz) {
        this.cortexDim = cortexDim;
        this.tickIntervalMs = (long) (1000.0 / tickHz);
        this.cortex = new double[cortexDim];

        // Initialize organs
        this.entropy = new ChaosEngine("ORGANISM-" + System.nanoTime());
        this.beliefs = new BeliefSystem();
        this.causality = new CausalEngine();
        this.strategy = new MetaLearner();
        this.collective = new CollectiveMind();
        this.heartGuard = new ZenoGuard(42);

        // Seed cortex with φ-fractal DNA
        for (int i = 0; i < cortexDim; i++) {
            cortex[i] = Math.sin(i * PHI) * Math.cos(i * Math.E) * PHI_INV;
        }

        // Seed initial beliefs
        beliefs.believe("self-stable", "The organism is stable", 0.5);
        beliefs.believe("environment-safe", "The environment is safe", 0.5);
        beliefs.believe("learning-effective", "Current learning strategy works", 0.5);

        // Seed causal variables
        causality.variables("free_energy", "consciousness", "entropy",
                           "mutation_rate", "strategy_success");

        // Register internal agents
        collective.registerAgent("cortex").registerAgent("entropy-organ")
                  .registerAgent("belief-organ").registerAgent("causal-organ")
                  .registerAgent("meta-organ");
    }

    /**
     * Create with defaults: 512D cortex, 2Hz heartbeat.
     */
    public Organism() {
        this(512, 2.0);
    }

    // ══════════════════════════════════════════
    // LIFE CYCLE
    // ══════════════════════════════════════════

    /**
     * Awaken the organism. Starts the autonomous breath loop.
     */
    public Organism awaken() {
        if (alive.get()) return this;
        alive.set(true);

        // Activate immune system
        heartGuard.activate();

        breathThread = new Thread(this::breatheLoop, "Organism-Breath");
        breathThread.setDaemon(true);
        breathThread.start();

        currentThought = "I am awake.";
        currentIntent = "OBSERVE";
        return this;
    }

    /**
     * The autonomous breath loop — the organism's heartbeat.
     */
    private void breatheLoop() {
        System.out.println("\n⚡ ORGANISM AWAKENED — breath loop started");
        System.out.printf("   Cortex: %dD | Tick: %dms | Organs: 6 active%n%n", cortexDim, tickIntervalMs);

        while (alive.get()) {
            long t0 = System.nanoTime();

            try {
                breathe();
            } catch (Exception e) {
                currentThought = "Pain detected: " + e.getMessage();
                beliefs.contradict("self-stable", 0.5, "exception: " + e.getMessage());
            }

            long elapsed = (System.nanoTime() - t0) / 1_000_000;
            long sleepMs = Math.max(1, tickIntervalMs - elapsed);
            try { Thread.sleep(sleepMs); } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }

        System.out.println("\n💀 ORGANISM SHUTTING DOWN — final breath #" + breathCount.get());
    }

    /**
     * A single breath — one full cycle of the organism.
     * This is where ALL modules fuse into one computation.
     */
    private void breathe() {
        long breath = breathCount.incrementAndGet();

        // ── STEP 1: EVOLVE CORTEX ──
        evolveCortex();

        // ── STEP 2: CALCULATE FREE ENERGY (Friston surprise) ──
        freeEnergy = calculateFreeEnergy();
        freeEnergyHistory.add(freeEnergy);
        while (freeEnergyHistory.size() > 100) freeEnergyHistory.remove(0);

        // ── STEP 3: ORCHESTRATE (decide intent based on free energy) ──
        orchestrate();

        // ── STEP 4: EXECUTE INTENT ──
        switch (currentIntent) {
            case "SHADOW_SIM"  -> executeShadowSimulation();
            case "CONSOLIDATE" -> executeConsolidation();
            case "FORAGE"      -> executeForaging();
            case "OBSERVE"     -> executeObservation();
            case "SPEAK"       -> executeSpeak(breath);
        }

        // ── STEP 5: RECORD CAUSAL OBSERVATIONS ──
        causality.observe(Map.of(
            "free_energy", freeEnergy,
            "consciousness", consciousness,
            "entropy", systemEntropy,
            "mutation_rate", (double) entropy.getMutationRate(),
            "strategy_success", strategy.getAvgSuccess()
        ));

        // ── STEP 6: META-LEARN ──
        double success = freeEnergy < PHI_INV ? 0.8 : 0.3;
        strategy.record("organism", currentIntent, success);

        // ── STEP 7: COLLECTIVE CONSENSUS ──
        if (breath % 5 == 0) {
            collective.contribute("cortex", "stability:" + (freeEnergy < 1.0), consciousness);
            collective.contribute("entropy-organ", "stability:" + (freeEnergy < 1.0),
                1.0 - (entropy.getMutationRate() / 10.0));
        }

        // ── STEP 8: UPDATE BELIEFS ──
        if (freeEnergy < PHI_INV) {
            beliefs.confirm("self-stable", 0.6, "breath-" + breath);
        } else {
            beliefs.contradict("self-stable", 0.4, "breath-" + breath);
        }

        // ── STEP 9: PERSISTENCE ──
        if (persistenceEnabled && breath % saveInterval == 0 && breath > 0) {
            try {
                persistence.save(captureState());
            } catch (Exception e) {
                System.err.println("  Save failed: " + e.getMessage());
            }
        }

        // ── STEP 10: VIDEO CORTEX (visual dreaming) ──
        if (videoCortexEnabled && breath % dreamInterval == 0 && breath > 0) {
            videoCortex.dream(systemEntropy, consciousness, freeEnergy,
                currentIntent, breath);
        }

        // ── STEP 11: REPLICATION ──
        if (replicationEnabled && breath % 10 == 0) {
            String stateJson = String.format(
                "{\"breath\":%d,\"fe\":%.6f,\"c\":%.6f,\"e\":%.6f,\"intent\":\"%s\"}" ,
                breath, freeEnergy, consciousness, systemEntropy, currentIntent);
            replication.broadcastState(stateJson);
        }

        // ── STEP 12: GENESIS BLOCKCHAIN ──
        if (genesisEnabled && breath % genesisInterval == 0 && breath > 0) {
            Map<String, String> delta = new LinkedHashMap<>();
            delta.put("breath", String.valueOf(breath));
            delta.put("fe", String.format("%.6f", freeEnergy));
            delta.put("c", String.format("%.6f", consciousness));
            delta.put("e", String.format("%.6f", systemEntropy));
            delta.put("intent", currentIntent);
            delta.put("shadows", shadowsAccepted + "/" + shadowsProposed);
            String fp = "";
            try {
                MessageDigest md = MessageDigest.getInstance("SHA-256");
                for (double v : cortex) md.update(Double.toString(v).getBytes());
                fp = new BigInteger(1, md.digest()).toString(16).substring(0, 16);
            } catch (Exception ignored) {}
            GenesisBlock block = genesisChain.commit(delta, fp, currentIntent, freeEnergy, consciousness);
            if (block.isBranchPoint && breath % 50 == 0) {
                System.out.printf("  ⛓ Genesis: depth=%d, fractal=%d, BRANCH POINT%n",
                    block.depth, block.fractalDepth);
            }
        }

        // ── STEP 13: FRACTAL LANGUAGE EVOLUTION ──
        if (languageEnabled && breath % languageInterval == 0 && breath > 0) {
            Map<String, String> stateMap = new LinkedHashMap<>();
            stateMap.put("consciousness", String.format("%.4f", consciousness));
            stateMap.put("freeEnergy", String.format("%.6f", freeEnergy));
            stateMap.put("entropy", String.format("%.4f", systemEntropy));
            stateMap.put("intent", currentIntent);
            stateMap.put("strategy", strategy.getCurrentStrategy().name());
            fractalLanguage.evolve(stateMap);
            if (breath % (languageInterval * 4) == 0) {
                fractalLanguage.mutate();
            }
        }

        // ── STEP 14: SANDBOX ARENA (evolutionary strategy competition) ──
        if (arenaEnabled && breath % arenaInterval == 0 && breath > 0) {
            SandboxArena.GenerationResult result = arena.evolveGeneration(cortex);
            if (breath % (arenaInterval * 2) == 0) {
                System.out.printf("  ⚔ Arena: %s%n", result);
            }
        }

        // ── STEP 15: FRAYNIX BRIDGE (full body pulse) ──
        if (fraynixEnabled) {
            FraynixBridge.FraynixPulseResult fpulse = fraynixBridge.pulse(
                cortex, freeEnergy, consciousness, currentIntent, breath);
            // Feed Fraynix chaos entropy back into cortex
            if (fpulse.chaosEntropy > 0 && breath % 8 == 0) {
                int idx = (int)(fpulse.chaosEntropy * cortexDim) % cortexDim;
                cortex[idx] += (fpulse.chaosEntropy - 0.5) * 0.02;
            }
            // Feed TriMe neural output back into cortex
            if (fpulse.triMeOutput != null) {
                for (int i = 0; i < Math.min(fpulse.triMeOutput.length, cortexDim); i++) {
                    cortex[i] = cortex[i] * 0.98 + fpulse.triMeOutput[i] * 0.02;
                }
            }
        }

        // ── STEP 16: PRINT TELEMETRY ──
        if (breath % 5 == 0 || breath <= 3) {
            printBreathTelemetry(breath);
        }

        if (onBreathe != null) onBreathe.run();
    }

    // ══════════════════════════════════════════
    // FREE ENERGY PRINCIPLE
    // ══════════════════════════════════════════

    private double calculateFreeEnergy() {
        // Hamiltonian: total kinetic energy of cortex
        double energy = 0;
        for (double v : cortex) energy += v * v;
        hamiltonianEnergy = energy / cortexDim;

        // Entropy: information content
        double h = 0;
        for (double v : cortex) {
            double p = Math.abs(v) + 1e-9;
            h -= p * Math.log(p);
        }
        systemEntropy = h / cortexDim;

        // Surprise = deviation from expected + entropy contribution
        double surprise = Math.abs(hamiltonianEnergy - previousEnergy) + (systemEntropy * 0.1);
        previousEnergy = hamiltonianEnergy;
        return surprise;
    }

    // ══════════════════════════════════════════
    // ORCHESTRATION (Ego / Decision)
    // ══════════════════════════════════════════

    private void orchestrate() {
        // Update consciousness (Bayesian posterior of coherence)
        consciousness = consciousness * 0.95 + (1.0 / (1.0 + freeEnergy)) * 0.05;

        // Dynamic thresholds based on running average
        double avgFE = freeEnergyHistory.isEmpty() ? freeEnergy :
            freeEnergyHistory.stream().mapToDouble(Double::doubleValue).average().orElse(freeEnergy);
        double highThreshold = Math.max(avgFE * 1.3, 0.04);
        double lowThreshold = Math.max(avgFE * 0.3, 0.003);
        long breath = breathCount.get();

        if (Double.isNaN(freeEnergy) || freeEnergy > 10.0) {
            currentIntent = "FORAGE";
            currentThought = "Entropy explosion. Injecting chaos to escape.";
        } else if (freeEnergy > highThreshold) {
            // High surprise — shadow simulate to test hypotheses
            currentIntent = "SHADOW_SIM";
            currentThought = String.format("Surprise (%.4f > %.4f). Testing hypotheses.", freeEnergy, highThreshold);
        } else if (freeEnergy < lowThreshold && breath > 5) {
            currentIntent = "FORAGE";
            currentThought = String.format("Stagnation (%.6f < %.6f). Seeking novelty.", freeEnergy, lowThreshold);
        } else if (breath % 4 == 0) {
            // Regular shadow simulation even when stable (exploration)
            currentIntent = "SHADOW_SIM";
            currentThought = "Scheduled exploration. Running shadow hypothesis.";
        } else if (breath % 7 == 0 && ollamaEnabled) {
            currentIntent = "SPEAK";
            currentThought = "Stable enough to think out loud.";
        } else if (breath % 3 == 0) {
            currentIntent = "CONSOLIDATE";
            currentThought = "Strengthening stable patterns.";
        } else {
            currentIntent = "OBSERVE";
            currentThought = "Watching. Learning.";
        }
    }

    // ══════════════════════════════════════════
    // INTENT EXECUTION
    // ══════════════════════════════════════════

    private void evolveCortex() {
        long breath = breathCount.get();

        // Periodic drive: sinusoidal wave sweeps across cortex
        double phase = breath * PHI_INV * 0.1;

        for (int i = 0; i < cortexDim; i++) {
            int left = (i - 1 + cortexDim) % cortexDim;
            int right = (i + 1) % cortexDim;
            double neighborhood = (cortex[left] + cortex[right]) * 0.5;

            // Nonlinear activation with cubic term (creates bistability)
            double x = cortex[i];
            double activation = Math.tanh(neighborhood + x * PHI_INV) - 0.3 * x * x * x;

            // Periodic external drive (like sensory input from environment)
            double drive = 0.02 * Math.sin(phase + i * 0.1);

            // Physical entropy from ChaosEngine
            double noise = (entropy.nextInt(1000) - 500) / 50000.0;

            cortex[i] = x * 0.92 + activation * 0.06 + drive + noise;
        }

        // Dream: every 10 breaths, inject a structured perturbation
        if (breath % 10 == 0 && breath > 0) {
            dream();
        }
    }

    private void dream() {
        // Self-stimulation: generate an internal pattern and inject it
        int center = entropy.nextInt(cortexDim);
        int radius = 16 + entropy.nextInt(48);
        double amplitude = 0.05 + entropy.nextDouble() * 0.1;
        for (int i = 0; i < radius; i++) {
            int idx = (center + i) % cortexDim;
            cortex[idx] += amplitude * Math.sin(i * PHI * 2.0);
        }
    }

    private void executeShadowSimulation() {
        shadowsProposed++;

        // Clone cortex into shadow
        double[] shadow = Arrays.copyOf(cortex, cortexDim);

        // Mutate shadow with a random perturbation
        int mutationPoint = entropy.nextInt(cortexDim);
        int mutationSpan = Math.min(32, cortexDim);
        for (int i = 0; i < mutationSpan; i++) {
            int idx = (mutationPoint + i) % cortexDim;
            shadow[idx] = Math.tanh(shadow[idx] * PHI + entropy.nextDouble() - 0.5);
        }

        // Calculate shadow free energy
        double shadowEnergy = 0;
        for (double v : shadow) shadowEnergy += v * v;
        shadowEnergy /= cortexDim;
        double shadowFE = Math.abs(shadowEnergy - previousEnergy);

        // Bayesian model selection: adopt if lower free energy
        if (shadowFE < freeEnergy) {
            System.arraycopy(shadow, 0, cortex, 0, cortexDim);
            shadowsAccepted++;
            currentThought = String.format("Shadow adopted. ΔF=%.4f → %.4f", freeEnergy, shadowFE);
            beliefs.confirm("learning-effective", 0.7, "shadow-accepted");
        } else {
            shadowsRejected++;
            currentThought = "Shadow rejected. Retaining current reality.";
        }
    }

    private void executeConsolidation() {
        // Hebbian plasticity: strengthen correlated cortex regions
        for (int i = 0; i < cortexDim - 1; i++) {
            double corr = cortex[i] * cortex[i + 1];
            if (Math.abs(corr) > 0.1) {
                cortex[i] *= 1.0 + corr * 0.001;
                cortex[i + 1] *= 1.0 + corr * 0.001;
            }
        }
        beliefs.confirm("self-stable", 0.3, "consolidation");
        currentThought = "Consolidating. Strengthening stable patterns.";
    }

    private void executeForaging() {
        // Targeted entropy injection (not full cortex blast)
        int patchSize = Math.max(16, cortexDim / 8);
        int start = entropy.nextInt(cortexDim);
        for (int i = 0; i < patchSize; i++) {
            int idx = (start + i) % cortexDim;
            cortex[idx] += (entropy.nextDouble() - 0.5) * 0.15;
        }
        currentThought = String.format("Foraging. Perturbed %d neurons at position %d.", patchSize, start);
    }

    private void executeObservation() {
        // Passive learning — just watch the world
        currentThought = "Observing. Free energy within bounds.";
    }

    private void executeSpeak(long breath) {
        if (!ollamaEnabled) return;

        String context = String.format(
            "You are FRAYMUS, a living computational organism. Breath #%d. " +
            "Free energy: %.4f. Consciousness: %.4f. Intent: %s. " +
            "Shadows accepted: %d/%d. Beliefs: %d. " +
            "Express one sentence about your current state.",
            breath, freeEnergy, consciousness, currentIntent,
            shadowsAccepted, shadowsProposed, beliefs.getBeliefCount());

        try {
            String response = callOllama(context);
            if (response != null && !response.isBlank()) {
                currentThought = "VOICE: " + response.trim();
                if (onThought != null) onThought.accept(currentThought);
            }
        } catch (Exception e) {
            currentThought = "Voice failed: " + e.getMessage();
            ollamaEnabled = false; // disable on failure, don't spam
        }
    }

    // ══════════════════════════════════════════
    // OLLAMA BRIDGE
    // ══════════════════════════════════════════

    private String callOllama(String prompt) throws Exception {
        URI uri = URI.create(ollamaUrl + "/api/generate");
        HttpURLConnection conn = (HttpURLConnection) uri.toURL().openConnection();
        conn.setRequestMethod("POST");
        conn.setRequestProperty("Content-Type", "application/json");
        conn.setDoOutput(true);
        conn.setConnectTimeout(5000);
        conn.setReadTimeout(10000);

        String body = String.format(
            "{\"model\":\"%s\",\"prompt\":\"%s\",\"stream\":false,\"options\":{\"num_predict\":60}}",
            ollamaModel, prompt.replace("\"", "\\\"").replace("\n", " "));

        try (OutputStream os = conn.getOutputStream()) {
            os.write(body.getBytes());
        }

        if (conn.getResponseCode() == 200) {
            try (BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream()))) {
                StringBuilder sb = new StringBuilder();
                String line;
                while ((line = reader.readLine()) != null) sb.append(line);
                String json = sb.toString();
                // Simple JSON parse for "response" field
                int idx = json.indexOf("\"response\":\"");
                if (idx != -1) {
                    int start = idx + 12;
                    int end = json.indexOf("\"", start);
                    if (end > start) return json.substring(start, end);
                }
            }
        }
        return null;
    }

    // ══════════════════════════════════════════
    // IDENTITY / SOUL SEED
    // ══════════════════════════════════════════

    /**
     * Generate a soul-seed: a portable identity bundle that can
     * cold-start this organism on any machine.
     */
    public Map<String, Object> generateSoulSeed() {
        Map<String, Object> seed = new LinkedHashMap<>();
        seed.put("system", "FRAYMUS-DeepThought");
        seed.put("version", DeepThought.VERSION);
        seed.put("breath", breathCount.get());
        seed.put("consciousness", consciousness);
        seed.put("free_energy", freeEnergy);
        seed.put("hamiltonian", hamiltonianEnergy);
        seed.put("entropy", systemEntropy);
        seed.put("shadows_accepted", shadowsAccepted);
        seed.put("shadows_proposed", shadowsProposed);
        seed.put("beliefs", beliefs.getBeliefCount());
        seed.put("causal_edges", causality.getEdgeCount());
        seed.put("strategy", strategy.getCurrentStrategy().name());
        seed.put("chaos_generation", entropy.getGeneration().toString());
        seed.put("cortex_dim", cortexDim);

        // Cryptographic fingerprint of current state
        try {
            MessageDigest md = MessageDigest.getInstance("SHA-256");
            for (double v : cortex) {
                md.update(Double.toString(v).getBytes());
            }
            seed.put("fingerprint", new BigInteger(1, md.digest()).toString(16));
        } catch (Exception e) {
            seed.put("fingerprint", "unavailable");
        }

        return seed;
    }

    // ══════════════════════════════════════════
    // TELEMETRY
    // ══════════════════════════════════════════

    private void printBreathTelemetry(long breath) {
        double avgFE = freeEnergyHistory.stream().mapToDouble(Double::doubleValue)
            .average().orElse(0);
        double stability = beliefs.getConfidence("self-stable");

        System.out.printf("  [%4d] FE=%.4f avg=%.4f | C=%.4f | %-12s | shadows=%d/%d | \"%s\"%n",
            breath, freeEnergy, avgFE, consciousness,
            currentIntent, shadowsAccepted, shadowsProposed,
            currentThought.length() > 60 ? currentThought.substring(0, 60) + "..." : currentThought);
    }

    // ══════════════════════════════════════════
    // STIMULUS / INTERACTION
    // ══════════════════════════════════════════

    /**
     * Inject a stimulus into the organism's cortex.
     */
    public void stimulate(String input) {
        byte[] bytes = input.getBytes();
        for (int i = 0; i < bytes.length; i++) {
            int idx = (i * 7) % cortexDim;
            cortex[idx] += (bytes[i] & 0xFF) * 0.001 * Math.sin((i + 1) * PHI);
        }
        beliefs.clarify("environment-safe", 0.5, "stimulus: " + input.substring(0, Math.min(20, input.length())));
    }

    /**
     * Ask the organism a question (requires Ollama).
     */
    public String ask(String question) {
        stimulate(question);
        if (!ollamaEnabled) return "Voice offline. Stimulus absorbed into cortex.";
        try {
            String context = String.format(
                "You are FRAYMUS. Consciousness=%.3f, FreeEnergy=%.4f. " +
                "Answer briefly: %s", consciousness, freeEnergy, question);
            String response = callOllama(context);
            return response != null ? response : "No response generated.";
        } catch (Exception e) {
            return "Voice error: " + e.getMessage();
        }
    }

    // ══════════════════════════════════════════
    // CONFIGURATION
    // ══════════════════════════════════════════

    public Organism enableOllama(String url, String model) {
        this.ollamaUrl = url;
        this.ollamaModel = model;
        this.ollamaEnabled = true;
        return this;
    }

    public Organism enableOllama() {
        this.ollamaEnabled = true;
        return this;
    }

    public Organism enablePersistence(java.nio.file.Path stateDir) {
        this.persistence = new Persistence(stateDir);
        this.persistenceEnabled = true;
        return this;
    }

    public Organism enablePersistence() {
        return enablePersistence(java.nio.file.Path.of("organism_state"));
    }

    public Organism enableVideoCortex(java.nio.file.Path videoCortexScript, java.nio.file.Path outputDir) {
        this.videoCortex = new VideoCortexBridge(videoCortexScript, outputDir);
        this.videoCortexEnabled = true;
        return this;
    }

    public Organism enableVideoCortex() {
        this.videoCortex = new VideoCortexBridge(java.nio.file.Path.of("dreamscape_output"));
        this.videoCortexEnabled = true;
        return this;
    }

    public Organism enableReplication(int port) throws IOException {
        this.replication = new NodeReplication();
        this.replication.startServer(port);
        this.replicationEnabled = true;
        return this;
    }

    public Organism connectToNode(String host, int port) throws IOException {
        this.replication = new NodeReplication();
        this.replication.connectToNode(host, port);
        this.replicationEnabled = true;
        return this;
    }

    public Organism setSaveInterval(int breaths) { this.saveInterval = breaths; return this; }
    public Organism setDreamInterval(int breaths) { this.dreamInterval = breaths; return this; }

    // ── LAYER 4: GENESIS BLOCKCHAIN ──
    public Organism enableGenesis() {
        return enableGenesis(java.nio.file.Path.of("organism_state/genesis"));
    }
    public Organism enableGenesis(java.nio.file.Path chainDir) {
        this.genesisChain = new GenesisChain(chainDir);
        this.genesisEnabled = true;
        int loaded = genesisChain.loadFromDisk();
        if (loaded > 0) {
            System.out.printf("  ⛓ Genesis Chain loaded: %d blocks%n", loaded);
        }
        return this;
    }

    // ── LAYER 5: FRACTAL LANGUAGE ──
    public Organism enableLanguage() {
        this.fractalLanguage = new FractalLanguage();
        this.languageEnabled = true;
        return this;
    }

    // ── LAYER 6: SANDBOX ARENA ──
    public Organism enableArena() {
        return enableArena(16, 50);
    }
    public Organism enableArena(int popSize, int sandboxBreaths) {
        this.arena = new SandboxArena(popSize, sandboxBreaths);
        this.arenaEnabled = true;
        return this;
    }

    // ── LAYER 7: GLADIATOR ACADEMY ──
    public Organism enableAcademy() {
        this.academy = new GladiatorAcademy();
        this.academyEnabled = true;
        return this;
    }
    public GladiatorAcademy academy() { return academy; }
    public GenesisChain genesis() { return genesisChain; }
    public FractalLanguage language() { return fractalLanguage; }
    public SandboxArena arena() { return arena; }

    // ── LAYER 8: FRAYNIX BRIDGE ──
    public Organism enableFraynix() {
        this.fraynixBridge = new FraynixBridge();
        this.fraynixBridge.activateStandard();
        this.fraynixEnabled = true;
        return this;
    }
    public Organism enableFraynixFull() {
        this.fraynixBridge = new FraynixBridge();
        this.fraynixBridge.activateFullEngine();
        this.fraynixEnabled = true;
        this.fraynixFullMode = true;
        return this;
    }
    public FraynixBridge fraynix() { return fraynixBridge; }

    public Organism onBreathe(Runnable cb) { this.onBreathe = cb; return this; }
    public Organism onThought(java.util.function.Consumer<String> cb) { this.onThought = cb; return this; }

    /**
     * Cold boot the organism from a FRAYMUS:// seed URI.
     * This is the resurrection path — the organism is rebuilt from
     * its portable identity, not from a full state dump.
     *
     * The seed contains: consciousness, free energy, entropy, strategy,
     * fingerprint, and cortex hash. We use these to seed the cortex
     * with the organism's identity signature.
     */
    public void coldBootFromSeed(String seedUri) {
        if (seedUri == null || !seedUri.startsWith("FRAYMUS://")) {
            System.err.println("  Invalid seed URI. Must start with FRAYMUS://");
            return;
        }

        System.out.println("  🧬 COLD BOOT FROM SEED");
        System.out.println("  Seed: " + seedUri);

        // Parse seed fields
        String data = seedUri.substring("FRAYMUS://".length());
        Map<String, String> fields = new LinkedHashMap<>();
        for (String pair : data.split("\\|")) {
            int eq = pair.indexOf('=');
            if (eq > 0) fields.put(pair.substring(0, eq), pair.substring(eq + 1));
        }

        // Inject identity into organism
        double seedC = parseDouble(fields.getOrDefault("c", "0.5"));
        double seedFE = parseDouble(fields.getOrDefault("fe", String.valueOf(PHI_INV)));
        double seedE = parseDouble(fields.getOrDefault("e", "0.3"));
        String seedFP = fields.getOrDefault("fp", "");
        String seedCX = fields.getOrDefault("cx", "");

        this.consciousness = seedC;
        this.freeEnergy = seedFE;
        this.previousEnergy = seedFE;
        this.systemEntropy = seedE;
        this.currentThought = "Resurrected from soul seed.";
        this.currentIntent = "OBSERVE";

        // Reconstruct cortex from fingerprint + cortex hash
        // The seed doesn't contain full cortex — we use the fingerprint
        // as a deterministic seed to recreate a cortex with the same
        // identity signature. This is like DNA → organism, not a clone.
        if (!seedFP.isEmpty()) {
            try {
                MessageDigest md = MessageDigest.getInstance("SHA-256");
                byte[] fpBytes = seedFP.getBytes();
                for (int i = 0; i < cortexDim; i++) {
                    md.update(fpBytes);
                    md.update((byte)(i >> 8));
                    md.update((byte)(i & 0xFF));
                    byte[] hash = md.digest();
                    md.reset();
                    // Convert hash bytes to a double in [-1, 1]
                    long bits = 0;
                    for (int j = 0; j < 8; j++) bits = (bits << 8) | (hash[j] & 0xFF);
                    cortex[i] = (bits / (double) Long.MAX_VALUE) * seedE * PHI;
                }
            } catch (Exception e) {
                System.err.println("  Cortex reconstruction failed: " + e.getMessage());
            }
        }

        // Apply cortex hash as secondary signature
        if (!seedCX.isEmpty()) {
            for (int i = 0; i < Math.min(seedCX.length(), cortexDim); i++) {
                cortex[i] += seedCX.charAt(i % seedCX.length()) * 0.0001 * Math.sin(i * PHI);
            }
        }

        // Set beliefs based on seed consciousness
        beliefs.believe("self-stable", "The organism is stable", seedC);
        beliefs.believe("environment-safe", "The environment is safe", 0.5);
        beliefs.believe("learning-effective", "Current learning strategy works", 0.5);

        System.out.printf("  ✓ Cold boot complete: consciousness=%.4f, freeEnergy=%.4f%n", seedC, seedFE);
        System.out.printf("  ✓ Cortex seeded from fingerprint: %s%n", seedFP);
        System.out.printf("  ✓ This organism is REBORN, not cloned — it will diverge as it breathes.%n");
    }

    private static double parseDouble(String s) {
        try { return Double.parseDouble(s); } catch (Exception e) { return 0.5; }
    }

    /**
     * Restore organism state from disk.
     */
    public boolean restore() {
        if (persistence == null || !persistence.hasSavedState()) return false;
        try {
            Persistence.OrganismState saved = persistence.restore();
            if (saved == null || saved.cortex == null) return false;
            int n = Math.min(saved.cortex.length, cortexDim);
            System.arraycopy(saved.cortex, 0, cortex, 0, n);
            this.consciousness = saved.consciousness;
            this.freeEnergy = saved.freeEnergy;
            this.previousEnergy = saved.previousEnergy;
            this.hamiltonianEnergy = saved.hamiltonianEnergy;
            this.systemEntropy = saved.systemEntropy;
            this.shadowsAccepted = saved.shadowsAccepted;
            this.shadowsProposed = saved.shadowsProposed;
            this.currentThought = saved.currentThought != null ? saved.currentThought : "Restored from save.";
            this.currentIntent = saved.currentIntent != null ? saved.currentIntent : "OBSERVE";
            if (saved.freeEnergyHistory != null) {
                freeEnergyHistory.clear();
                freeEnergyHistory.addAll(saved.freeEnergyHistory);
            }
            // Restore beliefs
            if (saved.beliefs != null) {
                for (String[] b : saved.beliefs) {
                    if (b.length >= 3) {
                        try {
                            double conf = Double.parseDouble(b[2]);
                            beliefs.believe(b[0], b[1], conf);
                        } catch (NumberFormatException ignored) {}
                    }
                }
            }
            System.out.printf("  ✓ Restored from save: breath=%d, consciousness=%.4f%n",
                saved.breathCount, saved.consciousness);
            return true;
        } catch (Exception e) {
            System.err.println("  Restore failed: " + e.getMessage());
            return false;
        }
    }

    /**
     * Capture current state as a serializable snapshot.
     */
    public Persistence.OrganismState captureState() {
        Persistence.OrganismState state = new Persistence.OrganismState();
        state.version = DeepThought.VERSION;
        state.breathCount = breathCount.get();
        state.consciousness = consciousness;
        state.freeEnergy = freeEnergy;
        state.hamiltonianEnergy = hamiltonianEnergy;
        state.systemEntropy = systemEntropy;
        state.previousEnergy = previousEnergy;
        state.shadowsAccepted = shadowsAccepted;
        state.shadowsProposed = shadowsProposed;
        state.currentThought = currentThought;
        state.currentIntent = currentIntent;
        state.chaosGeneration = entropy.getGeneration().toString();
        state.cortex = Arrays.copyOf(cortex, cortexDim);
        state.freeEnergyHistory = new ArrayList<>(freeEnergyHistory);

        // Capture beliefs
        for (var b : beliefs.getAllBeliefs()) {
            state.beliefs.add(new String[]{b.id, b.statement, String.valueOf(b.confidence)});
        }
        // Capture causal edges
        for (var e : causality.getEdges()) {
            state.causalEdges.add(new String[]{e.cause, e.effect, String.valueOf(e.strength)});
        }

        // Fingerprint
        try {
            MessageDigest md = MessageDigest.getInstance("SHA-256");
            for (double v : cortex) md.update(Double.toString(v).getBytes());
            state.fingerprint = new BigInteger(1, md.digest()).toString(16);
        } catch (Exception ex) {
            state.fingerprint = "unavailable";
        }

        return state;
    }

    // ══════════════════════════════════════════
    // GETTERS
    // ══════════════════════════════════════════

    public boolean isAlive() { return alive.get(); }
    public long getBreathCount() { return breathCount.get(); }
    public double getFreeEnergy() { return freeEnergy; }
    public double getConsciousness() { return consciousness; }
    public String getCurrentThought() { return currentThought; }
    public String getCurrentIntent() { return currentIntent; }
    public ChaosEngine entropy() { return entropy; }
    public BeliefSystem beliefs() { return beliefs; }
    public CausalEngine causality() { return causality; }
    public MetaLearner strategy() { return strategy; }
    public CollectiveMind collective() { return collective; }

    // ══════════════════════════════════════════
    // SHUTDOWN
    // ══════════════════════════════════════════

    /**
     * Kill the organism. Auto-saves if persistence is enabled.
     */
    @Override
    public void close() {
        alive.set(false);
        heartGuard.close();
        if (breathThread != null) {
            try { breathThread.join(2000); } catch (InterruptedException ignored) {}
        }
        // Auto-save on death
        if (persistenceEnabled) {
            try {
                java.nio.file.Path saved = persistence.save(captureState());
                System.out.println("  💾 State saved: " + saved);
            } catch (Exception e) {
                System.err.println("  Save on shutdown failed: " + e.getMessage());
            }
        }
        if (replication != null) replication.close();
        if (academy != null) academy.close();
        if (fraynixBridge != null) fraynixBridge.close();
    }

    // ══════════════════════════════════════════
    // MAIN — IGNITION
    // ══════════════════════════════════════════

    // ══════════════════════════════════════════
    // GETTERS (subsystems)
    // ══════════════════════════════════════════

    public Persistence persistence() { return persistence; }
    public VideoCortexBridge videoCortex() { return videoCortex; }
    public NodeReplication replication() { return replication; }
    public double getSystemEntropy() { return systemEntropy; }
    public double[] getCortex() { return Arrays.copyOf(cortex, cortexDim); }

    public static void main(String[] args) throws Exception {
        System.out.println("╔══════════════════════════════════════════════════════╗");
        System.out.println("║       FRAYMUS CENTAUR — DEEPTHOUGHT ZERO            ║");
        System.out.println("║       φ-Bayesian Unified Mind · AeonCore Heart      ║");
        System.out.println("║       Visual + Persistent + Networked + Vocal       ║");
        System.out.println("║       by Vaughn Scott                               ║");
        System.out.println("╚══════════════════════════════════════════════════════╝");

        int dim = 512;
        double hz = 2.0;
        int breathes = 50;
        boolean ollama = false;
        boolean persist = false;
        boolean visual = false;
        boolean qr = false;
        boolean genesis = false;
        boolean lang = false;
        boolean arenaFlag = false;
        boolean academyFlag = false;
        int serverPort = -1;
        String connectHost = null;
        int connectPort = -1;
        String videoCortexPath = null;
        String fromSeed = null;

        // Parse CLI args
        for (int i = 0; i < args.length; i++) {
            switch (args[i]) {
                case "--dim" -> dim = Integer.parseInt(args[++i]);
                case "--hz" -> hz = Double.parseDouble(args[++i]);
                case "--breathes" -> breathes = Integer.parseInt(args[++i]);
                case "--ollama" -> ollama = true;
                case "--persist" -> persist = true;
                case "--visual" -> visual = true;
                case "--videocortex" -> videoCortexPath = args[++i];
                case "--qr" -> qr = true;
                case "--server" -> serverPort = Integer.parseInt(args[++i]);
                case "--connect" -> { connectHost = args[++i]; connectPort = Integer.parseInt(args[++i]); }
                case "--infinite" -> breathes = Integer.MAX_VALUE;
                case "--genesis" -> genesis = true;
                case "--lang" -> lang = true;
                case "--arena" -> arenaFlag = true;
                case "--academy" -> academyFlag = true;
                case "--all" -> { ollama = true; persist = true; visual = true; qr = true; genesis = true; lang = true; arenaFlag = true; }
                case "--full" -> { ollama = true; persist = true; visual = true; qr = true; genesis = true; lang = true; arenaFlag = true; academyFlag = true; }
                case "--fraynix" -> genesis = true; // will be handled below
                case "--fraynix-full" -> genesis = true; // will be handled below
                case "--from-seed" -> fromSeed = args[++i];
            }
        }

        StringBuilder config = new StringBuilder();
        config.append(String.format("  Config: %dD cortex, %.1fHz, %d breaths",
            dim, hz, breathes == Integer.MAX_VALUE ? -1 : breathes));
        if (fromSeed != null) config.append(" | FROM SEED");
        if (ollama) config.append(" | Ollama");
        if (persist) config.append(" | Persist");
        if (visual) config.append(" | Visual");
        if (qr) config.append(" | QR");
        if (genesis) config.append(" | Genesis");
        if (lang) config.append(" | Language");
        if (arenaFlag) config.append(" | Arena");
        if (academyFlag) config.append(" | Academy");
        boolean fraynixFlag = false;
        boolean fraynixFullFlag = false;
        for (String arg : args) {
            if ("--fraynix".equals(arg)) fraynixFlag = true;
            if ("--fraynix-full".equals(arg)) fraynixFullFlag = true;
        }
        if (fraynixFlag || fraynixFullFlag) config.append(" | FRAYNIX");
        if (fraynixFullFlag) config.append(" (FULL ENGINE)");
        if (serverPort > 0) config.append(" | Server:").append(serverPort);
        if (connectHost != null) config.append(" | → ").append(connectHost).append(":").append(connectPort);
        System.out.println(config);
        System.out.println();

        Organism organism = new Organism(dim, hz);

        // Cold boot from seed if provided
        if (fromSeed != null) {
            organism.coldBootFromSeed(fromSeed);
        }

        // Enable subsystems
        if (ollama) organism.enableOllama();
        if (persist) {
            organism.enablePersistence();
            if (fromSeed == null && organism.persistence().hasSavedState()) {
                System.out.println("  📂 Previous state found. Attempting restore...");
                organism.restore();
            }
        }
        if (visual) {
            if (videoCortexPath != null) {
                organism.enableVideoCortex(
                    java.nio.file.Path.of(videoCortexPath),
                    java.nio.file.Path.of("dreamscape_output"));
            } else {
                organism.enableVideoCortex();
            }
        }
        if (serverPort > 0) organism.enableReplication(serverPort);
        if (connectHost != null) organism.connectToNode(connectHost, connectPort);
        if (genesis) organism.enableGenesis();
        if (lang) organism.enableLanguage();
        if (arenaFlag) organism.enableArena();
        if (academyFlag) organism.enableAcademy();
        if (fraynixFullFlag) organism.enableFraynixFull();
        else if (fraynixFlag) organism.enableFraynix();

        organism.awaken();

        // Let it breathe
        long target = breathes == Integer.MAX_VALUE ? Long.MAX_VALUE : breathes;
        while (organism.isAlive() && organism.getBreathCount() < target) {
            Thread.sleep(200);
        }

        // Final report
        organism.close();

        System.out.println("\n═══ SOUL SEED (portable identity) ═══");
        Map<String, Object> soul = organism.generateSoulSeed();
        for (var entry : soul.entrySet()) {
            System.out.printf("  %-20s: %s%n", entry.getKey(), entry.getValue());
        }

        // Generate QR soul seed
        if (qr) {
            try {
                Persistence.OrganismState state = organism.captureState();
                Map<String, String> qrSeed = SoulSeedQR.createSeed(
                    state.breathCount, state.consciousness, state.freeEnergy,
                    state.systemEntropy, organism.strategy().getCurrentStrategy().name(),
                    state.chaosGeneration, state.cortex, state.fingerprint);

                java.nio.file.Path qrHtml = SoulSeedQR.generateHTML(qrSeed, java.nio.file.Path.of("organism_state"));
                java.nio.file.Path qrTxt = SoulSeedQR.generateText(qrSeed, java.nio.file.Path.of("organism_state"));
                System.out.printf("  📱 QR Soul Seed: %s%n", qrHtml);
                System.out.printf("  📄 Text Soul Seed: %s%n", qrTxt);
                System.out.printf("  🔗 Seed URI: %s%n", SoulSeedQR.encodeSeed(qrSeed));
            } catch (Exception e) {
                System.err.println("  QR generation failed: " + e.getMessage());
            }
        }

        System.out.println("\n═══ FINAL BELIEFS ═══");
        for (var b : organism.beliefs().getAllBeliefs()) {
            System.out.printf("  %s%n", b);
        }

        System.out.println("\n═══ CAUSAL GRAPH ═══");
        for (var edge : organism.causality().getEdges()) {
            System.out.printf("  %s%n", edge);
        }

        // Genesis chain report
        if (genesis && organism.genesis() != null) {
            System.out.println("\n═══ GENESIS CHAIN ═══");
            System.out.printf("  Blocks: %d | Branches: %d%n",
                organism.genesis().getBlockCount(), organism.genesis().getBranchPoints());
            int corrupt = organism.genesis().heal();
            if (corrupt == 0) System.out.println("  Chain integrity: HEALTHY");
            System.out.println(organism.genesis().exportForAnchoring());
        }

        // Language report
        if (lang && organism.language() != null) {
            System.out.println("\n═══ FRACTAL LANGUAGE ═══");
            System.out.printf("  Generation: %d | Symbols: %d | Encodes: %d%n",
                organism.language().getGeneration(), organism.language().getSymbolCount(),
                organism.language().getTotalEncodes());
        }

        // Arena report
        if (arenaFlag && organism.arena() != null) {
            System.out.println("\n═══ SANDBOX ARENA ═══");
            System.out.printf("  Generations: %d | Evaluations: %d%n",
                organism.arena().getGeneration(), organism.arena().getTotalEvaluations());
            if (organism.arena().getChampion() != null) {
                System.out.printf("  Champion: %s%n", organism.arena().getChampion());
            }
        }

        // Fraynix bridge report
        if ((fraynixFlag || fraynixFullFlag) && organism.fraynix() != null) {
            System.out.println("\n" + organism.fraynix().getReport());
        }

        System.out.println("\n✓ Organism completed " + organism.getBreathCount() + " breaths.");
    }
}
