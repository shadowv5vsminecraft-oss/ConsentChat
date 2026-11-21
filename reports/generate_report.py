from pathlib import Path
from datetime import date

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    HRFlowable,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

PROJECT = Path(__file__).resolve().parents[1]
OUT = PROJECT / "ConsentChat-Technical-and-Compliance-Report.pdf"
JAR = PROJECT / "build" / "libs" / "consentchat-1.0.0.jar"
REPORT_DATE = "21 November 2026"
JAR_SHA256 = "4b41ec41ffba67643d20d4e0ad8535471920b0b66929bb137f20537af07e03d2"
JAR_BYTES = "20,372 bytes"

NAVY = colors.HexColor("#12304A")
BLUE = colors.HexColor("#1E5F8C")
LIGHT_BLUE = colors.HexColor("#DCEAF5")
LIGHT_GRAY = colors.HexColor("#F2F4F6")
MID_GRAY = colors.HexColor("#C7CDD3")
DARK_GRAY = colors.HexColor("#4A545D")
ORANGE = colors.HexColor("#B56A00")
LIGHT_ORANGE = colors.HexColor("#FFF3DF")
GREEN = colors.HexColor("#2E7D32")
LIGHT_GREEN = colors.HexColor("#E7F4E9")
RED = colors.HexColor("#A33A3A")
LIGHT_RED = colors.HexColor("#FCE8E8")

styles = getSampleStyleSheet()

S = {}
S["title"] = ParagraphStyle(
    "title", parent=styles["Title"], fontName="Helvetica-Bold",
    fontSize=25, leading=30, textColor=NAVY, alignment=TA_CENTER,
    spaceAfter=10,
)
S["subtitle"] = ParagraphStyle(
    "subtitle", parent=styles["Normal"], fontName="Helvetica",
    fontSize=13, leading=18, textColor=DARK_GRAY, alignment=TA_CENTER,
    spaceAfter=6,
)
S["cover_small"] = ParagraphStyle(
    "cover_small", parent=styles["Normal"], fontName="Helvetica",
    fontSize=9.5, leading=14, textColor=DARK_GRAY, alignment=TA_CENTER,
)
S["h1"] = ParagraphStyle(
    "h1", parent=styles["Heading1"], fontName="Helvetica-Bold",
    fontSize=15.5, leading=19, textColor=NAVY, spaceBefore=16, spaceAfter=7,
    keepWithNext=True,
)
S["h2"] = ParagraphStyle(
    "h2", parent=styles["Heading2"], fontName="Helvetica-Bold",
    fontSize=12, leading=16, textColor=BLUE, spaceBefore=11, spaceAfter=5,
    keepWithNext=True,
)
S["h3"] = ParagraphStyle(
    "h3", parent=styles["Heading3"], fontName="Helvetica-Bold",
    fontSize=10.5, leading=14, textColor=NAVY, spaceBefore=8, spaceAfter=4,
    keepWithNext=True,
)
S["body"] = ParagraphStyle(
    "body", parent=styles["BodyText"], fontName="Helvetica",
    fontSize=9.4, leading=13.4, alignment=TA_JUSTIFY, spaceAfter=6,
)
S["body_left"] = ParagraphStyle(
    "body_left", parent=S["body"], alignment=TA_LEFT,
)
S["bullet"] = ParagraphStyle(
    "bullet", parent=S["body"], alignment=TA_LEFT, leftIndent=15,
    bulletIndent=3, spaceAfter=3.5,
)
S["small"] = ParagraphStyle(
    "small", parent=styles["Normal"], fontName="Helvetica",
    fontSize=8, leading=10.8, textColor=DARK_GRAY,
)
S["cell"] = ParagraphStyle(
    "cell", parent=styles["Normal"], fontName="Helvetica",
    fontSize=8.1, leading=10.8, alignment=TA_LEFT,
)
S["cell_head"] = ParagraphStyle(
    "cell_head", parent=S["cell"], fontName="Helvetica-Bold",
    textColor=colors.white,
)
S["code"] = ParagraphStyle(
    "code", parent=styles["Code"], fontName="Courier", fontSize=7.3,
    leading=9.5, textColor=colors.HexColor("#1A1A1A"),
    backColor=LIGHT_GRAY, borderColor=MID_GRAY, borderWidth=0.5,
    borderPadding=5, leftIndent=2, rightIndent=2,
)
S["callout"] = ParagraphStyle(
    "callout", parent=S["body"], alignment=TA_LEFT,
    backColor=LIGHT_BLUE, borderColor=BLUE, borderWidth=0.8,
    borderPadding=8, leftIndent=4, rightIndent=4, spaceBefore=6, spaceAfter=8,
)
S["warn"] = ParagraphStyle(
    "warn", parent=S["body"], alignment=TA_LEFT,
    backColor=LIGHT_ORANGE, borderColor=ORANGE, borderWidth=0.8,
    borderPadding=8, leftIndent=4, rightIndent=4, spaceBefore=6, spaceAfter=8,
)
S["good"] = ParagraphStyle(
    "good", parent=S["body"], alignment=TA_LEFT,
    backColor=LIGHT_GREEN, borderColor=GREEN, borderWidth=0.8,
    borderPadding=8, leftIndent=4, rightIndent=4, spaceBefore=6, spaceAfter=8,
)
S["caption"] = ParagraphStyle(
    "caption", parent=styles["Normal"], fontName="Helvetica-Oblique",
    fontSize=8, leading=10.5, textColor=DARK_GRAY, spaceBefore=3, spaceAfter=8,
)


def P(text, style="body"):
    return Paragraph(text, S[style])


def B(items, style="bullet"):
    return [Paragraph("&bull;&nbsp; " + item, S[style]) for item in items]


def rule(color=MID_GRAY, thickness=0.7):
    return HRFlowable(width="100%", thickness=thickness, color=color, spaceBefore=3, spaceAfter=7)


def table(headers, rows, widths=None, head_bg=NAVY, font_size=8.1, repeat=1):
    data = [[Paragraph(str(h), S["cell_head"]) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), S["cell"]) for c in row])
    if widths is None:
        avail = LETTER[0] - 1.5 * inch
        widths = [avail / len(headers)] * len(headers)
    t = Table(data, colWidths=widths, repeatRows=repeat, hAlign="LEFT")
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), head_bg),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), font_size),
        ("GRID", (0, 0), (-1, -1), 0.45, MID_GRAY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
    ]
    t.setStyle(TableStyle(style))
    return t


