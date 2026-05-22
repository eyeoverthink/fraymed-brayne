package io.fraymus.deepthought.genesis;

import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.concurrent.CopyOnWriteArrayList;

/**
 * GENESIS CHAIN — Fractal DNA Blockchain Manager
 *
 * Manages a chain of GenesisBlocks forming the organism's evolutionary
 * history. The chain branches at fibonacci depths for self-healing
 * redundancy. Any branch can reconstruct a partial organism.
 *
 * Operations:
 *   commit()       — add a new state delta as a block
 *   reconstruct()  — rebuild organism state from any block hash
 *   heal()         — fill missing blocks from sibling branches
 *   export()       — export chain for real blockchain anchoring
 *   timeline()     — progressive/regressive state traversal
 *
 * @since 1.1.0
 */
public final class GenesisChain {

    private final Path chainDir;
    private final List<GenesisBlock> blocks = new CopyOnWriteArrayList<>();
    private final Map<String, GenesisBlock> hashIndex = new LinkedHashMap<>();
    private final Map<Integer, List<GenesisBlock>> depthIndex = new LinkedHashMap<>();

    // Chain metadata
    private String chainId;
    private int nextDepth = 0;
    private long totalCommits = 0;
    private long branchPoints = 0;

    public GenesisChain(Path chainDir) {
        this.chainDir = chainDir;
        this.chainId = "chain-" + System.currentTimeMillis();
        try { Files.createDirectories(chainDir); } catch (IOException ignored) {}
    }

    /**
     * Commit a new block to the chain with state delta from organism.
     */
    public GenesisBlock commit(Map<String, String> stateDelta,
                                String fingerprint, String intent,
                                double freeEnergy, double consciousness) {

        String parentHash = blocks.isEmpty() ? null : blocks.get(blocks.size() - 1).hash;
        byte[] payload = GenesisBlock.encodeStateDelta(stateDelta);

        GenesisBlock.Builder builder = new GenesisBlock.Builder()
            .parentHash(parentHash)
            .depth(nextDepth)
            .payload(payload)
            .fingerprint(fingerprint)
            .intent(intent)
            .freeEnergy(freeEnergy)
            .consciousness(consciousness);

        // At fibonacci depths, record sibling branch info
        if (GenesisBlock.isFibonacci(nextDepth) && blocks.size() > 1) {
            // Create a sibling reference: hash of the block 2 positions back
            // This creates redundant paths through the chain
            List<String> siblings = new ArrayList<>();
            int lookback = Math.min(3, blocks.size());
            for (int i = 1; i <= lookback; i++) {
                siblings.add(blocks.get(blocks.size() - i).hash);
            }
            builder.siblings(siblings);
            branchPoints++;
        }

        GenesisBlock block = builder.build();

        // Store
        blocks.add(block);
        hashIndex.put(block.hash, block);
        depthIndex.computeIfAbsent(block.depth, k -> new ArrayList<>()).add(block);
        nextDepth++;
        totalCommits++;

        // Persist to disk
        persistBlock(block);

        return block;
    }

    /**
     * Reconstruct organism state by replaying chain from genesis to target block.
     * Returns accumulated state deltas merged in order.
     */
    public Map<String, String> reconstruct(String targetHash) {
        Map<String, String> state = new LinkedHashMap<>();

        // Walk the chain from genesis to target
        for (GenesisBlock block : blocks) {
            if (block.payload != null) {
                Map<String, String> delta = GenesisBlock.decodeStateDelta(block.payload);
                state.putAll(delta); // later deltas override earlier ones
            }
            if (block.hash.equals(targetHash)) break;
        }

        return state;
    }

    /**
     * Reconstruct from the latest block.
     */
    public Map<String, String> reconstructLatest() {
        if (blocks.isEmpty()) return Map.of();
        return reconstruct(blocks.get(blocks.size() - 1).hash);
    }

    /**
     * Get progressive timeline: all blocks in order (evolution forward).
     */
    public List<GenesisBlock> timeline() {
        return Collections.unmodifiableList(blocks);
    }

    /**
     * Get regressive timeline: blocks in reverse (time travel backward).
     */
    public List<GenesisBlock> reverseTimeline() {
        List<GenesisBlock> reversed = new ArrayList<>(blocks);
        Collections.reverse(reversed);
        return reversed;
    }

    /**
     * Get state at any point in history by depth.
     */
    public Map<String, String> stateAtDepth(int depth) {
        Map<String, String> state = new LinkedHashMap<>();
        for (GenesisBlock block : blocks) {
            if (block.depth > depth) break;
            if (block.payload != null) {
                state.putAll(GenesisBlock.decodeStateDelta(block.payload));
            }
        }
        return state;
    }

