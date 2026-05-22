package io.fraymus.deepthought.organism;

import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.function.Consumer;

/**
 * NODE REPLICATION — Multi-Node TCP State Sync
 * 
 * Enables an organism to replicate its state to other nodes
 * on the network via simple TCP sockets. One node runs as
 * server (primary), others connect as replicas.
 * 
 * Protocol: newline-delimited JSON state snapshots.
 * 
 * @since 1.0.0
 */
public final class NodeReplication implements AutoCloseable {

    private final AtomicBoolean running = new AtomicBoolean(false);
    private ServerSocket serverSocket;
    private Socket clientSocket;
    private Thread serverThread;
    private Thread clientThread;
    private int port;

    // Metrics
    private long statesSent = 0;
    private long statesReceived = 0;
    private String mode = "OFFLINE";
    private String peerAddress = "none";

    // Callbacks
    private Consumer<String> onStateReceived;

    /**
     * Start as PRIMARY node — accept connections and broadcast state.
     */
    public NodeReplication startServer(int port) throws IOException {
        this.port = port;
        this.mode = "PRIMARY";
        this.running.set(true);

        serverSocket = new ServerSocket(port);
        serverSocket.setSoTimeout(1000); // 1s accept timeout for clean shutdown

        serverThread = new Thread(() -> {
            System.out.printf("  📡 NODE REPLICATION: Primary listening on port %d%n", port);
            while (running.get()) {
                try {
                    Socket client = serverSocket.accept();
                    peerAddress = client.getRemoteSocketAddress().toString();
                    System.out.printf("  📡 REPLICA CONNECTED: %s%n", peerAddress);

                    // Handle in separate thread
                    Thread handler = new Thread(() -> handleClient(client), "Node-Handler");
                    handler.setDaemon(true);
                    handler.start();
                } catch (SocketTimeoutException ignored) {
                    // Normal timeout, check running flag
                } catch (IOException e) {
                    if (running.get()) {
                        System.err.println("  📡 Server error: " + e.getMessage());
                    }
                }
            }
        }, "Node-Server");
        serverThread.setDaemon(true);
        serverThread.start();

        return this;
    }

    /**
     * Start as REPLICA node — connect to primary and receive state.
     */
    public NodeReplication connectToNode(String host, int port) throws IOException {
        this.port = port;
        this.mode = "REPLICA";
        this.running.set(true);

        clientSocket = new Socket(host, port);
        peerAddress = host + ":" + port;

        clientThread = new Thread(() -> {
            System.out.printf("  📡 CONNECTED TO PRIMARY: %s:%d%n", host, port);
            try (BufferedReader reader = new BufferedReader(
                    new InputStreamReader(clientSocket.getInputStream(), StandardCharsets.UTF_8))) {
                String line;
                while (running.get() && (line = reader.readLine()) != null) {
                    statesReceived++;
                    if (onStateReceived != null) {
                        onStateReceived.accept(line);
                    }
                }
            } catch (IOException e) {
                if (running.get()) {
                    System.err.println("  📡 Lost connection to primary: " + e.getMessage());
                }
            }
        }, "Node-Replica");
        clientThread.setDaemon(true);
        clientThread.start();

        return this;
    }

    /**
     * Broadcast state to all connected replicas (called from primary).
     */
    public void broadcastState(String stateJson) {
        if (!"PRIMARY".equals(mode)) return;
        // State is sent via handleClient's output streams
        synchronized (this) {
            lastBroadcast = stateJson;
            statesSent++;
        }
    }

    private volatile String lastBroadcast = null;

    private void handleClient(Socket client) {
        try (PrintWriter writer = new PrintWriter(
                new OutputStreamWriter(client.getOutputStream(), StandardCharsets.UTF_8), true);
             BufferedReader reader = new BufferedReader(
                new InputStreamReader(client.getInputStream(), StandardCharsets.UTF_8))) {

            String lastSent = null;
            while (running.get() && !client.isClosed()) {
                String current = lastBroadcast;
                if (current != null && !current.equals(lastSent)) {
                    writer.println(current);
                    lastSent = current;
                }

                // Check for incoming data from replica
                if (reader.ready()) {
                    String incoming = reader.readLine();
                    if (incoming != null) {
                        statesReceived++;
                        if (onStateReceived != null) onStateReceived.accept(incoming);
                    }
                }

                try { Thread.sleep(100); } catch (InterruptedException e) { break; }
            }
        } catch (IOException e) {
            if (running.get()) {
                System.err.println("  📡 Client handler error: " + e.getMessage());
            }
        }
    }

    /**
     * Send state to the primary (called from replica).
     */
    public void sendState(String stateJson) {
        if (!"REPLICA".equals(mode) || clientSocket == null) return;
        try {
            PrintWriter writer = new PrintWriter(
                new OutputStreamWriter(clientSocket.getOutputStream(), StandardCharsets.UTF_8), true);
            writer.println(stateJson);
            statesSent++;
        } catch (IOException e) {
            System.err.println("  📡 Failed to send state: " + e.getMessage());
        }
    }

    // Configuration
    public NodeReplication onStateReceived(Consumer<String> cb) { this.onStateReceived = cb; return this; }

    // Metrics
    public String getMode() { return mode; }
    public String getPeerAddress() { return peerAddress; }
    public long getStatesSent() { return statesSent; }
    public long getStatesReceived() { return statesReceived; }
    public boolean isRunning() { return running.get(); }

    @Override
    public void close() {
        running.set(false);
        try { if (serverSocket != null) serverSocket.close(); } catch (IOException ignored) {}
        try { if (clientSocket != null) clientSocket.close(); } catch (IOException ignored) {}
    }
}
