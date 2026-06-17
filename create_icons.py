"""Generate icon-192.png and icon-512.png for the PWA manifest."""
import struct, zlib

BG     = (13,  13,  13)   # #0d0d0d
ACCENT = (79, 142, 247)   # #4f8ef7


def make_png(size: int) -> bytes:
    px = [[BG] * size for _ in range(size)]

    # ── bar chart ──
    bars   = [0.42, 0.72, 0.54, 0.88, 0.62]
    margin = int(size * 0.17)
    bottom = int(size * 0.79)
    top    = int(size * 0.16)
    left   = margin
    right  = size - margin
    w      = right - left
    h      = bottom - top
    n      = len(bars)
    bw     = max(1, w // (n * 2 - 1))

    for i, frac in enumerate(bars):
        x0 = left + i * bw * 2
        x1 = x0 + bw
        bh = int(h * frac)
        y0 = bottom - bh
        for y in range(y0, bottom + 1):
            for x in range(x0, x1):
                if 0 <= x < size and 0 <= y < size:
                    t = (y - y0) / bh if bh else 1.0
                    r = int(ACCENT[0] * (0.65 + 0.35 * (1 - t)))
                    g = int(ACCENT[1] * (0.65 + 0.35 * (1 - t)))
                    b = int(ACCENT[2] * (0.85 + 0.15 * (1 - t)))
                    px[y][x] = (r, g, b)

    # ── trend line over bars ──
    ys = [bottom - int(h * f) for f in bars]
    xs = [left + i * bw * 2 + bw // 2 for i in range(n)]
    for i in range(n - 1):
        lx0, ly0, lx1, ly1 = xs[i], ys[i], xs[i + 1], ys[i + 1]
        steps = max(abs(lx1 - lx0), abs(ly1 - ly0), 1)
        for s in range(steps + 1):
            t  = s / steps
            lx = int(lx0 + (lx1 - lx0) * t)
            ly = int(ly0 + (ly1 - ly0) * t)
            for dy in range(-max(1, size // 64), max(2, size // 48)):
                ny = ly + dy
                if 0 <= lx < size and 0 <= ny < size:
                    px[ny][lx] = (255, 255, 255)

    # ── rounded corners (transparent) ──
    cr = size // 7
    corners = [(cr, cr), (size - 1 - cr, cr),
               (cr, size - 1 - cr), (size - 1 - cr, size - 1 - cr)]
    for y in range(size):
        for x in range(size):
            for (cx_, cy_) in corners:
                if abs(x - cx_) <= cr and abs(y - cy_) <= cr:
                    if (x - cx_) ** 2 + (y - cy_) ** 2 > cr * cr:
                        px[y][x] = None   # transparent
                        break

    # ── encode RGBA PNG ──
    def chunk(tag: bytes, data: bytes) -> bytes:
        crc = zlib.crc32(tag + data) & 0xFFFFFFFF
        return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', crc)

    ihdr  = struct.pack('>IIBBBBB', size, size, 8, 6, 0, 0, 0)
    raw   = b''.join(
        b'\x00' + b''.join(
            (bytes([*p, 255]) if p is not None else b'\x00\x00\x00\x00')
            for p in row
        )
        for row in px
    )
    idat  = zlib.compress(raw, 9)
    return (b'\x89PNG\r\n\x1a\n'
            + chunk(b'IHDR', ihdr)
            + chunk(b'IDAT', idat)
            + chunk(b'IEND', b''))


if __name__ == '__main__':
    for size in (192, 512):
        path = f'icon-{size}.png'
        with open(path, 'wb') as f:
            f.write(make_png(size))
        print(f'Created {path}')