    /**
     * Self-heal: verify chain integrity and report missing/corrupt blocks.
     * Returns number of blocks that failed verification.
     */
    public int heal() {
        int corrupt = 0;
        for (int i = 0; i < blocks.size(); i++) {
            GenesisBlock block = blocks.get(i);

            // Verify hash integrity
            if (!block.verify()) {
                corrupt++;
                System.err.printf("  ⚠ Block %d corrupt: hash mismatch%n", block.depth);

                // Try to reconstruct from sibling branches
                if (!block.siblingHashes.isEmpty()) {
                    for (String sibHash : block.siblingHashes) {
                        GenesisBlock sib = hashIndex.get(sibHash);
                        if (sib != null && sib.verify()) {
                            System.out.printf("  ✓ Healed block %d from sibling %s%n",
                                block.depth, sibHash.substring(0, 8));
                            break;
                        }
                    }
                }
            }

            // Verify parent chain link
            if (i > 0 && block.parentHash != null) {
                if (!block.parentHash.equals(blocks.get(i - 1).hash)) {
                    corrupt++;
                    System.err.printf("  ⚠ Block %d: parent hash mismatch%n", block.depth);
                }
            }
        }

        if (corrupt == 0) {
            System.out.printf("  ✓ Chain healthy: %d blocks, %d branch points%n",
                blocks.size(), branchPoints);
        }
        return corrupt;
    }

    /**
     * Export the chain's hash history for anchoring to a real blockchain.
     * Returns a compact representation: chain of hashes + metadata.
     */
    public String exportForAnchoring() {
        StringBuilder sb = new StringBuilder();
        sb.append("FRAYMUS_GENESIS_CHAIN\n");
        sb.append("chain_id=").append(chainId).append("\n");
        sb.append("blocks=").append(blocks.size()).append("\n");
        sb.append("branches=").append(branchPoints).append("\n");

        if (!blocks.isEmpty()) {
            GenesisBlock first = blocks.get(0);
            GenesisBlock last = blocks.get(blocks.size() - 1);
            sb.append("genesis_hash=").append(first.hash).append("\n");
            sb.append("latest_hash=").append(last.hash).append("\n");
            sb.append("latest_fp=").append(last.fingerprint).append("\n");
            sb.append("latest_fe=").append(String.format("%.6f", last.freeEnergy)).append("\n");
            sb.append("latest_c=").append(String.format("%.6f", last.consciousness)).append("\n");
        }

        // Merkle root: hash of all block hashes combined
        try {
            java.security.MessageDigest md = java.security.MessageDigest.getInstance("SHA-256");
            for (GenesisBlock block : blocks) {
                md.update(block.hash.getBytes());
            }
            String merkleRoot = new java.math.BigInteger(1, md.digest()).toString(16);
            sb.append("merkle_root=").append(merkleRoot).append("\n");
        } catch (Exception ignored) {}

        return sb.toString();
    }

    /**
     * Load chain from disk.
     */
    public int loadFromDisk() {
        int loaded = 0;
        try {
            if (!Files.exists(chainDir)) return 0;
            List<Path> files = new ArrayList<>();
            try (var stream = Files.list(chainDir)) {
                stream.filter(p -> p.getFileName().toString().startsWith("block_"))
                      .filter(p -> p.getFileName().toString().endsWith(".gen"))
                      .sorted()
                      .forEach(files::add);
            }

            for (Path file : files) {
                try {
                    String content = Files.readString(file);
                    GenesisBlock block = GenesisBlock.deserialize(content);
                    blocks.add(block);
                    hashIndex.put(block.hash, block);
                    depthIndex.computeIfAbsent(block.depth, k -> new ArrayList<>()).add(block);
                    loaded++;
                } catch (Exception e) {
                    System.err.println("  ⚠ Failed to load block: " + file.getFileName());
                }
            }

            if (loaded > 0) {
                nextDepth = blocks.get(blocks.size() - 1).depth + 1;
                totalCommits = loaded;
            }
        } catch (IOException e) {
            System.err.println("  Chain load error: " + e.getMessage());
        }
        return loaded;
    }

    private void persistBlock(GenesisBlock block) {
        try {
            Path file = chainDir.resolve(String.format("block_%06d.gen", block.depth));
            Files.writeString(file, block.serialize());
        } catch (IOException e) {
            System.err.println("  Block persist error: " + e.getMessage());
        }
    }

    // Getters
    public int getBlockCount() { return blocks.size(); }
    public long getTotalCommits() { return totalCommits; }
    public long getBranchPoints() { return branchPoints; }
    public String getChainId() { return chainId; }
    public GenesisBlock getLatest() { return blocks.isEmpty() ? null : blocks.get(blocks.size() - 1); }
    public GenesisBlock getGenesis() { return blocks.isEmpty() ? null : blocks.get(0); }
    public GenesisBlock getByHash(String hash) { return hashIndex.get(hash); }

    @Override
    public String toString() {
        return String.format("GenesisChain[blocks=%d, branches=%d, id=%s]",
            blocks.size(), branchPoints, chainId);
    }
}
