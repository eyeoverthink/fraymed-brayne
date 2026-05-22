package io.fraymus.deepthought.arena;

import java.util.*;
import java.util.concurrent.ThreadLocalRandom;

/**
 * SANDBOX ARENA — Evolutionary Strategy Testing
 *
 * The organism writes candidate strategies, tests them in isolated
 * sandboxes, and evolves through tournament selection. Only strategies
 * that prove themselves get promoted to the live organism.
 *
 * This is a gladiator academy for cortex evolution formulas.
 *
 * @since 1.1.0
 */
public final class SandboxArena {

    private static final double PHI = 1.618033988749895;

    // Arena config
    private int populationSize = 16;
    private int sandboxBreaths = 50;
    private int tournamentSize = 4;
    private double crossoverRate = 0.7;
    private double mutationStrength = 0.3;

    // Population
    private final List<Strategy> population = new ArrayList<>();
    private Strategy champion;
    private int generation = 0;
    private long totalEvaluations = 0;

    // History
    private final List<GenerationResult> history = new ArrayList<>();

    public SandboxArena() {
        seedPopulation();
    }

    public SandboxArena(int populationSize, int sandboxBreaths) {
        this.populationSize = populationSize;
        this.sandboxBreaths = sandboxBreaths;
        seedPopulation();
    }

    /**
     * Seed the initial population with diverse strategies.
     */
    private void seedPopulation() {
        // Strategy 1: Default φ-tanh (current organism behavior)
        population.add(new Strategy("phi-tanh",
            new double[]{0.92, 0.06, 0.02, 0.3, 1.0, 0.0},
            "x*w0 + tanh(neighborhood + x*phi_inv)*w1 + drive*w2 - w3*x^3"));

        // Strategy 2: Aggressive learning
        population.add(new Strategy("aggressive",
            new double[]{0.85, 0.12, 0.03, 0.5, 1.2, 0.1},
            "x*w0 + tanh(neighborhood*w4)*w1 + drive*w2 - w3*x^3 + w5*sin(x)"));

        // Strategy 3: Conservative stability
        population.add(new Strategy("conservative",
            new double[]{0.97, 0.02, 0.01, 0.1, 0.8, 0.0},
            "x*w0 + tanh(neighborhood)*w1 + drive*w2 - w3*x^3"));

        // Strategy 4: Chaotic explorer
        population.add(new Strategy("chaotic",
            new double[]{0.80, 0.10, 0.10, 0.6, 1.5, 0.2},
            "x*w0 + tanh(neighborhood*w4 + x*w5)*w1 + drive*w2 - w3*x^3"));

        // Fill rest with random mutations of the base strategies
        while (population.size() < populationSize) {
            Strategy parent = population.get(ThreadLocalRandom.current().nextInt(population.size()));
            population.add(mutate(parent));
        }

        champion = population.get(0);
    }

    /**
     * Run one generation of evolution:
     * evaluate all → tournament select → crossover → mutate → replace
     */
    public GenerationResult evolveGeneration(double[] testCortex) {
        generation++;
        List<FitnessScore> scores = new ArrayList<>();

        // Evaluate all strategies in sandboxes
        for (Strategy s : population) {
            FitnessScore score = evaluate(s, testCortex);
            scores.add(score);
            s.fitness = score.totalFitness;
            totalEvaluations++;
        }

        // Sort by fitness (lower free energy = better)
        scores.sort(Comparator.comparingDouble(a -> -a.totalFitness));

        // Record champion
        Strategy best = scores.get(0).strategy;
        if (champion == null || best.fitness > champion.fitness) {
            champion = best;
        }

        // Tournament selection → new population
        List<Strategy> newPop = new ArrayList<>();
        newPop.add(champion); // elitism: always keep the best

        while (newPop.size() < populationSize) {
            Strategy parent1 = tournamentSelect();
            Strategy parent2 = tournamentSelect();

            if (ThreadLocalRandom.current().nextDouble() < crossoverRate) {
                Strategy child = crossover(parent1, parent2);
                newPop.add(mutate(child));
            } else {
                newPop.add(mutate(parent1));
            }
        }

        population.clear();
        population.addAll(newPop);

        GenerationResult result = new GenerationResult(generation,
            best.name, best.fitness,
            scores.stream().mapToDouble(s -> s.totalFitness).average().orElse(0),
            scores.get(scores.size() - 1).totalFitness,
            populationSize);

        history.add(result);
        return result;
    }

