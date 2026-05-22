package io.fraymus.deepthought.meta;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

/**
 * META-LEARNER: Learn How To Learn
 * 
 * Adaptive strategy selection using Bayesian bandit algorithms.
 * The system evaluates multiple learning strategies, tracks their success,
 * and automatically switches to the best one based on evidence.
 * 
 * Uses Upper Confidence Bound (UCB) for exploration/exploitation balance.
 * Supports cross-domain pattern transfer.
 * 
 * @since 1.0.0
 */
public final class MetaLearner {

    /**
     * Available learning strategies.
     */
    public enum Strategy {
        EXPLORATION,      // High variance, discover new patterns
        EXPLOITATION,     // Low variance, refine known patterns
        TRANSFER,         // Apply patterns across domains
        CONSOLIDATION,    // Strengthen existing knowledge
        SYNTHESIS         // Combine patterns creatively
    }

    private Strategy currentStrategy = Strategy.EXPLORATION;
    private double learningRate = 0.1;
    private double explorationRate = 0.3;

    private final Map<Strategy, StrategyStats> strategyStats = new ConcurrentHashMap<>();
    private final List<LearningEvent> history = Collections.synchronizedList(new ArrayList<>());
    private final Map<String, DomainTracker> domains = new ConcurrentHashMap<>();

    // Tuning
    private double adaptationSpeed = 0.05;
    private int evaluationWindow = 50;
    private double successThreshold = 0.6;
    private int maxHistory = 2000;

    // Metrics
    private int totalEvents = 0;
    private double avgSuccess = 0.5;
    private double metaProgress = 0;
    private int strategyChanges = 0;

    public MetaLearner() {
        for (Strategy s : Strategy.values()) {
            strategyStats.put(s, new StrategyStats(s));
        }
    }

    /**
     * Record a learning event and let the meta-learner adapt.
     *
     * @param domain  The domain this learning occurred in
     * @param pattern What was learned
     * @param success How successful was it (0.0 to 1.0)
     */
    public void record(String domain, String pattern, double success) {
        history.add(new LearningEvent(domain, pattern, success, currentStrategy));
        totalEvents++;

        DomainTracker dt = domains.computeIfAbsent(domain, DomainTracker::new);
        dt.addPattern(pattern, success);

        while (history.size() > maxHistory) history.remove(0);

        // Auto-evaluate every 10 events
        if (totalEvents % 10 == 0) {
            evaluateAndAdapt();
        }
    }

    /**
     * Evaluate performance and adapt strategy if needed.
     */
    public void evaluateAndAdapt() {
        if (history.size() < evaluationWindow) return;

        double recentSuccess = calculateRecentSuccess();

        StrategyStats current = strategyStats.get(currentStrategy);
        current.recordOutcome(recentSuccess > successThreshold);

        if (shouldChangeStrategy(recentSuccess)) {
            Strategy best = selectBestStrategy();
            if (best != currentStrategy) {
                currentStrategy = best;
                strategyChanges++;
                adaptParameters();
            }
        }

        adaptLearningRate(recentSuccess);
        metaProgress = metaProgress * 0.99 + (recentSuccess - avgSuccess) * 0.01;
        avgSuccess = avgSuccess * 0.95 + recentSuccess * 0.05;
    }

    /**
     * Get optimized learning parameters for a domain.
     */
    public LearningParams getParams(String domain) {
        LearningParams params = new LearningParams(learningRate, explorationRate, currentStrategy);

        DomainTracker dt = domains.get(domain);
        if (dt != null) {
            if (dt.avgSuccess > 0.7) {
                params.explorationRate *= 0.5;
                params.learningRate *= 1.2;
            } else if (dt.avgSuccess < 0.4) {
                params.explorationRate *= 1.5;
                params.learningRate *= 0.8;
            }
        }

        String transfer = findTransferSource(domain);
        if (transfer != null) {
            params.transferSource = transfer;
        }

        return params;
    }

    /**
     * Get transferable patterns from successful domains.
     */
    public List<String> getTransferablePatterns(String targetDomain) {
        List<String> transferable = new ArrayList<>();
        for (Map.Entry<String, DomainTracker> entry : domains.entrySet()) {
            if (entry.getKey().equals(targetDomain)) continue;
            DomainTracker source = entry.getValue();
            if (source.avgSuccess > 0.7) {
                source.getTopPatterns(3).forEach(p ->
                    transferable.add(source.domain + ":" + p));
            }
        }
        return transferable;
    }

    // --- Internal ---

    private double calculateRecentSuccess() {
        int window = Math.min(evaluationWindow, history.size());
        if (window == 0) return 0.5;
        double sum = 0;
        synchronized (history) {
            for (int i = history.size() - window; i < history.size(); i++) {
                sum += history.get(i).success;
            }
        }
        return sum / window;
    }

