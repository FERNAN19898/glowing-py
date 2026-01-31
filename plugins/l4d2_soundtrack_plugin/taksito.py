import fseq
import time
import socket

# --- PEGA AQUÍ TU CLASE DDPClient COMPLETA ---
class DDPClient:
    def __init__(self, ip, port=4048):
        self.ip: str = ip
        self.port: int = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sequence = 0

    def send_frame(self, pixels: list):
        # ... (Tu código de clase sin cambios) ...
        try:
            flat_pixels = bytearray()
            for led in pixels:
                if len(led) >= 3:
                    r, g, b = int(led[0]) & 0xFF, int(led[1]) & 0xFF, int(led[2]) & 0xFF
                    flat_pixels.extend([r, g, b])
                else:
                    flat_pixels.extend([0, 0, 0])

            count = len(flat_pixels)
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


# --- FIN DE LA CLASE DDPClient ---

# --- Lógica Principal del Script ---
DDP_IP = "192.168.18.14"
client = DDPClient(DDP_IP)

with open("Taank.fseq", "rb") as f:
    reader = fseq.parse(f)

    # Atributo step_time_in_ms (como indica la imagen que enviaste)
    delay = reader.step_time_in_ms / 1000.0
    num_channels = reader.channel_count_per_frame

    print(f"Iniciando reproducción a {1/delay:.2f} FPS. Canales: {num_channels}")

    try:
        for i in range(reader.number_of_frames):
            start_time = time.time()

            # 1. Obtener los datos planos del FSEQ: [R1, G1, B1, R2, G2, B2...]
            frame_data = reader.get_frame(i)

            # 2. Convertir los datos planos al formato que espera tu clase: [[R, G, B], ...]
            pixels_list = []
            for j in range(0, num_channels, 3):
                r = frame_data[j] if j < num_channels else 0
                g = frame_data[j + 1] if j + 1 < num_channels else 0
                b = frame_data[j + 2] if j + 2 < num_channels else 0
                pixels_list.append([r, g, b])

            # 3. Enviar el frame usando tu cliente funcional
            client.send_frame(pixels_list)

            # Sincronización
            elapsed = time.time() - start_time
            time.sleep(max(0, delay - elapsed))

    except KeyboardInterrupt:
        print("\nTransmisión DDP detenida.")
    finally:
        client.close()  # Cierra el socket al terminar
