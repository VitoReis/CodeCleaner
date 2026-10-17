import logging
import threading
import time

import winsound

logger = logging.getLogger(__name__)

TONES = {
    "ready": ((880, 120), (1175, 120), (1568, 220)),
    "coin": ((1047, 100), (1319, 180)),
    "error": ((392, 180), (294, 300)),
}


def play_tone(event):
    threading.Thread(
        target=_play_tone,
        args=(event,),
        daemon=True,
    ).start()


def _play_tone(event):
    tones = TONES.get(event)
    if tones is None:
        logger.error("Unknown notification tone: %s", event)
        return

    for frequency, duration in tones:
        try:
            winsound.Beep(frequency, duration)
        except RuntimeError:
            logger.exception("Could not play notification tone %s", event)
            return
        time.sleep(0.04)
