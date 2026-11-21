# ConsentChat privacy notice

**Last updated: 2026-11-21**

ConsentChat is a client-side Minecraft mod. It is designed to collect **nothing**.

## What we do not collect

- No chat messages, usernames, UUIDs, IP addresses, or server chat logs.
- No account information, email addresses, phone numbers, or birth dates.
- No telemetry, analytics, crash reporting, diagnostics, or usage statistics.
- No advertising identifiers, profiles, or cross-context behavioural tracking.
- No data from children or adults is sent to the developer or any third party.

## What is stored locally

The mod writes one file on your computer:

```text
config/consentchat.json
```

It contains only:

- your chosen default privacy mode;
- per-server mode choices;
- which servers you have acknowledged the disclosure for;
- if enabled, a salted hash of a locally chosen parent-control PIN.

You can delete this file at any time to reset everything.

## Network behaviour

The mod opens **no custom network connections** and uses **no custom network packets**.

It changes only vanilla options through Minecraft's own option API. When a privacy mode is
active, Minecraft may send its normal vanilla client-information update to the server,
exactly as it does when you change the same setting in the vanilla Options screen.

## Children and parents

- The default mode on multiplayer servers is **Silent**, the most private option.
- The disclosure screen explains the mode before it is used.
- A parent can set a local PIN to prevent casual mode changes.
- The parent lock is not age verification and does not send anything anywhere.

## Your choices

Press **O** in game to open the privacy dashboard. You can switch between Public, Trusted,
and Silent at any time, subject to the optional parent lock. Public restores vanilla
behaviour. Silent sends no ordinary chat messages.

## Contact and changes

There is no service, account, or backend behind this mod. If this notice changes, the new
version will ship with the mod. The rule remains: no collection, no sale, no sharing, no
cloud.
