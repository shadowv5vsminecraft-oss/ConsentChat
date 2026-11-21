package com.shadow.consentchat;

import net.minecraft.client.Minecraft;
import net.minecraft.client.Options;
import net.minecraft.client.multiplayer.ServerData;
import net.minecraft.world.entity.player.ChatVisiblity;

/**
 * Applies the chosen privacy scope through vanilla options only.
 *
 * <p>There is deliberately no packet interception, no signature stripping and
 * no mixin into Mojang's chat pipeline. The original option values are saved
 * on first apply and restored on disconnect so this mod never permanently
 * changes a player's settings.</p>
 */
public final class PrivacyManager {
    private static boolean applied = false;
    private static ChatVisiblity originalVisibility;
    private static boolean originalOnlyShowSecureChat;

    private PrivacyManager() {
    }

    /** Server address, or an empty string when in singleplayer/LAN. */
    public static String currentServerKey() {
        Minecraft client = Minecraft.getInstance();
        ServerData entry = client.getCurrentServer();
        return entry == null ? "" : entry.ip;
    }

    public static Mode effectiveMode() {
        String key = currentServerKey();
        // Singleplayer and LAN have no Mojang chat reporting, so do not touch anything.
        if (key.isBlank()) {
            return Mode.PUBLIC;
        }
        return Config.get().modeFor(key);
    }

    public static void apply() {
        Minecraft client = Minecraft.getInstance();
        Options options = client.options;

        if (!applied) {
            originalVisibility = options.chatVisibility().get();
            originalOnlyShowSecureChat = options.onlyShowSecureChat().get();
            applied = true;
        }

        switch (effectiveMode()) {
            case SILENT -> {
                // "Commands Only": the player can still run commands (including
                // a server's /chat command) but sends no chat messages at all.
                options.chatVisibility().set(ChatVisiblity.SYSTEM);
                options.onlyShowSecureChat().set(true);
            }
            case TRUSTED -> {
                options.chatVisibility().set(ChatVisiblity.FULL);
                options.onlyShowSecureChat().set(true);
            }
            case PUBLIC -> {
                restore();
                return;
            }
        }

        // This is the same vanilla client-information sync the Options screen uses.
        options.broadcastOptions();
    }

    public static void restore() {
        if (!applied) {
            return;
        }
        Options options = Minecraft.getInstance().options;
        options.chatVisibility().set(originalVisibility);
        options.onlyShowSecureChat().set(originalOnlyShowSecureChat);
        options.broadcastOptions();
        applied = false;
    }

    /** True when a non-public mode is active but its vanilla settings drifted. */
    public static boolean needsEnforcement() {
        if (!applied) {
            return false;
        }
        Options options = Minecraft.getInstance().options;
        return switch (effectiveMode()) {
            case SILENT -> options.chatVisibility().get() != ChatVisiblity.SYSTEM
                    || !options.onlyShowSecureChat().get();
            case TRUSTED -> options.chatVisibility().get() != ChatVisiblity.FULL
                    || !options.onlyShowSecureChat().get();
            case PUBLIC -> false;
        };
    }

    public static String describe(Mode mode) {
        return switch (mode) {
            case PUBLIC -> "Vanilla chat. Messages are signed and can be reported to Mojang.";
            case TRUSTED -> "Only chats from trusted players are shown. Messages are still signed and reportable.";
            case SILENT -> "Commands Only. No ordinary chat messages are sent, so there is no chat message to report. Commands still use vanilla handling.";
        };
    }
}
