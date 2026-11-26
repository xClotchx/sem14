"""
generar_puntos.py  ·  Laboratorio semana 14 (PROG 409)
Convierte puntos.csv (pixeles de la foto equirectangular) en puntos.json
(posiciones 3D) para que A-Frame los cree con JavaScript.
Uso:  python generar_puntos.py
"""
import csv
import json
import math

ANCHO = 4096      # ancho de la foto 360 en pixeles (proporcion 2:1)
ALTO = 2048       # alto de la foto 360 en pixeles
R = 6             # distancia (m) a la que se colocan los puntos
ALTURA_OJOS = 1.6


def pixel_a_angulos(px, py):
    """TODO 1: pixel -> (yaw, pitch) en grados."""
    yaw = (px / ANCHO - 0.5) * 360      # 0 al frente, + a la derecha
    pitch = (0.5 - py / ALTO) * 180     # 0 en el horizonte, + hacia arriba
    return yaw, pitch


def angulos_a_posicion(yaw, pitch, r=R):
    """TODO 2: (yaw, pitch) -> (x, y, z) a distancia r del visitante."""
    yaw_r = math.radians(yaw)
    pitch_r = math.radians(pitch)
    x = r * math.cos(pitch_r) * math.sin(yaw_r)       # +X es la derecha
    y = ALTURA_OJOS + r * math.sin(pitch_r)           # altura de los ojos
    z = -r * math.cos(pitch_r) * math.cos(yaw_r)      # -Z es al frente
    return x, y, z


def main():
    puntos = []
    with open("puntos.csv", encoding="utf-8", newline="") as f:
        for fila in csv.DictReader(f):
            px, py = float(fila["px"]), float(fila["py"])
            yaw, pitch = pixel_a_angulos(px, py)
            x, y, z = angulos_a_posicion(yaw, pitch)
            puntos.append({
                "id": fila["id"],
                "titulo": fila["titulo"],
                "descripcion": fila["descripcion"],
                "yaw": round(yaw, 1),
                "pitch": round(pitch, 1),
                "posicion": {"x": round(x, 3), "y": round(y, 3), "z": round(z, 3)},
            })

    with open("puntos.json", "w", encoding="utf-8") as f:
        json.dump(puntos, f, ensure_ascii=False, indent=2)

    print(f"{'id':<10}{'yaw':>8}{'pitch':>8}   posicion (x, y, z)")
    for p in puntos:
        q = p["posicion"]
        print(f"{p['id']:<10}{p['yaw']:>8}{p['pitch']:>8}   ({q['x']}, {q['y']}, {q['z']})")
    print(f"\nSe escribio puntos.json con {len(puntos)} puntos.")


if __name__ == "__main__":
    main()
