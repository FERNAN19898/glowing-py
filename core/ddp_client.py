import socket

class DDPClient:
    def __init__(self, ip, port=4048):
        self.ip: str = ip
        self.port: int = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sequence = 0

    def send_frame(self, pixels: list):
        """
        Sends a list of RGB colors to WLED via DDP protocol.
        this function constructs the DDP packet and sends it over UDP.
        
        pixels: An array of RGB sub arrays, where each sub array is [R, G, B] and represents one LED.
        e.g., [[255,0,0], [0,255,0], [0,0,255], ...]
        """

        try:
            # Flatten the array of RGB arrays into a single byte array 
            # [[r1, g1, b1], [r2, g2, b2]] to -> [r1, b1, b1, r2, g2, b2]
            flat_pixels = bytearray()
            
            for led in pixels:
                if len(led) >= 3: 
                    # Is a valid led data
                    r, g, b = int(led[0]) & 0xFF, int(led[1]) & 0xFF, int(led[2]) & 0xFF
                    flat_pixels.extend([r, g, b])
                else:
                    # If malformed, pad with zeros
                    flat_pixels.extend([0, 0, 0])

            # Length in DDP header is number of data bytes, not number of pixels
            count = len(flat_pixels)

            # --- DDP HEADER CONSTRUCTION ---
            # Byte 0: 0x41 (Flags: Ver1 + Push)
            # Byte 1: Sequence (0-15)
            # Byte 2: 0x01 (Data Type: RGB)
            # Byte 3: 0x01 (Source ID)
            # Byte 4-7: Offset (0)
            # Byte 8-9: Length (High, Low)

            header = bytearray(
                [
                    0x41,
                    self.sequence & 0x0F,
                    0x01,
                    0x01,
                    0x00,
                    0x00,
                    0x00,
                    0x00,
                    (count >> 8) & 0xFF,
                    count & 0xFF,
                ]
            )

            packet = header + flat_pixels
            self.sock.sendto(packet, (self.ip, self.port))

            self.sequence = (self.sequence + 1) % 16

        except Exception as e:
            print(f"[DDP Error] Failed to send packet to {self.ip}: {e}")

    def close(self):
        self.sock.close()