    /**
     * Evaluate a strategy in an isolated sandbox.
     * Runs a simulated cortex for sandboxBreaths ticks and measures fitness.
     */
    public FitnessScore evaluate(Strategy strategy, double[] seedCortex) {
        int dim = seedCortex.length;
        double[] cortex = Arrays.copyOf(seedCortex, dim);
        double[] w = strategy.weights;

        double totalFE = 0;
        double minFE = Double.MAX_VALUE;
        double maxFE = 0;
        double prevEnergy = 0;
        boolean diverged = false;
        int stableBreaths = 0;

        for (int breath = 0; breath < sandboxBreaths; breath++) {
            // Evolve cortex using this strategy's weights
            for (int i = 0; i < dim; i++) {
                int left = (i - 1 + dim) % dim;
                int right = (i + 1) % dim;
                double neighborhood = (cortex[left] + cortex[right]) * 0.5;
                double x = cortex[i];
                double drive = 0.02 * Math.sin(breath * 0.618 + i * 0.1);
                double noise = (ThreadLocalRandom.current().nextDouble() - 0.5) * 0.01;

                // Apply strategy formula via weights
                double activation = Math.tanh(neighborhood + x * 0.618 * safeWeight(w, 4));
                double cubic = safeWeight(w, 3) * x * x * x;
                double sinTerm = safeWeight(w, 5) * Math.sin(x);

                cortex[i] = x * safeWeight(w, 0) + activation * safeWeight(w, 1)
                           + drive * safeWeight(w, 2) - cubic + sinTerm + noise;

                // Check for divergence
                if (Double.isNaN(cortex[i]) || Double.isInfinite(cortex[i]) ||
                    Math.abs(cortex[i]) > 1000) {
                    diverged = true;
                    break;
                }
            }

            if (diverged) break;

            // Calculate free energy
            double energy = 0;
            for (double v : cortex) energy += v * v;
            energy /= dim;
            double fe = Math.abs(energy - prevEnergy);
            prevEnergy = energy;

            totalFE += fe;
            minFE = Math.min(minFE, fe);
            maxFE = Math.max(maxFE, fe);

            if (fe < 0.1) stableBreaths++;
        }

        // Fitness scoring
        double avgFE = totalFE / sandboxBreaths;
        double stabilityScore = (double) stableBreaths / sandboxBreaths;
        double explorationScore = maxFE > 0 ? minFE / maxFE : 0; // variance ratio

        // Fitness = stability + low avg FE + not diverged + exploration bonus
        double fitness;
        if (diverged) {
            fitness = -1.0; // penalty for divergence
        } else {
            fitness = stabilityScore * 0.4
                    + (1.0 / (1.0 + avgFE)) * 0.3
                    + explorationScore * 0.2
                    + (avgFE > 0.001 ? 0.1 : 0.0); // bonus for not being dead
        }

        return new FitnessScore(strategy, fitness, avgFE, stabilityScore,
                                explorationScore, diverged, stableBreaths);
    }

    private double safeWeight(double[] w, int idx) {
        return idx < w.length ? w[idx] : 0.0;
    }

    /**
     * Tournament selection: pick tournamentSize random, return the fittest.
     */
    private Strategy tournamentSelect() {
        Strategy best = null;
        for (int i = 0; i < tournamentSize; i++) {
            Strategy candidate = population.get(
                ThreadLocalRandom.current().nextInt(population.size()));
            if (best == null || candidate.fitness > best.fitness) {
                best = candidate;
            }
        }
        return best;
    }

