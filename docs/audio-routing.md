## Audio Signal Path

The CM6206 operates in two distinct modes:

- 🟦 **PCM Mode**: PCM audio is looped back through Line In and mixed with the microphone.
- 🟪 **Encoded Mode**: Dolby/encoded audio bypasses the mixer and is passed directly to S/PDIF Out.

```mermaid
flowchart LR

    INPUT(["🔌 TOSLINK IN<br/>S/PDIF Source"])
    OUTPUT(["🔊 S/PDIF OUT<br/>AV Receiver / Speakers"])

    subgraph PCM["🟦 PCM + Microphone Mode"]
        direction LR

        FRONT["🎵 Front Output"]
        LOOP["🔁 External<br/>TRS Loop"]
        LINE["🎚️ Line In"]
        MIXER{{"🎛️ CM6206<br/>Mixer"}}
        MIC(["🎤 Microphone"])

        FRONT --> LOOP
        LOOP --> LINE
        LINE --> MIXER
        MIC --> MIXER
    end

    subgraph ENCODED["🟪 Dolby / Encoded Mode"]
        direction LR

        PASS["🔐 Bitstream<br/>Passthrough"]
    end

    INPUT -->|"PCM"| FRONT
    MIXER -->|"PCM + Mic"| OUTPUT

    INPUT -->|"Dolby / DTS / Encoded"| PASS
    PASS -->|"Unmodified Bitstream"| OUTPUT

    classDef input fill:#334155,stroke:#94a3b8,color:#ffffff,stroke-width:2px;
    classDef pcm fill:#0e7490,stroke:#22d3ee,color:#ffffff,stroke-width:2px;
    classDef mixer fill:#0369a1,stroke:#38bdf8,color:#ffffff,stroke-width:3px;
    classDef mic fill:#047857,stroke:#34d399,color:#ffffff,stroke-width:2px;
    classDef encoded fill:#6d28d9,stroke:#a78bfa,color:#ffffff,stroke-width:2px;
    classDef output fill:#b45309,stroke:#fbbf24,color:#ffffff,stroke-width:2px;

    class INPUT input;
    class FRONT,LOOP,LINE pcm;
    class MIXER mixer;
    class MIC mic;
    class PASS encoded;
    class OUTPUT output;
```

### Signal Summary

| Mode | Input | Processing | Microphone | Output |
|---|---|---|---|---|
| 🟦 `pcm` | PCM S/PDIF | Front Out → TRS Loop → Line In → Mixer | ✅ Mixed | PCM S/PDIF |
| 🟪 `encoded` | Dolby / DTS / Encoded S/PDIF | Direct bitstream passthrough | ❌ Bypassed | Original encoded S/PDIF |

### PCM Mode

```text
TOSLINK IN
    │
    ▼
Front Output ──► External TRS Loop ──► Line In
                                          │
Microphone ───────────────────────────────┤
                                          ▼
                                     CM6206 Mixer
                                          │
                                          ▼
                                     S/PDIF OUT
```

PCM mode allows the CM6206 to combine the incoming PCM audio with the microphone before sending the resulting PCM stream to the S/PDIF output.

### Encoded Mode

```text
TOSLINK IN ──► Encoded Bitstream Passthrough ──► S/PDIF OUT
                       ▲
                       │
             Mixer and Mic bypassed
```

Encoded mode avoids processing the incoming bitstream. This allows formats such as Dolby Digital to reach the downstream decoder without being altered by the PCM mixing path.

> **Why the external TRS loop?**  
> In PCM mode, the CM6206's Front Output is physically looped back into Line In. This makes the incoming PCM audio available to the CM6206 mixer alongside the microphone input.
