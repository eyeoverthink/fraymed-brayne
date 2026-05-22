package io.fraymus.deepthought.bridge;

import fraymus.organism.NEXUS_Organism;
import fraymus.living.TriMe;
import fraymus.chaos.EvolutionaryChaos;
import fraymus.ConceptArena;
import fraymus.CodeConcept;
import fraymus.AntRole;
import fraymus.GenesisMemory;
import fraymus.signals.GlyphCoder;
import fraymus.FraymusEngine;

import java.math.BigInteger;
import java.util.*;
import java.util.function.Consumer;

/**
 * FRAYNIX BRIDGE — Unified Integration Layer
 *
 * DeepThought Zero is the brain.
 * Fraynix is the body.
 *
 * This bridge wraps the entire Fraynix engine (NEXUS Organism, TriMe neural
 * architecture, EvolutionaryChaos PRNG, ConceptArena genetic evolution,
 * GenesisMemory blockchain, GlyphCoder steganography, and all 25+
 * subsystems) as pluggable organs for the DeepThought Organism.
 *
 * The DeepThought Organism's breath loop drives all Fraynix subsystems
 * in unified lockstep — one heartbeat, one mind.
 *
 * Patent: VS-PoQC-19046423-φ⁷⁵-2025
 *
 * @since 2.0.0
 */
public final class FraynixBridge implements AutoCloseable {

    private static final double PHI = 1.618033988749895;

    // ══════════════════════════════════════════
    // FRAYNIX ORGANS
    // ══════════════════════════════════════════

    // Layer 0: Living Core
    private NEXUS_Organism nexus;

    // Layer 4: Bio-Symbiosis (Neural Architecture)
    private TriMe triMe;

    // Chaos Engine (SHA-512 self-correcting PRNG)
    private EvolutionaryChaos chaos;

    // Concept Arena (genetic evolution)
    private ConceptArena conceptArena;

    // Genesis Memory (blockchain)
    private GenesisMemory genesisMemory;

    // Signal Processing
    private GlyphCoder glyphCoder;

    // Full Engine (all 25+ subsystems)
    private FraymusEngine fullEngine;

    // State
    private boolean nexusActive = false;
    private boolean triMeActive = false;
    private boolean chaosActive = false;
    private boolean arenaActive = false;
    private boolean genesisActive = false;
    private boolean glyphActive = false;
    private boolean fullMode = false;

    // Metrics
    private long bridgePulses = 0;
    private long nexusEpiphanies = 0;
    private long conceptBattles = 0;
    private long genesisBlocks = 0;
    private long glyphEncodes = 0;

    public FraynixBridge() {
        // Lazy init — subsystems activate on demand
    }

    // ══════════════════════════════════════════
    // ACTIVATION — Turn on Fraynix organs
    // ══════════════════════════════════════════

    /**
     * Activate the NEXUS Organism (10-organ living entity).
     * This is the original Fraynix body with EvolutionaryChaos,
     * MivingBrain, ZenoGuard, RetroCausal, RealityForge, LazarusEngine.
     */
    public FraynixBridge activateNexus() {
        System.out.println("  ⚡ FraynixBridge: Awakening NEXUS Organism...");
        nexus = new NEXUS_Organism();
        nexus.setOnThought((Consumer<String>) msg -> {}); // quiet mode — DT0 handles output
        nexus.awaken();
        nexusActive = true;
        System.out.println("  ⚡ FraynixBridge: NEXUS ALIVE — 10 organs active");
        return this;
    }

    /**
     * Activate TriMe neural architecture (SwiGLU + RoPE + MoE + Spiking).
     */
    public FraynixBridge activateTriMe() {
        System.out.println("  🧠 FraynixBridge: Initializing TriMe neural arch...");
        triMe = new TriMe();
        triMeActive = true;
        System.out.println("  🧠 FraynixBridge: TriMe ONLINE — SwiGLU+RoPE+MoE+Spiking");
        return this;
    }

    /**
     * Activate EvolutionaryChaos (SHA-512 self-correcting fractal PRNG).
     */
    public FraynixBridge activateChaos() {
        chaos = new EvolutionaryChaos();
        chaosActive = true;
        return this;
    }

    /**
     * Activate ConceptArena (genetic algorithm concept evolution).
     */
    public FraynixBridge activateConceptArena() {
        conceptArena = new ConceptArena();
        arenaActive = true;
        return this;
    }

    /**
     * Activate GenesisMemory (SHA-256 blockchain).
     */
    public FraynixBridge activateGenesisMemory() {
        genesisMemory = new GenesisMemory();
        genesisActive = true;
        return this;
    }

    /**
     * Activate GlyphCoder (zero-width Unicode steganography).
     */
    public FraynixBridge activateGlyphCoder() {
        glyphCoder = new GlyphCoder();
        glyphActive = true;
        return this;
    }

