package io.fraymus.deepthought.collective;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

/**
 * COLLECTIVE MIND — Multi-Agent Bayesian Consensus
 * 
 * Enables multiple entities/agents to share patterns, build consensus,
 * and form collective knowledge through Bayesian belief aggregation.
 * 
 * When enough independent agents agree on a pattern, it gets promoted
 * to "collective knowledge" — a high-confidence shared belief.
 * 
 * @since 1.0.0
 */
public final class CollectiveMind {

    private final Map<String, SharedPattern> patterns = new ConcurrentHashMap<>();
    private final Map<String, AgentProfile> agents = new ConcurrentHashMap<>();

    private double collectiveCoherence = 0.5;
    private double consensusThreshold = 0.7;
    private int totalContributions = 0;
    private int consensusReached = 0;

    /**
     * Register an agent/entity for participation.
     */
    public CollectiveMind registerAgent(String agentId) {
        agents.computeIfAbsent(agentId, AgentProfile::new);
        return this;
    }

    /**
     * Agent broadcasts a pattern/observation with confidence.
     */
    public void contribute(String agentId, String pattern, double confidence) {
        agents.computeIfAbsent(agentId, AgentProfile::new);

        SharedPattern sp = patterns.computeIfAbsent(pattern, SharedPattern::new);
        sp.addContribution(agentId, confidence);
        totalContributions++;

        AgentProfile profile = agents.get(agentId);
        profile.contributions++;

        if (sp.getConsensusLevel() > consensusThreshold && !sp.isCollective) {
            sp.isCollective = true;
            consensusReached++;
            for (String contributor : sp.contributors.keySet()) {
                AgentProfile p = agents.get(contributor);
                if (p != null) p.influence += 0.1;
            }
        }

        updateCoherence();
    }

    /**
     * Query the collective for patterns matching a topic.
     */
    public List<SharedPattern> query(String topic, int maxResults) {
        List<SharedPattern> results = new ArrayList<>();
        String lower = topic.toLowerCase();

        for (SharedPattern sp : patterns.values()) {
            if (sp.pattern.toLowerCase().contains(lower) ||
                lower.contains(sp.pattern.toLowerCase())) {
                results.add(sp);
            }
        }

        results.sort((a, b) -> Double.compare(
            b.avgConfidence * b.getConsensusLevel(),
            a.avgConfidence * a.getConsensusLevel()));

        return results.subList(0, Math.min(maxResults, results.size()));
    }

    /**
     * Get all patterns that have reached collective consensus.
     */
    public List<SharedPattern> getCollectiveKnowledge() {
        List<SharedPattern> knowledge = new ArrayList<>();
        for (SharedPattern sp : patterns.values()) {
            if (sp.isCollective) knowledge.add(sp);
        }
        knowledge.sort((a, b) -> Double.compare(b.avgConfidence, a.avgConfidence));
        return knowledge;
    }

    /**
     * Get the most influential agents.
     */
    public List<AgentProfile> getTopAgents(int count) {
        List<AgentProfile> sorted = new ArrayList<>(agents.values());
        sorted.sort((a, b) -> Double.compare(b.influence, a.influence));
        return sorted.subList(0, Math.min(count, sorted.size()));
    }

    private void updateCoherence() {
        if (patterns.isEmpty()) return;
        double total = 0;
        for (SharedPattern sp : patterns.values()) {
            total += sp.getConsensusLevel();
        }
        collectiveCoherence = collectiveCoherence * 0.9 + (total / patterns.size()) * 0.1;
    }

    // --- Configuration ---

    public CollectiveMind setConsensusThreshold(double t) { consensusThreshold = t; return this; }

    // --- Metrics ---

    public double getCoherence() { return collectiveCoherence; }
    public int getAgentCount() { return agents.size(); }
    public int getPatternCount() { return patterns.size(); }
    public int getConsensusCount() { return consensusReached; }
    public int getTotalContributions() { return totalContributions; }

    // --- Data classes ---

    public static final class SharedPattern {
        public final String pattern;
        public final Map<String, Double> contributors = new HashMap<>();
        public double avgConfidence = 0;
        public boolean isCollective = false;

        SharedPattern(String pattern) { this.pattern = pattern; }

        void addContribution(String agent, double confidence) {
            contributors.put(agent, confidence);
            double sum = 0;
            for (double c : contributors.values()) sum += c;
            avgConfidence = sum / contributors.size();
        }

        public double getConsensusLevel() {
            return Math.min(1.0, contributors.size() / 5.0) * avgConfidence;
        }

        public int getContributorCount() { return contributors.size(); }

        @Override public String toString() {
            return String.format("Pattern[\"%s\" consensus=%.3f, agents=%d, collective=%s]",
                pattern, getConsensusLevel(), contributors.size(), isCollective);
        }
    }

    public static final class AgentProfile {
        public final String id;
        public double influence = 1.0;
        public int contributions = 0;

        AgentProfile(String id) { this.id = id; }

        @Override public String toString() {
            return String.format("Agent[%s influence=%.2f, contributions=%d]", id, influence, contributions);
        }
    }
}
