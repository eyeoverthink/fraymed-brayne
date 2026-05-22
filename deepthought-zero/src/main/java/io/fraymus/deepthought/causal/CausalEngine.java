package io.fraymus.deepthought.causal;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

/**
 * CAUSAL REASONING ENGINE
 * 
 * Builds causal graphs from observations, then reasons about:
 * - Why did X happen? (explanation)
 * - What if I change X? (intervention)
 * - What would have happened if X was different? (counterfactual)
 * - Is the correlation real or caused by a confounder? (confounding detection)
 * 
 * This goes beyond correlation — it models cause and effect.
 * 
 * @since 1.0.0
 */
public final class CausalEngine {

    private final Map<String, CausalNode> nodes = new ConcurrentHashMap<>();
    private final List<CausalEdge> edges = Collections.synchronizedList(new ArrayList<>());
    private final List<Observation> observations = Collections.synchronizedList(new ArrayList<>());

    private int maxObservations = 2000;
    private int minObservationsForLearning = 20;
    private double edgeThreshold = 0.3;

    // Metrics
    private int edgesDiscovered = 0;
    private int interventionsRun = 0;
    private int counterfactualsEvaluated = 0;

    /**
     * Register a variable in the causal graph.
     */
    public CausalEngine variable(String name) {
        nodes.computeIfAbsent(name, CausalNode::new);
        return this;
    }

    /**
     * Register multiple variables.
     */
    public CausalEngine variables(String... names) {
        for (String n : names) variable(n);
        return this;
    }

    /**
     * Record an observation of variable states.
     * Call this repeatedly to build the causal graph.
     */
    public void observe(Map<String, Double> variableStates) {
        observations.add(new Observation(variableStates));
        while (observations.size() > maxObservations) observations.remove(0);

        // Auto-register any new variables
        for (String key : variableStates.keySet()) variable(key);

        // Periodically learn causal relationships
        if (observations.size() % 50 == 0) {
            learnCausalRelationships();
        }
    }

    /**
     * Convenience: observe from parallel arrays.
     */
    public void observe(String[] names, double[] values) {
        Map<String, Double> states = new HashMap<>();
        for (int i = 0; i < names.length && i < values.length; i++) {
            states.put(names[i], values[i]);
        }
        observe(states);
    }

    /**
     * Force learning of causal relationships from current observations.
     */
    public void learn() {
        learnCausalRelationships();
    }

    /**
     * Simulate an intervention: "What happens if we set X to value?"
     * Returns predicted downstream effects.
     */
    public Map<String, Double> intervene(String variable, double value) {
        interventionsRun++;
        Map<String, Double> effects = new HashMap<>();

        Set<String> visited = new HashSet<>();
        Queue<String> queue = new LinkedList<>();
        queue.add(variable);

        while (!queue.isEmpty()) {
            String current = queue.poll();
            if (visited.contains(current)) continue;
            visited.add(current);

            CausalNode node = nodes.get(current);
            if (node == null) continue;

            for (String child : node.children) {
                CausalEdge edge = findEdge(current, child);
                if (edge != null) {
                    double expectedChange = value * edge.strength;
                    effects.put(child, expectedChange);
                    queue.add(child);
                }
            }
        }

        return effects;
    }

    /**
     * Counterfactual: "What would have happened if X had been different?"
     */
    public Map<String, Double> counterfactual(String variable, double actualValue,
                                               double hypotheticalValue,
                                               Map<String, Double> actualOutcomes) {
        counterfactualsEvaluated++;
        Map<String, Double> hypothetical = new HashMap<>();
        double delta = hypotheticalValue - actualValue;

        CausalNode node = nodes.get(variable);
        if (node == null) return hypothetical;

        for (String child : node.children) {
            CausalEdge edge = findEdge(variable, child);
            if (edge != null) {
                double actual = actualOutcomes.getOrDefault(child, 0.0);
                hypothetical.put(child, actual + (delta * edge.strength));
            }
        }

        return hypothetical;
    }

    /**
     * Explain why an effect occurred — list causes ranked by strength.
     */
    public List<Explanation> explain(String effect) {
        List<Explanation> explanations = new ArrayList<>();

        CausalNode node = nodes.get(effect);
        if (node == null) return explanations;

        for (String parent : node.parents) {
            CausalEdge edge = findEdge(parent, effect);
            if (edge != null) {
                double confidence = Math.min(1.0, edge.observations / 100.0);
                explanations.add(new Explanation(parent, effect, edge.strength, confidence));
            }
        }

        explanations.sort((a, b) -> Double.compare(b.strength, a.strength));
        return explanations;
    }

    /**
     * Find confounding variables between a cause and effect.
     */
    public List<String> findConfounders(String cause, String effect) {
        CausalNode causeNode = nodes.get(cause);
        CausalNode effectNode = nodes.get(effect);
        if (causeNode == null || effectNode == null) return List.of();

        Set<String> common = new HashSet<>(causeNode.parents);
        common.retainAll(effectNode.parents);
        return new ArrayList<>(common);
    }