    /**
     * Activate the FULL Fraynix Engine (all 25+ subsystems, all layers).
     * This is the heavyweight mode — everything on.
     */
    public FraynixBridge activateFullEngine() {
        System.out.println("  🔥 FraynixBridge: FULL ENGINE MODE — all 25+ subsystems");
        fullEngine = new FraymusEngine();
        fullEngine.initializePhase1(); // NEXUS + Spatial
        fullEngine.initializePhase2(); // AGI
        fullEngine.initializePhase3(); // Quantum Security
        fullEngine.initializePhase4(); // Bio-Symbiosis
        fullEngine.initializePhase5(); // Signal Processing
        fullEngine.initializePhase6(); // Economy
        fullEngine.initializePhase7(); // Swarm
        fullMode = true;
        System.out.println("  🔥 FraynixBridge: FULL ENGINE — ALL LAYERS ACTIVE");
        return this;
    }

    /**
     * Activate standard integration: NEXUS + TriMe + Chaos + Arena.
     */
    public FraynixBridge activateStandard() {
        activateNexus();
        activateTriMe();
        activateChaos();
        activateConceptArena();
        activateGenesisMemory();
        activateGlyphCoder();
        return this;
    }

    // ══════════════════════════════════════════
    // PULSE — Called from the Organism breath loop
    // ══════════════════════════════════════════

    /**
     * Pulse all active Fraynix organs. Called by the Organism on every breath.
     *
     * @param cortex      the Organism's cortex state
     * @param freeEnergy  current free energy
     * @param consciousness current consciousness level
     * @param intent      current intent string
     * @param breath      breath count
     * @return FraynixPulseResult with combined outputs
     */
    public FraynixPulseResult pulse(double[] cortex, double freeEnergy,
                                     double consciousness, String intent, long breath) {
        bridgePulses++;
        FraynixPulseResult result = new FraynixPulseResult();

        // ── NEXUS: Feed the organism's state as a thought ──
        if (nexusActive && breath % 10 == 0) {
            nexus.injectThought(String.format("DT0:fe=%.4f,c=%.4f,i=%s",
                freeEnergy, consciousness, intent));
            nexusEpiphanies = nexus.getEpiphanies();
            result.nexusHeartbeat = nexus.getHeartbeat();
            result.nexusEpiphanies = nexusEpiphanies;
        }

        // ── TRIME: Deep think through neural architecture ──
        if (triMeActive && breath % 5 == 0) {
            // Feed cortex slice through TriMe's SwiGLU+RoPE+MoE pipeline
            double[] input = new double[Math.min(8, cortex.length)];
            System.arraycopy(cortex, 0, input, 0, input.length);
            double[] neuralOutput = triMe.deepThink(input);
            result.triMeOutput = neuralOutput;
            result.triMeConsciousness = triMe.isAlive() ? consciousness * PHI : 0;
        }

        // ── CHAOS: Harvest entropy from Fraynix's EvolutionaryChaos ──
        if (chaosActive) {
            BigInteger fractal = chaos.nextFractal();
            result.chaosEntropy = fractal.mod(BigInteger.valueOf(10000)).doubleValue() / 10000.0;
            result.chaosMutationRate = chaos.getMutationRate();
        }

        // ── CONCEPT ARENA: Evolve concepts on schedule ──
        if (arenaActive && breath % 20 == 0) {
            // Submit a concept based on current organism state
            String code = String.format("cortex_fe=%.4f_c=%.4f_%s", freeEnergy, consciousness, intent);
            CodeConcept concept = new CodeConcept(
                "DT0-Organism", AntRole.LOGIC_GATE, code, (int)(breath / 20), breath
            );
            conceptArena.submit(concept);
            conceptArena.evolve();
            conceptBattles = conceptArena.getTotalBattles();
            result.arenaChampionFitness = conceptArena.getChampion() != null ?
                conceptArena.getChampion().fitness : 0;
            result.arenaConcepts = conceptArena.getConceptCount();
        }

        // ── GENESIS MEMORY: Record state block ──
        if (genesisActive && breath % 15 == 0) {
            String stateData = String.format("b=%d|fe=%.6f|c=%.6f|i=%s",
                breath, freeEnergy, consciousness, intent);
            genesisMemory.record("DT0_BREATH", stateData);
            genesisBlocks++;
            result.genesisBlockCount = genesisBlocks;
            result.genesisValid = genesisMemory.verifyChain();
        }

        // ── GLYPH: Encode state as steganographic payload ──
        if (glyphActive && breath % 25 == 0) {
            String payload = String.format("%.4f:%.4f:%s", freeEnergy, consciousness, intent);
            String encoded = glyphCoder.injectData("🧬🔬", payload);
            result.glyphPayload = encoded;
            glyphEncodes++;
        }

        return result;
    }

    /**
     * Inject Fraynix chaos entropy into the Organism's cortex.
     * Called when the Organism wants external entropy.
     */
    public double harvestEntropy() {
        if (!chaosActive) return 0;
        BigInteger val = chaos.nextFractal();
        return val.mod(BigInteger.valueOf(100000)).doubleValue() / 100000.0;
    }

