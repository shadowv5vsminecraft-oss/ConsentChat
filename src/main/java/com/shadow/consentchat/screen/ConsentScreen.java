package com.shadow.consentchat.screen;

import com.shadow.consentchat.Config;
import com.shadow.consentchat.Mode;
import com.shadow.consentchat.PrivacyManager;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.network.chat.Component;

/** Local privacy dashboard. Never contacts a server or a developer endpoint. */
public final class ConsentScreen extends Screen {
    private boolean showNotice;

    public ConsentScreen(Screen previous) {
        super(Component.literal("ConsentChat - Privacy Scope"));
    }

    @Override
    protected void init() {
        int cx = this.width / 2;
        int top = 96;
        Mode current = PrivacyManager.effectiveMode();
        boolean locked = Config.get().isLocked();

        addRenderableWidget(Button.builder(
                        Component.literal("Public - vanilla, signed, reportable" + marker(current, Mode.PUBLIC)),
                        b -> choose(Mode.PUBLIC))
                .bounds(cx - 150, top, 300, 20).build());

        addRenderableWidget(Button.builder(
                        Component.literal("Trusted - show only trusted chats" + marker(current, Mode.TRUSTED)),
                        b -> choose(Mode.TRUSTED))
                .bounds(cx - 150, top + 26, 300, 20).build());

        addRenderableWidget(Button.builder(
                        Component.literal("Silent - Commands Only, no chat to report" + marker(current, Mode.SILENT)),
                        b -> choose(Mode.SILENT))
                .bounds(cx - 150, top + 52, 300, 20).build());

        addRenderableWidget(Button.builder(
                        Component.literal(locked ? "Parent controls: LOCKED" : "Parent controls"),
                        b -> this.minecraft.gui.setScreen(new PinScreen(this)))
                .bounds(cx - 150, top + 90, 145, 20).build());

        addRenderableWidget(Button.builder(
                        Component.literal(showNotice ? "Hide privacy notice" : "Privacy notice"),
                        b -> {
                            showNotice = !showNotice;
                            rebuildWidgets();
                        })
                .bounds(cx + 5, top + 90, 145, 20).build());

        addRenderableWidget(Button.builder(
                        Component.literal("Done"),
                        b -> this.minecraft.gui.setScreen(null))
                .bounds(cx - 60, this.height - 32, 120, 20).build());
    }

    private void choose(Mode mode) {
        Config config = Config.get();
        if (config.isLocked()) {
            this.minecraft.gui.setScreen(new PinScreen(this));
            return;
        }
        config.setModeFor(PrivacyManager.currentServerKey(), mode);
        PrivacyManager.apply();
        rebuildWidgets();
    }

    private static String marker(Mode current, Mode candidate) {
        return current == candidate ? "  <" : "";
    }

    @Override
    public void extractRenderState(GuiGraphicsExtractor extractor, int mouseX, int mouseY, float delta) {
        this.extractBackground(extractor, mouseX, mouseY, delta);
        int cx = this.width / 2;

        extractor.text(this.getFont(), Component.literal("ConsentChat - Privacy Scope"), cx - 100, 24, 0xFFFFFF);

        String server = PrivacyManager.currentServerKey();
        String scopeLine = server.isBlank()
                ? "Scope: default for all servers (singleplayer/LAN is unaffected)"
                : "Scope for " + server + ": " + PrivacyManager.effectiveMode().displayName();
        extractor.text(this.getFont(), Component.literal(scopeLine), cx - 180, 50, 0xAAAAAA);

        extractor.text(this.getFont(), Component.literal(PrivacyManager.describe(PrivacyManager.effectiveMode())),
                cx - 180, 68, 0xAAAAAA);

        if (Config.get().isLocked()) {
            extractor.text(this.getFont(), Component.literal("Settings locked by parent controls."),
                    cx - 180, 80, 0xFFAA55);
        }

        if (showNotice) {
            int y = 150;
            String[] lines = {
                    "ConsentChat collects nothing: no telemetry, no analytics, no accounts, no chat logs.",
                    "All preferences stay in config/consentchat.json on this computer.",
                    "It does not strip signatures, spoof packets, or hide any Mojang warning.",
                    "Silent mode simply uses vanilla 'Commands Only', so no chat message is sent.",
                    "On servers running the companion Paper plugin, /chat sends an unsigned",
                    "server message that players cannot report to Mojang.",
                    "Everyone starts in Silent mode; a parent can lock these settings."
            };
            for (String line : lines) {
                extractor.text(this.getFont(), Component.literal(line), cx - 210, y, 0xCCCCCC);
                y += 14;
            }
        }

        super.extractRenderState(extractor, mouseX, mouseY, delta);
    }
}
