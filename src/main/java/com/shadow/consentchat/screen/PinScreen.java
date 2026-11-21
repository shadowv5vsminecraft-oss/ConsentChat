package com.shadow.consentchat.screen;

import com.shadow.consentchat.Config;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.components.EditBox;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.network.chat.Component;

/** Local parent-control gate. The PIN is hashed with a random salt and never leaves the machine. */
public final class PinScreen extends Screen {
    private final Screen previous;
    private EditBox pinField;
    private String message = "";

    public PinScreen(Screen previous) {
        super(Component.literal("Parent controls"));
        this.previous = previous;
    }

    @Override
    protected void init() {
        int cx = this.width / 2;
        int y = this.height / 2 - 20;

        pinField = new EditBox(this.font, cx - 80, y, 160, 20, Component.literal("PIN"));
        pinField.setMaxLength(32);
        pinField.setHint(Component.literal("4+ digits"));
        addRenderableWidget(pinField);
        setInitialFocus(pinField);

        String action = Config.get().hasPin() ? "Unlock" : "Set PIN and lock";
        addRenderableWidget(Button.builder(Component.literal(action), b -> submit())
                .bounds(cx - 80, y + 28, 160, 20).build());

        addRenderableWidget(Button.builder(Component.literal("Back"), b -> this.minecraft.gui.setScreen(previous))
                .bounds(cx - 80, y + 54, 160, 20).build());
    }

    private void submit() {
        Config config = Config.get();
        String value = pinField.getValue().trim();
        if (!config.hasPin()) {
            if (config.setPin(value)) {
                message = "Parent controls enabled.";
            } else {
                message = "PIN must be at least 4 characters.";
            }
        } else if (config.checkPin(value)) {
            config.unlockSession();
            message = "Unlocked for this session.";
        } else {
            message = "Incorrect PIN.";
        }
    }

    @Override
    public void extractRenderState(GuiGraphicsExtractor extractor, int mouseX, int mouseY, float delta) {
        this.extractBackground(extractor, mouseX, mouseY, delta);
        int cx = this.width / 2;
        extractor.text(this.getFont(), Component.literal("Parent controls"), cx - 70, this.height / 2 - 50, 0xFFFFFF);
        extractor.text(this.getFont(), Component.literal(message), cx - 140, this.height / 2 + 84, 0xFFAA55);
        super.extractRenderState(extractor, mouseX, mouseY, delta);
    }
}
