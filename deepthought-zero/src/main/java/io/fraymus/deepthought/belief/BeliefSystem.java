package io.fraymus.deepthought.belief;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.function.Consumer;

/**
 * BAYESIAN BELIEF SYSTEM
 * 
 * Framework-agnostic Bayesian confidence tracking with evidence-based updates.
 * Every belief has a confidence ∈ [0,1] that evolves as evidence arrives.
 * 
 * Core formula: P(H|E) ∝ P(E|H) × P(H)
 * Implemented as: confidence = confidence × α + evidence × (1 - α)
 * 
 * Features:
 * - Named beliefs with confidence scores
 * - Evidence-based updates (confirmation, contradiction, clarification)
 * - Asymmetric learning (contradictions weigh more than confirmations)
 * - Evidence history with source tracking
 * - Low-confidence alerts
 * - Belief decay over time (optional)
 * 
 * @since 1.0.0
 */
public final class BeliefSystem {

    private final Map<String, Belief> beliefs = new ConcurrentHashMap<>();
    private final List<EvidenceRecord> evidenceLog = Collections.synchronizedList(new ArrayList<>());

    // Global tuning
    private double confirmationWeight = 0.1;
    private double contradictionWeight = 0.15;
    private double clarificationWeight = 0.05;
    private double decayRate = 0.0; // 0 = no decay
    private int maxEvidenceLog = 10000;

    // Metrics
    private long totalUpdates = 0;
    private long confirmations = 0;
    private long contradictions = 0;

    // Events
    private Consumer<BeliefChangeEvent> onBeliefChanged;

    /**
     * Register a new belief with an initial confidence.
     */
    public Belief believe(String id, String statement, double initialConfidence) {
        Belief belief = new Belief(id, statement, clamp(initialConfidence));
        beliefs.put(id, belief);
        return belief;
    }

    /**
     * Submit confirming evidence for a belief.
     * Confidence increases by confirmationWeight × strength.
     */
    public double confirm(String beliefId, double strength, String source) {
        return update(beliefId, EvidenceType.CONFIRMATION, strength, source);
    }

    /**
     * Submit contradicting evidence for a belief.
     * Confidence decreases by contradictionWeight × strength.
     */
    public double contradict(String beliefId, double strength, String source) {
        return update(beliefId, EvidenceType.CONTRADICTION, strength, source);
    }

    /**
     * Submit clarifying evidence for a belief.
     * Mild confidence increase.
     */
    public double clarify(String beliefId, double strength, String source) {
        return update(beliefId, EvidenceType.CLARIFICATION, strength, source);
    }

    /**
     * General evidence update.
     */
    public double update(String beliefId, EvidenceType type, double strength, String source) {
        Belief belief = beliefs.get(beliefId);
        if (belief == null) return -1;

        double oldConfidence = belief.confidence;

        switch (type) {
            case CONFIRMATION -> {
                belief.confidence = Math.min(1.0, belief.confidence + strength * confirmationWeight);
                belief.confirmCount++;
                confirmations++;
            }
            case CONTRADICTION -> {
                belief.confidence = Math.max(0.01, belief.confidence - strength * contradictionWeight);
                belief.contradictCount++;
                contradictions++;
            }
            case CLARIFICATION -> {
                belief.confidence = Math.min(1.0, belief.confidence + strength * clarificationWeight);
                belief.clarifyCount++;
            }
        }

        belief.lastUpdated = System.currentTimeMillis();
        belief.totalEvidence++;
        totalUpdates++;

        // Log evidence
        EvidenceRecord record = new EvidenceRecord(beliefId, type, strength, source, 
            oldConfidence, belief.confidence);
        evidenceLog.add(record);
        belief.evidenceHistory.add(record);
        while (evidenceLog.size() > maxEvidenceLog) evidenceLog.remove(0);
        while (belief.evidenceHistory.size() > 100) belief.evidenceHistory.remove(0);

        if (onBeliefChanged != null) {
            onBeliefChanged.accept(new BeliefChangeEvent(
                belief, type, oldConfidence, belief.confidence, source));
        }

        return belief.confidence;
    }