    /**
     * Get the causal path from one variable to another (BFS).
     */
    public List<String> getPath(String from, String to) {
        Map<String, String> parent = new HashMap<>();
        Queue<String> queue = new LinkedList<>();
        queue.add(from);
        parent.put(from, null);

        while (!queue.isEmpty()) {
            String current = queue.poll();
            if (current.equals(to)) {
                List<String> path = new ArrayList<>();
                String node = to;
                while (node != null) {
                    path.add(0, node);
                    node = parent.get(node);
                }
                return path;
            }
            CausalNode n = nodes.get(current);
            if (n != null) {
                for (String child : n.children) {
                    if (!parent.containsKey(child)) {
                        parent.put(child, current);
                        queue.add(child);
                    }
                }
            }
        }
        return List.of();
    }

    /**
     * Get all edges in the causal graph.
     */
    public List<CausalEdge> getEdges() {
        List<CausalEdge> sorted = new ArrayList<>(edges);
        sorted.sort((a, b) -> Double.compare(b.strength, a.strength));
        return sorted;
    }

    // --- Internal ---

    private void learnCausalRelationships() {
        if (observations.size() < minObservationsForLearning) return;

        List<String> vars = new ArrayList<>(nodes.keySet());
        for (int i = 0; i < vars.size(); i++) {
            for (int j = 0; j < vars.size(); j++) {
                if (i == j) continue;
                double strength = estimateCausalStrength(vars.get(i), vars.get(j));
                if (strength > edgeThreshold) {
                    addOrUpdateEdge(vars.get(i), vars.get(j), strength);
                }
            }
        }
    }

    private double estimateCausalStrength(String cause, String effect) {
        if (observations.size() < 10) return 0;

        double[] causeVals = new double[observations.size() - 1];
        double[] effectVals = new double[observations.size() - 1];
        int valid = 0;

        synchronized (observations) {
            for (int i = 0; i < observations.size() - 1; i++) {
                Double cv = observations.get(i).states.get(cause);
                Double ev = observations.get(i + 1).states.get(effect);
                if (cv != null && ev != null) {
                    causeVals[valid] = cv;
                    effectVals[valid] = ev;
                    valid++;
                }
            }
        }

        if (valid < 5) return 0;
        return Math.abs(correlate(
            Arrays.copyOf(causeVals, valid),
            Arrays.copyOf(effectVals, valid)));
    }

    private void addOrUpdateEdge(String cause, String effect, double strength) {
        for (CausalEdge edge : edges) {
            if (edge.cause.equals(cause) && edge.effect.equals(effect)) {
                edge.strength = edge.strength * 0.8 + strength * 0.2;
                edge.observations++;
                return;
            }
        }
        edges.add(new CausalEdge(cause, effect, strength));
        edgesDiscovered++;

        CausalNode causeNode = nodes.get(cause);
        CausalNode effectNode = nodes.get(effect);
        if (causeNode != null) causeNode.children.add(effect);
        if (effectNode != null) effectNode.parents.add(cause);
    }

    private CausalEdge findEdge(String cause, String effect) {
        for (CausalEdge edge : edges) {
            if (edge.cause.equals(cause) && edge.effect.equals(effect)) return edge;
        }
        return null;
    }

    private static double correlate(double[] a, double[] b) {
        int n = Math.min(a.length, b.length);
        if (n < 2) return 0;
        double sA = 0, sB = 0, sAB = 0, sA2 = 0, sB2 = 0;
        for (int i = 0; i < n; i++) {
            sA += a[i]; sB += b[i]; sAB += a[i]*b[i];
            sA2 += a[i]*a[i]; sB2 += b[i]*b[i];
        }
        double num = n * sAB - sA * sB;
        double den = Math.sqrt((n * sA2 - sA * sA) * (n * sB2 - sB * sB));
        return den > 0 ? num / den : 0;
    }

    // --- Configuration ---

    public CausalEngine setEdgeThreshold(double t) { this.edgeThreshold = t; return this; }
    public CausalEngine setMaxObservations(int m) { this.maxObservations = m; return this; }

    // --- Metrics ---

    public int getNodeCount() { return nodes.size(); }
    public int getEdgeCount() { return edges.size(); }
    public int getObservationCount() { return observations.size(); }
    public int getEdgesDiscovered() { return edgesDiscovered; }

    // --- Data classes ---

    private static final class CausalNode {
        final String name;
        final Set<String> parents = new HashSet<>();
        final Set<String> children = new HashSet<>();
        CausalNode(String name) { this.name = name; }
    }

    public static final class CausalEdge {
        public final String cause;
        public final String effect;
        public double strength;
        public int observations = 1;
        CausalEdge(String c, String e, double s) { cause = c; effect = e; strength = s; }
        @Override public String toString() {
            return String.format("%s → %s (strength=%.3f, obs=%d)", cause, effect, strength, observations);
        }
    }

    private record Observation(Map<String, Double> states) {
        Observation(Map<String, Double> states) {
            this.states = new HashMap<>(states);
        }
    }

    public record Explanation(String cause, String effect, double strength, double confidence) {
        @Override public String toString() {
            return String.format("%s causes %s (strength=%.3f, confidence=%.3f)", cause, effect, strength, confidence);
        }
    }
}