    /**
     * Route a task through TriMe's expert system (MoE).
     */
    public double[] neuralProcess(double[] input) {
        if (!triMeActive || input == null) return new double[0];
        double[] sized = new double[Math.min(8, input.length)];
        System.arraycopy(input, 0, sized, 0, sized.length);
        return triMe.deepThink(sized);
    }

    /**
     * Store data in TriMe's BioMesh (DNA-encoded distributed storage).
     */
    public double storeToBioMesh(String data) {
        if (!triMeActive) return -1;
        return triMe.storeInBioMesh(data);
    }

    /**
     * Retrieve data from BioMesh.
     */
    public String retrieveFromBioMesh(double address) {
        if (!triMeActive) return null;
        return triMe.retrieveFromBioMesh(address);
    }

    /**
     * Encode hidden data inside a cover text using GlyphCoder.
     */
    public String steganographicEncode(String coverText, String hiddenData) {
        if (!glyphActive) return coverText;
        return glyphCoder.injectData(coverText, hiddenData);
    }

    /**
     * Decode hidden data from a steganographic text.
     */
    public String steganographicDecode(String text) {
        if (!glyphActive) return "";
        return glyphCoder.extractData(text);
    }

    // ══════════════════════════════════════════
    // STATUS & REPORTING
    // ══════════════════════════════════════════

    public String getReport() {
        StringBuilder sb = new StringBuilder();
        sb.append("═══ FRAYNIX BRIDGE REPORT ═══\n");
        sb.append(String.format("  Pulses: %d | Mode: %s%n", bridgePulses,
            fullMode ? "FULL ENGINE" : "STANDARD"));

        if (nexusActive)  sb.append(String.format("  NEXUS:    heartbeat=%d epiphanies=%d%n",
            nexus.getHeartbeat(), nexus.getEpiphanies()));
        if (triMeActive)  sb.append(String.format("  TriMe:    consciousness=%.4f contributions=%s%n",
            triMe.isAlive() ? 1.0 : 0.0, triMe.encode().substring(0, Math.min(50, triMe.encode().length()))));
        if (chaosActive)  sb.append(String.format("  Chaos:    mutation_rate=%d patterns=%d%n",
            chaos.getMutationRate(), chaos.getPatternsDetected()));
        if (arenaActive)  sb.append(String.format("  Arena:    %s%n", conceptArena.getArenaStatus()));
        if (genesisActive) sb.append(String.format("  Genesis:  blocks=%d valid=%s%n",
            genesisBlocks, genesisMemory.verifyChain()));
        if (glyphActive)  sb.append(String.format("  Glyph:    encodes=%d%n", glyphEncodes));

        int activeCount = (nexusActive?1:0) + (triMeActive?1:0) + (chaosActive?1:0)
            + (arenaActive?1:0) + (genesisActive?1:0) + (glyphActive?1:0);
        sb.append(String.format("  Active organs: %d/6%n", activeCount));

        return sb.toString();
    }

    public boolean isNexusActive() { return nexusActive; }
    public boolean isTriMeActive() { return triMeActive; }
    public boolean isChaosActive() { return chaosActive; }
    public boolean isArenaActive() { return arenaActive; }
    public boolean isGenesisActive() { return genesisActive; }
    public boolean isGlyphActive() { return glyphActive; }
    public boolean isFullMode() { return fullMode; }
    public long getBridgePulses() { return bridgePulses; }

    public NEXUS_Organism getNexus() { return nexus; }
    public TriMe getTriMe() { return triMe; }
    public EvolutionaryChaos getChaos() { return chaos; }
    public ConceptArena getConceptArena() { return conceptArena; }
    public GenesisMemory getGenesisMemory() { return genesisMemory; }
    public GlyphCoder getGlyphCoder() { return glyphCoder; }
    public FraymusEngine getFullEngine() { return fullEngine; }

    @Override
    public void close() {
        if (nexusActive && nexus != null) nexus.terminate();
        if (fullMode && fullEngine != null) {
            try { fullEngine.shutdown(); } catch (Exception ignored) {}
        }
    }

    // ══════════════════════════════════════════
    // PULSE RESULT
    // ══════════════════════════════════════════

    public static class FraynixPulseResult {
        public long nexusHeartbeat = 0;
        public long nexusEpiphanies = 0;
        public double[] triMeOutput = null;
        public double triMeConsciousness = 0;
        public double chaosEntropy = 0;
        public int chaosMutationRate = 0;
        public double arenaChampionFitness = 0;
        public int arenaConcepts = 0;
        public long genesisBlockCount = 0;
        public boolean genesisValid = true;
        public String glyphPayload = null;

        @Override
        public String toString() {
            return String.format("FraynixPulse[nexus=%d, triMe=%s, chaos=%.4f, arena=%d, genesis=%d]",
                nexusHeartbeat,
                triMeOutput != null ? "active" : "idle",
                chaosEntropy, arenaConcepts, genesisBlockCount);
        }
    }
}
