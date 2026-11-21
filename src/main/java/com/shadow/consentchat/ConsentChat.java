package com.shadow.consentchat;

import com.mojang.blaze3d.platform.InputConstants;
import com.shadow.consentchat.screen.ConsentScreen;
import com.shadow.consentchat.screen.DisclosureScreen;
import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents;
import net.fabricmc.fabric.api.client.keymapping.v1.KeyMappingHelper;
import net.fabricmc.fabric.api.client.networking.v1.ClientPlayConnectionEvents;
import net.minecraft.client.KeyMapping;
import net.minecraft.client.Minecraft;
import net.minecraft.resources.Identifier;

/**
 * Client-side entrypoint.
 *
 * <p>Design constraints (EULA + US privacy law):</p>
 * <ul>
 *   <li>No mixin into Mojang's chat/signature pipeline.</li>
 *   <li>No hiding or altering of vanilla dialogs, warnings or errors.</li>
 *   <li>No telemetry, analytics, accounts or network calls of any kind.</li>
 *   <li>High-privacy defaults, with per-server informed consent.</li>
 * </ul>
 */
public final class ConsentChat implements ClientModInitializer {
    private static final KeyMapping.Category CATEGORY =
            KeyMapping.Category.register(Identifier.fromNamespaceAndPath("consentchat", "general"));

    public static final KeyMapping OPEN_SCREEN =
            new KeyMapping("key.consentchat.open", InputConstants.KEY_O, CATEGORY);

    private static boolean pendingDisclosure;

    @Override
    public void onInitializeClient() {
        KeyMappingHelper.registerKeyMapping(OPEN_SCREEN);

        ClientTickEvents.END_CLIENT_TICK.register(client -> {
            // Keep the chosen mode effective even if another settings screen changes it.
            if (client.level != null && PrivacyManager.needsEnforcement()) {
                PrivacyManager.apply();
            }

            // Only open our own UI when no Mojang screen is active. This preserves
            // vanilla dialogs, warnings and errors exactly as Mojang shipped them.
            if (pendingDisclosure && client.gui.screen() == null) {
                pendingDisclosure = false;
                client.gui.setScreen(new DisclosureScreen(null, PrivacyManager.currentServerKey()));
                return;
            }

            if (OPEN_SCREEN.consumeClick() && client.gui.screen() == null) {
                client.gui.setScreen(new ConsentScreen(null));
            }
        });

        ClientPlayConnectionEvents.JOIN.register((handler, sender, client) -> {
            PrivacyManager.apply();

            String server = PrivacyManager.currentServerKey();
            if (server.isBlank()
                    || PrivacyManager.effectiveMode() == Mode.PUBLIC
                    || Config.get().acknowledged.contains(server)) {
                return;
            }

            // Additive, per-server consent. If a vanilla screen is already open,
            // queue ours; never replace or hide Mojang's dialog.
            if (client.gui.screen() == null) {
                client.gui.setScreen(new DisclosureScreen(null, server));
            } else {
                pendingDisclosure = true;
            }
        });

        ClientPlayConnectionEvents.DISCONNECT.register((handler, client) -> {
            pendingDisclosure = false;
            PrivacyManager.restore();
        });
    }
}
