package com.shadow.consentchat;

import java.util.Locale;

/**
 * The privacy scope the player has chosen for a given server.
 *
 * <p>None of these modes modify or strip Mojang's chat signatures. They only
 * drive vanilla, player-facing chat settings, so Minecraft's own warnings and
 * dialogs stay exactly as Mojang shipped them.</p>
 */
public enum Mode {
    /** Vanilla signed chat. Fully reportable, exactly like an unmodded client. */
    PUBLIC,
    /** Vanilla "Only show trusted chats" plus full chat visibility. */
    TRUSTED,
    /** Vanilla "Commands Only" chat visibility: no chat messages are sent, so none can be signed or reported. */
    SILENT;

    public String displayName() {
        return name().charAt(0) + name().substring(1).toLowerCase(Locale.ROOT);
    }
}
