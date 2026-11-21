package com.shadow.consentchat;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import net.fabricmc.loader.api.FabricLoader;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

/**
 * Local-only configuration. Nothing here is ever sent over the network.
 *
 * <p>The file lives at {@code config/consentchat.json}. It contains only
 * preferences and a salted PIN hash for optional parent controls - no account
 * identifiers, no chat logs, no telemetry.</p>
 */
public final class Config {
    private static final Gson GSON = new GsonBuilder().setPrettyPrinting().create();
    private static final Path FILE = FabricLoader.getInstance().getConfigDir().resolve("consentchat.json");

    /** High-privacy default, as required by age-appropriate design codes. */
    public Mode defaultMode = Mode.SILENT;
    /** Per-server overrides, keyed by the server address shown in the multiplayer list. */
    public Map<String, Mode> servers = new HashMap<>();
    /** Servers where the disclosure screen has already been accepted. */
    public Set<String> acknowledged = new HashSet<>();

    /** Optional parent lock. When true, mode changes in-game require the PIN. */
    public boolean parentLock = false;
    public String pinSalt = "";
    public String pinHash = "";

    private transient boolean unlockedThisSession = false;

    private static Config instance;

    public static Config get() {
        if (instance == null) {
            instance = load();
        }
        return instance;
    }

    private static Config load() {
        if (!Files.exists(FILE)) {
            Config fresh = new Config();
            fresh.save();
            return fresh;
        }
        try {
            String json = Files.readString(FILE, StandardCharsets.UTF_8);
            Config parsed = GSON.fromJson(json, Config.class);
            if (parsed == null) {
                return new Config();
            }
            if (parsed.servers == null) parsed.servers = new HashMap<>();
            if (parsed.acknowledged == null) parsed.acknowledged = new HashSet<>();
            if (parsed.defaultMode == null) parsed.defaultMode = Mode.SILENT;
            return parsed;
        } catch (IOException | RuntimeException e) {
            return new Config();
        }
    }

    public void save() {
        try {
            Files.createDirectories(FILE.getParent());
            Files.writeString(FILE, GSON.toJson(this), StandardCharsets.UTF_8);
        } catch (IOException ignored) {
            // A failed save only means preferences are not persisted; no data leaves the machine.
        }
    }

    public Mode modeFor(String server) {
        if (server == null || server.isBlank()) {
            return defaultMode;
        }
        return servers.getOrDefault(server, defaultMode);
    }

    public void setModeFor(String server, Mode mode) {
        if (server == null || server.isBlank()) {
            defaultMode = mode;
        } else {
            servers.put(server, mode);
        }
        save();
    }

    public boolean isLocked() {
        return parentLock && !unlockedThisSession;
    }

    public boolean hasPin() {
        return pinSalt != null && !pinSalt.isBlank() && pinHash != null && !pinHash.isBlank();
    }

    public boolean setPin(String pin) {
        if (pin == null || pin.length() < 4) {
            return false;
        }
        byte[] salt = new byte[16];
        new SecureRandom().nextBytes(salt);
        pinSalt = hex(salt);
        pinHash = hash(pinSalt, pin);
        parentLock = true;
        unlockedThisSession = true;
        save();
        return true;
    }

    public boolean checkPin(String pin) {
        return hasPin() && hash(pinSalt, pin).equals(pinHash);
    }

    public void unlockSession() {
        unlockedThisSession = true;
    }

    private static String hash(String salt, String pin) {
        try {
            MessageDigest md = MessageDigest.getInstance("SHA-256");
            byte[] out = md.digest((salt + pin).getBytes(StandardCharsets.UTF_8));
            return hex(out);
        } catch (NoSuchAlgorithmException e) {
            throw new IllegalStateException(e);
        }
    }

    private static String hex(byte[] bytes) {
        StringBuilder sb = new StringBuilder(bytes.length * 2);
        for (byte b : bytes) {
            sb.append(String.format("%02x", b & 0xFF));
        }
        return sb.toString();
    }
}
