package io.fraymus.deepthought.chaos;

import java.math.BigInteger;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.ArrayList;
import java.util.List;
import java.util.function.Consumer;

/**
 * EVOLUTIONARY CHAOS ENGINE
 * 
 * A self-correcting, entropy-seeded cryptographic random generator.
 * 
 * What makes it different from java.util.Random or SecureRandom:
 * - Seeds from PHYSICAL entropy (nanoTime jitter, GC memory state)
 * - SHA-512 cryptographic mixing (avalanche effect)
 * - Self-awareness: monitors its own output for bias
 * - Auto-mutation: escapes detected patterns by mutating state
 * - Infinite state space via BigInteger (never overflows, never loops)
 * - Recursive: every output depends on ALL previous history
 * 
 * Patent: VS-PoQC-19046423-φ⁷⁵-2025
 * Author: Vaughn Scott
 * 
 * @since 1.0.0
 */
public final class ChaosEngine {

    private BigInteger fractalState;
    private final List<Integer> shortTermMemory = new ArrayList<>();
    private final MessageDigest hasher;
    private int mutationRate = 0;
    private BigInteger generation = BigInteger.ZERO;

    // Self-awareness metrics
    private long totalMutations = 0;
    private long patternsDetected = 0;
    private int maxMutationRate = 0;

    // Configuration
    private int biasWindow = 50;
    private int biasThreshold = 10; // >20% of window triggers mutation

    // Event callback
    private Consumer<MutationEvent> onMutation;

    /**
     * Create a new ChaosEngine seeded from physical entropy.
     */
    public ChaosEngine() {
        try {
            this.hasher = MessageDigest.getInstance("SHA-512");
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("SHA-512 not available", e);
        }
        String seed = System.nanoTime() + ":" +
                       new Object().hashCode() + ":" +
                       Thread.currentThread().getId() + ":" +
                       Runtime.getRuntime().freeMemory();
        this.fractalState = new BigInteger(1, hash(seed));
    }

    /**
     * Create a ChaosEngine with a custom initial seed.
     * Physical entropy is still mixed in on every call.
     */
    public ChaosEngine(String seed) {
        try {
            this.hasher = MessageDigest.getInstance("SHA-512");
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("SHA-512 not available", e);
        }
        String fullSeed = seed + ":" + System.nanoTime() + ":" +
                          Runtime.getRuntime().freeMemory();
        this.fractalState = new BigInteger(1, hash(fullSeed));
    }

    /**
     * Generate the next fractal state value.
     * Each call mixes physical entropy, hashes with SHA-512,
     * and checks for self-bias.
     *
     * @return the full BigInteger fractal state
     */
    public BigInteger nextFractal() {
        long jitter = System.nanoTime() % 999;
        long memoryJitter = Runtime.getRuntime().freeMemory() % 1000;

        String input = fractalState.toString() + ":" +
                        jitter + ":" + memoryJitter + ":" +
                        mutationRate + ":" + generation.toString();

        byte[] hashBytes = hasher.digest(input.getBytes());
        BigInteger nextValue = new BigInteger(1, hashBytes);
        fractalState = fractalState.add(nextValue);

        analyzeSelf(nextValue);
        generation = generation.add(BigInteger.ONE);

        return fractalState;
    }

    /**
     * Generate a random integer in [0, bound).
     */
    public int nextInt(int bound) {
        return nextFractal().mod(BigInteger.valueOf(bound)).intValue();
    }

    /**
     * Generate a random long in [0, bound).
     */
    public long nextLong(long bound) {
        return nextFractal().mod(BigInteger.valueOf(bound)).longValue();
    }

    /**
     * Generate a random double in [0.0, 1.0).
     */
    public double nextDouble() {
        return nextFractal().mod(BigInteger.valueOf(1_000_000_000L))
                .doubleValue() / 1_000_000_000.0;
    }

    /**
     * Generate random bytes.
     */
    public byte[] nextBytes(int count) {
        byte[] result = new byte[count];
        int filled = 0;
        while (filled < count) {
            byte[] chunk = nextFractal().toByteArray();
            int toCopy = Math.min(chunk.length, count - filled);
            System.arraycopy(chunk, 0, result, filled, toCopy);
            filled += toCopy;
        }
        return result;
    }

    /**
     * Self-awareness: detect bias in recent outputs and mutate to escape.
     */
    private void analyzeSelf(BigInteger value) {
        int vibe = value.mod(BigInteger.TEN).intValue();
        shortTermMemory.add(vibe);
        if (shortTermMemory.size() > biasWindow) {
            shortTermMemory.remove(0);
        }

        int repeats = 0;
        for (int i : shortTermMemory) {
            if (i == vibe) repeats++;
        }

        if (repeats > biasThreshold) {
            patternsDetected++;
            totalMutations++;
            mutationRate++;
            if (mutationRate > maxMutationRate) {
                maxMutationRate = mutationRate;
            }

            // Mutate state to escape the pattern
            fractalState = fractalState.multiply(BigInteger.valueOf(31337));
            String breakPattern = System.nanoTime() + ":" + mutationRate + ":MUTATE";
            fractalState = fractalState.add(new BigInteger(1, hash(breakPattern)));

            if (onMutation != null) {
                onMutation.accept(new MutationEvent(
                    vibe, repeats, biasWindow, mutationRate, generation));
            }
        } else {
            if (mutationRate > 0) mutationRate--;
        }
    }

    /**
     * Force a mutation (for testing or manual entropy injection).
     */
    public void forceMutation() {
        mutationRate += 10;
        totalMutations++;
        fractalState = fractalState.multiply(BigInteger.valueOf(1337));
        fractalState = fractalState.add(
            new BigInteger(1, hash("FORCE:" + System.nanoTime())));
    }

    /**
     * Inject external entropy into the state.
     */
    public void injectEntropy(String entropy) {
        fractalState = fractalState.add(
            new BigInteger(1, hash(entropy + ":" + System.nanoTime())));
    }

    private byte[] hash(String input) {
        return hasher.digest(input.getBytes());
    }

    // --- Configuration ---

    public ChaosEngine setBiasWindow(int window) {
        this.biasWindow = window;
        return this;
    }

    public ChaosEngine setBiasThreshold(int threshold) {
        this.biasThreshold = threshold;
        return this;
    }

    public ChaosEngine onMutation(Consumer<MutationEvent> callback) {
        this.onMutation = callback;
        return this;
    }

    // --- Metrics ---

    public BigInteger getState() { return fractalState; }
    public BigInteger getGeneration() { return generation; }
    public int getMutationRate() { return mutationRate; }
    public long getTotalMutations() { return totalMutations; }
    public long getPatternsDetected() { return patternsDetected; }
    public int getMaxMutationRate() { return maxMutationRate; }
    public int getStateDigits() { return fractalState.toString().length(); }

    /**
     * Event fired when the engine detects bias and mutates.
     */
    public record MutationEvent(
        int biasedValue,
        int frequency,
        int windowSize,
        int mutationRate,
        BigInteger generation
    ) {}
}
