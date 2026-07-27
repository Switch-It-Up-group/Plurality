import keyring

def decimal_color_rgb(rgb:tuple):
    r,g,b = rgb
    return (r * 65536) + (g * 256) + b