    private boolean shouldChangeStrategy(double recentSuccess) {
        StrategyStats current = strategyStats.get(currentStrategy);
        if (recentSuccess > successThreshold && current.getSuccessRate() > 0.6) return false;
        if (current.trials > 20 && current.getSuccessRate() < 0.4) return true;
        return Math.random() < (1 - recentSuccess) * 0.618 * 0.1;
    }

    /**
     * UCB-based strategy selection (Bayesian Bandit).
     */
    private Strategy selectBestStrategy() {
        Strategy best = currentStrategy;
        double bestScore = 0;
        for (Strategy s : Strategy.values()) {
            StrategyStats stats = strategyStats.get(s);
            double explorationBonus = 1.0 / Math.sqrt(stats.trials + 1);
            double score = stats.getSuccessRate() + explorationBonus * explorationRate;
            if (score > bestScore) {
                bestScore = score;
                best = s;
            }
        }
        return best;
    }

    private void adaptParameters() {
        switch (currentStrategy) {
            case EXPLORATION    -> { explorationRate = Math.min(0.5, explorationRate * 1.2);
                                     learningRate = Math.max(0.05, learningRate * 0.9); }
            case EXPLOITATION   -> { explorationRate = Math.max(0.1, explorationRate * 0.8);
                                     learningRate = Math.min(0.3, learningRate * 1.1); }
            case TRANSFER       -> { explorationRate = 0.2; learningRate = 0.15; }
            case CONSOLIDATION  -> { explorationRate = 0.1; learningRate = 0.05; }
            case SYNTHESIS      -> { explorationRate = 0.3; learningRate = 0.2; }
        }
    }

    private void adaptLearningRate(double recentSuccess) {
        if (recentSuccess > successThreshold)
            learningRate = Math.min(0.3, learningRate * (1 + adaptationSpeed));
        else
            learningRate = Math.max(0.01, learningRate * (1 - adaptationSpeed));
    }

    private String findTransferSource(String target) {
        DomainTracker tgt = domains.get(target);
        if (tgt != null && tgt.avgSuccess > 0.6) return null;
        String best = null;
        double bestScore = 0;
        for (Map.Entry<String, DomainTracker> e : domains.entrySet()) {
            if (e.getKey().equals(target)) continue;
            DomainTracker src = e.getValue();
            if (src.avgSuccess > 0.6 && src.patternCount > 10) {
                double score = src.avgSuccess;
                if (score > bestScore) { bestScore = score; best = src.domain; }
            }
        }
        return bestScore > 0.3 ? best : null;
    }

    // --- Getters ---

    public Strategy getCurrentStrategy() { return currentStrategy; }
    public double getLearningRate() { return learningRate; }
    public double getExplorationRate() { return explorationRate; }
    public double getAvgSuccess() { return avgSuccess; }
    public double getMetaProgress() { return metaProgress; }
    public int getStrategyChanges() { return strategyChanges; }
    public int getTotalEvents() { return totalEvents; }
    public int getDomainCount() { return domains.size(); }

    public Map<Strategy, Double> getStrategyPerformance() {
        Map<Strategy, Double> perf = new LinkedHashMap<>();
        for (Strategy s : Strategy.values()) {
            perf.put(s, strategyStats.get(s).getSuccessRate());
        }
        return perf;
    }

    // --- Data classes ---

    public static final class LearningParams {
        public double learningRate;
        public double explorationRate;
        public Strategy strategy;
        public String transferSource;
        LearningParams(double lr, double er, Strategy s) {
            learningRate = lr; explorationRate = er; strategy = s;
        }
    }

    private record LearningEvent(String domain, String pattern, double success, Strategy strategy) {}

    private static final class StrategyStats {
        final Strategy strategy;
        int trials = 0;
        int successes = 0;
        StrategyStats(Strategy s) { strategy = s; }
        void recordOutcome(boolean success) { trials++; if (success) successes++; }
        double getSuccessRate() { return trials > 0 ? (double) successes / trials : 0.5; }
    }

    private static final class DomainTracker {
        final String domain;
        final Map<String, PatternInfo> patterns = new HashMap<>();
        int patternCount = 0;
        double avgSuccess = 0.5;
        DomainTracker(String d) { domain = d; }

        void addPattern(String pattern, double success) {
            PatternInfo pi = patterns.computeIfAbsent(pattern, PatternInfo::new);
            pi.occurrences++;
            pi.avgSuccess = pi.avgSuccess * 0.9 + success * 0.1;
            patternCount++;
            avgSuccess = avgSuccess * 0.95 + success * 0.05;
        }

        List<String> getTopPatterns(int count) {
            return patterns.entrySet().stream()
                .sorted((a, b) -> Double.compare(b.getValue().avgSuccess, a.getValue().avgSuccess))
                .limit(count)
                .map(Map.Entry::getKey)
                .toList();
        }
    }

    private static final class PatternInfo {
        final String pattern;
        int occurrences = 0;
        double avgSuccess = 0.5;
        PatternInfo(String p) { pattern = p; }
    }
}