    /**
     * Apply time-based decay to all beliefs.
     * Call periodically if decay is enabled.
     */
    public void decayAll() {
        if (decayRate <= 0) return;
        long now = System.currentTimeMillis();
        for (Belief b : beliefs.values()) {
            double age = (now - b.lastUpdated) / 60000.0; // minutes
            b.confidence *= Math.exp(-decayRate * age);
            b.confidence = Math.max(0.01, b.confidence);
        }
    }

    /**
     * Get beliefs below a confidence threshold.
     */
    public List<Belief> getWeakBeliefs(double threshold) {
        List<Belief> weak = new ArrayList<>();
        for (Belief b : beliefs.values()) {
            if (b.confidence < threshold) weak.add(b);
        }
        weak.sort(Comparator.comparingDouble(b -> b.confidence));
        return weak;
    }

    /**
     * Get beliefs above a confidence threshold.
     */
    public List<Belief> getStrongBeliefs(double threshold) {
        List<Belief> strong = new ArrayList<>();
        for (Belief b : beliefs.values()) {
            if (b.confidence >= threshold) strong.add(b);
        }
        strong.sort((a, b) -> Double.compare(b.confidence, a.confidence));
        return strong;
    }

    /**
     * Get all beliefs sorted by confidence (highest first).
     */
    public List<Belief> getAllBeliefs() {
        List<Belief> all = new ArrayList<>(beliefs.values());
        all.sort((a, b) -> Double.compare(b.confidence, a.confidence));
        return all;
    }

    /**
     * Query a specific belief.
     */
    public Belief getBelief(String id) {
        return beliefs.get(id);
    }

    /**
     * Get the confidence of a specific belief, or -1 if not found.
     */
    public double getConfidence(String id) {
        Belief b = beliefs.get(id);
        return b != null ? b.confidence : -1;
    }

    /**
     * Remove a belief.
     */
    public boolean removeBelief(String id) {
        return beliefs.remove(id) != null;
    }

    // --- Configuration (fluent) ---

    public BeliefSystem setConfirmationWeight(double w) { this.confirmationWeight = w; return this; }
    public BeliefSystem setContradictionWeight(double w) { this.contradictionWeight = w; return this; }
    public BeliefSystem setClarificationWeight(double w) { this.clarificationWeight = w; return this; }
    public BeliefSystem setDecayRate(double rate) { this.decayRate = rate; return this; }
    public BeliefSystem onBeliefChanged(Consumer<BeliefChangeEvent> cb) { this.onBeliefChanged = cb; return this; }

    // --- Metrics ---

    public int getBeliefCount() { return beliefs.size(); }
    public long getTotalUpdates() { return totalUpdates; }
    public long getConfirmations() { return confirmations; }
    public long getContradictions() { return contradictions; }

    private static double clamp(double v) {
        return Math.max(0.01, Math.min(1.0, v));
    }

    // --- Data classes ---

    public enum EvidenceType {
        CONFIRMATION, CONTRADICTION, CLARIFICATION
    }

    public static final class Belief {
        public final String id;
        public final String statement;
        public double confidence;
        public final long createdAt;
        public long lastUpdated;
        public int totalEvidence = 0;
        public int confirmCount = 0;
        public int contradictCount = 0;
        public int clarifyCount = 0;
        public final List<EvidenceRecord> evidenceHistory = new ArrayList<>();

        Belief(String id, String statement, double confidence) {
            this.id = id;
            this.statement = statement;
            this.confidence = confidence;
            this.createdAt = System.currentTimeMillis();
            this.lastUpdated = this.createdAt;
        }

        public double getAge() {
            return (System.currentTimeMillis() - createdAt) / 1000.0;
        }

        @Override
        public String toString() {
            return String.format("Belief[%s: \"%s\" c=%.3f, evidence=%d (+%d/-%d)]",
                id, statement, confidence, totalEvidence, confirmCount, contradictCount);
        }
    }

    public record EvidenceRecord(
        String beliefId,
        EvidenceType type,
        double strength,
        String source,
        double confidenceBefore,
        double confidenceAfter
    ) {}

    public record BeliefChangeEvent(
        Belief belief,
        EvidenceType type,
        double oldConfidence,
        double newConfidence,
        String source
    ) {}
}
