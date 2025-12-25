from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from time import sleep

# SPI 초기화
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=1, block_orientation=90)

# O 패턴 (8x8)
O_pattern = [
    (2,1),(3,1),(4,1),(5,1),
    (1,2),(6,2),
    (1,3),(6,3),
    (1,4),(6,4),
    (1,5),(6,5),
    (2,6),(3,6),(4,6),(5,6)
]

# X 패턴 (8x8)
X_pattern = [
    (1,1),(6,1),
    (2,2),(5,2),
    (3,3),(4,3),
    (3,4),(4,4),
    (2,5),(5,5),
    (1,6),(6,6)
]

def draw_pattern(pattern):
    with canvas(device) as draw:
        for x, y in pattern:
            draw.point((x, y), fill=255)

while True:
    draw_pattern(O_pattern)
    sleep(1.5)
    draw_pattern(X_pattern)
    sleep(1.5)