def risk_table(headers, rows, widths):
    data = [[Paragraph(str(h), S["cell_head"]) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), S["cell"]) for c in row])
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    st = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("GRID", (0, 0), (-1, -1), 0.45, MID_GRAY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    for i, row in enumerate(rows, start=1):
        rating = row[2].lower()
        if "low" in rating:
            bg = LIGHT_GREEN
        elif "medium" in rating or "moderate" in rating:
            bg = LIGHT_ORANGE
        elif "high" in rating:
            bg = LIGHT_RED
        else:
            bg = colors.white
        st.append(("BACKGROUND", (2, i), (2, i), bg))
    t.setStyle(TableStyle(st))
    return t


def cover_decorations(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, LETTER[1] - 0.32 * inch, LETTER[0], 0.32 * inch, stroke=0, fill=1)
    canvas.setFillColor(BLUE)
    canvas.rect(0, 0, LETTER[0], 0.18 * inch, stroke=0, fill=1)
    canvas.setFillColor(DARK_GRAY)
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(LETTER[0] / 2, 0.38 * inch, "CONFIDENTIAL TECHNICAL ASSESSMENT • NOT LEGAL ADVICE")
    canvas.restoreState()


def page_decorations(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, LETTER[1] - 0.28 * inch, LETTER[0], 0.28 * inch, stroke=0, fill=1)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawString(0.75 * inch, LETTER[1] - 0.19 * inch, "CONSENTCHAT — TECHNICAL & COMPLIANCE REPORT")
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(LETTER[0] - 0.75 * inch, LETTER[1] - 0.19 * inch, REPORT_DATE)
    canvas.setStrokeColor(MID_GRAY)
    canvas.setLineWidth(0.4)
    canvas.line(0.75 * inch, 0.62 * inch, LETTER[0] - 0.75 * inch, 0.62 * inch)
    canvas.setFillColor(DARK_GRAY)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(0.75 * inch, 0.44 * inch, "ConsentChat-Fabric • Minecraft Java 26.3 • Report CC-CMP-2026-11-21")
    canvas.drawRightString(LETTER[0] - 0.75 * inch, 0.44 * inch, "Page %d" % doc.page)
    canvas.restoreState()


story = []

# -----------------------------------------------------------------------------
# COVER
# -----------------------------------------------------------------------------
story += [
    Spacer(1, 0.75 * inch),
    P("ConsentChat", "title"),
    P("Technical &amp; Compliance Report", "subtitle"),
    P("How the client-side Fabric mod works — and whether Mojang can strike it down", "subtitle"),
    Spacer(1, 0.25 * inch),
    rule(BLUE, 1.2),
    Spacer(1, 0.18 * inch),
]

cover_facts = table(
    ["Field", "Value"],
    [
        ["Report ID", "CC-CMP-2026-11-21"],
        ["Date", REPORT_DATE],
        ["Prepared for", "Shadow"],
        ["Project", "ConsentChat-Fabric"],
        ["Artifact assessed", "build/libs/consentchat-1.0.0.jar"],
        ["Artifact size", JAR_BYTES],
        ["SHA-256", JAR_SHA256],
        ["Target game", "Minecraft Java Edition 26.3"],
        ["Toolchain", "Fabric Loader 0.20.1 • Fabric API 0.166.2+26.3 • Java 25 • Gradle 9.8.2"],
        ["Assessment type", "Source review, build verification, policy mapping, risk analysis"],
        ["Legal status", "Informational engineering report; not legal advice"],
    ],
    widths=[1.55 * inch, 5.0 * inch],
)
story += [cover_facts, Spacer(1, 0.28 * inch)]

story += [
    P(
        "<b>Bottom line.</b> ConsentChat is not a chat-report bypass. It is a local privacy-scope "
        "selector that drives ordinary Minecraft chat settings. Its current design has a low risk of "
        "conflicting with Mojang’s present EULA and Usage Guidelines because it does not strip "
        "signatures, alter packets, hide dialogs, collect data, or pretend to be official. However, "
        "Mojang has final say, can change rules or client code, and can takedown software it believes "
        "violates its guidelines. No mod can be guaranteed immune.",
        "callout",
    ),
    Spacer(1, 0.2 * inch),
    P(
        "This report was generated from the actual project source and a successful Gradle build. "
        "It also incorporates official Mojang policy text and current public descriptions of the "
        "Java chat-report system. It does not include an in-game smoke test and is not a legal opinion.",
        "small",
    ),
    PageBreak(),
]

# -----------------------------------------------------------------------------
# CONTENTS
# -----------------------------------------------------------------------------
story += [P("Contents", "h1"), rule()]
toc_rows = [
    ["1", "Executive summary", "Findings, overall posture, and direct answer"],
    ["2", "Scope, method, and limitations", "What was reviewed and what was not tested"],
    ["3", "System overview", "Architecture, components, and target versions"],
    ["4", "Privacy modes and chat-report effect", "Public, Trusted, Silent explained precisely"],
    ["5", "Runtime behaviour", "Join, tick enforcement, disclosure, dashboard, disconnect"],
    ["6", "Implementation walkthrough", "Source-file-level explanation with exact API calls"],
    ["7", "Data and privacy architecture", "Local storage, network behaviour, report contents"],
    ["8", "EULA and Usage Guidelines analysis", "Policy-by-policy mapping"],
    ["9", "Can Mojang strike it down?", "Direct answer and risk register"],
    ["10", "US child/adult privacy posture", "COPPA, state laws, CCPA/CPRA design notes"],
    ["11", "Limitations and residual risks", "Technical and operational caveats"],
    ["12", "Verification evidence", "Build, jar contents, static checks"],
    ["13", "Recommendations", "Concrete hardening and publication advice"],
    ["14", "Conclusion", "Final assessment"],
    ["A–C", "Appendices", "Artifact inventory, glossary, references"],
]
story += [table(["#", "Section", "Purpose"], toc_rows, widths=[0.5 * inch, 2.15 * inch, 3.9 * inch])]

# -----------------------------------------------------------------------------
# 1 EXECUTIVE SUMMARY
# -----------------------------------------------------------------------------
story += [PageBreak(), P("1. Executive summary", "h1"), rule()]
story += [
    P(
        "ConsentChat is a client-only Fabric mod for Minecraft Java 26.3. It presents three explicit "
        "privacy scopes — <b>Public</b>, <b>Trusted</b>, and <b>Silent</b> — and applies each one through "
        "vanilla Minecraft options. It does not intercept chat packets, remove cryptographic signatures, "
        "modify the chat pipeline with mixins, hide Mojang dialogs, or send data anywhere.",
        "body",
    ),
    P("Key findings", "h2"),
]
findings = [
    "<b>Technical mechanism:</b> the mod calls <font face='Courier'>Options.chatVisibility()</font> and "
    "<font face='Courier'>Options.onlyShowSecureChat()</font>, then "
    "<font face='Courier'>broadcastOptions()</font>. Silent maps to "
    "<font face='Courier'>ChatVisiblity.SYSTEM</font>, the vanilla “Commands Only” setting.",
    "<b>Practical privacy effect:</b> Silent prevents ordinary chat messages from being sent, so there "
    "is no ordinary signed chat message to place in a Mojang chat report. Trusted only filters what the "
    "local player sees; it does not make the player’s own messages unreportable.",
    "<b>Data posture:</b> zero collection. Preferences live only in "
    "<font face='Courier'>config/consentchat.json</font>. No chat logs, telemetry, accounts, analytics, "
    "cloud services, custom packets, or third-party SDKs are present.",
    "<b>EULA posture:</b> current design fits the EULA’s mod permission: original code, free, "
    "client-only, not a redistributed or hacked client, and not presented as official.",
    "<b>Usage Guidelines posture:</b> the design deliberately avoids hiding or altering Mojang dialogs, "
    "prompts, warnings, or errors. If a vanilla screen is open, ConsentChat queues its own disclosure "
    "instead of replacing it.",
    "<b>Can Mojang strike it down?</b> Yes in the contractual/platform sense — Mojang reserves final "
    "say, may change rules, and may takedown software it believes violates guidelines. But based on the "
    "current public policy text reviewed for this report, this implementation does not present a clear "
    "current violation.",
    "<b>Overall risk:</b> low current policy conflict risk; medium future-policy and technical-fragility "
    "risk; low privacy-law risk due to data minimisation.",
]
story += B(findings)

story += [
    P("Overall posture", "h2"),
    table(
        ["Dimension", "Rating", "Reason"],
        [
            ["Current EULA/Usage Guidelines conflict", "Low", "Uses vanilla APIs; no circumvention, no hidden dialogs, no sale, no official branding."],
            ["Privacy-law exposure", "Low", "No personal information is collected, transmitted, sold, or retained off-device."],
            ["Technical durability", "Medium", "Hard-pinned to MC 26.3 and specific 26.3 mappings; game updates can break it."],
            ["Effectiveness clarity", "Medium", "Silent is effective for ordinary chat, but Trusted and command-based text can be misunderstood."],
            ["Future Mojang policy change", "Medium", "Guidelines are expressly subject to change; Mojang has final say."],
        ],
        widths=[2.05 * inch, 0.85 * inch, 3.65 * inch],
    ),
    P(
        "The safest public positioning is “privacy scope and informed consent”, not “anti-report”. "
        "Any future release that adds signature stripping, packet rewriting, warning suppression, "
        "telemetry, monetisation, or official-looking branding would materially increase takedown risk.",
        "warn",
    ),
]

# -----------------------------------------------------------------------------
# 2 SCOPE
# -----------------------------------------------------------------------------
story += [PageBreak(), P("2. Scope, method, and limitations", "h1"), rule()]
story += [
    P("Sources reviewed", "h2"),
]
scope_rows = [
    ["Source code", "All seven Java classes under src/main/java and all resources under src/main/resources."],
    ["Build configuration", "build.gradle, gradle.properties, settings.gradle, fabric.mod.json, Gradle wrapper."],
    ["Built artifact", "consentchat-1.0.0.jar, size and SHA-256 recorded on the cover page."],
    ["Project documentation", "README.md and PRIVACY.md."],
    ["Mojang policy", "Minecraft EULA, Minecraft Usage Guidelines, player-reporting help/article pages."],
    ["Game API evidence", "Minecraft 26.3 deobfuscated classes inspected during development; 26.3 mappings used by Loom."],
    ["Privacy law references", "FTC COPPA Rule materials, CCPA/CPRA reference material, state privacy/AADC considerations."],
]
story += [table(["Category", "Material"], scope_rows, widths=[1.55 * inch, 5.0 * inch])]

story += [
    P("Method", "h2"),
    *B([
        "Read the implementation to establish exactly what the mod does and does not do.",
        "Confirm the Gradle build succeeds against Minecraft 26.3 mappings.",
        "Inspect the jar contents to verify no mixin config, network channel, or analytics code is bundled.",
        "Map implementation behaviour to official Mojang EULA/Usage Guidelines language.",
        "Create a risk register covering policy, legal, technical, and reputational exposure.",
    ]),
    P("Limitations", "h2"),
    *B([
        "<b>No in-game smoke test:</b> functionality was verified by compilation and source review, not by launching Minecraft with the mod installed.",
        "<b>Not legal advice:</b> this is an engineering assessment. Mojang’s guidelines state they cannot advise whether a specific project complies and suggest speaking to an attorney where unsure.",
        "<b>Version-specific:</b> all API claims apply to Minecraft Java 26.3 as built.",
        "<b>Policy volatility:</b> Mojang’s EULA and Usage Guidelines can change; this report reflects material checked on " + REPORT_DATE + ".",
    ]),
]

# -----------------------------------------------------------------------------
# 3 SYSTEM OVERVIEW
# -----------------------------------------------------------------------------
story += [PageBreak(), P("3. System overview", "h1"), rule()]
story += [
    P(
        "The mod is a normal Fabric client mod. It is loaded only in the client environment and uses "
        "Fabric lifecycle events. It does not bundle a server plugin, does not register custom payloads, "
        "and does not ship a Mojang client or any substantial Mojang code.",
        "body",
    ),
    P("Architecture", "h2"),
    table(
        ["Layer", "Component", "Responsibility"],
        [
            ["Entry", "ConsentChat", "Client initializer; registers keybind, tick callback, JOIN and DISCONNECT callbacks."],
            ["Policy", "PrivacyManager", "Resolves effective mode, applies/restores vanilla options, detects settings drift."],
            ["State", "Config", "Loads/saves local JSON preferences and optional parent-lock PIN hash."],
            ["Model", "Mode", "PUBLIC / TRUSTED / SILENT enum and display names."],
            ["UI", "ConsentScreen", "Local privacy dashboard with mode buttons and privacy notice."],
            ["UI", "DisclosureScreen", "Additive per-server disclosure and explicit public-chat opt-in."],
            ["UI", "PinScreen", "Local parent-control gate using a salted SHA-256 PIN hash."],
            ["Resources", "fabric.mod.json, en_us.json, LICENSE", "Metadata, keybind/category labels, MIT license."],
        ],
        widths=[0.9 * inch, 1.35 * inch, 4.3 * inch],
    ),
    P("Target environment", "h2"),
    table(
        ["Property", "Value"],
        [
            ["Minecraft", "26.3"],
            ["Java", "25 (compile release 25)"],
            ["Fabric Loader", "0.20.1 or newer"],
            ["Fabric API", "0.166.2+26.3"],
            ["Loom", "1.19-SNAPSHOT (resolved to 1.19.4 in the successful build)"],
            ["Gradle", "9.8.2 wrapper"],
            ["Environment", "client"],
            ["License", "MIT"],
        ],
        widths=[1.55 * inch, 5.0 * inch],
    ),
    P("Figure 1 — control boundary", "caption"),
    table(
        ["Inside ConsentChat", "Vanilla Minecraft", "Outside ConsentChat"],
        [
            ["Choose mode; save local JSON; open own screens; call vanilla option setters.",
             "Owns chat signing, reporting, dialogs, warnings, client info packet, and option behaviour.",
             "Servers, Realms, Microsoft account data, Mojang moderation, other mods."],
        ],
        widths=[2.15 * inch, 2.15 * inch, 2.25 * inch],
    ),
]

# -----------------------------------------------------------------------------
# 4 MODES
# -----------------------------------------------------------------------------
story += [PageBreak(), P("4. Privacy modes and chat-report effect", "h1"), rule()]
story += [
    table(
        ["Mode", "Vanilla mechanism applied", "Effect on ordinary chat", "Reportability"],
        [
            ["Public", "No persistent change. Original options are restored from the pre-connect snapshot.",
             "Normal signed chat behaves exactly as vanilla.",
             "Fully reportable."],
            ["Trusted", "chatVisibility = FULL; onlyShowSecureChat = true.",
             "The local client shows only secure/trusted chats. The player can still type and send chat.",
             "Still signed and reportable. This is a display filter, not a privacy guarantee."],
            ["Silent", "chatVisibility = SYSTEM (“Commands Only”); onlyShowSecureChat = true.",
             "No ordinary chat messages are sent. Commands still work under vanilla handling.",
             "No ordinary signed chat message exists to report. Some commands may still produce signed or server-visible text."],
        ],
        widths=[0.7 * inch, 1.85 * inch, 2.0 * inch, 2.0 * inch],
    ),
    P("Precise claims to use", "h2"),
    *B([
        "“Silent sends no ordinary chat messages.”",
        "“There is no ordinary signed chat message to include in a chat report while Silent is active.”",
        "“Trusted changes what you see, not whether your own messages are signed.”",
        "“Commands still use vanilla handling and can be visible to the server.”",
    ]),
    P("Claims to avoid", "h2"),
    *B([
        "“Mojang cannot ban you.”",
        "“This makes you completely anonymous.”",
        "“Trusted makes your chat unreportable.”",
        "“No commands can ever create reportable evidence.”",
    ]),
    P(
        "This distinction matters legally and reputationally. A mod that honestly says “no ordinary chat "
        "message is sent” is describing vanilla behaviour. A mod that says “reporting is disabled” would "
        "be a much stronger claim and could be treated as circumvention marketing.",
        "warn",
    ),
    P("Singleplayer and LAN", "h2"),
    P(
        "PrivacyManager.currentServerKey() returns an empty string when there is no current server entry. "
        "In that case effectiveMode() returns PUBLIC and apply() restores the original options rather than "
        "changing anything. This avoids unnecessary modification of singleplayer/LAN settings.",
        "body",
    ),
]

# -----------------------------------------------------------------------------
# 5 RUNTIME
# -----------------------------------------------------------------------------
story += [PageBreak(), P("5. Runtime behaviour", "h1"), rule()]
story += [
    P("5.1 Mod load", "h2"),
    *B([
        "Registers the O keybind through KeyMappingHelper in the ConsentChat category.",
        "Registers an END_CLIENT_TICK callback.",
        "Registers ClientPlayConnectionEvents.JOIN and DISCONNECT callbacks.",
        "Does not register mixins, custom network channels, scheduled tasks, telemetry hooks, or services.",
    ]),
    P("5.2 Join a multiplayer server", "h2"),
]
join_rows = [
    ["1", "JOIN callback fires", "Fabric client play connection event."],
    ["2", "PrivacyManager.apply()", "Reads current server key, resolves mode, snapshots original options once, applies vanilla settings."],
    ["3", "broadcastOptions()", "Sends the same vanilla client-information update used by the Options screen."],
    ["4", "Disclosure decision", "If server is blank, mode is PUBLIC, or server is acknowledged, no disclosure is shown."],
    ["5", "Screen preservation", "If no Mojang screen is open, DisclosureScreen is opened; otherwise pendingDisclosure is set."],
]
story += [table(["Step", "Action", "Detail"], join_rows, widths=[0.5 * inch, 1.75 * inch, 4.3 * inch])]
story += [
    P(
        "Note: the mode is applied on join; the disclosure is shown immediately after. This is privacy-protective "
        "because the default is Silent, but strict “consent before any state change” language would be inaccurate. "
        "The player can choose Public explicitly on the disclosure screen.",
        "small",
    ),
    P("5.3 Disclosure handling", "h2"),
    *B([
        "The disclosure explains the active mode and states that ConsentChat does not change signatures or hide Mojang warnings.",
        "“Stay private” keeps the current non-public mode; if the effective mode is somehow PUBLIC, it selects SILENT.",
        "“Use public, reportable chat on this server” writes Mode.PUBLIC for that server and restores vanilla options.",
        "Acceptance is recorded only in the local acknowledged set.",
    ]),
    P("5.4 Tick enforcement", "h2"),
    P(
        "Every client tick, while a level is loaded, the mod checks PrivacyManager.needsEnforcement(). If a "
        "non-public mode is active and the vanilla settings have drifted, apply() runs again. This maintains "
        "the chosen scope if another settings screen or mod changes the values. It does not inspect chat text.",
        "body",
    ),
    P("5.5 Dashboard", "h2"),
    *B([
        "Press O when no screen is open to open ConsentScreen.",
        "Buttons select Public, Trusted, or Silent for the current server, or the global default when no server is present.",
        "Choosing a mode writes config and reapplies settings immediately.",
        "Parent controls and the privacy notice are available from the same screen.",
    ]),
    P("5.6 Disconnect", "h2"),
    P(
        "On DISCONNECT the pending disclosure flag is cleared and PrivacyManager.restore() puts the saved "
        "original chat visibility and secure-chat preference back, then calls broadcastOptions(). The mod "
        "therefore does not permanently overwrite vanilla preferences.",
        "body",
    ),
    P("Figure 2 — join flow", "caption"),
    table(
        ["JOIN", "Blank server?", "Public / acknowledged?", "Apply mode", "Vanilla screen open?", "Result"],
        [
            ["Client joins multiplayer", "Yes → no changes", "Yes → no disclosure", "Vanilla options set + broadcast", "Yes → queue disclosure; No → open disclosure", "Tick enforces chosen scope; disconnect restores originals"],
        ],
        widths=[0.9 * inch, 0.95 * inch, 1.05 * inch, 1.1 * inch, 1.25 * inch, 1.3 * inch],
    ),
]

# -----------------------------------------------------------------------------
# 6 IMPLEMENTATION
# -----------------------------------------------------------------------------
story += [PageBreak(), P("6. Implementation walkthrough", "h1"), rule()]
story += [
    P("6.1 ConsentChat.java — entrypoint", "h2"),
    P("The mod uses Fabric events only. The key points are:", "body_left"),
    *B([
        "KeyMapping.Category.register(Identifier.fromNamespaceAndPath(\"consentchat\", \"general\"))",
        "new KeyMapping(\"key.consentchat.open\", InputConstants.KEY_O, CATEGORY)",
        "KeyMappingHelper.registerKeyMapping(OPEN_SCREEN)",
        "ClientTickEvents.END_CLIENT_TICK, ClientPlayConnectionEvents.JOIN, ClientPlayConnectionEvents.DISCONNECT",
        "client.gui.screen() and client.gui.setScreen(...) for Minecraft 26.3 screen access",
    ]),
    P("6.2 PrivacyManager.java — vanilla option control", "h2"),
    P(
        "This class is the entire privacy mechanism. It saves two vanilla values once, applies the selected "
        "mode, broadcasts options, detects drift, and restores on disconnect.",
        "body",
    ),
]
code = (
    'options.chatVisibility().set(ChatVisiblity.SYSTEM);   // "Commands Only"\n'
    'options.onlyShowSecureChat().set(true);\n'
    'options.broadcastOptions();\n\n'
    'options.chatVisibility().set(ChatVisiblity.FULL);    // Trusted mode\n'
    'options.onlyShowSecureChat().set(true);\n\n'
    'options.chatVisibility().set(originalVisibility);    // Public / restore\n'
    'options.onlyShowSecureChat().set(originalOnlyShowSecureChat);'
)
story += [Preformatted(code, S["code"])]
story += [
    P(
        "There is no call to any signature API, no packet constructor, no mixin annotation, and no chat "
        "component mutation. The misspelling <font face='Courier'>ChatVisiblity</font> is the correct "
        "Minecraft 26.3 mapping.",
        "small",
    ),
    P("6.3 Config.java — local-only state", "h2"),
    table(
        ["Field", "Type", "Purpose", "Stored locally?"],
        [
            ["defaultMode", "Mode", "Scope used when no server-specific override exists. Default SILENT.", "Yes"],
            ["servers", "Map&lt;String, Mode&gt;", "Per-server mode overrides keyed by server address.", "Yes"],
            ["acknowledged", "Set&lt;String&gt;", "Servers where disclosure was accepted.", "Yes"],
            ["parentLock", "boolean", "Whether a PIN is required to change modes.", "Yes"],
            ["pinSalt", "String", "Random 16-byte salt in hex.", "Yes"],
            ["pinHash", "String", "SHA-256 hex of salt + PIN.", "Yes"],
            ["unlockedThisSession", "boolean", "Transient unlock flag; not persisted by Gson.", "No"],
        ],
        widths=[1.2 * inch, 1.35 * inch, 3.1 * inch, 0.9 * inch],
    ),
    P(
        "The config path is FabricLoader.getInstance().getConfigDir().resolve(\"consentchat.json\"). "
        "Load failures fall back to defaults; save failures are ignored. Neither case transmits anything.",
        "small",
    ),
    P("6.4 UI screens", "h2"),
]
ui_rows = [
    ["ConsentScreen", "Mode buttons, parent-control button, privacy notice toggle, Done. Uses extractRenderState(GuiGraphicsExtractor, ...)."],
    ["DisclosureScreen", "Plain-language per-server explanation plus two explicit choices. Does not replace an existing Mojang screen."],
    ["PinScreen", "EditBox PIN entry, set/unlock/back actions, local status message."],
]
story += [table(["Screen", "Behaviour"], ui_rows, widths=[1.35 * inch, 5.2 * inch])]
story += [
    P(
        "The UI uses Minecraft 26.3 APIs: GuiGraphicsExtractor, extractBackground(...), "
        "extractor.text(...), and super.extractRenderState(...). This is a rendering API migration, "
        "not a change to game behaviour.",
        "small",
    ),
    P("6.5 Resources", "h2"),
    *B([
        "fabric.mod.json declares environment: client and a single client entrypoint.",
        "en_us.json supplies the keybind and category labels.",
        "LICENSE is the MIT license, consistent with free mod distribution under the EULA.",
    ]),
]

# -----------------------------------------------------------------------------
# 7 DATA AND PRIVACY
# -----------------------------------------------------------------------------
story += [PageBreak(), P("7. Data and privacy architecture", "h1"), rule()]
story += [
    P(
        "The design principle is data minimisation: if a value is not necessary to remember the user’s "
        "local choice, it is not stored. If it is stored, it never leaves the machine through ConsentChat.",
        "body",
    ),
    P("7.1 Data inventory", "h2"),
    table(
        ["Data", "Purpose", "Stored?", "Leaves machine via mod?", "Retention"],
        [
            ["Default mode", "Remember privacy scope", "Yes, local JSON", "No", "Until user deletes/edits config"],
            ["Server address key", "Scope preferences per server", "Yes, local JSON", "No", "Until user deletes/edits config"],
            ["Acknowledged servers", "Avoid repeating disclosure", "Yes, local JSON", "No", "Until user deletes/edits config"],
            ["PIN salt + hash", "Local parent-control gate", "Yes, local JSON", "No", "Until user resets/deletes config"],
            ["Chat text", "Not used", "No", "No", "None"],
            ["UUID / account ID", "Not used", "No", "No", "None"],
            ["IP address / geolocation", "Not used", "No", "No", "None"],
            ["Age / birthday / real name", "Not used", "No", "No", "None"],
            ["Telemetry / analytics / crash reports", "Not used", "No", "No", "None"],
        ],
        widths=[1.35 * inch, 1.6 * inch, 1.0 * inch, 1.25 * inch, 1.35 * inch],
    ),
    P("7.2 Network behaviour", "h2"),
    *B([
        "<b>Custom network traffic:</b> none. No custom payloads, HTTP clients, sockets, analytics SDKs, or cloud endpoints exist in the source or jar.",
        "<b>Vanilla traffic:</b> changing chat options calls Minecraft’s own broadcastOptions(), which sends the normal vanilla client-information update. This is the same traffic generated by the vanilla Options screen.",
        "<b>Server visibility:</b> a server can see the chat visibility setting you broadcast and whatever vanilla commands you choose to run. ConsentChat does not hide that.",
    ]),
    P("7.3 What a Mojang chat report contains", "h2"),
    P(
        "This is separate from ConsentChat’s own storage. A submitted Minecraft chat report is sent to "
        "Mojang/Microsoft and can include the reported profile UUID, selected signed messages and "
        "surrounding signed context, timestamps, reason category, reporter comments, server address or "
        "Realm identifier, client version, and locale. It does not include a physical-location field, "
        "real name field, age field, or date-of-birth field. Microsoft’s account records are a separate "
        "matter and are governed by Microsoft’s privacy materials.",
        "body",
    ),
    table(
        ["Question", "Answer"],
        [
            ["Does a report find my house or GPS location?", "No location field. Server address may identify the server, not the player’s physical location."],
            ["Does it include my real name?", "No. It identifies a Minecraft profile UUID, which Mojang can associate with account records it already holds."],
            ["Does it include my age?", "No age/DOB field in the report payload."],
            ["Is it anonymous?", "No. Submitting a report requires an authenticated Minecraft session, so the reporter is identifiable to Mojang."],
            ["Does ConsentChat add anything to a report?", "No. ConsentChat does not touch report creation or submission."],
        ],
        widths=[2.15 * inch, 4.4 * inch],
    ),
    P("7.4 Child and adult design notes", "h2"),
    *B([
        "<b>Children:</b> no collection from anyone, high-privacy Silent default, plain-language disclosure, local parent lock, no profiling or advertising.",
        "<b>Parent lock:</b> a convenience control, not age verification and not a security boundary against someone with filesystem access.",
        "<b>Adults:</b> no sale/share, no sensitive personal information, no cross-context behavioural advertising, no cloud retention to access or delete.",
        "<b>Reset:</b> deleting config/consentchat.json removes all mod-held preferences.",
    ]),
]

# -----------------------------------------------------------------------------
# 8 EULA
# -----------------------------------------------------------------------------
story += [PageBreak(), P("8. EULA and Usage Guidelines analysis", "h1"), rule()]
story += [
    P(
        "The following mapping is an engineering interpretation of official policy text checked on "
        + REPORT_DATE + ". It is not a legal determination. Mojang explicitly reserves final say on what "
        "counts as a Mod and states that guidelines may change.",
        "body",
    ),
    P("8.1 Policy-to-implementation mapping", "h2"),
    table(
        ["Policy principle", "What official text says (paraphrased)", "ConsentChat implementation", "Assessment"],
        [
            ["Mods allowed", "Java Edition players may modify the game with original modifications, tools, or plugins.", "Original Java code, MIT license, no Minecraft client bundled.", "Aligned"],
            ["No modded versions", "Mods may be distributed; hacked versions or Modded Versions may not.", "Only a small Fabric jar is built; no game files are redistributed.", "Aligned"],
            ["No sale", "Mods must not be sold or used to make money.", "Free project; no payments, donations, ads, or premium features in the mod.", "Aligned"],
            ["Not official", "Tools must not appear official or approved; no misleading logos or claims.", "Name, metadata, and docs present it as independent; no Mojang/Microsoft branding.", "Aligned"],
            ["No griefing", "Mojang would appreciate mods not being used for griefing.", "No gameplay disruption, chat flooding, spoofing, or server manipulation.", "Aligned"],
            ["Dialogs/prompts", "Guidelines say not to hide or alter Minecraft dialogs, prompts, warnings, or errors.", "No mixins; disclosure queues if a vanilla screen is open; vanilla toast untouched.", "Aligned"],
            ["Takedown rights", "Mojang says it may takedown mods/software violating Usage Guidelines and has final say.", "Accepted as a residual risk; no guarantee claimed.", "Residual risk"],
            ["Subject to change", "Guidelines may change and changes take effect on next use of services.", "Report recommends re-review at every Minecraft release.", "Residual risk"],
        ],
        widths=[1.15 * inch, 1.95 * inch, 2.25 * inch, 1.2 * inch],
    ),
    P("8.2 Why this is different from signature-stripping mods", "h2"),
]
diff_rows = [
    ["Chat packets", "Not intercepted or rewritten", "May be altered or unsigned"],
    ["Message signatures", "Not stripped or forged", "Removed, disabled, or bypassed"],
    ["Vanilla warnings", "Left untouched", "Historically some implementations hid/handled the unverified-message toast"],
    ["Mechanism", "Vanilla Options API only", "Client/server mixins and protocol manipulation"],
    ["Claim", "No ordinary chat message is sent in Silent", "Signed chat continues but is made unreportable"],
    ["Policy exposure", "Low current conflict risk", "Higher circumvention and dialog-alteration risk"],
]
story += [table(["Aspect", "ConsentChat", "Signature-stripping approach"], diff_rows, widths=[1.45 * inch, 2.4 * inch, 2.7 * inch])]
story += [
    P(
        "This difference is the core compliance argument. ConsentChat does not defeat a safety mechanism; "
        "it changes whether the user generates the ordinary chat content that the mechanism operates on.",
        "good",
    ),
    P("8.3 What could change the assessment", "h2"),
    *B([
        "Adding a mixin into chat signing, message decoration, reporting, or toast/display code.",
        "Sending unsigned chat while presenting it as ordinary chat.",
        "Hiding, suppressing, moving, or restyling Mojang warnings, errors, EULA prompts, or safety dialogs.",
        "Using Minecraft logos, official language, or implying Mojang endorsement.",
        "Selling the mod, gating it behind payment, or bundling unrelated monetised services.",
        "Adding telemetry, advertising, accounts, or third-party data collection.",
        "Marketing it as a guaranteed way to avoid bans, moderation, or accountability.",
    ]),
]

# -----------------------------------------------------------------------------
# 9 CAN MOJANG STRIKE IT DOWN
# -----------------------------------------------------------------------------
story += [PageBreak(), P("9. Can Mojang strike it down?", "h1"), rule()]
story += [
    P(
        "<b>Direct answer: yes, Mojang can harm or remove almost any mod — but that is different from saying "
        "this mod currently violates the rules.</b> Mojang owns the platform, reserves final say over what "
        "counts as a Mod, can change the EULA/Usage Guidelines, can ask hosting platforms to remove software, "
        "and can enforce against accounts that violate policy. The question is whether there is a current, "
        "specific basis to do so here.",
        "callout",
    ),
    P("9.1 Four meanings of “strike down”", "h2"),
    table(
        ["Meaning", "Can it happen?", "Assessment for ConsentChat"],
        [
            ["Declare non-compliant", "Yes", "Possible if Mojang interprets any automatic option enforcement as circumvention, but current public text does not clearly prohibit it."],
            ["Takedown from hosts", "Yes", "CurseForge/Modrinth and Mojang can act under their own policies. Low current trigger risk given no bypassing features."],
            ["Technical breakage", "Yes, likely over time", "Hard-pinned to MC 26.3 APIs. A game update can prevent loading until ported."],
            ["Account enforcement", "Yes, in theory", "No clear current basis from this code. Risks rise sharply if anti-report or hiding features are added."],
        ],
        widths=[1.5 * inch, 1.2 * inch, 3.85 * inch],
    ),
    P("9.2 Best defensible position", "h2"),
    *B([
        "The mod uses only vanilla, player-facing settings that Mojang itself ships.",
        "Public mode is identical to vanilla.",
        "Silent mode uses “Commands Only”, a first-party comfort/accessibility setting.",
        "No safety prompt, warning, error, or dialog is hidden or altered.",
        "No data is collected; no third party receives anything.",
        "The documentation explicitly says the mod does not defeat reporting and does not guarantee anonymity.",
    ]),
    P("9.3 Risk register", "h2"),
]
risk_rows = [
    ["R1", "Mojang changes EULA/Usage Guidelines to restrict privacy-scope mods.", "Medium", "Medium", "Re-review policy at every release; keep scope vanilla-only."],
    ["R2", "Mojang interprets enforced chat visibility as evading safety systems.", "Low–Medium", "High", "Keep wording precise; never claim reporting is disabled; document vanilla mechanism."],
    ["R3", "Host platform removes the mod under its own rules.", "Low", "Medium", "Avoid anti-report branding; include clear non-affiliation notice."],
    ["R4", "A future feature hides toasts or alters packets.", "Low current", "High", "Do not add; make it a hard project rule."],
    ["R5", "Users misunderstand Trusted mode as protective.", "Medium", "Medium", "Use persistent UI text: still signed and reportable."],
    ["R6", "Command text still creates reportable/server-visible content.", "Medium", "Medium", "Document that Silent affects ordinary chat only."],
    ["R7", "MC update breaks API compatibility.", "High over time", "Low–Medium", "Pin versions, test per release, ship source for rapid porting."],
    ["R8", "Parent lock mistaken for real age verification or strong security.", "Medium", "Low", "Document as convenience only; consider PBKDF2 if stronger local protection is desired."],
    ["R9", "Bundling/endorsing the Paper plugin creates server-side policy exposure.", "Low current", "Medium", "Keep separate; client mod must not communicate with or advertise it."],
    ["R10", "Modded-client flag appears in reports submitted by the user.", "Low", "Low", "Accurate documentation; not a defect in ConsentChat."],
]
story += [risk_table(["ID", "Risk", "Likelihood", "Impact", "Mitigation"], risk_rows, widths=[0.4 * inch, 2.0 * inch, 0.85 * inch, 0.7 * inch, 2.6 * inch])]
story += [
    P("9.4 Overall answer", "h2"),
    P(
        "On the current evidence, ConsentChat is defensible as an ordinary mod and has a low current "
        "conflict risk. It is not immune: Mojang can change the rules, reinterpret them, or make technical "
        "changes. The strongest protection is not a legal argument but product discipline — keep the mod "
        "vanilla-only, transparent, free, non-affiliated, and honest about what Silent can and cannot do.",
        "good",
    ),
]

# -----------------------------------------------------------------------------
# 10 PRIVACY LAW
# -----------------------------------------------------------------------------
story += [PageBreak(), P("10. US child/adult privacy posture", "h1"), rule()]
story += [
    P(
        "This section is design guidance, not legal advice. The mod is not a website, app store service, "
        "advertiser, or data broker. Because it does not collect personal information, many statutory "
        "obligations that depend on collection are not triggered by this code. The design nevertheless "
        "borrows from child-privacy and adult-rights expectations.",
        "body",
    ),
    P("10.1 COPPA", "h2"),
    *B([
        "COPPA applies to operators of child-directed online services and to operators with actual knowledge of collecting personal information from children under 13.",
        "The FTC’s amended COPPA Rule was published on 22 April 2025; the final rule provides a 365-day period for full compliance with amendments that do not specify earlier dates.",
        "ConsentChat collects no personal information from any user, so it creates no COPPA collection, retention, disclosure, or parental-consent workflow.",
        "Silent default and plain-language disclosure reduce risk for child users without pretending to verify age.",
        "The local PIN lock is not verifiable parental consent under COPPA; it is only a local convenience control.",
    ]),
    P("10.2 State age-appropriate design and privacy laws", "h2"),
    *B([
        "Several states have age-appropriate design or minor-focused privacy statutes; scope and litigation status vary.",
        "High-privacy defaults, limited data, clear disclosures, easy reset, and no profiling are conservative design choices across those regimes.",
        "No behavioural advertising, recommendation engine, engagement tracking, or persistent online identifier is created by the mod.",
    ]),
    P("10.3 CCPA/CPRA and adult privacy rights", "h2"),
    table(
        ["Right / concept", "ConsentChat posture"],
        [
            ["Right to know", "No collected personal information held by the project."],
            ["Right to delete", "Delete config/consentchat.json; no server-side copy exists."],
            ["Right to correct", "Edit the local JSON or use the in-game UI."],
            ["Right to opt out of sale/share", "No sale or sharing; no cross-context behavioural advertising."],
            ["Sensitive personal information", "Not collected."],
            ["Retention", "Local preferences persist until deleted; no cloud retention."],
        ],
        widths=[2.1 * inch, 4.45 * inch],
    ),
    P("10.4 Privacy notice", "h2"),
    P(
        "PRIVACY.md states the same rule as the code: no chat messages, usernames, UUIDs, IP addresses, "
        "account information, birth dates, telemetry, analytics, advertising IDs, or third-party collection. "
        "The only local file is config/consentchat.json.",
        "body",
    ),
]

# -----------------------------------------------------------------------------
# 11 LIMITATIONS
# -----------------------------------------------------------------------------
story += [PageBreak(), P("11. Limitations and residual risks", "h1"), rule()]
limitations = [
    ["Client-only boundary", "A client cannot make a normal signed chat message both ordinary and unreportable. Silent avoids creating the message; it does not alter reporting."],
    ["Commands", "Commands can still be logged by servers and some command arguments can be signed under vanilla rules. Silent is not a general text-privacy mode."],
    ["Trusted mode", "It filters incoming display only. The player’s outgoing messages remain signed and reportable."],
    ["Name/skin/screenshot reports", "The mod does not prevent other report categories or server-side evidence."],
    ["Server rules", "A server may set its own rules about chat visibility, commands, or mods. That is separate from Mojang EULA compliance."],
    ["Version lock", "Built only for MC 26.3. Official mappings and API shapes can change."],
    ["No in-game test", "Compilation and jar inspection passed; actual client launch and screen behaviour were not smoke-tested."],
    ["Parent lock strength", "Salted single-round SHA-256 is adequate for casual UI gating but is not a password KDF and does not resist filesystem access."],
    ["Config resilience", "Malformed JSON falls back to defaults; failed saves are silently ignored. Users may lose preferences but no data leaves the machine."],
    ["Disclosure timing", "Mode is applied on JOIN before the disclosure screen appears. This favours privacy but is not strict pre-application consent."],
    ["Option enforcement", "Tick-level reapplication can override changes made in the vanilla options screen while connected. This is intentional but should be explained."],
]
story += [table(["Area", "Residual risk / caveat"], limitations, widths=[1.6 * inch, 4.95 * inch])]

# -----------------------------------------------------------------------------
# 12 VERIFICATION
# -----------------------------------------------------------------------------
story += [PageBreak(), P("12. Verification evidence", "h1"), rule()]
story += [
    P("12.1 Build", "h2"),
    P(
        "The project was compiled and packaged with JDK 25 using the Gradle wrapper. Both compileJava "
        "and full build completed successfully against Minecraft 26.3 mappings.",
        "body",
    ),
    table(
        ["Check", "Result"],
        [
            ["compileJava", "BUILD SUCCESSFUL"],
            ["build", "BUILD SUCCESSFUL"],
            ["Warnings", "Gradle reported generic deprecation/incubating-problems notices, not source compile errors."],
            ["Artifact", JAR_BYTES + ", SHA-256 " + JAR_SHA256],
        ],
        widths=[1.25 * inch, 5.3 * inch],
    ),
    P("12.2 Jar contents", "h2"),
    P(
        "The jar contains only mod classes, metadata, language file, license, and manifest. No mixin config, "
        "no bundled server plugin, no analytics library, no HTTP client, and no custom networking code is present.",
        "body",
    ),
]
jar_rows = [
    ["com/shadow/consentchat/", "Config.class, ConsentChat.class, Mode.class, PrivacyManager.class, PrivacyManager$1.class"],
    ["com/shadow/consentchat/screen/", "ConsentScreen.class, DisclosureScreen.class, PinScreen.class"],
    ["fabric.mod.json", "Client-only metadata and version dependencies"],
    ["assets/consentchat/lang/en_us.json", "Keybind and category labels"],
    ["LICENSE_*", "MIT license"],
    ["META-INF/MANIFEST.MF", "Standard jar manifest"],
]
story += [table(["Path", "Contents"], jar_rows, widths=[2.25 * inch, 4.3 * inch])]
story += [
    P("12.3 Static checks", "h2"),
    *B([
        "Source search found no HttpClient, Socket, URL, HttpRequest, analytics SDK, or telemetry uploader.",
        "No packet classes, custom payload identifiers, or network channel registrations are present.",
        "No mixin classes or mixin configuration file are present.",
        "No code modifies message signatures, components, report classes, or Mojang dialogs.",
    ]),
    P(
        "These checks support the stated architecture. They are not a substitute for runtime profiling or "
        "a full security audit.",
        "small",
    ),
]

# -----------------------------------------------------------------------------
# 13 RECOMMENDATIONS
# -----------------------------------------------------------------------------
story += [PageBreak(), P("13. Recommendations", "h1"), rule()]
recs = [
    ["R-1", "High", "Add a clear non-affiliation line to README, mod description, and first-run UI: “Not affiliated with or endorsed by Mojang or Microsoft.”"],
    ["R-2", "High", "Keep all public wording focused on “no ordinary chat message is sent” rather than “reporting disabled” or “unreportable”."],
    ["R-3", "High", "Never add signature stripping, packet rewriting, dialog hiding, or hidden toast suppression. Treat these as hard project boundaries."],
    ["R-4", "Medium", "Document that commands can still be logged and some command arguments may be signed."],
    ["R-5", "Medium", "Re-review EULA, Usage Guidelines, and Minecraft mappings at every game update; do not claim forward compatibility."],
    ["R-6", "Medium", "Add an in-game smoke-test checklist: join server, verify Silent applies, verify O key, verify disclosure queue, verify restore on disconnect."],
    ["R-7", "Medium", "Consider PBKDF2WithHmacSHA256 with many iterations instead of one-round SHA-256 if parent lock is described as security rather than convenience."],
    ["R-8", "Medium", "Add config schema versioning so future releases can migrate preferences without silently dropping them."],
    ["R-9", "Low", "Keep the Paper plugin entirely separate. Do not bundle it, auto-install it, or advertise it inside the client UI."],
    ["R-10", "Low", "Publish source and build instructions so reviewers can verify the zero-data claim."],
]
story += [table(["ID", "Priority", "Recommendation"], recs, widths=[0.5 * inch, 0.8 * inch, 5.25 * inch])]
story += [
    P("Suggested public summary", "h2"),
    P(
        "“ConsentChat is a free, client-side Fabric mod that lets players choose a local privacy scope "
        "using Minecraft’s own chat settings. It does not strip signatures, modify packets, hide warnings, "
        "collect data, or claim to defeat Mojang’s safety systems. Silent mode uses the vanilla Commands "
        "Only setting so no ordinary chat message is sent.”",
        "callout",
    ),
]

# -----------------------------------------------------------------------------
# 14 CONCLUSION
# -----------------------------------------------------------------------------
story += [PageBreak(), P("14. Conclusion", "h1"), rule()]
story += [
    P(
        "ConsentChat is best understood as a consent and scope-control layer. It does not defeat chat "
        "reporting cryptographically; it reduces the existence of ordinary signed chat content by using "
        "vanilla options. That design choice is also its main compliance defence.",
        "body",
    ),
    P(
        "Based on the current source, the built artifact, and official Mojang policy text reviewed for this "
        "report, the mod has a low current risk of conflicting with the Minecraft EULA and Usage Guidelines. "
        "It has no clear data-collection exposure. The principal risks are future policy change, technical "
        "breakage on game updates, and user misunderstanding about Trusted mode and command text.",
        "body",
    ),
    P(
        "Mojang can still strike it down in the sense that it can change rules, pressure hosts, or enforce "
        "against software it believes violates its guidelines. What Mojang cannot reasonably claim from the "
        "current implementation is that the client strips signatures, rewrites packets, hides warnings, sells "
        "mods, or collects data — because it does none of those things.",
        "good",
    ),
    P(
        "The practical recommendation is to keep the mod boring: vanilla-only APIs, no data, no bypass "
        "marketing, no official branding, and continuous policy review on every Minecraft release.",
        "body",
    ),
]

# -----------------------------------------------------------------------------
# APPENDIX A
# -----------------------------------------------------------------------------
story += [PageBreak(), P("Appendix A — Artifact and source inventory", "h1"), rule()]
appendix_a = [
    ["build/libs/consentchat-1.0.0.jar", "Final Fabric mod jar assessed by this report."],
    ["src/main/java/com/shadow/consentchat/ConsentChat.java", "Client entrypoint, keybind, Fabric event registration."],
    ["src/main/java/com/shadow/consentchat/PrivacyManager.java", "Vanilla option application, enforcement, restoration."],
    ["src/main/java/com/shadow/consentchat/Config.java", "Local JSON config and parent lock."],
    ["src/main/java/com/shadow/consentchat/Mode.java", "Mode enum."],
    ["src/main/java/com/shadow/consentchat/screen/ConsentScreen.java", "Privacy dashboard."],
    ["src/main/java/com/shadow/consentchat/screen/DisclosureScreen.java", "Per-server disclosure."],
    ["src/main/java/com/shadow/consentchat/screen/PinScreen.java", "Parent-control gate."],
    ["src/main/resources/fabric.mod.json", "Fabric metadata."],
    ["src/main/resources/assets/consentchat/lang/en_us.json", "English keybind/category labels."],
    ["README.md", "User-facing explanation and build/install instructions."],
    ["PRIVACY.md", "Short privacy notice."],
    ["LICENSE", "MIT license."],
]
story += [table(["Path", "Role"], appendix_a, widths=[3.55 * inch, 3.0 * inch])]

# -----------------------------------------------------------------------------
# APPENDIX B
# -----------------------------------------------------------------------------
story += [P("Appendix B — Glossary", "h1"), rule()]
glossary = [
    ["Chat report", "A player-submitted report to Mojang containing selected signed chat evidence and context."],
    ["Signed chat", "Ordinary Minecraft chat carrying a cryptographic signature tied to the sender’s profile session."],
    ["ChatVisiblity.SYSTEM", "The MC 26.3 mapping for “Commands Only” chat visibility. Note the spelling."],
    ["Only show secure chat", "Vanilla option that hides messages failing secure-chat verification."],
    ["broadcastOptions()", "Vanilla method that syncs changed client options to the server."],
    ["Mixin", "Fabric/Forge bytecode injection mechanism. ConsentChat uses none."],
    ["Custom payload", "A mod-defined network message. ConsentChat registers none."],
    ["COPPA", "US Children’s Online Privacy Protection Act; enforced through the FTC COPPA Rule."],
    ["CCPA/CPRA", "California privacy law and amendments covering consumer rights."],
    ["AADC", "Age-appropriate design code; state-level design guidance/law affecting minors’ services."],
]
story += [table(["Term", "Meaning"], glossary, widths=[1.65 * inch, 4.9 * inch])]

# -----------------------------------------------------------------------------
# APPENDIX C
# -----------------------------------------------------------------------------
story += [PageBreak(), P("Appendix C — References", "h1"), rule()]
refs = [
    ["Minecraft EULA", "minecraft.net/en-us/eula", "Mod permissions, no modded versions, no sale, no official appearance, takedown/final-say language."],
    ["Minecraft Usage Guidelines", "minecraft.net/en-us/usage-guidelines", "Subject to change; no hiding/altering dialogs, prompts, warnings, or errors."],
    ["Report a Player in Minecraft: Java Edition", "help.minecraft.net/hc/en-us/articles/7149823936781", "Official reporting flow."],
    ["Addressing Player Reporting Tool", "minecraft.net/en-us/article/addressing-player-chat-reporting-tool", "Mojang’s official explanation of player reporting and private servers."],
    ["Removing obfuscation in Java Edition", "minecraft.net/en-us/article/removing-obfuscation-in-java-edition", "Mojang’s 2025 modding transparency announcement; EULA/Usage Guidelines still apply."],
    ["FTC COPPA Rule", "ftc.gov/legal-library/browse/rules/childrens-online-privacy-protection-rule-coppa", "COPPA scope and amended rule materials."],
    ["FTC COPPA Final Rule Amendments", "ftc.gov/legal-library/browse/federal-register-notices/16-cfr-part-312-coppa-final-rule-amendments", "Publication and compliance timing."],
    ["California Privacy Protection Agency", "cppa.ca.gov", "CCPA/CPRA regulator reference."],
    ["Fabric Example Mod 26.3", "github.com/FabricMC/fabric-example-mod/tree/26.3", "Version-aligned toolchain reference."],
    ["Local project files", "ConsentChat-Fabric/README.md, PRIVACY.md, source tree", "Primary evidence for implementation claims."],
]
ref_data = []
for name, url, note in refs:
    display = url.replace("&", "&amp;")
    ref_data.append([name, "<font size='7.5'>" + display + "</font>", note])
story += [table(["Source", "Location", "Relevance"], ref_data, widths=[1.55 * inch, 2.35 * inch, 2.65 * inch], font_size=7.7)]

story += [
    Spacer(1, 0.2 * inch),
    P("Prepared from source and policy evidence available on " + REPORT_DATE + ". End of report.", "small"),
]

# -----------------------------------------------------------------------------
# BUILD
# -----------------------------------------------------------------------------
doc = SimpleDocTemplate(
    str(OUT),
    pagesize=LETTER,
    leftMargin=0.75 * inch,
    rightMargin=0.75 * inch,
    topMargin=0.82 * inch,
    bottomMargin=0.78 * inch,
    title="ConsentChat Technical & Compliance Report",
    author="Shadow",
    subject="How ConsentChat works and Mojang policy risk assessment",
)
doc.build(story, onFirstPage=cover_decorations, onLaterPages=page_decorations)
print(OUT)
