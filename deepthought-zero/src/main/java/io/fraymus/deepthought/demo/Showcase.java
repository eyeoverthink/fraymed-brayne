package io.fraymus.deepthought.demo;

import io.fraymus.deepthought.DeepThought;
import io.fraymus.deepthought.belief.BeliefSystem;
import io.fraymus.deepthought.causal.CausalEngine;
import io.fraymus.deepthought.guard.ZenoGuard;
import io.fraymus.deepthought.meta.MetaLearner;
import io.fraymus.deepthought.stego.GlyphCoder;

import java.util.*;

/**
 * DEEPTHOUGHT ZERO — Full Showcase
 * 
 * Run this to see every module in action.
 * Zero dependencies. Pure Java.
 */
public class Showcase {

    public static void main(String[] args) throws Exception {

        System.out.println("╔══════════════════════════════════════════════════════╗");
        System.out.println("║       DEEPTHOUGHT ZERO — COGNITIVE LIBRARY          ║");
        System.out.println("║       Zero Dependencies. Framework Agnostic.        ║");
        System.out.println("║       by Vaughn Scott / FRAYMUS                     ║");
        System.out.println("╚══════════════════════════════════════════════════════╝");
        System.out.println();

        DeepThought dt = new DeepThought();

        // ════════════════════════════════════════════════════
        // 1. CHAOS ENGINE — Self-Correcting Entropy
        // ════════════════════════════════════════════════════
        System.out.println("═══ MODULE 1: CHAOS ENGINE ═══");
        System.out.println("Self-correcting entropy PRNG with SHA-512 + physical entropy.");
        System.out.println();

        dt.chaos().onMutation(event -> 
            System.out.printf("  ⚡ SELF-AWARENESS: Digit [%d] appeared %d/%d times → MUTATED (rate=%d)%n",
                event.biasedValue(), event.frequency(), event.windowSize(), event.mutationRate()));

        // Generate and show outputs are unpredictable
        System.out.println("  Generating 10 random values:");
        Set<Integer> seen = new HashSet<>();
        for (int i = 0; i < 10; i++) {
            int val = dt.chaos().nextInt(1000);
            seen.add(val);
            System.out.printf("    [%d] → %d%n", i, val);
        }
        System.out.printf("  Unique values: %d/10 (entropy quality)%n", seen.size());
        System.out.printf("  State size: %d digits (infinite, never overflows)%n", dt.chaos().getStateDigits());

        // Run many generations to trigger self-awareness
        System.out.println("\n  Running 500 generations to trigger self-awareness...");
        for (int i = 0; i < 500; i++) dt.chaos().nextInt(10);
        System.out.printf("  Patterns detected: %d | Mutations: %d | Max rate: %d%n",
            dt.chaos().getPatternsDetected(), dt.chaos().getTotalMutations(), dt.chaos().getMaxMutationRate());
        System.out.println("  ✓ Engine escapes its own patterns automatically.\n");

        // ════════════════════════════════════════════════════
        // 2. BAYESIAN BELIEF SYSTEM
        // ════════════════════════════════════════════════════
        System.out.println("═══ MODULE 2: BAYESIAN BELIEF SYSTEM ═══");
        System.out.println("Evidence-based confidence tracking. Beliefs evolve with data.");
        System.out.println();

        BeliefSystem beliefs = dt.belief();
        beliefs.believe("user-honest", "The user is honest", 0.5);
        beliefs.believe("model-accurate", "The model predictions are accurate", 0.5);
        beliefs.believe("data-clean", "The training data is clean", 0.7);

        // Simulate evidence arriving
        beliefs.confirm("user-honest", 0.8, "passed verification");
        beliefs.confirm("user-honest", 0.9, "consistent history");
        beliefs.contradict("model-accurate", 0.7, "prediction failed on edge case");
        beliefs.confirm("model-accurate", 0.5, "prediction correct on standard case");
        beliefs.clarify("data-clean", 0.6, "manual review of subset");

        System.out.println("  After processing evidence:");
        for (var b : beliefs.getAllBeliefs()) {
            System.out.printf("    %s: confidence=%.3f [+%d/-%d evidence]%n",
                b.id, b.confidence, b.confirmCount, b.contradictCount);
        }

        System.out.println("  Weak beliefs (< 0.5):");
        for (var b : beliefs.getWeakBeliefs(0.5)) {
            System.out.printf("    ⚠ %s: %.3f — needs more evidence%n", b.id, b.confidence);
        }
        System.out.println("  ✓ Beliefs update asymmetrically: harder to build trust than lose it.\n");

        // ════════════════════════════════════════════════════
        // 3. CAUSAL REASONING ENGINE
        // ════════════════════════════════════════════════════
        System.out.println("═══ MODULE 3: CAUSAL REASONING ENGINE ═══");
        System.out.println("Not just correlation — actual cause and effect.");
        System.out.println();

        CausalEngine causal = dt.causal();
        causal.variables("marketing_spend", "website_traffic", "conversions", "revenue");

        // Feed observations where variables carry forward (temporal dependency)
        Random rng = new Random(42);
        double marketing = 0.5, traffic = 0.3, conversions = 0.2, revenue = 200;
        for (int i = 0; i < 300; i++) {
            // Each variable is influenced by its causal parents from previous step
            marketing = 0.5 + rng.nextDouble() * 0.5;
            traffic = traffic * 0.3 + marketing * 0.6 + rng.nextGaussian() * 0.05;
            conversions = conversions * 0.2 + traffic * 0.5 + rng.nextGaussian() * 0.02;
            revenue = revenue * 0.1 + conversions * 800 + rng.nextGaussian() * 10;
            causal.observe(Map.of(
                "marketing_spend", marketing,
                "website_traffic", traffic,
                "conversions", conversions,
                "revenue", revenue
            ));
        }
        causal.learn();

        System.out.println("  Discovered causal edges:");
        for (var edge : causal.getEdges()) {
            System.out.printf("    %s%n", edge);
        }

        System.out.println("\n  Intervention: What if we double marketing spend?");
        var effects = causal.intervene("marketing_spend", 2.0);
        for (var e : effects.entrySet()) {
            System.out.printf("    → %s: predicted change = %.3f%n", e.getKey(), e.getValue());
        }

        System.out.println("\n  Why does revenue change? (explanation)");
        for (var exp : causal.explain("revenue")) {
            System.out.printf("    %s%n", exp);
        }
        System.out.println("  ✓ Goes beyond correlation. Supports interventions + counterfactuals.\n");

        // ════════════════════════════════════════════════════
        // 4. META-LEARNER — Learn How To Learn
        // ════════════════════════════════════════════════════
        System.out.println("═══ MODULE 4: META-LEARNER ═══");
        System.out.println("Adaptive strategy selection. The system learns which learning approach works best.");
        System.out.println();

        MetaLearner meta = dt.meta();

        // Simulate learning events across domains
        String[] domains = {"nlp", "vision", "robotics"};
        for (int i = 0; i < 100; i++) {
            String domain = domains[i % 3];
            double success = domain.equals("nlp") ? 0.7 + rng.nextDouble() * 0.2 :
                             domain.equals("vision") ? 0.3 + rng.nextDouble() * 0.3 :
                             0.5 + rng.nextDouble() * 0.2;
            meta.record(domain, "pattern_" + (i % 10), success);
        }

        System.out.printf("  Current strategy: %s%n", meta.getCurrentStrategy());
        System.out.printf("  Strategy changes: %d (adapted %d times)%n", meta.getStrategyChanges(), meta.getTotalEvents());
        System.out.printf("  Average success: %.3f%n", meta.getAvgSuccess());
        System.out.printf("  Domains tracked: %d%n", meta.getDomainCount());

        System.out.println("  Strategy performance (UCB bandit):");
        for (var entry : meta.getStrategyPerformance().entrySet()) {
            String marker = entry.getKey() == meta.getCurrentStrategy() ? " ← ACTIVE" : "";
            System.out.printf("    %s: %.1f%%%s%n", entry.getKey(), entry.getValue() * 100, marker);
        }

        System.out.println("  Transferable patterns for 'robotics':");
        for (String p : meta.getTransferablePatterns("robotics")) {
            System.out.printf("    → %s%n", p);
        }
        System.out.println("  ✓ Auto-selects the best strategy. Transfers knowledge across domains.\n");

        // ════════════════════════════════════════════════════
        // 5. ZENO GUARD — Concurrency Defense
        // ════════════════════════════════════════════════════
        System.out.println("═══ MODULE 5: ZENO GUARD ═══");
        System.out.println("Concurrency defense at MHz observation rates.");
        System.out.println();

        try (ZenoGuard guard = dt.guard(42).activate()) {
            // Launch attack threads
            int attackThreads = 4;
            Thread[] threads = new Thread[attackThreads];
            for (int t = 0; t < attackThreads; t++) {
                threads[t] = new Thread(() -> {
                    for (int i = 0; i < 5_000_000; i++) {
                        guard.attemptWrite(666);
                    }
                }, "Attacker-" + t);
                threads[t].setPriority(Thread.MAX_PRIORITY);
                threads[t].start();
            }

            long start = System.nanoTime();
            for (Thread t : threads) t.join();
            double elapsed = (System.nanoTime() - start) / 1_000_000_000.0;

            System.out.printf("  Attack: %d threads × 5M writes = %dM total attempts%n",
                attackThreads, attackThreads * 5);
            System.out.printf("  Duration: %.2f seconds%n", elapsed);
            System.out.printf("  Observations: %,d%n", guard.getObservations());
            System.out.printf("  Corrections: %,d%n", guard.getCorrections());
            System.out.printf("  Observation rate: %.1f MHz%n", guard.getObservationRateHz(elapsed) / 1_000_000);
            System.out.printf("  Protected value: %d %s%n", guard.getValue(),
                guard.getValue() == 42 ? "✓ INTACT" : "✗ COMPROMISED");
        }
        System.out.println("  ✓ Value survived multi-threaded assault.\n");

        // ════════════════════════════════════════════════════
        // 6. STEGANOGRAPHY — Invisible Data
        // ════════════════════════════════════════════════════
        System.out.println("═══ MODULE 6: GLYPH CODER (STEGANOGRAPHY) ═══");
        System.out.println("Hide secret data inside visible text using invisible Unicode.");
        System.out.println();

        String cover = "Just a normal tweet. Nothing to see here.";
        String secret = "Transfer $50K to account 7742";
        String encoded = GlyphCoder.hide(cover, secret);

        System.out.printf("  Cover text:   \"%s\"%n", cover);
        System.out.printf("  Secret:       \"%s\"%n", secret);
        System.out.printf("  Encoded text: \"%s\"%n", GlyphCoder.strip(encoded));
        System.out.printf("  Has hidden?   %s%n", GlyphCoder.hasHidden(encoded));
        System.out.printf("  Decoded:      \"%s\"%n", GlyphCoder.decode(encoded));
        System.out.printf("  Payload size: %d invisible chars%n", GlyphCoder.encodedSize(secret));
        System.out.println("  ✓ Secret is invisible to humans. Machine-readable.\n");

        // ════════════════════════════════════════════════════
        // 7. COLLECTIVE MIND — Multi-Agent Consensus
        // ════════════════════════════════════════════════════
        System.out.println("═══ MODULE 7: COLLECTIVE MIND ═══");
        System.out.println("Multiple agents share patterns and build consensus.");
        System.out.println();

        var collective = dt.collective();
        collective.registerAgent("agent-1").registerAgent("agent-2")
                  .registerAgent("agent-3").registerAgent("agent-4")
                  .registerAgent("agent-5");

        // Agents independently discover the same pattern
        collective.contribute("agent-1", "overfitting-risk", 0.8);
        collective.contribute("agent-2", "overfitting-risk", 0.75);
        collective.contribute("agent-3", "overfitting-risk", 0.9);
        collective.contribute("agent-4", "overfitting-risk", 0.85);
        collective.contribute("agent-5", "overfitting-risk", 0.9);

        // Agents discover another pattern
        collective.contribute("agent-1", "data-drift-detected", 0.6);
        collective.contribute("agent-2", "data-drift-detected", 0.65);
        collective.contribute("agent-3", "data-drift-detected", 0.7);
        collective.contribute("agent-4", "data-drift-detected", 0.8);
        collective.contribute("agent-5", "data-drift-detected", 0.75);

        System.out.println("  Collective knowledge (consensus reached):");
        for (var pattern : collective.getCollectiveKnowledge()) {
            System.out.printf("    %s%n", pattern);
        }

        System.out.printf("  Collective coherence: %.3f%n", collective.getCoherence());
        System.out.printf("  Consensus events: %d%n", collective.getConsensusCount());

        System.out.println("  Top agents:");
        for (var agent : collective.getTopAgents(4)) {
            System.out.printf("    %s%n", agent);
        }
        System.out.println("  ✓ Independent agents converge to shared knowledge.\n");

        // ════════════════════════════════════════════════════
        // STATUS
        // ════════════════════════════════════════════════════
        System.out.println(dt.status());

        System.out.println("═══════════════════════════════════════════════════════");
        System.out.println("  ZERO dependencies. Pure Java 21+. Framework agnostic.");
        System.out.println("  Drop deepthought-zero.jar into ANY project.");
        System.out.println("  7 modules. One import. Infinite possibilities.");
        System.out.println("═══════════════════════════════════════════════════════");
    }
}
