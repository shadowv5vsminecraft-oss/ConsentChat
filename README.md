# ConsentChat — Fabric client privacy scope

A **client-side-only Fabric mod for Minecraft Java 26.3** inspired by the privacy goal of
No Chat Reports, redesigned to stay inside Mojang's EULA/Usage Guidelines and to follow
US child/adult privacy expectations.

> Short version: this mod does **not** strip signatures, rewrite packets, or defeat chat
> reporting. It gives the player explicit, local privacy scopes using **only vanilla
> settings**, with a high-privacy default and informed consent per server.

## What it actually does

| Mode | Vanilla mechanism | Effect on chat reports |
|---|---|---|
| **Public** | No changes; original options restored | Ordinary vanilla signed chat. Fully reportable. |
| **Trusted** | `Only show secure chat` = on, chat visibility = All | Reduces who you see; **your own messages are still signed and reportable**. |
| **Silent** | `Chat visibility` = **Commands Only**, `Only show secure chat` = on | **No ordinary chat messages are sent**, so there is no chat message to report. Commands still use vanilla handling. |

The mod also provides:

- a local privacy dashboard (default key: **O**, rebindable);
- a one-time-per-server disclosure screen before non-public modes are used;
- per-server mode memory in `config/consentchat.json`;
- an optional local parent lock (salted PIN hash) that requires a PIN to change modes;
- automatic enforcement of the chosen vanilla settings while connected;
- restoration of the player's original options on disconnect.

## Why this design instead of No Chat Reports' approach

No Chat Reports removes or avoids Mojang's chat signature chain. A client-only signature
strip is unreliable on servers with `enforce-secure-profile=true`, and a server-side
conversion of player chat to system chat changes how Mojang's safety/reporting system
behaves. This mod takes a different route:

1. **No signature or packet tampering.** No mixin touches Mojang's chat pipeline.
2. **No hidden dialogs.** The mod never replaces, suppresses, or edits Mojang warnings,
   dialogs, errors, or the "messages cannot be verified" toast.
3. **No circumvention claims.** If you want to keep talking while avoiding reports, that
   requires a server that voluntarily sends unsigned/system messages. The existing
   companion Paper plugin in the workspace can do that; this client mod does not pretend
   a client-only mod can do it safely.
4. **Zero data.** No telemetry, analytics, accounts, cloud storage, chat logs, custom
   network channels, or third-party SDKs.

## EULA / Usage Guidelines posture

- Modding is allowed; this is a normal Fabric mod, not a redistributed Minecraft client.
- It is free and not sold.
- It does not unlock paid content or bypass subscriptions.
- It does not hide or alter Mojang dialogs, prompts, warnings, or errors.
- Public mode is exactly vanilla behaviour.
- Silent mode uses a first-party vanilla setting that Mojang ships for player comfort.
- The mod makes no claim to defeat Mojang's reporting or safety systems.

This is a design posture, not a legal guarantee. Mojang has final say over what is allowed
on its services.

## US privacy posture

This mod is built around data minimisation rather than consent to collection.

### Children (COPPA and state age-appropriate design codes)

- No personal information is collected from anyone, including children.
- No account, email, phone number, persistent online identifier, or profile is created.
- No behavioural advertising, profiling, recommendation engine, or engagement tracking.
- High-privacy default: everyone starts in **Silent** mode on multiplayer servers.
- Disclosure is plain-language and shown before a non-public mode is used.
- Parent lock is local and optional. It is a convenience control, **not** age verification.
- Settings are easy to find, change, and reset locally.

### Adults (CCPA/CPRA-style rights)

- No personal information is sold or shared.
- No sensitive personal information is collected.
- No cross-context behavioural advertising.
- No retention: there is no server-side record to access, delete, or correct.
- The only stored data is local preference JSON on the player's own machine.

See [`PRIVACY.md`](PRIVACY.md) for the short privacy notice.

## Build

Requires **JDK 25** (Minecraft 26.3 uses Java 25).

```powershell
$env:JAVA_HOME = "C:\Program Files\Eclipse Adoptium\jdk-25.0.5.8-hotspot"
.\gradlew.bat build
```

Output:

```text
build/libs/consentchat-1.0.0.jar
```

Target versions:

- Minecraft `26.3`
- Fabric Loader `0.20.1`
- Fabric API `0.166.2+26.3`
- Loom `1.19-SNAPSHOT`

## Install

1. Install Fabric Loader 0.20.1 for Minecraft 26.3.
2. Install Fabric API `0.166.2+26.3`.
3. Copy `consentchat-1.0.0.jar` into `.minecraft/mods`.
4. Join a server. The default mode is **Silent** until you choose otherwise.
5. Press **O** to open the privacy dashboard.

## Local data

File: `config/consentchat.json`

Contents:

- default mode;
- per-server mode overrides;
- per-server disclosure acknowledgement;
- optional parent-lock flag and salted PIN hash.

No chat text, timestamps, IP addresses, UUIDs, tokens, or analytics IDs are stored.

## Companion server plugin (optional, separate)

The workspace also contains `NoChatReports-Paper`, a Paper plugin that converts player
chat into unsigned system messages and disables `enforce-secure-profile`. That is a
**server operator's choice**. This client mod does not require it, do not communicate with
it, and do not advertise it inside the client UI.

## Limitations

- A client alone cannot make a normal chat message unreportable while still sending it as
  a normal signed chat message.
- **Trusted** mode reduces what you see; it does not make your messages unreportable.
- **Silent** mode means no chat conversation. Use commands or a server-provided `/chat`
  mechanism if the server supports it.
- Parent lock prevents casual changes by someone with access to the game, not a
  determined attacker with filesystem access.

## License

MIT. See [`LICENSE`](LICENSE).
