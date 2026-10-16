"""The voice nudge. Mock mode prints the line and, on macOS, speaks it with the
built-in `say` command so you still get audio with zero keys. Live mode calls
ElevenLabs and saves/plays an mp3.
"""
import shutil
import subprocess
import config


def say(text):
    print(f'\n  ParWatch (voice): "{text}"')

    if not config.VOICE_LIVE:
        # Free local fallback so the demo has audio even without a key.
        if shutil.which("say"):
            try:
                subprocess.run(["say", text], check=False)
            except Exception:  # noqa: BLE001
                pass
        return

    # ── Live ElevenLabs ───────────────────────────────────────────────
    try:
        from elevenlabs.client import ElevenLabs  # type: ignore
    except ImportError:
        print("[voice] elevenlabs not installed; printed only. `pip install elevenlabs`")
        return
    try:
        client = ElevenLabs(api_key=config.get("ELEVENLABS_API_KEY"))
        audio = client.text_to_speech.convert(
            voice_id=config.get("ELEVENLABS_VOICE_ID"),
            model_id="eleven_turbo_v2_5",
            text=text,
        )
        # convert() streams bytes chunks; collect and save to an mp3.
        data = b"".join(audio)
        out = config.HERE / "nudge.mp3"
        out.write_bytes(data)
        # Play it (macOS afplay is reliable; falls back to just saving).
        if shutil.which("afplay"):
            subprocess.run(["afplay", str(out)], check=False)
        else:
            print(f"[voice] saved audio to {out}")
    except Exception as e:  # noqa: BLE001
        print(f"[voice] ElevenLabs error ({e}); printed only.")