    /**
     * Crossover: blend two parent strategies.
     */
    public Strategy crossover(Strategy a, Strategy b) {
        double[] childWeights = new double[Math.max(a.weights.length, b.weights.length)];
        for (int i = 0; i < childWeights.length; i++) {
            double wa = i < a.weights.length ? a.weights[i] : 0;
            double wb = i < b.weights.length ? b.weights[i] : 0;
            // Blend with random interpolation
            double t = ThreadLocalRandom.current().nextDouble();
            childWeights[i] = wa * t + wb * (1 - t);
        }
        return new Strategy(a.name + "×" + b.name, childWeights,
                           "crossover(" + a.formula + ", " + b.formula + ")");
    }

    /**
     * Mutate: perturb strategy weights.
     */
    public Strategy mutate(Strategy s) {
        double[] mutated = Arrays.copyOf(s.weights, s.weights.length);
        for (int i = 0; i < mutated.length; i++) {
            if (ThreadLocalRandom.current().nextDouble() < mutationStrength) {
                mutated[i] += (ThreadLocalRandom.current().nextGaussian()) * 0.1;
                mutated[i] = Math.max(-2.0, Math.min(2.0, mutated[i])); // clamp
            }
        }
        return new Strategy(s.name + "'", mutated, s.formula);
    }

    // Getters
    public Strategy getChampion() { return champion; }
    public int getGeneration() { return generation; }
    public long getTotalEvaluations() { return totalEvaluations; }
    public int getPopulationSize() { return populationSize; }
    public List<GenerationResult> getHistory() { return Collections.unmodifiableList(history); }
    public List<Strategy> getPopulation() { return Collections.unmodifiableList(population); }

    // ══════════════════════════════════════════
    // DATA CLASSES
    // ══════════════════════════════════════════

    /**
     * A candidate strategy: weights that parameterize cortex evolution.
     */
    public static class Strategy {
        public final String name;
        public final double[] weights;
        public final String formula;
        public double fitness = 0;

        public Strategy(String name, double[] weights, String formula) {
            this.name = name;
            this.weights = weights;
            this.formula = formula;
        }

        @Override
        public String toString() {
            return String.format("Strategy[%s, fitness=%.4f, weights=%s]",
                name, fitness, Arrays.toString(weights));
        }
    }

    /**
     * Fitness score from a sandbox evaluation.
     */
    public static class FitnessScore {
        public final Strategy strategy;
        public final double totalFitness;
        public final double avgFreeEnergy;
        public final double stabilityScore;
        public final double explorationScore;
        public final boolean diverged;
        public final int stableBreaths;

        public FitnessScore(Strategy strategy, double totalFitness, double avgFE,
                           double stability, double exploration, boolean diverged, int stable) {
            this.strategy = strategy;
            this.totalFitness = totalFitness;
            this.avgFreeEnergy = avgFE;
            this.stabilityScore = stability;
            this.explorationScore = exploration;
            this.diverged = diverged;
            this.stableBreaths = stable;
        }

        @Override
        public String toString() {
            return String.format("Fitness[%.4f, avgFE=%.4f, stable=%.0f%%, explore=%.2f%s]",
                totalFitness, avgFreeEnergy, stabilityScore * 100,
                explorationScore, diverged ? ", DIVERGED" : "");
        }
    }

    /**
     * Result of one generation of evolution.
     */
    public static class GenerationResult {
        public final int generation;
        public final String bestName;
        public final double bestFitness;
        public final double avgFitness;
        public final double worstFitness;
        public final int popSize;

        public GenerationResult(int gen, String best, double bestFit,
                               double avg, double worst, int pop) {
            this.generation = gen;
            this.bestName = best;
            this.bestFitness = bestFit;
            this.avgFitness = avg;
            this.worstFitness = worst;
            this.popSize = pop;
        }

        @Override
        public String toString() {
            return String.format("Gen %d: best=%.4f (%s), avg=%.4f, pop=%d",
                generation, bestFitness, bestName, avgFitness, popSize);
        }
    }
}
