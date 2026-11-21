package com.shadow.consentchat.screen;

import com.shadow.consentchat.Config;
import com.shadow.consentchat.Mode;
import com.shadow.consentchat.PrivacyManager;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.network.chat.Component;

/**
 * Additive, first-time-per-server disclosure. This does not replace or hide
 * any Minecraft dialog - it is an extra consent screen shown before chat use.
 */
public final class DisclosureScreen extends Screen {
    private final String server;

    public DisclosureScreen(Screen previous, String server) {
        super(Component.literal("Chat privacy on " + server));
        this.server = server;
    }

    @Override
    protected void init() {
        int cx = this.width / 2;
        Mode mode = PrivacyManager.effectiveMode();

        addRenderableWidget(Button.builder(
                        Component.literal("Stay private (keep " + mode.displayName() + ")"),
                        b -> accept(Mode.PUBLIC == mode ? Mode.SILENT : mode))
                .bounds(cx - 150, this.height / 2 + 40, 300, 20).build());

        addRenderableWidget(Button.builder(
                        Component.literal("Use public, reportable chat on this server"),
                        b -> accept(Mode.PUBLIC))
                .bounds(cx - 150, this.height / 2 + 66, 300, 20).build());
    }

    private void accept(Mode mode) {
        Config config = Config.get();
        config.acknowledged.add(server);
        config.setModeFor(server, mode);
        PrivacyManager.apply();
        this.minecraft.gui.setScreen(null);
    }

    @Override
    public void extractRenderState(GuiGraphicsExtractor extractor, int mouseX, int mouseY, float delta) {
        this.extractBackground(extractor, mouseX, mouseY, delta);
        int cx = this.width / 2;
        int y = this.height / 2 - 70;

        extractor.text(this.getFont(), Component.literal("Chat privacy on " + server), cx - 140, y, 0xFFFFFF);
        y += 20;
        String[] lines = {
                "This server uses the privacy scope: " + PrivacyManager.effectiveMode().displayName() + ".",
                PrivacyManager.describe(PrivacyManager.effectiveMode()),
                "",
                "ConsentChat does not change signatures or hide Mojang's warnings.",
                "Choosing public chat restores vanilla behaviour exactly.",
                "Your choice is stored only in config/consentchat.json."
        };
        for (String line : lines) {
            extractor.text(this.getFont(), Component.literal(line), cx - 210, y, 0xCCCCCC);
            y += 14;
        }

        super.extractRenderState(extractor, mouseX, mouseY, delta);
    }
}
