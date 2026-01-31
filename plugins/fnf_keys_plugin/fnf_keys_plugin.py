import asyncio
from pynput.keyboard import Listener, Key
from ..base_plugin import BasePlugin

# Global color mappings for keys D, F, J, K (RGB)
COLOR_D = [195, 74, 153]
COLOR_F = [38, 253, 252]
COLOR_J = [18, 250, 4]
COLOR_K = [255, 20, 20]

# Fade configuration: delay between interpolation steps (seconds)
FADE_STEP_DELAY = 0.025
# Number of interpolation steps to reach the target color
FADE_STEPS = 2
redMode = False

class Plugin(BasePlugin):
    """
    FNF-style plugin: split the strip into 4 segments controlled by keys
    D, F, J, K. Pressing a key fades its segment in to the assigned color;
    releasing fades it out. A single frame is sent each loop so segments
    don't interfere with each other's animation.
    """

    def __init__(self, ddp_client):
        print("Anon")
        super().__init__(ddp_client)

        self.led_count = 38
        # Segment sizes: distribute remainder so total == led_count
        base = self.led_count // 4
        rem = self.led_count % 4
        sizes = [(base + (1 if i < rem else 0)) for i in range(4)]

        # Compute ranges as (start, end) with end exclusive
        self.segments = []
        idx = 0
        for s in sizes:
            self.segments.append((idx, idx + s))
            idx += s

        # Map keys to segment index and assigned color
        self.key_map = {
            "d": (0, COLOR_D),
            "f": (1, COLOR_F),
            "j": (2, COLOR_J),
            "k": (3, COLOR_K),
        }

        # Current pressed state per key
        self.key_states = {k: False for k in self.key_map}

        # Current color per segment (float values for smooth interpolation)
        self.current_segment_colors = [[0.0, 0.0, 0.0] for _ in range(4)]

        self.listener = None

    def _on_press(self, key):
        if key == Key.space:
            print("espeis")
            global COLOR_D, COLOR_F, COLOR_J, COLOR_K, redMode
            if not redMode:
                print("Modo rojoa ctivado")
                COLOR_D = [255, 0, 0]
                COLOR_F = [255, 0, 0]
                COLOR_J = [255, 0, 0]
                COLOR_K = [255, 0, 0]
                
                self.key_map = {
                "d": (0, COLOR_D),
                "f": (1, COLOR_F),
                "j": (2, COLOR_J),
                "k": (3, COLOR_K),
                }
                redMode = True
            else:
                print("Modo rojoa DEctivado")
                COLOR_D = [195, 74, 153]
                COLOR_F = [37, 253, 252]
                COLOR_J = [18, 250, 4]
                COLOR_K = [255, 20, 20]
                
                self.key_map = {
                "d": (0, COLOR_D),
                "f": (1, COLOR_F),
                "j": (2, COLOR_J),
                "k": (3, COLOR_K),
                }
                redMode = False

        try:
            ch = key.char.lower()
        except Exception:
            return

        if ch in self.key_states:
            self.key_states[ch] = True

    def _on_release(self, key):
        try:
            ch = key.char.lower()
        except Exception:
            return

        if ch in self.key_states:
            self.key_states[ch] = False

    async def run(self):
        print("FnF Plugin Started")

        # Start keyboard listener in a background thread
        self.listener = Listener(on_press=self._on_press, on_release=self._on_release)
        self.listener.start()

        try:
            while self.active:
                # For each segment compute target color and step current towards it
                for key, (seg_idx, color) in self.key_map.items():
                    target = color if self.key_states[key] else [0, 0, 0]
                    cur = self.current_segment_colors[seg_idx]

                    # Interpolate towards target
                    for c in range(3):
                        diff = float(target[c]) - cur[c]
                        step = diff / FADE_STEPS
                        cur[c] = cur[c] + step
                        # clamp
                        if cur[c] < 0:
                            cur[c] = 0.0
                        elif cur[c] > 255:
                            cur[c] = 255.0

                # Build a single full-frame pixel array from current_segment_colors
                pixels = []
                for seg_idx, (start, end) in enumerate(self.segments):
                    # Round current color to ints for sending
                    r, g, b = [
                        int(round(x)) for x in self.current_segment_colors[seg_idx]
                    ]
                    for _ in range(start, end):
                        pixels.append([r, g, b])

                # Send one frame representing all segments
                self.ddp.send_frame(pixels)

                await asyncio.sleep(FADE_STEP_DELAY)

        except asyncio.CancelledError:
            pass

        finally:
            # Ensure listener is stopped and LEDs off
            if self.listener:
                try:
                    self.listener.stop()
                except Exception:
                    pass

            # Fade everything to off immediately
            off_pixels = [[0, 0, 0]] * self.led_count
            self.ddp.send_frame(off_pixels)

            print("FnF Plugin Stopped")
